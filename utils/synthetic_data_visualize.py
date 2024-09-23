import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import json
from pathlib import Path
import ast

# %%
with open('config_synthetic.json', 'r') as config_file:
    config = json.load(config_file)

for key, value in config.items():
    print(f"\t\033[94m{key}\033[0m\t\033[90m{value}\033[0m")

# %%
std = 0.001
data_save_path = Path(config['data_save_path'])
sim_data_file = config['synthetic_data_filename'] + f'_std_{std}.csv'

# %%
df = pd.read_csv(data_save_path / sim_data_file)

# %% Defining Conversion Functions
def convert_to_array(x):
    try:
        return np.array(ast.literal_eval(x))
    except (SyntaxError, ValueError):  # Handle cases that cannot be converted
        return x  # Returns the original value
# Apply the conversion function to each column
for column in df.columns:
    df[column] = df[column].apply(convert_to_array)
    
# %% Suppose points is a 1000x3 ndarray, where each row represents the xyz coordinate of a point.
points = np.concatenate(np.array(df["source_coordinates"]), axis=0).reshape(-1, 3)
mics = np.array(config['mic_coordinates'])
print(mics.shape)

# Take the x, y, and z coordinates.
x = points[:, 0]
y = points[:, 1]
z = points[:, 2]

# Creating a 3D coordinate system
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# %% Plotting Scatter Plots
ax.scatter(x, y, z)

# Add a solid line for the x-axis
ax.plot([0, 100], [0, 0], [0, 0], color='red')

# Add a solid line for the y-axis
ax.plot([0, 0], [0, 100], [0, 0], color='green')

# Add a solid line for the z-axis
ax.plot([0, 0], [0, 0], [0, 100], color='blue')

# %% Setting Axis Limits
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# %%
ax.scatter(mics[:, 0], mics[:,1], mics[:,2], color='red', s=100)

# %% Display Graphics
plt.show()
