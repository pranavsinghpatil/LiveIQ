import argparse
import yaml
from pipelines.data_pipeline import load_sample_dataset
from embeddings.classical import ClassicalEmbedder
from embeddings.quantum import QuantumEmbedder
from pipelines.trainer import train_and_eval
from pipelines.analyzer import save_report
import os
import numpy as np
import random

def set_seed(seed=42):
    import torch, random
    np.random.seed(seed)
    random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
    except:
        pass

def run_experiment(cfg):
    set_seed(cfg.get("seed", 42))
    print("Loading dataset...")
    X_train, y_train, X_test, y_test = load_sample_dataset(cfg["dataset"]["name"], n_per_class=cfg["dataset"].get("n_per_class", 200))
    results = {}

    # Classical embeddings
    print("Computing classical embeddings...")
    cls = ClassicalEmbedder(model_name=cfg["classical"]["model_name"])
    X_train_cls = cls.encode(X_train)
    X_test_cls = cls.encode(X_test)
    res_cls = train_and_eval(X_train_cls, y_train, X_test_cls, y_test, cfg["trainer"])
    results["classical"] = res_cls

    # Quantum embeddings
    print("Computing quantum embeddings (this may be slow)...")
    qd = QuantumEmbedder(n_qubits=cfg["quantum"]["n_qubits"], dev_name=cfg["quantum"].get("dev","default.qubit"))
    X_train_q = qd.encode(X_train)
    X_test_q = qd.encode(X_test)
    res_q = train_and_eval(X_train_q, y_train, X_test_q, y_test, cfg["trainer"])
    results["quantum"] = res_q

    out_dir = cfg.get("output_dir","./outputs")
    os.makedirs(out_dir, exist_ok=True)
    save_report(results, out_dir)
    print("Experiment finished. Results saved to", out_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="src/config.yaml")
    args = parser.parse_args()
    cfg = yaml.safe_load(open(args.config))
    run_experiment(cfg)
