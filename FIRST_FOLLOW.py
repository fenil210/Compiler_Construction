from Grammar_FF import Grammar_FF
from Grammar_LR import Grammar_LR

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
    
    grammar_lr = Grammar_LR(rules)
    if not grammar_lr.has_left_recursion():
        print("The given grammar does not have left recursion.")
    else:
        print("The given grammar has left recursion. Eliminating...")
        grammar_lr.eliminate_left_recursion() 
        print("\nGrammar after left recursion elimination:")
        print(grammar_lr)
    
    grammar_ff = Grammar_FF(grammar_lr)
    print("\nFIRST and FOLLOW sets:")
    print(grammar_ff)
    print(grammar_ff.symbol_mapping)

if __name__ == "__main__":
    main() 