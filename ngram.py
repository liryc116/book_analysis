import utils
import extract
from konlpy.tag import Okt

okt = Okt()

def all_korean(l):
    for w in l:
        if not utils.only_korean(w):
            return False
    return True

def n_gram_histogram(dictionnary, text: str, n_gram_max: int):

    content = okt.pos(text, norm=True, stem=True)
    tokens = []

    for (w, _) in content:
        tokens.append(w)

    n_tokens = len(tokens)
    for i in range(n_tokens):
        for j in range(i+2, min(n_tokens, i+n_gram_max)+1):
            if all_korean(tokens[i:j]):
                joined = str.join(' ', tokens[i:j])
                if dictionnary.get(joined) == None:
                    dictionnary[joined] = 0
                dictionnary[joined] += 1

    return dictionnary

def filter_ngrams(dic, occurence):
    filtered_dict = {}
    for (w,c) in dic.items():
        if c >= occurence:
            filtered_dict[w] = c

    sorted_dict = {}
    for key in reversed(sorted(filtered_dict, key=filtered_dict.get)):
        sorted_dict[key] = filtered_dict[key]

    print(list(sorted_dict.keys())[-50:])
    return sorted_dict


def get_ngrams(config):
    ngram_dic = {}

    for path in config['input']:
        text = extract.extract(path, config['output_dir'])
        ngram_dic = n_gram_histogram(
            ngram_dic,
            text,
            config['max_ngram_len']
            )

    ngram_dic = filter_ngrams(ngram_dic, config['ngram_occurence_limit'])
    filename = config['output_dir'] + config['ngrams_output']
    filehandler = open(filename, 'wt')
    data = str(ngram_dic)
    filehandler.write(data.replace(', ', ',\n'))
    return ngram_dic
