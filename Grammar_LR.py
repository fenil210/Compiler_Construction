import string

class Grammar_LR:
    def __init__(self, rules):
        self.rules = {}
        for rule in rules:
            lhs, rhs = rule.split('->')
            lhs = lhs.strip()
            rhs = [prod.strip() for prod in rhs.split('|')]
            self.rules[lhs] = rhs
        
        self.non_terminals = list(self.rules.keys())
        self.new_symbol_map = {}
        self.used_symbols = set(self.non_terminals)
    
    def _generate_new_symbol(self):
        for char in string.ascii_uppercase:
            if char not in self.used_symbols:
                self.used_symbols.add(char)
                return char
        raise ValueError("Ran out of available uppercase letters for new symbols")

    def has_left_recursion(self):
        for nt in self.non_terminals:
            if self._has_direct_left_recursion(nt) or self._has_indirect_left_recursion(nt):
                return True
        return False
    
    def _has_direct_left_recursion(self, non_terminal):
        return any(prod.startswith(non_terminal) for prod in self.rules[non_terminal])
    
    def _has_indirect_left_recursion(self, non_terminal):
        visited = set()
        return self._dfs_check_indirect_recursion(non_terminal, visited)
    
    def _dfs_check_indirect_recursion(self, current, visited):
        if current in visited:
            return True 
        visited.add(current)
        for prod in self.rules[current]:
            first_symbol = prod.split()[0]
            if first_symbol in self.non_terminals:
                if self._dfs_check_indirect_recursion(first_symbol, visited.copy()):
                    return True
        return False
    
    def eliminate_left_recursion(self):
        self._eliminate_indirect_left_recursion()
        self._eliminate_direct_left_recursion()
    
    def _eliminate_indirect_left_recursion(self):
        for i, Ai in enumerate(self.non_terminals):
            for j in range(i):
                Aj = self.non_terminals[j]
                new_productions = []
                for production in self.rules[Ai]:
                    if production.startswith(Aj):
                        for Aj_prod in self.rules[Aj]:
                            new_productions.append((Aj_prod + production[len(Aj):]).strip())
                    else:
                        new_productions.append(production.strip())
                self.rules[Ai] = new_productions
    
    def _eliminate_direct_left_recursion(self):
        for A in self.non_terminals:
            alpha = []
            beta = []
            for production in self.rules[A]:
                if production.startswith(A):
                    alpha.append(production[len(A):].strip())
                else:
                    beta.append(production.strip())
                    
            if alpha:
                new_non_terminal = self._generate_new_symbol()
                self.new_symbol_map[A] = new_non_terminal 
                self.rules[A] = [f"{b}{new_non_terminal}".strip() for b in beta] if beta else [new_non_terminal]
                self.rules[new_non_terminal] = [f"{a}{new_non_terminal}".strip() for a in alpha] + ["ε"]
                self.non_terminals.append(new_non_terminal)
    
    def __str__(self):
        print("self.rules.items()",self.rules.items())
        return "\n".join(f"{nt} -> {' | '.join(prods)}" for nt, prods in self.rules.items())

    def get_symbol_mapping(self):
        return {v: f"{k}'" for k, v in self.new_symbol_map.items()}