from ExampleDatasets import *

# Load the metadata
dfMeta = load_datasets_metadata()
print(dfMeta.head)

# Get a specified dataset
dfData = example_dataset("mtcars", keep = True)
print(dfData)

# Get a random dataset
dfData2 = example_dataset()
print(dfData2)
