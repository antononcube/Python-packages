import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple, List


class DataFrameCategorizer:
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
        return pd.api.types.is_numeric_dtype(s)

    def _make_log_col(self, s: pd.Series) -> pd.Series:
        mask = s > self.log_threshold
        out = pd.Series(self.below_log_threshold_value, index=s.index, dtype="float64")
        out[mask] = np.log10(s[mask])
        return out

    def _fit_numeric_col(
            self,
            s: pd.Series,
            col_name: str
    ):
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
        cats = pd.Index(s.dropna().astype("string").unique())
        self.columns_info_[col_name] = {
            "type": "string",
            "categories": cats,
        }

    def _transform_string_col(self, s: pd.Series, col_name: str) -> pd.Series:
        info = self.columns_info_[col_name]
        cats: pd.Index = info["categories"]
        s_str = s.astype("string")
        mask = s_str.isin(cats)
        return s_str.where(mask, np.nan)

    def _serialize_categories(self, cats: pd.Index) -> List[Any]:
        return [None if pd.isna(cat) else str(cat) for cat in cats]

    def _serialize_intervals(self, intervals: pd.IntervalIndex) -> List[Dict[str, Any]]:
        serialized = []
        for interval in intervals:
            serialized.append({
                "left": interval.left,
                "right": interval.right,
                "closed": interval.closed
            })
        return serialized

    def _build_transformation_map(self):
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
        if not self.fitted_:
            raise RuntimeError("DataFrameCategorizer must be fitted before accessing the transformation map.")
        return self.transformation_map_

    def fit(self, df: pd.DataFrame) -> "DataFrameCategorizer":
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
        self.fit(df)
        return self.transform(df)


def data_frame_columns_alignment(base: pd.DataFrame, target: pd.DataFrame, default_value=None) -> pd.DataFrame:
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