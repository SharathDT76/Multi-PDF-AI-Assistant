from services.pdf_loader import PDFLoader
from services.chunking import TextChunker
from services.embeddings import EmbeddingService
from services.vector_store import VectorStore
from services.retriever import Retriever
from services.prompt_builder import PromptBuilder
from services.llm import LLMService

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

    # Step 4 : Build FAISS Index
    print("\nBuilding FAISS Index...")
    vector_store = VectorStore()

    vector_store.build_index(chunks)
    vector_store.save_index()

    print("\nKnowledge Base Created Successfully!")

    return len(chunks)


def ask_question(question):

    print("=" * 80)
    print("QUESTION")
    print("=" * 80)

    print(question)

    retriever = Retriever()

    retrieved_chunks = retriever.search(question)

    prompt_builder = PromptBuilder()

    prompt = prompt_builder.build_prompt(
        question,
        retrieved_chunks
    )

    llm = LLMService()

    answer = llm.generate_response(prompt)

    return answer


def main():

    # Build Knowledge Base
    # build_knowledge_base()

    # Example Question
    question = "What is StringBuilder?"

    prompt = ask_question(question)

    print("\n" + "=" * 80)
    print("PROMPT SENT TO LLM")
    print("=" * 80)
    print(prompt)


if __name__ == "__main__":
    main()