from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

def train_and_eval(X_train, y_train, X_test, y_test, cfg):
    model_type = cfg.get("model","svm")
    if model_type == "svm":
        params = cfg.get("svm",{})
        model = SVC(C=params.get("C",1.0), kernel='rbf', probability=False)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='macro')
        return {"accuracy": float(acc), "f1_macro": float(f1)}
    else:
        raise NotImplementedError("Only svm implemented in MVP")
