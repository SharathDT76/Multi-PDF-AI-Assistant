import json

from services.embeddings import EmbeddingService
from services.vector_store import VectorStore


class Retriever:

    def __init__(self):
        print("Initializing Retriever...")

        # Embedding Service
        self.embedding_service = EmbeddingService()

        # Load FAISS Index
        self.vector_store = VectorStore()
        self.vector_store.load_index()

        # Load Chunk Metadata
        with open(
            "storage/metadata/chunks.json",
            "r",
            encoding="utf-8"
        ) as file:
            self.chunks = json.load(file)

        print(f"Loaded {len(self.chunks)} chunks.")
        print("Retriever initialized successfully.")

    def search(self, question, top_k=3):
        """
        Retrieve the most relevant chunks for a user question.
        """

        # Step 1: Generate query embedding
        query_embedding = self.embedding_service.generate_query_embedding(
            question
        )

        # Step 2: Search the FAISS index
        distances, indices = self.vector_store.index.search(
            query_embedding,
            top_k
        )

        # Step 3: Collect matching chunks
        results = []

        for index in indices[0]:
            if index == -1:
                continue

            results.append(self.chunks[index])

        return results