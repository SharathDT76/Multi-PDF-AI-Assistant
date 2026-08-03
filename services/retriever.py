import json
import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL
from services.vector_store import VectorStore

class Retriever:

    def __init__(self):
        print("Initializing Retriever...")
        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )
        self.vector_store = VectorStore()
        self.vector_store.load_index()
        with open(
            "storage/metadata/chunks.json",
            "r",
            encoding="utf-8"
        ) as file:
            self.chunks = json.load(file)

        print(f"Loaded {len(self.chunks)} chunks.")
        print("retriever initialized successfully.")

    def query_embedding(self,question):
        embedding = self.embedding_model.encode([question])
        return np.array(
            embedding,
            dtype = np.float32
        )

    def search(self , question, top_k = 3):
        #Step 1: Generate embedding for the question
        query_embedding = self.query_embedding(question)

        #Step 2: Search Faiss

        distances, indices = self.vector_store.index.search(
            query_embedding,
            top_k
        )

        #Step 3 : Collect the matching chunks
        results = []
        for index in indices[0]:
            results.append(self.chunks[index])
        return results