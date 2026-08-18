from rank_bm25 import BM25Okapi
import json


class BM25Search:

    def __init__(self):

        with open(
            "storage/metadata/chunks.json",
            "r",
            encoding="utf-8"
        ) as file:

            self.chunks = json.load(file)

        corpus = []

        for chunk in self.chunks:

            corpus.append(
                chunk["content"].lower().split()
            )

        self.bm25 = BM25Okapi(corpus)

        print("BM25 Search Initialized")

    def search(self, question, top_k=5):

        tokens = question.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(

            zip(scores, self.chunks),

            key=lambda x: x[0],

            reverse=True

        )

        results = []

        for score, chunk in ranked[:top_k]:

            data = chunk.copy()

            data["bm25_score"] = float(score)

            results.append(data)

        return results