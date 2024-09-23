# %%
import json
import argparse
import numpy as np
import csv
import pandas as pd
from pathlib import Path
import ast

# %%
def get_args():
    parser = argparse.ArgumentParser(description='Generate synthetic data for TDoA')
    parser.add_argument('--std', type=float, default=0.001, help='Standard deviation of the noise added to the time delays')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    # %%
    with open('config_synthetic.json', 'r') as config_file:
        config = json.load(config_file)

    for key, value in config.items():
        print(f"\t\033[94m{key}\033[0m\t\033[90m{value}\033[0m")

    # %%
    std = args.std
    data_save_path = Path(config['data_save_path'])
    sim_data_file = config['synthetic_data_filename'] + f'_std_{std}.csv'

    # %%
    df = pd.read_csv(data_save_path / sim_data_file)
    print(f"Successfully loaded the synthetic data \033[91m{sim_data_file}\033[0m.")

    # Defining Conversion Functions
    def convert_to_array(x):
        try:
            return np.array(ast.literal_eval(x))
        except (SyntaxError, ValueError):  # Handle cases that cannot be converted
            return x  # Returns the original value
        
    # Apply the conversion function to each column
    for column in df.columns:
        df[column] = df[column].apply(convert_to_array)

    # %%
    mic_coordinates = np.array(config['mic_coordinates'])
    source_coordinates = df['source_coordinates']
    real_time_delays = df['time_delays']
    noisy_time_delay = df['noisy_time_delays']

    # %%
    df = pd.DataFrame(
        {
            'real_time_delays': real_time_delays.tolist(),
            'noisy_time_delays': noisy_time_delay.tolist(),
            'source_coordinates': source_coordinates.tolist(),
            'predicted_source_position': np.zeros(len(source_coordinates)),
            'Difference': np.zeros(len(source_coordinates))
        }
    )

    # %%
    i = 0
    for observed_time_delay, actual_source_position in zip(noisy_time_delay, source_coordinates):
        # %%
        r_vec = np.vstack((observed_time_delay[1] - observed_time_delay[0],
                        observed_time_delay[2] - observed_time_delay[0],
                        observed_time_delay[3] - observed_time_delay[0],
                        observed_time_delay[4] - observed_time_delay[0],)
                        ) * config['sound_speed']

        # %%
        A = np.hstack((
            np.vstack((mic_coordinates[1] - mic_coordinates[0],
                    mic_coordinates[2] - mic_coordinates[0],
                    mic_coordinates[3] - mic_coordinates[0],
                    mic_coordinates[4] - mic_coordinates[0],)
                    ),
            r_vec)
            )

        # %%
        theta = (np.vstack((np.linalg.norm(mic_coordinates[1]),
                        np.linalg.norm(mic_coordinates[2]),
                        np.linalg.norm(mic_coordinates[3]),
                        np.linalg.norm(mic_coordinates[4]))
                        )**2 - np.linalg.norm(mic_coordinates[0])**2 - r_vec**2) / 2

        # %%
        predicted_source_position = np.linalg.inv(A).dot(theta)[:3].reshape(3,)

        # %%
        difference = np.linalg.norm(predicted_source_position - actual_source_position)*100
        # print(f"Difference:\t\033[92m{difference}\033[0m\tcm")
        df.at[i, "predicted_source_position"] = np.array2string(predicted_source_position)
        df.at[i, "Difference(cm)"] = difference

        i += 1

    result_save_path = Path("result/localization")
    result_save_path.mkdir(parents=True, exist_ok=True)
    result_filename = f'localization_result_predicted_std_{std}.csv'

    df = df.sort_values(by='Difference(cm)', ascending=False)
    df.to_csv(result_save_path / result_filename, index=False)

    print(f"The maximum difference is:\t\033[91m{df['Difference(cm)'].max()}\033[0m\tcm")