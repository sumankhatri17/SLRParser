class LR0Item:
    def __init__(self, lhs, rhs, dot):
        self.lhs = lhs
        self.rhs = rhs  
        self.dot = dot

    def __eq__(self, other):
        if not isinstance(other, LR0Item):
            return False
        return self.lhs == other.lhs and self.rhs == other.rhs and self.dot == other.dot

    def __hash__(self):
        return hash((self.lhs, self.rhs, self.dot))


class State:
    def __init__(self, state_id, items, transitions=None):
        self.state_id = state_id
        self.items = items  
        self.transitions = transitions if transitions is not None else {}


def _item_sort_key(item, grammar):
    production_index = len(grammar.productions)
    for index, prod in enumerate(grammar.productions):
        if prod.lhs == item.lhs and prod.rhs == item.rhs:
            production_index = index
            break
    return (production_index, item.dot)


def _next_symbols(items, grammar):
    available = set()
    for item in items:
        if item.dot < len(item.rhs):
            available.add(item.rhs[item.dot])

    ordered_symbols = []
    for symbol in grammar.get_symbol_order():
        if symbol in available and symbol not in ordered_symbols:
            ordered_symbols.append(symbol)
    return ordered_symbols


def compute_closure(items, grammar):
    ordered_items = sorted(list(items), key=lambda item: _item_sort_key(item, grammar))
    seen = set(ordered_items)

    index = 0
    while index < len(ordered_items):
        item = ordered_items[index]
        if item.dot < len(item.rhs):
            next_symbol = item.rhs[item.dot]
            if next_symbol in grammar.non_terminals:
                for prod in grammar.get_productions_for(next_symbol):
                    new_item = LR0Item(prod.lhs, prod.rhs, 0)
                    if new_item not in seen:
                        seen.add(new_item)
                        ordered_items.append(new_item)
        index += 1

    return tuple(ordered_items)


def compute_goto(items, symbol, grammar):
    goto_set = set()
    for item in items:
        if item.dot < len(item.rhs) and item.rhs[item.dot] == symbol:
            goto_set.add(LR0Item(item.lhs, item.rhs, item.dot + 1))
    return compute_closure(goto_set, grammar)


def build_canonical_collection(grammar):
    start_prod = grammar.productions[0]
    start_item = LR0Item(start_prod.lhs, start_prod.rhs, 0)
    
    initial_items = compute_closure({start_item}, grammar)
    states = [State(0, initial_items, {})]
    
    queue = [0]
    state_map = {frozenset(initial_items): 0}
    
    while queue:
        current_id = queue.pop(0)
        current_state = states[current_id]
        
        for symbol in _next_symbols(current_state.items, grammar):
            goto_items = compute_goto(current_state.items, symbol, grammar)
            if not goto_items:
                continue
                
            goto_key = frozenset(goto_items)

            if goto_key not in state_map:
                new_id = len(states)
                state_map[goto_key] = new_id
                states.append(State(new_id, goto_items, {}))
                queue.append(new_id)
                
            current_state.transitions[symbol] = state_map[goto_key]
            
    return states