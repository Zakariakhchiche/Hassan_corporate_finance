import pypdf

def extract_text(pdf_path, output_path, max_pages=5):
    with open(pdf_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        text = ""
        for i in range(min(max_pages, len(reader.pages))):
            text += f"--- Page {i+1} ---\n"
            text += reader.pages[i].extract_text() + "\n"
        
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(text)

if __name__ == "__main__":
    extract_text('sparx.pdf', 'sparx_content.txt')
