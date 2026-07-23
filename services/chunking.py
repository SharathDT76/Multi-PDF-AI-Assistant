from config import CHUNK_SIZE, CHUNK_OVERLAP
class TextChunker:

    def __init__(self):
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
            )

    def chunk_documents(self,documents):
        chunks = []
        for document in documents:
            start = 0
            chunk_id = 1
            text = document["content"]
            source = document["source"]
            page = document["page"]
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                chunk_text = text[start:end]
                if not chunk_text:
                    break
                
                chunk_data = {
                    "id": f"{source}_page_{page}_chunk_{chunk_id}",
                    "content" : chunk_text,
                    "source" : source,
                    "page" : page,
                    "chunk_id" : chunk_id
                }
                chunks.append(chunk_data) 

                if end == len(text):
                    break
                
                start = end - self.chunk_overlap
                chunk_id += 1
        return chunks