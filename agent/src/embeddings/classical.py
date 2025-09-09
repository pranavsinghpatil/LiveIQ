from sentence_transformers import SentenceTransformer
import numpy as np
class ClassicalEmbedder:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        print("Loading SBERT model:", model_name)
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, batch_size=32):
        return np.array(self.model.encode(texts, batch_size=batch_size, show_progress_bar=True))
