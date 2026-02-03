import fitz
import os

def load_pdfs(data_folder="data"):
    documents = []
    for file in os.listdir(data_folder):
        if file.endswith(".pdf"):
            path = os.path.join(data_folder, file)
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            documents.append({
                "source": file,
                "text": text
            })
    return documents
