import pandas
import ssl
from SparseMatrixRecommender.SparseMatrixRecommender import *

ssl._create_default_https_context = ssl._create_unverified_context

dfData0 = pandas.read_csv(
    "https://raw.githubusercontent.com/antononcube/MathematicaVsR/master/Data/MathematicaVsR-Data-Mushroom.csv")
dfData0["id"] = ["id." + str(x) for x in dfData0["id"]]

print(dfData0.shape)
print(dfData0.head().to_string())

print(160 * "=")
print("Recommend by profile")
print(160 * "-")

smrObj = (SparseMatrixRecommender()
          .create_from_wide_form(dfData0,
                                 item_column_name="id",
                                 columns=["cap-Shape", "cap-Surface", "cap-Color", "bruises?", "odor", "gill-Attachment", "gill-Spacing", "gill-Size", "gill-Color", "edibility"],
                                 add_tag_types_to_column_names=True,
                                 tag_value_separator=":")
          .apply_term_weight_functions("IDF", "None", "Cosine"))

smrObj.take_M()[1:100:10, :].print_matrix()

recs = (smrObj
        .recommend_by_profile({"cap-Shape:convex": 1.2, "edibility:poisonous": 1.4}, nrecs=12)
        .join_across(dfData0, on="id")
        .take_value())

print(recs)

print(160 * "=")
print("Recommend by history")
print(160 * "-")

recs = (smrObj
        .recommend("id.10", nrecs=12, remove_history=False)
        .join_across(dfData0, on="id")
        .take_value())

print(recs.to_string())
