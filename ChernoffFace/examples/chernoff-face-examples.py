import matplotlib.cm

from ChernoffFace import *

# Get USA arrests data
dfData = load_usa_arrests_data_frame()

# Transform into numerical array
data = dfData.to_numpy()
data = data[:, 1:5]

# Rescale
data2 = variables_rescale(data)

# Make Chernoff faces figure
fig = chernoff_face(data=data2,
                    n_columns=5,
                    long_face=False,
                    color_mapper=matplotlib.cm.rainbow,
                    titles=dfData.StateName.tolist(),
                    figsize=(12, 12))

# Display
fig.tight_layout()
fig.show()


# Alternatively just use variables_rescale of the data frame.
fig = chernoff_face(data=variables_rescale(dfData),
                    n_columns=5,
                    long_face=False,
                    color_mapper=matplotlib.cm.jet,
                    figsize=(12, 12))

# Display
fig.tight_layout()
fig.show()
