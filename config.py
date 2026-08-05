# Application
APP_NAME = "Multi-PDF AI Assistant"

# Directories
UPLOAD_FOLDER = "uploads"
FAISS_INDEX_PATH = "storage/faiss_index/index.faiss"
METADATA_PATH = "storage/metadata/metadata.pkl"

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 120

# Retrieval
TOP_K = 5

# Embedding Model
EMBEDDING_MODEL = "BAAI/bge-m3"

# LLM
OLLAMA_MODEL = "llama3"

# Logging
LOG_FILE = "logs/app.log"

#Embedding Model

EMBEDDING_MODEL  = "BAAI/bge-m3"  # Can replace the model later with any model

FAISS_INDEX_PATH = "storage/faiss_index/index.faiss"