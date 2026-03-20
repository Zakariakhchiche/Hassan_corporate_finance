import pypdf
import sys

def extract_text(pdf_path, max_pages=20):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        # Search for "Equipe", "Team", "Team Members", "Founder"
        keywords = ["equipe", "team", "founder", "fondateur", "membres"]
        for i in range(len(reader.pages)):
            page_text = reader.pages[i].extract_text()
            if any(key in page_text.lower() for key in keywords):
                text += f"--- Page {i+1} ---\n"
                text += page_text + "\n"
        if not text:
             # Fallback: extract first 15 pages if keywords not found
             for i in range(min(15, len(reader.pages))):
                text += f"--- Page {i+1} ---\n"
                text += reader.pages[i].extract_text() + "\n"
        print(text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_text("sparx.pdf")
