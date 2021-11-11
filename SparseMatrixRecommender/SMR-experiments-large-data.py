import ssl
from SparseMatrixRecommender.src.SparseMatrixRecommender.CrossTabulate import *
from SparseMatrixRecommender.src.SparseMatrixRecommender.SparseMatrixRecommender import *

ssl._create_default_https_context = ssl._create_unverified_context

dfTitanic = pandas.read_csv(
    "https://raw.githubusercontent.com/antononcube/MathematicaVsR/master/Data/MathematicaVsR-Data-Titanic.csv")

dfTitanic["id"] = [str(x) for x in dfTitanic["id"]]

aSMats = cross_tabulate(data=dfTitanic, index="id",
                        columns=["passengerClass", "passengerSex", "passengerAge", "passengerSurvival"])

print(dfTitanic.head(12))

print(type(aSMats))

for s in aSMats.items():
    print(s[0], " : ", s[1].shape())

print(160 * "=")
print("Recommend by profile")
print(160 * "-")

smrObj = SparseMatrixRecommender()
smrObj = smrObj.create_from_matrices(aSMats)

# recs = smrObj.create_from_matrices(aSMats).recommend_by_profile(["male", "died", "1st"]).take_value()
#
recs = (smrObj
        .create_from_matrices(aSMats)
        .recommend_by_profile({"male": 1.2, "died": 1.4, "1st": 0.3}, nrecs=12)
        .join_across(dfTitanic, on="id")
        .take_value())

print(recs)

print(160 * "=")
print("Recommend by history")
print(160 * "-")

recs = (smrObj
        .create_from_matrices(aSMats)
        .recommend("10", nrecs=12, remove_history=False)
        .join_across(dfTitanic, on="id")
        .take_value())

print(recs)