from services.pdf_loader import PDFLoader
from services.chunking import TextChunker
from utils.file_utils import save_chunks
from services.embeddings import EmbeddingService


def main():
    print("Loading PDFs...")
    loader = PDFLoader()
    documents = loader.load_pdfs("uploads")
    print(f"Loaded {len(documents)} pages")
    print("Chunking documents...")
    chunker = TextChunker()
    chunks = chunker.chunk_documents(documents)
    # for chunk in chunks:
    #     print("=" * 80)
    #     print(f"Source : {chunk['source']}")
    #     print(f"Page   : {chunk['page']}")
    #     print(f"Chunk ID: {chunk['chunk_id']}")
    #     print("-" * 80)
    #     print(chunk["content"])
    #     print("=" * 80)
    #     print()
    save_chunks(chunks)
    print("Initializing embedding service...")
    embedding_service = EmbeddingService()
    print("Generating embeddings...")
    chunks = embedding_service.generate_embeddings(chunks)
    print("Embedding service initialized successfully.")

    # Temporary verification
    print(f"Total Chunks : {len(chunks)}")
    print(f"Embedding Dimension : {len(chunks[0]['embedding'])}")

    print("\nFirst 10 values of the first embedding:")
    print(chunks[0]["embedding"][:10])

if __name__ == "__main__":
    main()