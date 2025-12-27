import requests

def craft_search_query(word:str, decks_config: list):
    query = ""
    for deck in decks_config:
        if not deck['strict']:
            word = f'*{word}*'
        s = f"(deck:\"{deck['name']}\" \"{config['field']}:{word}\")"

        if query != "":
            query += " OR "
        query += s
    return query

def in_anki(word:str, config:dict):
    query = craft_search_query(word, config)
    payload = f"{\"action\": \"findCards\", \"version\": 5, \"params\":{ \"query\": \"{query}\"\"}}"
    response = requests.post(config['anki_endpoint'], data=payload)
    return response.json()['result']['cards']

def is_suspended(card_id):
    query = craft_search_query(word, config)
    payload = f"{\"action\": \"areSuspended\", \"version\": 5, \"params\":{ \"cards\": [{card_id}]\"}}"
    response = requests.post(config['anki_endpoint'], data=payload)
    return response.json()['result'][0]

def is_known(cards: list):
    for card in cards:
        if card['reps'] != 0 or areSuspended(card['cardId']):
            return True

    return False


def known_word(word: str, config: dict):
    if is_known(in_anki(word, config)):
        print(f"{word} is already known")
    else:
        print(f"{word} is not known")



