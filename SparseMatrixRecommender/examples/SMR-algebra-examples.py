import pandas
import random
from SparseMatrixRecommender import *
from SparseMatrixRecommender.DataLoaders import *

dfData0 = load_mint_bubbles_transactions_data_frame()

print(dfData0.shape)
print(dfData0.head().to_string())

print(160 * "=")
print("Create first recommender")
print(160 * "-")

smrObj1 = (SparseMatrixRecommender()
           .create_from_wide_form(data=dfData0[200:dfData0.shape[0]][["id", "Date", "Description", "Amount"]],
                                  item_column_name="id"))

print(smrObj1)

print(160 * "=")
print("Create second recommender")
print(160 * "-")

smrObj2 = (SparseMatrixRecommender()
           .create_from_wide_form(data=dfData0[0:300][["id", "Date", "Transaction.Type", "Category", "Account.Name"]],
                                  item_column_name="id"))

print(smrObj2)

print(160 * "=")
print("Outer join of the recommenders")
print(160 * "-")

smrObj3 = smrObj1.join(smrObj2, join_type="outer")

print(smrObj3)

print(160 * "=")
print("Inner join of the recommenders")
print(160 * "-")

smrObj4 = smrObj1.join(smrObj2, join_type="inner")

print(smrObj4)

print(160 * "=")
print("Left join of the recommenders")
print(160 * "-")

smrObj5 = smrObj1.join(smrObj2, join_type="left")

print(smrObj5)
