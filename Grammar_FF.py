class Grammar_FF:
    def __init__(self, grammar_lr):
        self.rules = grammar_lr.rules
        self.non_terminals = grammar_lr.non_terminals
        self.symbol_mapping = grammar_lr.get_symbol_mapping()
        self.terminals = self._get_terminals()
        self.FIRST = self._compute_first()
        self.FOLLOW = self._compute_follow()

    def _get_terminals(self):
        terminals = set()
        for productions in self.rules.values():
            for prod in productions:
                terminals.update(sym for sym in prod if sym not in self.non_terminals and sym != 'ε')
        return terminals

    def _compute_first(self):
        first = {nt: set() for nt in self.non_terminals}
        first.update({t: {t} for t in self.terminals})
        first['ε'] = {'ε'}

        while True:
            updated = False
            for nt, productions in self.rules.items():
                for production in productions:
                    k = 0
                    while k < len(production):
                        symbol = production[k]
                        if symbol not in first:
                            first[symbol] = {symbol}
                        first_k = first[symbol] - {'ε'}
                        if first_k - first[nt]:
                            first[nt].update(first_k)
                            updated = True
                        if 'ε' not in first[symbol]:
                            break
                        k += 1
                    if k == len(production):
                        if 'ε' not in first[nt]:
                            first[nt].add('ε')
                            updated = True
            if not updated:
                break
        return first

    def _compute_follow(self):
        follow = {nt: set() for nt in self.non_terminals}
        follow[self.non_terminals[0]].add('$')  # Add $ to start symbol

        while True:
            updated = False
            for nt, productions in self.rules.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if symbol in self.non_terminals:
                            if i < len(production) - 1:
                                first_next = self.FIRST[production[i+1]]
                                follow[symbol].update(first_next - {'ε'})
                                if 'ε' in first_next:
                                    follow[symbol].update(follow[nt])
                            else:
                                follow[symbol].update(follow[nt])
                            if follow[symbol] - follow[symbol]:
                                updated = True
            if not updated:
                break
        return follow

    def __str__(self):
        grammar_str = "\n".join(f"{nt} -> {' | '.join(prods)}" for nt, prods in self.rules.items())
        first_follow_str = "{: ^20}{: ^20}{: ^20}".format('Non Terminals', 'First', 'Follow')
        for non_terminal in self.non_terminals:
            first_str = str(self.FIRST[non_terminal])
            follow_str = str(self.FOLLOW[non_terminal])
            display_nt = self.symbol_mapping.get(non_terminal, non_terminal)
            first_follow_str += f"\n{display_nt: ^20}{first_str: ^20}{follow_str: ^20}"
        return f"Grammar:\n{grammar_str}\n\nFIRST and FOLLOW sets:\n{first_follow_str}"