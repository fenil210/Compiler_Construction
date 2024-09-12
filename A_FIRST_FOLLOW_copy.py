from A_grammar_copy import Grammar

def main():
    print("Enter the grammar rules. Enter an empty line to finish.")
    print("Format: Non-terminal -> production1 | production2 | ...")
    
    rules = []
    while True:
        rule = input().strip()
        if not rule:
            break
        rules.append(rule)
    
    if not rules:
        print("No grammar rules entered. Exiting.")
        return
    print(type(rules))
    grammar = Grammar(rules)
    print(grammar)

if __name__ == "__main__":
    main()