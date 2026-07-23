import fitz
from pathlib import Path

class PDFLoader:
    def __init__(self):
        pass
    def load_pdfs(self,upload_folder):
        folder = Path(upload_folder)
        pdf_files = list(folder.glob("*.pdf")) #Uploads only the documents ending with .pdf and ignores the rest of the files in the uploads folder
        documents = [] # List to store the loaded PDF documents

        for pdf_file in pdf_files: # Loop through each PDF file found in the uploads folder
            with fitz.open(pdf_file) as document: # Loads the PDF into memory.
                for page_number, page in enumerate(document): # enumerate is used to get the page number and the page object for each page in the PDF document.
                    text = page.get_text().strip() # Extracts the text from the current page.
                    if not text:
                        continue # If the extracted text is empty, skip to the next page.

                    page_data = {
                        "content" : text,
                        "source" : pdf_file.name,
                        "page" : page_number + 1
                    }
                    documents.append(page_data) # Appends a dictionary containing the file name, page number, and extracted text to the documents list.

        return documents


            

