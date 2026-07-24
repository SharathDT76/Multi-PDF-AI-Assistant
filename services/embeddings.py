from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

class EmbeddingService:
    
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        print("Loaded Embedding Model Successfully")

    def generate_embeddings(self, chunks):
        texts = []
        for chunk in chunks:
            texts.append(chunk['content'])

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
        )
        for chunk , embedding in zip(chunks,embeddings):
            chunk["embedding"] = embedding.tolist()
        return chunks