import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import FastICA
from sklearn.model_selection import train_test_split
WINDOW_SIZE = 35


def normalize(data: pd.DataFrame) -> pd.DataFrame:
    return (data-data.mean())/data.std()


def bpf(data: pd.DataFrame) -> pd.DataFrame:
    b, a = butter(N=10, Wn=[1, 40], btype='band',
                  analog=False, output='ba', fs=128)
    for i in range(data.shape[1]):
        data.iloc[:, i] = lfilter(b, a, data.iloc[:, i])
    return data


def ica(data: pd.DataFrame) -> pd.DataFrame:
    transformer = FastICA(random_state=0)
    data_transformed = transformer.fit_transform(data)
    return pd.DataFrame(data_transformed, columns=data.columns)


def feature_extract(data: pd.DataFrame) -> pd.DataFrame:
    data_min = data.rolling(WINDOW_SIZE).min()[WINDOW_SIZE::WINDOW_SIZE//2]
    data_max = data.rolling(WINDOW_SIZE).max()[WINDOW_SIZE::WINDOW_SIZE//2]
    data = pd.concat([data_min, data_max], axis=1)
    return data


def classify(X: pd.DataFrame, y: pd.DataFrame) -> float:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
                                                        random_state=10)
    model = RandomForestClassifier(max_depth=15, random_state=0)
    model.fit(X_train, y_train)
    return model.score(X_test, y_test)


def plot_bar(direct_score: float, feature_score: float):
    x = [1, 2]
    label = ["Without Feature Extraction", "With Feature Extraction"]
    score = [direct_score*100, feature_score*100]
    plt.ylim(0, 100)
    plt.bar(x, score, width=0.5)
    plt.xticks(x, label)
    plt.ylabel("Accuracy of Prediction (%)")
    plt.show()
    return


df = pd.read_csv("eeg-eye-state.csv")
eeg_input = df.iloc[:, :-1]
open_shut = df.iloc[:, -1]

# normalize input for faster convergence
eeg_input = normalize(eeg_input)

# perform bandpass filtering on input
preprocessed_eeg = bpf(eeg_input)

# Perform ICA on input
ica_eeg = ica(preprocessed_eeg)

# extract features from preprocessed and ICA extracted components separately
preprocessed_eeg = feature_extract(preprocessed_eeg)
ica_eeg = feature_extract(ica_eeg)
open_shut_windowed = open_shut.rolling(WINDOW_SIZE).mean()[WINDOW_SIZE::WINDOW_SIZE//2].round(0)

# Use an ML algorithm to predict
score_direct = classify(eeg_input, open_shut)
score_feature = classify(preprocessed_eeg, open_shut_windowed)
plot_bar(score_direct, score_feature)
