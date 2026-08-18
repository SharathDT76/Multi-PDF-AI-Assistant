import json

from services.embedding.embeddings import EmbeddingService
from services.embedding.vector_store import VectorStore


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

    def _search_single_query(self, question, top_k=10):

        query_embedding = (
            self.embedding_service.generate_query_embedding(
                question
            )
        )

        distances, indices = self.vector_store.index.search(
            query_embedding,
            top_k
        )

        DISTANCE_THRESHOLD = 1.20

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index == -1:
                continue

            if distance > DISTANCE_THRESHOLD:
                continue

            chunk = self.chunks[index].copy()

            chunk["score"] = float(distance)

            results.append(chunk)

        return results

    def search(self, question, top_k=10):

        """
        Search using either:

        1. A single question string
        2. A list of expanded queries
        """

        print("\nSearching for:", question)

        # --------------------------------------------------
        # Convert single query into a list
        # --------------------------------------------------

        if isinstance(question, str):

            queries = [question]

        else:

            queries = question

        # --------------------------------------------------
        # Search every query
        # --------------------------------------------------

        all_results = []

        for query in queries:

            print(f"Searching query: {query}")

            results = self._search_single_query(
                query,
                top_k
            )

            all_results.extend(results)

        # --------------------------------------------------
        # Remove duplicate chunks
        # --------------------------------------------------

        unique_results = {}

        for chunk in all_results:

            chunk_id = chunk["id"]

            # Keep the best score
            if (
                chunk_id not in unique_results
                or chunk["score"] < unique_results[chunk_id]["score"]
            ):

                unique_results[chunk_id] = chunk

        results = list(unique_results.values())

        # --------------------------------------------------
        # Sort by relevance
        # Lower FAISS L2 distance = better match
        # --------------------------------------------------

        results.sort(
            key=lambda x: x["score"]
        )

        # --------------------------------------------------
        # Keep final top results
        # --------------------------------------------------

        results = results[:5]

        # --------------------------------------------------
        # Debug information
        # --------------------------------------------------

        print("\n" + "=" * 80)
        print("Top Retrieved Chunks")
        print("=" * 80)

        if len(results) == 0:

            print("No relevant chunks found.")

        else:

            for i, chunk in enumerate(
                results,
                start=1
            ):

                print(
                    f"{i}. "
                    f"{chunk['source']} | "
                    f"Page {chunk['page']} | "
                    f"Distance = {chunk['score']:.4f}"
                )

        print("=" * 80 + "\n")

        return results