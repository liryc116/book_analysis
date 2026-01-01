import anki
import extract
import histogram
import ngram

import argparse
import os
import pickle
import sys
import yaml

def save_dic(dictionnary: dict, path: str):
    sorted_dict = {}
    for key in reversed(sorted(dictionnary, key=dictionnary.get)):
        sorted_dict[key] = dictionnary[key]

    with open(path, "w") as file:
        file.write(str(sorted_dict).replace(', ', ',\n'))

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
    parser = argparse.ArgumentParser(
        description="A software to analyze Korean books and documents (in pdf or epub format)"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.yml",
        help="the config file to use"
    )
    parser.add_argument(
        "--ngrams",
        action="store_true",
        help="wether to process ngrams, this may take time"
    )
    parser.add_argument(
        "--anki_filtering",
        action="store_true",
        help="wether to filter tf-idf with known words from anki, this may take time"
    )

    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    os.makedirs(config['output_dir'], exist_ok=True)
    config['input'] = expand_dirs(config['input'])

    all_dicts = []
    for path in config['input']:
        text = extract.extract(path, config['output_dir'])
        dictionnary = histogram.histogram(text, path, config['output_dir'])
        all_dicts.append(dictionnary)

    common_dict = histogram.merge_histogram(all_dicts)

    tf_idf = histogram.filter_korean(histogram.tf_idf(all_dicts))
    save_dic(tf_idf, config['output_dir'] + "tf_idf.json")

    if args.anki_filtering:
        tf_idf = anki.filter_known_words(tf_idf, config)
        save_dic(tf_idf, config['output_dir'] + "tf_idf_filtered.json")

    if args.ngrams:
        ngram_dic = ngram.get_ngrams(config)
        save_dic(tf_idf, config['output_dir'] + "ngram.json")

if __name__ == "__main__":
    main()
