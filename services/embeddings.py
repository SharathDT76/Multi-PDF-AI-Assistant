import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


class EmbeddingService:

    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        print("Loaded Embedding Model Successfully")

    def generate_embeddings(self, chunks):
        """
        Generate embeddings for all document chunks.
        """

        texts = []

        for chunk in chunks:
            texts.append(chunk["content"])

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True
        )

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding.tolist()

        return chunks

    def generate_query_embedding(self, question):
        """
        Generate embedding for a user's question.
        """

        embedding = self.model.encode(
            [question]
        )

        return np.array(
            embedding,
            dtype=np.float32
        )