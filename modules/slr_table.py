class SLRTable:
    def __init__(self):
        self.action = {}
        self.goto = {}
        self.conflicts = []


def build_slr_table(grammar, dfa, follow_sets):
    table = SLRTable()
    symbol_order = grammar.get_symbol_order()
    
    for state in dfa.states:
        table.action[state.state_id] = {}
        table.goto[state.state_id] = {}
        
        ordered_transitions = []
        for symbol, next_state in state.transitions.items():
            if symbol in symbol_order:
                key_val = symbol_order.index(symbol)
            else:
                key_val = len(symbol_order)
            ordered_transitions.append((symbol, next_state, key_val))
            
        ordered_transitions.sort(key=lambda x: x[2])

        for symbol, next_state, _ in ordered_transitions:
            if symbol in grammar.terminals:
                _add_action(table, state.state_id, symbol, "S" + str(next_state))
            elif symbol in grammar.non_terminals:
                table.goto[state.state_id][symbol] = next_state
                
        for item in state.items:
            if item.dot == len(item.rhs):
                if item.lhs == grammar.start_symbol:
                    _add_action(table, state.state_id, '$', "ACC")
                else:
                    prod_idx = -1
                    for idx, prod in enumerate(grammar.productions):
                        if prod.lhs == item.lhs and prod.rhs == item.rhs:
                            prod_idx = idx
                            break
                    
                    if prod_idx != -1:
                        for f in follow_sets.get(item.lhs, []):
                            _add_action(table, state.state_id, f, "R" + str(prod_idx))

    return table


def _add_action(table, state_id, symbol, action):
    if symbol in table.action[state_id]:
        existing = table.action[state_id][symbol]
        if existing != action:
            table.conflicts.append("State " + str(state_id) + " on '" + symbol + "': " + existing + " / " + action)
    else:
        table.action[state_id][symbol] = action