import fitz


def extract_from_pdf(file_bytes: bytes) -> dict:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    tables = []
    for page in doc:
        text += page.get_text()
        tabs = page.find_tables()
        for tab in tabs:
            tables.append(tab.to_markdown())
    metadata = doc.metadata
    page_count = len(doc)
    doc.close()
    return {"text": text, "tables": tables, "metadata": metadata, "page_count": page_count}