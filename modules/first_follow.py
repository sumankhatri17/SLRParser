def _first_of_sequence(symbols, first_sets):
    if not symbols:
        return set()
    first_symbol = symbols[0]
    return first_sets.get(first_symbol, {first_symbol})


def compute_first_sets(grammar):
    first = {}
    for nt in grammar.non_terminals:
        first[nt] = set()
    for t in grammar.terminals:
        first[t] = {t}

    changed = True
    while changed:
        changed = False
        for prod in grammar.productions:
            rhs_first = _first_of_sequence(prod.rhs, first)
            before_size = len(first[prod.lhs])
            first[prod.lhs].update(rhs_first)

            if len(first[prod.lhs]) != before_size:
                changed = True
                
    return first


def compute_follow_sets(grammar, first_sets):
    follow = {}
    for nt in grammar.non_terminals:
        follow[nt] = set()
        
    follow[grammar.start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for prod in grammar.productions:
            for i, symbol in enumerate(prod.rhs):
                if symbol in grammar.non_terminals:
                    before_size = len(follow[symbol])
                    
                    suffix = prod.rhs[i + 1:]
                    if suffix:
                        suffix_first = _first_of_sequence(suffix, first_sets)
                        follow[symbol].update(suffix_first)
                    
                    if i == len(prod.rhs) - 1:
                        follow[symbol].update(follow[prod.lhs])

                    if len(follow[symbol]) != before_size:
                        changed = True
    return follow