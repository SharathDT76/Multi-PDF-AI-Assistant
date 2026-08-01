import json
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

        print(f"Loaded{len(self.chunks)} chunks.")
        print("retriever initialized successfully.")

    def search(self , question, top_k = 3):
        pass