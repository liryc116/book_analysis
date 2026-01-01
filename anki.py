import requests
import json

def craft_search_query(word:str, decks_config: list):
    query = ""
    for deck in decks_config:
        if deck.get("strict") != None and not deck["strict"]:
            word = f'*{word}*'
        s = f'(deck:"{deck["name"]}" {deck["field"]}:"{word}")'

        if query != "":
            query += " OR "
        query += s
    obj = {}
    obj["query"]=query
    return obj

def in_anki(word:str, config:dict):
    query = craft_search_query(word, config['anki_decks'])
    payload = {'action': 'findCards', 'version': 5, 'params':query}
    response = requests.post(config['anki_endpoint'], json=payload)
    return response.json()['result']

def are_suspended(cards_id: list, config: dict):
    payload = {'action':"areSuspended", "version": 5, "params": {"cards": cards_id}}
    response = requests.post(config['anki_endpoint'], json=payload)
    return response.json()['result']

def cards_info(cards_id: list, config: dict):
    payload = {'action':"cardsInfo", "version": 5, "params": {"cards": cards_id}}
    response = requests.post(config['anki_endpoint'], json=payload)
    return response.json()['result']

def are_known(cards_id: list, config: dict):
    for is_suspended in are_suspended(cards_id, config):
        if is_suspended:
            return True

    for info in cards_info(cards_id, config):
        if info['reps'] != 0:
            return True

    return False

def is_known_word(word: str, config: dict):
    if are_known(in_anki(word, config), config):
        return True
        print(f"{word} is already known")
    else:
        return False
        print(f"{word} is not known")


def filter_known_words(dic: dict, config: dict, limit=-1):
    out = {}

    for (w,v) in dic.items():
        if not is_known_word(w,config):
            out[w] = v
        if len(out) == limit:
            break

    return out

