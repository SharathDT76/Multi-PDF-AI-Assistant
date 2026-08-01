from services.pdf_loader import PDFLoader
from services.chunking import TextChunker
from services.embeddings import EmbeddingService
from services.vector_store import VectorStore
from services.retriever import Retriever

from utils.file_utils import save_chunks


def build_knowledge_base():

    print("=" * 80)
    print("BUILDING KNOWLEDGE BASE")
    print("=" * 80)

    # Step 1 : Load PDFs
    print("Loading PDFs...")
    loader = PDFLoader()
    documents = loader.load_pdfs("uploads")
    print(f"Loaded {len(documents)} pages")

    # Step 2 : Chunk Documents
    print("\nChunking documents...")
    chunker = TextChunker()
    chunks = chunker.chunk_documents(documents)
    save_chunks(chunks)
    print(f"Created {len(chunks)} chunks")

    # Step 3 : Generate Embeddings
    print("\nGenerating embeddings...")
    embedding_service = EmbeddingService()
    chunks = embedding_service.generate_embeddings(chunks)
    print("Embeddings generated successfully.")

    # Step 4 : Build FAISS
    print("\nBuilding FAISS Index...")
    vector_store = VectorStore()
    vector_store.build_index(chunks)
    vector_store.save_index()
    print("Knowledge Base Created Successfully!")
    return len(chunks)


def ask_question(question):
    print("=" * 80)
    print("QUESTION")
    print("=" * 80)
    print(question)
    retriever = Retriever()
    results = retriever.search(question)
    print("\nRetrieved Chunks\n")
    for i, result in enumerate(results, start=1):
        print("=" * 80)
        print(f"Result #{i}")
        print(f"Source : {result['source']}")
        print(f"Page   : {result['page']}")
        print("-" * 80)
        print(result["content"])
        print("=" * 80)
    return results

def main():
    build_knowledge_base()
    ask_question("What is StringBuilder?")

if __name__ == "__main__":
    main()