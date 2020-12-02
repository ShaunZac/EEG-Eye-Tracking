import pandas as pd
from scipy.signal import butter, lfilter
from sklearn.decomposition import FastICA


def bpf(data: pd.DataFrame) -> pd.DataFrame:
    b, a = butter(N=10, Wn=[1, 40], btype='band',
                  analog=False, output='ba', fs=128)
    for i in range(data.shape[1]):
        data.iloc[:, i] = lfilter(b, a, data.iloc[:, i])
    return data


def ica(data: pd.DataFrame) -> pd.DataFrame:
    transformer = FastICA(random_state=0)
    data_transformed = transformer.fit_transform(data)
    return data_transformed


df = pd.read_csv("eeg-eye-state.csv")
eeg_input = df.iloc[:, :-1]
open_shut = df.iloc[:, -1]

# normalize input for faster convergence
eeg_input = (eeg_input-eeg_input.mean())/eeg_input.std()

# perform bandpass filtering on input
preprocessed_eeg = bpf(eeg_input)

# Perform ICA on input
ica_eeg = ica(eeg_input)

# extract features from preprocessed and ICA extracted components separately

# Use an ML algorithm to predict
