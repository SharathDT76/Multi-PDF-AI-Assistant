from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        print("=" * 80)
        print("Loading Cross Encoder...")
        print("=" * 80)

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("Cross Encoder Ready.")
        print("=" * 80)

    def rerank(
        self,
        question,
        chunks,
        top_k=5
    ):

        if not chunks:
            return []

        pairs = []

        for chunk in chunks:

            pairs.append(
                (
                    question,
                    chunk["content"]
                )
            )

        scores = self.model.predict(pairs)

        reranked = []

        for chunk, score in zip(chunks, scores):

            data = chunk.copy()

            data["rerank_score"] = float(score)

            reranked.append(data)

        reranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        # --------------------------------------------------
        # Relevance threshold
        # --------------------------------------------------

        MIN_RERANK_SCORE = -5.0

        filtered = [
            chunk
            for chunk in reranked
            if chunk["rerank_score"] >= MIN_RERANK_SCORE
        ]

        return filtered[:top_k]