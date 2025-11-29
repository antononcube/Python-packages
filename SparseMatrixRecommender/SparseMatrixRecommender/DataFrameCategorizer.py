import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple, List


class DataFrameCategorizer:
    r"""
    Categorize Pandas DataFrame columns via binning, log transforms, and string handling.

    Parameters
    ----------
    n_unique_threshold : int, optional
        Maximum number of unique values for a numeric column to be treated as low-cardinality categorical,
        by default ``5``.
    use_log : bool, optional
        If ``True``, create log-transformed companion features for high-cardinality numeric columns,
        by default ``True``.
    n_bins : int, optional
        Number of bins for numeric binning; if ``<= 0`` the numeric data is treated as string,
        by default ``10``.
    use_quantile_bins : bool, optional
        If ``True``, use quantile-based binning; otherwise use equal-width binning,
        by default ``False``.
    keep_original_numeric : bool, optional
        If ``True``, retain transformed versions of the original numeric columns; if ``False``, drop them,
        by default ``True``.
    log_threshold : float, optional
        Minimum positive value for log transformation; values at or below this threshold
        are filled with ``below_log_threshold_value``, by default ``0.0``.
    below_log_threshold_value : Any, optional
        Fill value for data at or below ``log_threshold`` during log transformation,
        by default ``np.nan``.
    """

    def __init__(
        self,
        n_unique_threshold: int = 5,
        use_log: bool = True,
        n_bins: int = 10,
        use_quantile_bins: bool = False,
        keep_original_numeric: bool = True,
        log_threshold: float = 0.0,
        below_log_threshold_value: Any = np.nan,
    ):
        self.n_unique_threshold = n_unique_threshold
        self.use_log = use_log
        self.n_bins = n_bins
        self.use_quantile_bins = use_quantile_bins
        self.keep_original_numeric = keep_original_numeric
        self.log_threshold = log_threshold
        self.below_log_threshold_value = below_log_threshold_value

        self.bins_: Dict[str, Any] = {}
        self.columns_info_: Dict[str, Dict[str, Any]] = {}
        self.transformation_map_: Dict[str, Any] = {}
        self.fitted_ = False

    def _is_numeric(self, s: pd.Series) -> bool:
        r"""
        Determine whether a ``Series`` contains numeric data.

        Parameters
        ----------
        s : pandas.Series
            Series to inspect.

        Returns
        -------
        bool
            ``True`` if the dtype is numeric, otherwise ``False``.
        """
        return pd.api.types.is_numeric_dtype(s)

    def _make_log_col(self, s: pd.Series) -> pd.Series:
        r"""
        Apply a base-10 logarithm to values above ``log_threshold`` while filling lower
        values with ``below_log_threshold_value``.

        Parameters
        ----------
        s : pandas.Series
            Numeric series to transform.

        Returns
        -------
        pandas.Series
            Log-transformed series with threshold handling.
        """
        mask = s > self.log_threshold
        out = pd.Series(self.below_log_threshold_value, index=s.index, dtype="float64")
        out[mask] = np.log10(s[mask])
        return out

    def _fit_numeric_col(
        self,
        s: pd.Series,
        col_name: str
    ):
        r"""
        Analyze a numeric column and configure its transformation strategy.

        Parameters
        ----------
        s : pandas.Series
            Numeric data to analyze.
        col_name : str
            Column name for bookkeeping.

        Returns
        -------
        tuple[pandas.IntervalIndex | None, bool]
            Interval bins (if created) and flag indicating whether binning occurred.
        """
        uniq = s.dropna().unique()
        n_unique = len(uniq)

        if n_unique <= self.n_unique_threshold:
            self.columns_info_[col_name] = {
                "type": "numeric_low_cardinality",
                "categories": sorted(map(str, uniq)),
            }
            return None, False

        if self.n_bins <= 0:
            self.columns_info_[col_name] = {
                "type": "numeric_as_str",
                "as_str": True,
            }
            return None, False

        if self.use_quantile_bins:
            _, bins = pd.qcut(s, q=self.n_bins, retbins=True, duplicates="drop")
        else:
            _, bins = pd.cut(s, bins=self.n_bins, retbins=True, duplicates="drop")

        if len(bins) <= 1:
            self.columns_info_[col_name] = {
                "type": "numeric_as_str",
                "as_str": True,
            }
            return None, False

        bins = np.concatenate(([-np.inf], bins, [np.inf]))

        interval_index = pd.IntervalIndex.from_breaks(bins, closed="right")
        self.bins_[col_name] = interval_index
        self.columns_info_[col_name] = {
            "type": "numeric_binned",
            "binned": True,
        }
        return interval_index, True

    def _transform_numeric_col(
        self,
        s: pd.Series,
        col_name: str
    ) -> pd.Series:
        r"""
        Convert a numeric column according to its previously determined strategy.

        Parameters
        ----------
        s : pandas.Series
            Numeric data to transform.
        col_name : str
            Column identifier used to look up transformation metadata.

        Returns
        -------
        pandas.Series
            Transformed categorical representation.
        """
        info = self.columns_info_[col_name]
        if info["type"] == "numeric_low_cardinality":
            return s.astype("string")

        if info["type"] == "numeric_as_str":
            return s.astype("string")

        if info["type"] == "numeric_binned":
            bins = self.bins_[col_name]
            out = pd.cut(s, bins=bins)
            return out.astype("string")

        return s

    def _fit_log_for_col(self, s: pd.Series, col_name: str):
        r"""
        Configure log-transformed companion features for a numeric column when enabled.

        Parameters
        ----------
        s : pandas.Series
            Original numeric data.
        col_name : str
            Base column name.

        Returns
        -------
        tuple[pandas.IntervalIndex | None, bool] | None
            Result from numeric fitting for the log column or ``None`` if log usage is disabled.
        """
        if not self.use_log:
            return None

        log_col_name = f"{col_name}_log"
        log_s = self._make_log_col(s)
        uniq = log_s.dropna().unique()
        n_unique = len(uniq)

        return self._fit_numeric_col(log_s, log_col_name)

    def _transform_log_for_col(
        self,
        s: pd.Series,
        col_name: str
    ) -> Optional[pd.Series]:
        r"""
        Apply transformations to the log companion column if it exists.

        Parameters
        ----------
        s : pandas.Series
            Original numeric series.
        col_name : str
            Base column name.

        Returns
        -------
        pandas.Series | None
            Transformed log series or ``None`` when no log metadata is available.
        """
        if not self.use_log:
            return None

        log_col_name = f"{col_name}_log"
        if log_col_name not in self.columns_info_:
            return None

        log_s = self._make_log_col(s)
        info = self.columns_info_[log_col_name]

        if info["type"] == "numeric_low_cardinality":
            return log_s.astype("string")

        if info["type"] == "numeric_as_str":
            return log_s.astype("string")

        if info["type"] == "numeric_binned":
            bins = self.bins_[log_col_name]
            out = pd.cut(log_s, bins=bins)
            return out.astype("string")

        return log_s

    def _fit_string_col(self, s: pd.Series, col_name: str):
        r"""
        Capture unique categories for a string-based column.

        Parameters
        ----------
        s : pandas.Series
            String or categorical series.
        col_name : str
            Column identifier.
        """
        cats = pd.Index(s.dropna().astype("string").unique())
        self.columns_info_[col_name] = {
            "type": "string",
            "categories": cats,
        }

    def _transform_string_col(self, s: pd.Series, col_name: str) -> pd.Series:
        r"""
        Enforce known categories for a string column, setting unknowns to ``NaN``.

        Parameters
        ----------
        s : pandas.Series
            Series to transform.
        col_name : str
            Column identifier.

        Returns
        -------
        pandas.Series
            Series with unknown categories replaced by ``NaN``.
        """
        info = self.columns_info_[col_name]
        cats: pd.Index = info["categories"]
        s_str = s.astype("string")
        mask = s_str.isin(cats)
        return s_str.where(mask, np.nan)

    def _serialize_categories(self, cats: pd.Index) -> List[Any]:
        r"""
        Convert category values to JSON-serializable types.

        Parameters
        ----------
        cats : pandas.Index
            Categories to serialize.

        Returns
        -------
        list[Any]
            List of serializable category values.
        """
        return [None if pd.isna(cat) else str(cat) for cat in cats]

    def _serialize_intervals(self, intervals: pd.IntervalIndex) -> List[Dict[str, Any]]:
        r"""
        Serialize interval bins for storage or inspection.

        Parameters
        ----------
        intervals : pandas.IntervalIndex
            Interval bins to serialize.

        Returns
        -------
        list[dict[str, Any]]
            Serialized representation containing bounds and closure information.
        """
        serialized = []
        for interval in intervals:
            serialized.append({
                "left": interval.left,
                "right": interval.right,
                "closed": interval.closed
            })
        return serialized

    def _build_transformation_map(self):
        r"""
        Assemble a structured description of all fitted column transformations.

        Returns
        -------
        None
            Constructs and stores ``transformation_map_`` in-place.
        """
        transformation_map: Dict[str, Any] = {
            "config": {
                "n_unique_threshold": self.n_unique_threshold,
                "use_log": self.use_log,
                "n_bins": self.n_bins,
                "use_quantile_bins": self.use_quantile_bins,
                "keep_original_numeric": self.keep_original_numeric,
                "log_threshold": self.log_threshold,
                "below_log_threshold_value": self.below_log_threshold_value,
            },
            "columns": {}
        }

        for col, info in self.columns_info_.items():
            col_info = dict(info)
            if info["type"] in {"string"}:
                col_info["categories"] = self._serialize_categories(info["categories"])
            if info["type"] in {"numeric_low_cardinality"}:
                col_info["categories"] = [None if pd.isna(cat) else str(cat) for cat in info["categories"]]
            if info["type"] == "numeric_binned":
                col_info["bins"] = self._serialize_intervals(self.bins_[col])
            transformation_map["columns"][col] = col_info

        self.transformation_map_ = transformation_map

    def get_transformation_map(self) -> Dict[str, Any]:
        r"""
        Retrieve the fitted transformation specification.

        Returns
        -------
        dict[str, Any]
            Mapping containing configuration and per-column metadata.

        Raises
        ------
        RuntimeError
            If the categorizer has not been fitted.
        """
        if not self.fitted_:
            raise RuntimeError("DataFrameCategorizer must be fitted before accessing the transformation map.")
        return self.transformation_map_

    def fit(self, df: pd.DataFrame) -> "DataFrameCategorizer":
        r"""
        Learn transformation strategies for each column in the DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            Training data.

        Returns
        -------
        DataFrameCategorizer
            The fitted instance.

        Raises
        ------
        ValueError
            Propagated from Pandas when fitting columns fails.
        """
        self.bins_.clear()
        self.columns_info_.clear()
        self.transformation_map_.clear()

        for col in df.columns:
            s = df[col]
            if self._is_numeric(s):
                if self.keep_original_numeric:
                    self._fit_numeric_col(s, col)
                else:
                    self.columns_info_[col] = {
                        "type": "numeric_dropped",
                    }
                if len(s.unique()) > self.n_unique_threshold:
                    self._fit_log_for_col(s, col)
            else:
                self._fit_string_col(s, col)

        self._build_transformation_map()
        self.fitted_ = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        r"""
        Apply learned transformations to a DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            Data to transform.

        Returns
        -------
        pandas.DataFrame
            Transformed DataFrame with aligned columns.

        Raises
        ------
        RuntimeError
            If the instance has not been fitted.
        """
        if not self.fitted_:
            raise RuntimeError("DataFrameCategorizer must be fitted before calling transform.")

        out_cols: Dict[str, pd.Series] = {}

        for col in df.columns:
            s = df[col]

            if col not in self.columns_info_:
                out_cols[col] = s
                continue

            info = self.columns_info_[col]

            if info["type"].startswith("numeric"):
                if info["type"] == "numeric_dropped":
                    pass
                else:
                    out_cols[col] = self._transform_numeric_col(s, col)
                log_series = self._transform_log_for_col(s, col)
                if log_series is not None:
                    out_cols[f"{col}_log"] = log_series
            elif info["type"] == "string":
                out_cols[col] = self._transform_string_col(s, col)
            else:
                out_cols[col] = s

        for col in df.columns:
            log_col_name = f"{col}_log"
            if log_col_name in self.columns_info_ and log_col_name not in out_cols:
                s = df[col]
                out_cols[log_col_name] = self._transform_log_for_col(s, col)

        return pd.DataFrame(out_cols, index=df.index)

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        r"""
        Fit the categorizer and immediately transform the provided DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            Data used for both fitting and transforming.

        Returns
        -------
        pandas.DataFrame
            Transformed DataFrame after fitting.
        """
        self.fit(df)
        return self.transform(df)


def data_frame_columns_alignment(base: pd.DataFrame, target: pd.DataFrame, default_value=None) -> pd.DataFrame:
    r"""
    Align a target DataFrame's columns to match a base DataFrame.

    Parameters
    ----------
    base : pandas.DataFrame
        Reference DataFrame supplying the desired column order and presence.
    target : pandas.DataFrame
        DataFrame to align.
    default_value : Any, optional
        Value used to fill newly added columns, by default ``None``.

    Returns
    -------
    pandas.DataFrame
        Column-aligned copy of ``target``.
    """
    target_aligned = target.copy()

    missing_cols = [c for c in base.columns if c not in target_aligned.columns]
    if missing_cols:
        target_aligned = pd.concat(
            [target_aligned, pd.DataFrame(default_value, index=target_aligned.index, columns=missing_cols)],
            axis=1
        )

    extra_cols = [col for col in target_aligned.columns if col not in base.columns]
    if extra_cols:
        target_aligned = target_aligned.drop(columns=extra_cols)

    target_aligned = target_aligned[base.columns]

    return target_aligned