import string

def get_pascal_name(name: str) -> str:
    out = ''
    upper = True
    for ch in name:
        if ch == '_':
            upper = True
        elif upper:
            out += ch.upper()
            upper = False
        else:
            out += ch
    return out
