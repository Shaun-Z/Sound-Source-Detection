# %%
import json
import os
import numpy as np
import csv
import pandas as pd
import argparse
from pathlib import Path

# %%
def get_args():
    parser = argparse.ArgumentParser(description='Generate synthetic data for TDoA')
    parser.add_argument('--std', type=float, default=0.001, help='Standard deviation of the noise added to the time delays')

    return parser.parse_args()

# %%
def generate_random_vector(min_value, max_value):
    # Generating random vectors in a spherical coordinate system
    radius = np.random.uniform(min_value, max_value)
    theta = np.random.uniform(0, np.pi * 2)  # Polar angle range: 0 to 2π
    phi = np.random.uniform(0, np.pi)  # Elevation range: 0 to π

    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    return np.array([x, y, z])

# %%
# Calculating sound wave propagation time
def calculate_time_delays(coordinates, microphone_positions, speed_of_sound=343, is_noisy=False, std=0.01):
    time_delays = []
    for source in coordinates:
        delays_for_source = []
        for mic_position in microphone_positions:
            distance = np.linalg.norm(source - mic_position) if is_noisy else np.linalg.norm(source - mic_position) + np.random.normal(0, std) # Calculate the distance from the sound source to the microphone
            time = distance / speed_of_sound  # Calculating sound wave propagation time
            delays_for_source.append(time)
        delays_for_source = delays_for_source - np.min(delays_for_source)  # Normalizing the time delays
        time_delays.append(delays_for_source)
    return np.array(time_delays)

if __name__ == '__main__':
    # %% Parse arguments
    args = get_args()
    # %%
    with open('config_synthetic.json', 'r') as config_file:
        config = json.load(config_file)

    for key, value in config.items():
        print(f"\t\033[94m{key}\033[0m\t\033[90m{value}\033[0m")

    # %%
    vectors = np.array([generate_random_vector(config['closest_distance'], config['farest_distance']) for _ in range(config['num_samples'])])

    # %%
    time_delays = calculate_time_delays(vectors, config['mic_coordinates'], speed_of_sound=config['sound_speed'])

    # %%
    # Add Noise
    std = args.std
    noisy_time_delays = calculate_time_delays(coordinates=vectors, microphone_positions=config['mic_coordinates'], speed_of_sound=config['sound_speed'], is_noisy=True, std=std)

    # %%
    df = pd.DataFrame({
        "source_coordinates": vectors.tolist(),
        "distances_to_origin": np.linalg.norm(vectors, axis=1),
        "noisy_time_delays": noisy_time_delays.tolist(),
        "time_delays": time_delays.tolist(),
        "differece": (noisy_time_delays - time_delays).tolist()
    })
    data_save_path = Path(config['data_save_path'])
    filename = config['synthetic_data_filename'] + f"_std_{std}.csv"
    data_save_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(data_save_path/filename, index=False)

    # %%
    print(f"Successfully generated \033[92m{config['num_samples']}\033[0m synthetic data!\nSaved to \033[92m{data_save_path/filename}\033[0m")
