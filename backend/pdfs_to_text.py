# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pymupdf",
# ]
# ///

# use os.walkdir for looping throgh all pdf's in unzipped_raw_data/documents_data folder store the text in a list
import fitz  # PyMuPDF
import os 
pdf_texts = []

# pdf_dir = "unzipped_raw_data/analytics_data"
pdf_dir = os.path.join(os.getcwd(), "unzipped_raw_data", "documents_data")
print(f"pdf_dir: {pdf_dir}")
for root, dirs, files in os.walk(pdf_dir):
    print(files)
    for file in files:
        if file.lower().endswith(".pdf"):
            
            file_path = os.path.join(root, file)
            try:
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                    with open(os.path.join(os.getcwd(), "processed_pdfs_docs", file + ".txt"), "w", encoding="utf-8") as f:
                        f.write(text)
                pdf_texts.append(text)
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")

