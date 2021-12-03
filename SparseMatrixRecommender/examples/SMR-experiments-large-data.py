import pandas
import random
from SparseMatrixRecommender import *
from SparseMatrixRecommender.DataLoaders import *

dfData0 = load_mushroom_data_frame()

print(dfData0.shape)
print(dfData0.head().to_string())

print(160 * "=")
print("Create recommender")
print(160 * "-")

smrObj = (SparseMatrixRecommender()
          .create_from_wide_form(dfData0,
                                 item_column_name="id",
                                 columns=["cap-Shape", "cap-Surface", "cap-Color", "bruises?", "odor", "gill-Attachment", "gill-Spacing", "gill-Size", "gill-Color", "edibility"],
                                 add_tag_types_to_column_names=True,
                                 tag_value_separator=":")
          .apply_term_weight_functions("IDF", "None", "Cosine"))

print("The obtained recommender object:")
print(repr(smrObj))

print("Recommender matrix sample:")
sample_rows = random.sample(smrObj.take_M().row_names(), 10)
smrObj.take_M()[sample_rows, :].print_matrix()

print(160 * "=")
print("Recommend by profile")
print(160 * "-")

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
