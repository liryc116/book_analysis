import extract

path1 = '/home/cyril/Downloads/books/헤밍웨이, 어니스트 _ 헤밍웨이, - 노인과 바다 (2012_2013, 더클래식) - libgen.li.epub'
path2 = '/home/cyril/Downloads/books/한강 - 소년이 온다 (2016, (주)창비) - libgen.li.epub'

def main():
    extract.extract(path2)

if __name__ == "__main__":
    # calling the main function
    main()
