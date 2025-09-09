import json
import os
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

def save_report(results, out_dir):
    # save JSON
    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    # quick bar plot
    labels = list(results.keys())
    accs = [ results[k]["accuracy"] for k in labels ]
    plt.figure(figsize=(6,4))
    plt.bar(labels, accs)
    plt.title("Accuracy by embedding type")
    plt.ylabel("Accuracy")
    plt.savefig(os.path.join(out_dir, "accuracy_bar.png"))
    plt.close()
