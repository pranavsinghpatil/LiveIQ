import pennylane as qml
from pennylane import numpy as np
from tqdm import tqdm
from sklearn.decomposition import PCA

class QuantumEmbedder:
    def __init__(self, n_qubits=4, dev_name="default.qubit"):
        self.n_qubits = n_qubits
        self.dev = qml.device(dev_name, wires=n_qubits)
        # simple circuit with angle embedding + small variational layer
        def circuit(x, weights):
            qml.AngleEmbedding(x, wires=range(self.n_qubits))
            for i in range(len(weights)):
                for w in range(self.n_qubits):
                    qml.RY(weights[i][w], wires=w)
                    qml.RZ(weights[i][w]*0.5, wires=w)
            return [qml.expval(qml.PauliZ(i)) for i in range(self.n_qubits)]
        self.qnode = qml.QNode(circuit, self.dev)
        # random weights as we only need deterministic mapping; could learn later
        self.weights = np.random.normal(0, 0.1, (1, self.n_qubits))

    def text_to_angles(self, text):
        # Very simple text -> numeric vector: hash tokens -> top-k normalization
        # This is a placeholder. Replace with better tokenizer -> numeric features mapped to angles.
        vec = [ (ord(c) % 10)/10.0 for c in text[:self.n_qubits] ]
        # pad
        while len(vec) < self.n_qubits:
            vec.append(0.0)
        return np.array(vec)

    def encode(self, texts):
        emb = []
        for t in tqdm(texts, desc="Quantum encode"):
            angles = self.text_to_angles(t)
            out = self.qnode(angles, self.weights)
            emb.append(np.array(out, dtype=float))
        emb = np.stack(emb)
        # Optionally expand using PCA or kernel trick later; return as numpy
        return np.array(emb)
