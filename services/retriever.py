import json

from services.embeddings import EmbeddingService
from services.vector_store import VectorStore


class Retriever:

    def __init__(self):
        print("=" * 80)
        print("Initializing Retriever...")
        print("=" * 80)

        # Initialize Embedding Service
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
        print("=" * 80)

    def search(self, question, top_k=10):
        """
        Retrieve the most relevant chunks for a user question.
        """

        print("\nSearching for:", question)

        # Step 1 : Generate Query Embedding
        query_embedding = self.embedding_service.generate_query_embedding(
            question
        )

        # Step 2 : Search FAISS
        distances, indices = self.vector_store.index.search(
            query_embedding,
            top_k
        )

        # ------------------------------------------------------------------
        # Distance Threshold
        #
        # Lower distance = Better Match
        #
        # Tune this value later based on your embedding model.
        # ------------------------------------------------------------------

        DISTANCE_THRESHOLD = 1.20

        results = []

        for distance, index in zip(distances[0], indices[0]):

            # Invalid Index
            if index == -1:
                continue

            # Ignore weak matches
            if distance > DISTANCE_THRESHOLD:
                continue

            chunk = self.chunks[index].copy()

            chunk["score"] = float(distance)

            results.append(chunk)

        # Sort by Best Match
        results.sort(key=lambda x: x["score"])

        # Keep only top 5
        results = results[:5]

        # Debug Information
        print("\n" + "=" * 80)
        print("Top Retrieved Chunks")
        print("=" * 80)

        if len(results) == 0:
            print("No relevant chunks found.")
        else:

            for i, chunk in enumerate(results, start=1):

                print(
                    f"{i}. "
                    f"{chunk['source']} | "
                    f"Page {chunk['page']} | "
                    f"Distance = {chunk['score']:.4f}"
                )

        print("=" * 80 + "\n")

        return results