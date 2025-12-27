import anki
import extract
import histogram
import ngram

import os
import pickle
import sys
import yaml

def print_dic_top(dictionnary: dict, n=50):
    sorted_dict = {}
    for key in sorted(dictionnary, key=dictionnary.get):
        sorted_dict[key] = dictionnary[key]

    print(list(sorted_dict.keys())[-n:])

def expand_dirs(input_path_list: list):
    new_path = []
    for path in input_path_list:
        if path[-1] == '/':
            for f in os.listdir(path):
                if os.path.isfile(os.path.join(path, f)):
                    new_path.append(os.path.join(path, f))
        elif os.path.isfile(path):
            new_path.append(path)
        else:
            print(f"{path} is not a file or a folder ending in /")
    return new_path

def main():
    config_path = "config.yml"
    if len(sys.argv) == 3 and sys.argv[1] == '-c':
        config_path = sys.argv[2]

    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    os.makedirs(config['output_dir'], exist_ok=True)
    config['input'] = expand_dirs(config['input'])

    all_dicts = []
    for path in config['input']:
        print(path)
        text = extract.extract(path, config['output_dir'])

        dictionnary = histogram.histogram(text, path, config['output_dir'])
        print_dic_top(dictionnary)
        all_dicts.append(dictionnary)

    common_dict = histogram.merge_histogram(all_dicts)

    print_dic_top(common_dict)

    tf_idf = histogram.filter_korean(histogram.tf_idf(all_dicts))
    print_dic_top(tf_idf, 100)

    #print_dic_top(ngram.get_ngrams(config), 250)
    anki.known_word("엄마", config)

if __name__ == "__main__":
    # calling the main function
    main()
