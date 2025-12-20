import extract

import os
import sys
import yaml

path1 = '/home/cyril/Downloads/books/헤밍웨이, 어니스트 _ 헤밍웨이, - 노인과 바다 (2012_2013, 더클래식) - libgen.li.epub'
path2 = '/home/cyril/Downloads/books/한강 - 소년이 온다 (2016, (주)창비) - libgen.li.epub'

def main():
    config_path = "config.yml"
    if len(sys.argv) == 3 and sys.argv[1] == '-c':
        config_path = sys.argv[2]

    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    os.makedirs(config['output_dir'], exist_ok=True)

    for path in config['input']:
        text = extract.extract(path)

        base = os.path.basename(path)
        out = config['output_dir'] + base + ".md"

        with open(out, 'w') as f:
            f.write(text)

if __name__ == "__main__":
    # calling the main function
    main()
