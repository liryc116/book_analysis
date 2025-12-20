import os
from wisup_e2m import EpubParser

def extract(path: str):
    _, file_extension = os.path.splitext(path)

    if file_extension == '.epub':
        return extract_epub(path)
    return

def extract_epub(path: str):

    parser = EpubParser(engine="unstructured") # epub engines: unstructured
    epub_data = parser.parse(path)
    #print(epub_data.text)

    return epub_data.text

