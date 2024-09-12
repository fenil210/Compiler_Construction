def is_non_terminal(symbol):
    return symbol.isupper()

def is_terminal(symbol):
    return not is_non_terminal(symbol)

def split_production(production):
    return production.split()