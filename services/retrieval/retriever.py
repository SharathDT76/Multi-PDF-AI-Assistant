import json

from services.embedding.embeddings import EmbeddingService
from services.embedding.vector_store import VectorStore

from services.retrieval.bm25_search import BM25Search
from services.retrieval.reranker import Reranker


class Retriever:

    def __init__(self):

        print("=" * 80)
        print("Initializing Hybrid Retriever...")
        print("=" * 80)

        # --------------------------------------------------
        # Embedding Service
        # --------------------------------------------------

        self.embedding_service = EmbeddingService()

        # --------------------------------------------------
        # FAISS Vector Store
        # --------------------------------------------------

        self.vector_store = VectorStore()
        self.vector_store.load_index()

        # --------------------------------------------------
        # Chunk Metadata
        # --------------------------------------------------

        with open(
            "storage/metadata/chunks.json",
            "r",
            encoding="utf-8"
        ) as file:

            self.chunks = json.load(file)

        print(
            f"Loaded {len(self.chunks)} chunks."
        )

        # --------------------------------------------------
        # BM25
        # --------------------------------------------------

        self.bm25 = BM25Search()

        # --------------------------------------------------
        # Cross Encoder
        # --------------------------------------------------

        self.reranker = Reranker()

        print("Hybrid Retriever initialized successfully.")
        print("=" * 80)

    # ======================================================
    # VECTOR SEARCH
    # ======================================================

    def _vector_search(
        self,
        question,
        top_k=10
    ):

        query_embedding = (
            self.embedding_service
            .generate_query_embedding(question)
        )

        distances, indices = (
            self.vector_store.index.search(
                query_embedding,
                top_k
            )
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index == -1:
                continue

            chunk = self.chunks[index].copy()

            chunk["vector_score"] = float(distance)

            results.append(chunk)

        return results

    # ======================================================
    # HYBRID SEARCH
    # ======================================================

    def search(
        self,
        questions,
        top_k=5
    ):

        # --------------------------------------------------
        # Accept either:
        #
        # "What is DFS?"
        #
        # OR
        #
        # [
        #     "What is DFS?",
        #     "Depth First Search",
        #     "Graph Traversal"
        # ]
        # --------------------------------------------------

        if isinstance(questions, str):

            queries = [questions]

        else:

            queries = questions

        print("\n" + "=" * 80)
        print("HYBRID RETRIEVAL")
        print("=" * 80)

        print("Queries:")

        for query in queries:

            print(f"  - {query}")

        # --------------------------------------------------
        # Candidate storage
        # --------------------------------------------------

        candidates = {}

        # --------------------------------------------------
        # Search every expanded query
        # --------------------------------------------------

        for query in queries:

            # ==============================================
            # FAISS
            # ==============================================

            vector_results = self._vector_search(
                query,
                top_k=10
            )

            # ==============================================
            # BM25
            # ==============================================

            bm25_results = self.bm25.search(
                query,
                top_k=10
            )

            # ==============================================
            # Add FAISS results
            # ==============================================

            for chunk in vector_results:

                chunk_id = chunk["id"]

                if chunk_id not in candidates:

                    candidates[chunk_id] = chunk

                else:

                    existing = candidates[chunk_id]

                    if (
                        "vector_score" not in existing
                        or chunk["vector_score"]
                        < existing["vector_score"]
                    ):

                        existing["vector_score"] = (
                            chunk["vector_score"]
                        )

            # ==============================================
            # Add BM25 results
            # ==============================================

            for chunk in bm25_results:

                chunk_id = chunk["id"]

                if chunk_id not in candidates:

                    candidates[chunk_id] = chunk

                else:

                    existing = candidates[chunk_id]

                    if "bm25_score" in chunk:

                        if (
                            "bm25_score" not in existing
                            or chunk["bm25_score"]
                            > existing["bm25_score"]
                        ):

                            existing["bm25_score"] = (
                                chunk["bm25_score"]
                            )

        # --------------------------------------------------
        # Convert dictionary to list
        # --------------------------------------------------

        candidate_chunks = list(
            candidates.values()
        )

        print(
            f"\nCandidate chunks before reranking: "
            f"{len(candidate_chunks)}"
        )

        # --------------------------------------------------
        # Nothing found
        # --------------------------------------------------

        if not candidate_chunks:

            print("No candidates found.")

            return []

        # --------------------------------------------------
        # Cross Encoder Reranking
        # --------------------------------------------------

        reranked_chunks = self.reranker.rerank(
            queries[0],
            candidate_chunks,
            top_k=top_k
        )

        # --------------------------------------------------
        # Debug
        # --------------------------------------------------

        print("\n" + "-" * 80)
        print("FINAL RERANKED RESULTS")
        print("-" * 80)

        for i, chunk in enumerate(
            reranked_chunks,
            start=1
        ):

            print(
                f"\n{i}. "
                f"{chunk['source']} | "
                f"Page {chunk['page']} | "
                f"Rerank = "
                f"{chunk.get('rerank_score', 0):.4f}"
            )

            print("-" * 60)

            print(
                chunk["content"][:500]
            )

            print("-" * 60)

        return reranked_chunks