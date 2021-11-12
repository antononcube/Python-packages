from SparseMatrixRecommender.src.SparseMatrixRecommender.CrossTabulate import *
from SparseMatrixRecommender.src.SparseMatrixRecommender.SparseMatrixRecommender import *
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

dfSMRMatrix = pandas.read_csv(
    "https://raw.githubusercontent.com/antononcube/Raku-ML-StreamsBlendingRecommender/main/resources/WLExampleData-dfSMRMatrix.csv")

print(dfSMRMatrix.sample(12).to_string())

# Illustration of how the matrices are derived
# gb = dfSMRMatrix.sample(20).groupby("TagType")
# [print("Group :", x, "\n", gb.get_group(x)) for x in gb.groups]
# [cross_tabulate(gb.get_group(x), index="Item", columns="Value", values="Weight").print_matrix() for x in gb.groups]

smrObj = (SparseMatrixRecommender().
          create_from_long_form(dfSMRMatrix,
                                item_column_mame="Item",
                                tag_type_column_name="TagType",
                                tag_column_name="Value",
                                weight_column_name="Weight"))

recs = (smrObj
        .recommend_by_profile({"Word:chemical": 1}, nrecs=12)
        .take_value())

print(recs)

print(160 * "=")
print("Profile")
print(160 * "-")

prof = (smrObj
        .profile(["Statistics-FisherIris"])
        .take_value())

print(prof)
