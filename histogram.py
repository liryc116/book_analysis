from konlpy.tag import Okt
import numpy
import os
import pickle

import utils
okt = Okt()

def histogram(text: str, path: str, dir_out : str):
    base = os.path.basename(path)
    out = dir_out + base + ".pkl"

    dictionnary = {}

    if  os.path.isfile(out):
        with open(out, "rb") as file:
            return pickle.load(file)

    content = okt.pos(text, norm=True, stem=True)

    for (w, _) in content:
        if dictionnary.get(w) == None:
            dictionnary[w] = 0
        dictionnary[w] += 1

    with open(out, "wb") as file:
        pickle.dump(dictionnary, file)

    return dictionnary

def tf(dic):

    total = sum(t[1] for t in list(dic.items()))

    for (k, v) in dic.items():
        dic[k] = v / total

    return dic

def idf(all_dicts):
    common = {}

    for dic in all_dicts:
        for w in all_dicts[0].keys():
            if dic.get(w) != None:
                if common.get(w) == None:
                    common[w] = 1
                else:
                    common[w] += 1

    for (w,c) in common.items():
        common[w] = numpy.log(len(all_dicts)/common[w])

    return common


def tf_idf(all_dicts):
    term_freq = tf(all_dicts[0])
    doc_freq = idf(all_dicts)

    for (w, c) in term_freq.items():
        term_freq[w] *= doc_freq[w]

    return term_freq

def merge_histogram(to_merge):
    common = {}
    for to_add in to_merge:
        for (w,c) in to_add.items():
            if common.get(w) == None:
                common[w] = c
            else:
                common[w] += c

    return common

def filter_korean(histogram):
    res = {}
    for (w,c) in histogram.items():
        if utils.only_korean(w):
            res[w] = c

    return res

