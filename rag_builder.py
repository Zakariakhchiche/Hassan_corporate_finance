import os
import glob
import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def chunk_text(text, chunk_size=1000):
    # Split by sentences or paragraphs roughly
    chunks = []
    current_chunk = ""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def build_rag():
    pdf_dir = "rag_pdfs"
    output_dir = "scraped_rag_pdfs"
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path).replace(".pdf", ".md")
        output_path = os.path.join(output_dir, filename)
        
        print(f"Processing {pdf_path}...")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            chunks = chunk_text(text)
            
            with open(output_path, "w", encoding="utf-8") as f:
                for i, chunk in enumerate(chunks):
                    f.write(f"## Chunk {i+1}\n\n{chunk}\n\n")
            
            print(f"Saved {output_path} with {len(chunks)} chunks.")
        else:
            print(f"Failed to extract text from {pdf_path}")

if __name__ == "__main__":
    build_rag()
