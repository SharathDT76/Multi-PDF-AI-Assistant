import faiss
import numpy as np
from config import FAISS_INDEX_PATH

class VectorStore:
    def ____init__(self):
        self.index = None

    def build_index(self,chunks):
        embeddings = []
        for chunk in chunks:
            embeddings.append(chunk["embedding"])
        embedding_matrix = np.array(
            embeddings,
            dtype = np.float32
        )
        dimension = embedding_matrix.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embedding_matrix)

        print(f"FAISS index Created Successfully!")
        print(f"Total number of vectors in the index: {self.index.ntotal}")
        print(f"Dimension of the vectors in the index: {self.index.d}")


    def save_index(self):
        pass
    
    def load_index(self):
        pass