import faiss
import os
import numpy as np
from config import FAISS_INDEX_PATH

class VectorStore:
    def __init__(self):
        self.index = None

    def build_index(self,chunks):
        embeddings = []
        for chunk in chunks:
            embeddings.append(chunk["embedding"])
        embedding_matrix = np.array(
            embeddings,
            dtype = np.float32
        )
        # print(type(embedding_matrix))
        # print(embedding_matrix.shape)

        dimension = embedding_matrix.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embedding_matrix)

        print(f"FAISS index Created Successfully!")
        print(f"Total number of vectors in the index: {self.index.ntotal}")
        print(f"Dimension of the vectors in the index: {self.index.d}")


    def save_index(self):
        os.makedirs(
            os.path.dirname(FAISS_INDEX_PATH),
            exist_ok=True
        )

        faiss.write_index(
            self.index, 
            FAISS_INDEX_PATH
        )
        print(f"FAISS index saved to {FAISS_INDEX_PATH}")

    
    def load_index(self):
        self.index = faiss.read_index(FAISS_INDEX_PATH)
        print(f"FAISS index loaded from {FAISS_INDEX_PATH}")