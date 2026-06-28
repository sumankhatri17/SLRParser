class Production:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __hash__(self):
        return hash((self.lhs, self.rhs))


class Grammar:
    def __init__(self, text):
        self.raw_text = text
        self.productions = []
        self.terminals = set()
        self.non_terminals = set()
        self.non_terminal_order = []
        self.terminal_order = []
        self.start_symbol = ""
        self.original_start_symbol = ""
        
        self._parse_text(text)
        self._augment_grammar()
        self._identify_symbols()

    def _tokenize_rhs(self, rhs):
        tokens = []
        i = 0
        while i < len(rhs):
            if rhs[i].isspace():
                i += 1
                continue
            if rhs[i] == '|':
                tokens.append('|')
                i += 1
                continue
            if rhs[i].isalpha() or rhs[i] == '_':
                j = i + 1
                while j < len(rhs) and (rhs[j].isalnum() or rhs[j] == '_' or rhs[j] == "'"):
                    j += 1
                tokens.append(rhs[i:j])
                i = j
                continue
            tokens.append(rhs[i])
            i += 1
        return tokens

    def _parse_text(self, text):
        lines = [line.strip() for line in text.replace('\r', '').split('\n') if line.strip()]
        seen_lhs = set()
        
        for idx, line in enumerate(lines):
            if '->' not in line:
                raise ValueError("Invalid production format. Missing '->'.")
            
            lhs_str, rhs_str = line.split('->', 1)
            lhs = lhs_str.strip()

            for alternative in rhs_str.split('|'):
                rhs_tokens = self._tokenize_rhs(alternative)
                if not rhs_tokens:
                    raise ValueError("Empty alternative rule found.")
                self.productions.append(Production(lhs, tuple(rhs_tokens)))

            if lhs not in seen_lhs:
                self.non_terminal_order.append(lhs)
                seen_lhs.add(lhs)
            
            if idx == 0:
                self.original_start_symbol = lhs

    def _augment_grammar(self):
        self.start_symbol = self.original_start_symbol + "'"
        augmented_prod = Production(self.start_symbol, (self.original_start_symbol,))
        self.productions.insert(0, augmented_prod)

    def _identify_symbols(self):
        for prod in self.productions:
            self.non_terminals.add(prod.lhs)
            if prod.lhs not in self.non_terminal_order:
                self.non_terminal_order.append(prod.lhs)
            
        for prod in self.productions:
            for symbol in prod.rhs:
                if symbol not in self.non_terminals: 
                    self.terminals.add(symbol)
                    if symbol not in self.terminal_order:
                        self.terminal_order.append(symbol)
                    
    def get_productions_for(self, non_terminal):
        return [p for p in self.productions if p.lhs == non_terminal]

    def get_symbol_order(self):
        return self.non_terminal_order + self.terminal_order