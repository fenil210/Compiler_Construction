import sys
sys.setrecursionlimit(60)

class Grammar:
    def __init__(self, rules):
        self.rules = {}
        for rule in rules:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [prod.strip() for prod in rhs.split('|')]
            self.rules[lhs] = rhs
        
        self.non_terminals = list(self.rules.keys())
        self.terminals = set()
        for productions in self.rules.values():
            for prod in productions:
                self.terminals.update(sym for sym in prod if sym not in self.non_terminals and sym != 'ε')
        
        self.starting_symbol = self.non_terminals[0]
        self.FIRST = {nt: set() for nt in self.non_terminals}
        self.FOLLOW = {nt: set() for nt in self.non_terminals}
        
        self.calculate_first()
        self.calculate_follow()

    def first(self, string):
        first_ = set()
        if string in self.non_terminals:
            alternatives = self.rules[string]
            for alternative in alternatives:
                first_ |= self.first(alternative)
        elif string in self.terminals:
            first_ = {string}
        elif string == '' or string == 'ε':
            first_ = {'ε'}
        else:
            first_2 = self.first(string[0])
            if 'ε' in first_2:
                i = 1
                while 'ε' in first_2:
                    first_ |= (first_2 - {'ε'})
                    if string[i:] in self.terminals:
                        first_ |= {string[i:]}
                        break
                    elif string[i:] == '':
                        first_ |= {'ε'}
                        break
                    first_2 = self.first(string[i:])
                    first_ |= first_2 - {'ε'}
                    i += 1
            else:
                first_ |= first_2
        return first_

    def follow(self, nT):
        follow_ = set()
        if nT == self.starting_symbol:
            follow_ |= {'$'}
        for nt, rhs in self.rules.items():
            for alt in rhs:
                for i, char in enumerate(alt):
                    if char == nT:
                        following_str = alt[i+1:]
                        if following_str == '':
                            if nt != nT:
                                follow_ |= self.FOLLOW[nt]
                        else:
                            follow_2 = self.first(following_str)
                            if 'ε' in follow_2:
                                follow_ |= follow_2 - {'ε'}
                                follow_ |= self.FOLLOW[nt]
                            else:
                                follow_ |= follow_2
        return follow_

    def calculate_first(self):
        for non_terminal in self.non_terminals:
            self.FIRST[non_terminal] |= self.first(non_terminal)

    def calculate_follow(self):
        self.FOLLOW[self.starting_symbol] |= {'$'}
        for non_terminal in self.non_terminals:
            self.FOLLOW[non_terminal] |= self.follow(non_terminal)

    def __str__(self):
        grammar_str = "\n".join(f"{nt} -> {' | '.join(prods)}" for nt, prods in self.rules.items())
        first_follow_str = "{: ^20}{: ^20}{: ^20}".format('Non Terminals', 'First', 'Follow')
        for non_terminal in self.non_terminals:
            first_str = str(self.FIRST[non_terminal]).replace("'", "")
            follow_str = str(self.FOLLOW[non_terminal]).replace("'", "")
            first_follow_str += f"\n{non_terminal: ^20}{first_str: ^20}{follow_str: ^20}"
        return f"Grammar:\n{grammar_str}\n\nFIRST and FOLLOW sets:\n{first_follow_str}"