import json
import os
def save_chunks(chunks):
    #Creates a folder if it doesn't exists
    os.makedirs("storage/metadata", exist_ok=True)

    file_path = "storage/metadata/chunks.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)
    
    print(f"{len(chunks)} chunks saved to {file_path} successfully.")