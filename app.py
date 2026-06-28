import os
from flask import Flask, render_template, request
from modules.grammar import Grammar
from modules.first_follow import compute_first_sets, compute_follow_sets
from modules.lr0_items import build_canonical_collection
from modules.dfa_generator import DFA
from modules.slr_table import build_slr_table
from modules.parser_engine import parse_input
from modules.validator import validate_grammar_text
from visualizations.graph_builder import generate_dfa_graph

app = Flask(__name__)
app.config['SECRET_KEY'] = 'slr-parser-secret'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'graphs')

# Ensure directories exist
os.makedirs('static/graphs', exist_ok=True)
os.makedirs('static/css', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', result=None)

    raw_grammar = request.form.get('grammar', '').strip()
    input_string = request.form.get('input_string', '').strip()
    
    try:
        # 1. Validate & Parse Grammar
        validate_grammar_text(raw_grammar)
        grammar = Grammar(raw_grammar)
        
        # 2. Compute FIRST & FOLLOW Sets
        first_sets = compute_first_sets(grammar)
        follow_sets = compute_follow_sets(grammar, first_sets)
        
        # 3. Build Canonical LR(0) Collection
        states = build_canonical_collection(grammar)
        
        # 4. Generate DFA
        dfa = DFA(states)
        graph_path, graph_error = generate_dfa_graph(dfa, app.config['UPLOAD_FOLDER'])
        
        # 5. Build SLR(1) Parsing Table
        slr_table = build_slr_table(grammar, dfa, follow_sets)
        
        # 6. Parse Input String (if provided & no conflicts)
        parsing_trace = None
        parse_status = None
        if input_string and not slr_table.conflicts:
            parsing_trace, parse_status = parse_input(input_string, grammar, slr_table)
            
        result = {
            'grammar': grammar,
            'display_non_terminals': [nt for nt in grammar.non_terminal_order if nt != grammar.start_symbol],
            'first_sets': {nt: first_sets[nt] for nt in grammar.non_terminal_order if nt != grammar.start_symbol},
            'follow_sets': {nt: follow_sets[nt] for nt in grammar.non_terminal_order if nt != grammar.start_symbol},
            'states': states,
            'dfa_graph': os.path.basename(graph_path) if graph_path else None,
            'graph_error': graph_error,
            'action_table': slr_table.action,
            'goto_table': slr_table.goto,
            'conflicts': slr_table.conflicts,
            'terminals': list(grammar.terminal_order) + ['$'],
            'non_terminals': [nt for nt in grammar.non_terminal_order if nt != grammar.start_symbol],
            'parsing_trace': parsing_trace,
            'parse_status': parse_status,
            raw_grammar: raw_grammar,
            input_string: input_string
        }
        return render_template('index.html', result=result, raw_grammar=raw_grammar, input_string=input_string)

    except Exception as e:
        return render_template('index.html', error=str(e), raw_grammar=raw_grammar, input_string=input_string)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)