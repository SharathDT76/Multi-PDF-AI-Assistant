from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        print("Loading Cross Encoder...")

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("Cross Encoder Ready.")

    def rerank(self, question, chunks, top_k=5):

        if len(chunks) == 0:
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

        for chunk, score in zip(chunks, scores):

            chunk["rerank_score"] = float(score)

        chunks.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return chunks[:top_k]