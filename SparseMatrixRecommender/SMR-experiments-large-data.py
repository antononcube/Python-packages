import pandas

from SparseMatrixRecommender.src.SparseMatrixRecommender.CrossTabulate import *
from SparseMatrixRecommender.src.SparseMatrixRecommender.SparseMatrixRecommender import *


dfTitanic = pandas.read_csv("/Volumes/Macintosh HD 1/Users/antonov/MathematicaVsR/Data/MathematicaVsR-Data-Titanic.csv")
dfTitanic["id"] = [str(x) for x in dfTitanic["id"]]

aSMats = cross_tabulate(data=dfTitanic, index="id", columns=["passengerClass", "passengerSex", "passengerAge", "passengerSurvival"])

print(dfTitanic.head(12))

print(type(aSMats))

for s in aSMats.items():
    print(s[0], " : ", s[1].shape())

smrObj = SparseMatrixRecommender()
recs = smrObj.create_from_matrices(aSMats).recommend_by_profile(["male", "died", "1st"]).take_value()

dfRecs = pandas.DataFrame()
dfRecs["id"] = list(recs.keys())
dfRecs["Score"] = list(recs.values())
dfRecs = dfRecs[dfRecs["Score"] == 3]
print(dfRecs)

# print(dfTitanic[dfTitanic["id"].isin(recs.keys())])
print(dfRecs.merge(dfTitanic, on="id"))