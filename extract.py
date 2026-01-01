import os
from wisup_e2m import EpubParser, PdfParser

def extract(path_in: str, dir_out: str):
    base = os.path.basename(path_in)
    out = dir_out + base + ".md"

    if  os.path.isfile(out):
        path_in = out

    _, file_extension = os.path.splitext(path_in)
    if file_extension == '.md' or file_extension == '.txt':
        with open(out, 'r') as f:
            return f.read()
    else:
        if file_extension == '.epub':
            text = extract_epub(path_in)
        elif file_extension == '.pdf':
            text = extract_pdf(path_in)

        with open(out, 'w') as f:
            f.write(text)
        return text

    return ""

def extract_epub(path: str):
    parser = EpubParser(engine="unstructured") # epub engines: unstructured
    epub_data = parser.parse(path)

    return epub_data.text

def extract_pdf(path: str):
    #parser = PdfParser(engine="marker") # pdf engines: marker, unstructured, surya_layout
    parser = PdfParser(engine="unstructured") # pdf engines: marker, unstructured, surya_layout
    pdf_data = parser.parse(path)
    return pdf_data.text
