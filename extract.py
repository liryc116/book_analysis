import os
import ebooklib
from ebooklib import epub

def extract(path: str):
    return extract_epub(path)

def extract_epub(path: str):
    book = epub.read_epub(path, {'ignore_ncx': True})

    print(book)

    content = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            content.append(item.get_content().decode('utf-8'))
            print('==================================')
            print('NAME : ', item.get_name())
            print('LEN : ', len(item.get_content().decode('utf-8')))
            print('----------------------------------')
            print(item.get_content().decode('utf-8')[:1024])
            print('==================================')
