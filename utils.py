
def only_korean(string: str):
    for c in string:
        if (c < '\u1100' or c > '\u11FF') and (c < '\uAC00' or c > '\uD7AF'):
            return False
    return True
