import os
import graphviz
from graphviz.backend.execute import ExecutableNotFound

from modules.dfa_generator import DFA

def generate_dfa_graph(dfa: DFA, output_dir: str) -> tuple[str | None, str | None]:
    dot = graphviz.Digraph(format='svg')
    dot.attr(rankdir='LR', size='10,10')
    dot.attr('node', fontname='Courier', fontsize='10', shape='box', style='rounded,filled', fillcolor='#f3f4f6')
    dot.attr('edge', fontname='Courier', fontsize='9')

    for state in dfa.states:
        label = f"State {state.state_id}\n\n"
        for item in state.items:
            rhs_list = list(item.rhs)
            rhs_list.insert(item.dot, "•")
            label += f"{item.lhs} → {' '.join(rhs_list)}\n"
            
        dot.node(str(state.state_id), label)

    for state in dfa.states:
        for symbol, next_state in state.transitions.items():
            dot.edge(str(state.state_id), str(next_state), label=symbol)

    filename = 'dfa_graph'
    output_path = os.path.join(output_dir, filename)

    try:
        dot.render(output_path, cleanup=True)
        return f"{output_path}.svg", None
    except ExecutableNotFound:
        dot_path = f"{output_path}.dot"
        with open(dot_path, 'w', encoding='utf-8') as file_handle:
            file_handle.write(dot.source)
        return None, "Graphviz executables are not installed or not on PATH, so the DFA diagram could not be rendered."