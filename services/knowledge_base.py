from services.pdf_loader import PDFLoader
from services.chunking import TextChunker
from services.embeddings import EmbeddingService
from services.vector_store import VectorStore
from utils.file_utils import save_chunks


class KnowledgeBase:

    def __init__(self):
        pass

    def build(self, upload_folder):
        print("=" * 80)
        print("BUILDING KNOWLEDGE BASE")
        print("=" * 80)

        loader = PDFLoader()
        documents = loader.load_pdfs(upload_folder)

        chunker = TextChunker()
        chunks = chunker.chunk_documents(documents)

        save_chunks(chunks)

        embedding_service = EmbeddingService()
        chunks = embedding_service.generate_embeddings(chunks)

        vector_store = VectorStore()
        vector_store.build_index(chunks)
        vector_store.save_index()

        return {
            "documents": len(documents),
            "chunks": len(chunks)
        }