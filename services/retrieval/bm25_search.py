import json
import re

from rank_bm25 import BM25Okapi


class BM25Search:

    def __init__(self):

        print("=" * 80)
        print("Initializing BM25 Search...")
        print("=" * 80)

        with open(
            "storage/metadata/chunks.json",
            "r",
            encoding="utf-8"
        ) as file:

            self.chunks = json.load(file)

        corpus = [
            self._tokenize(chunk["content"])
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(corpus)

        print(f"BM25 indexed {len(self.chunks)} chunks.")
        print("BM25 Search Initialized.")
        print("=" * 80)

    def _tokenize(self, text):

        return re.findall(
            r"\b[\w+#.-]+\b",
            text.lower()
        )

    def search(self, question, top_k=10):

        tokens = self._tokenize(question)

        if not tokens:
            return []

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(scores, self.chunks),
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for score, chunk in ranked[:top_k]:

            # Ignore chunks with zero lexical relevance
            if score <= 0:
                continue

            data = chunk.copy()

            data["bm25_score"] = float(score)

            results.append(data)

        return results