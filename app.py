from services.pdf_loader import PDFLoader
from services.chunking import TextChunker
from utils.file_utils import save_chunks
from services.embeddings import EmbeddingService
from services.vector_store import VectorStore

def main():
    print("Loading PDFs...")
    loader = PDFLoader()
    documents = loader.load_pdfs("uploads")
    print(f"Loaded {len(documents)} pages")


    print("Chunking documents...")
    chunker = TextChunker()
    chunks = chunker.chunk_documents(documents)
    save_chunks(chunks)


    print("Initializing embedding service...")
    embedding_service = EmbeddingService()

    print("Generating embeddings...")
    chunks = embedding_service.generate_embeddings(chunks)
    print("Embedding service initialized successfully.")

    print("Vectore store initialization...")
    vector_store = VectorStore()    
    print("Building FAISS index...")
    vector_store.build_index(chunks)
    vector_store.save_index()

if __name__ == "__main__":
    main()