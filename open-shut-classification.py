import numpy as np
import pandas as pd
from scipy.signal import butter, lfilter


def bpf(data: pd.DataFrame) -> pd.DataFrame:
    b, a = butter(10, [1, 40], 'band', False, 'ba', 128)
    for i in range(14):
        data.iloc[:, i] = lfilter(b, a, data.iloc[:, i])
    return data


df = pd.read_csv("eeg-eye-state.csv")
# perform bandpass filtering on input
df = bpf(df)
# extract min and max amplitude from temporal windows

# Perform ICA on the min-max channels

# Use an ML algorithm to predict
