from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_20newsgroups
import random

def load_sample_dataset(name="sst2", n_per_class=200):
    # Quick small dataset: use 20newsgroups subset as substitute if SST2 not present
    # For MVP we sample two classes to make binary classification
    cats = ['rec.sport.hockey', 'sci.space']
    data = fetch_20newsgroups(subset='train', categories=cats, remove=('headers','footers','quotes'))
    texts = data.data
    labels = data.target
    # Sample balanced subset
    import numpy as np
    X = np.array(texts)
    y = np.array(labels)
    Xs, ys = [], []
    for cls in np.unique(y):
        idx = np.where(y==cls)[0]
        sel = np.random.choice(idx, size=min(n_per_class, len(idx)), replace=False)
        Xs.extend(X[sel].tolist())
        ys.extend(y[sel].tolist())
    X_train, X_test, y_train, y_test = train_test_split(Xs, ys, test_size=0.2, random_state=42, stratify=ys)
    return X_train, y_train, X_test, y_test
