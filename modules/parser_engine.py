def tokenize_input(input_string, terminals):
    term_list = list(terminals)
    term_list.sort(key=len, reverse=True)
    
    tokens = []
    i = 0
    while i < len(input_string):
        if input_string[i].isspace():
            i += 1
            continue
        
        match = None
        for t in term_list:
            if input_string.startswith(t, i):
                match = t
                break
                
        if match:
            tokens.append(match)
            i += len(match)
        else:
            raise ValueError("Lexical error: Unknown token starting at '" + input_string[i:] + "'")
            
    if not tokens or tokens[-1] != '$':
        tokens.append('$')
        
    return tokens


def _format_trace_action(action, grammar):
    if not action:
        return "ERROR"
    if action == "ACC" or action.startswith("S"):
        return action
    if action.startswith("R"):
        prod_idx = int(action[1:])
        production = grammar.productions[prod_idx]
        rhs_text = " ".join(production.rhs)
        return "r" + str(prod_idx) + " : " + production.lhs + " -> " + rhs_text
    return action


def parse_input(input_string, grammar, table):
    tokens = tokenize_input(input_string, grammar.terminals)
    
    stack = [0]
    trace = []
    pointer = 0
    
    while True:
        state = stack[-1]
        current_token = tokens[pointer]
        
        action = table.action.get(state, {}).get(current_token, None)
        
        step = {
            'stack': list(stack),
            'input': "".join(tokens[pointer:]),
            'action': action if action else "ERROR",
            'display_action': _format_trace_action(action, grammar)
        }
        trace.append(step)
        
        if not action:
            return trace, "REJECTED (Syntax Error)"
            
        if action == "ACC":
            return trace, "ACCEPTED"
            
        if action.startswith("S"):
            next_state = int(action[1:])
            stack.append(current_token)
            stack.append(next_state)
            pointer += 1
            
        elif action.startswith("R"):
            prod_idx = int(action[1:])
            prod = grammar.productions[prod_idx]
            
            pop_count = len(prod.rhs)
            for _ in range(pop_count):
                if stack: stack.pop()
                if stack: stack.pop()
                
            top_state = stack[-1]
            next_state = table.goto.get(top_state, {}).get(prod.lhs)
            
            if next_state is None:
                trace.append({
                    'stack': list(stack), 
                    'input': "".join(tokens[pointer:]), 
                    'action': "ERROR (Missing GOTO)", 
                    'display_action': "ERROR (Missing GOTO)"
                })
                return trace, "REJECTED"
                
            stack.append(prod.lhs)
            stack.append(next_state)