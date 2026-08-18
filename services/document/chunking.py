from config import CHUNK_SIZE, CHUNK_OVERLAP


class TextChunker:

    def __init__(self):

        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
            )

    def chunk_documents(self, documents):

        chunks = []

        for document in documents:

            text = document["content"].strip()

            source = document["source"]

            page = document["page"]

            chunk_id = 1

            # -------------------------------------------------
            # Split page into paragraphs
            # -------------------------------------------------

            paragraphs = [
                p.strip()
                for p in text.split("\n\n")
                if p.strip()
            ]

            for paragraph in paragraphs:

                # Small paragraph
                if len(paragraph) <= self.chunk_size:

                    chunks.append({

                        "id": f"{source}_page_{page}_chunk_{chunk_id}",

                        "content": paragraph,

                        "source": source,

                        "page": page,

                        "chunk_id": chunk_id,

                        "word_count": len(paragraph.split()),

                        "contains_code": "{" in paragraph or ";" in paragraph

                    })

                    chunk_id += 1

                    continue

                # ---------------------------------------------
                # Large paragraph
                # ---------------------------------------------

                start = 0

                while start < len(paragraph):

                    end = min(
                        start + self.chunk_size,
                        len(paragraph)
                    )

                    chunk_text = paragraph[start:end]

                    chunks.append({

                        "id": f"{source}_page_{page}_chunk_{chunk_id}",

                        "content": chunk_text,

                        "source": source,

                        "page": page,

                        "chunk_id": chunk_id,

                        "word_count": len(chunk_text.split()),

                        "contains_code": "{" in chunk_text or ";" in chunk_text

                    })

                    chunk_id += 1

                    if end == len(paragraph):
                        break

                    start = end - self.chunk_overlap

        return chunks