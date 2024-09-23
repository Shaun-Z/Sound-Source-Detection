# Sound-Source-Detection
This is a project for Task "Sound Source Detection"

- [Sound-Source-Detection](#sound-source-detection)
  - [Time Delay of Arrival (TDoA) Algorithm](#time-delay-of-arrival-tdoa-algorithm)
    - [Generate synthetic data](#generate-synthetic-data)
    - [Visualize synthetic data](#visualize-synthetic-data)
    - [Validate TDoA-WLS algoritm](#validate-tdoa-wls-algoritm)
  - [Time Delay Estimation](#time-delay-estimation)


## Time Delay of Arrival (TDoA) Algorithm

### Generate synthetic data
```python
python utils/systhetic_data_generate.py --std 0.001
```
- std: standard deviation of the Gaussian noise

Synthetic data will be stored under `data/tdoa/synthetic`.

File name: `synthetic_data_std_{std}.csv`

### Visualize synthetic data

```python
python utils/synthetic_data_visualize.py
```

### Validate TDoA-WLS algoritm
```python
python TDoA_WLS_test.py --std 0.001
```

The result will be saved to `result/localization`.

File name: `localization_result_predicted_std_{std}.csv`

Source: [Time Difference of Arrival (TDoA) Localization Combining Weighted Least Squares and Firefly Algorithm](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6603714/)

## Time Delay Estimation

TBC