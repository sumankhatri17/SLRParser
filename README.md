# SLR Parser Web Application

This repository contains a web-based implementation of an SLR(1) Parser, built with Python and Flask. The application allows users to input a context-free grammar and an input string to visualize the entire parsing process.

## Features

- **Grammar Validation:** Validates the provided context-free grammar.
- **FIRST and FOLLOW Sets:** Computes and displays FIRST and FOLLOW sets for all non-terminals.
- **Canonical LR(0) Collection:** Generates the canonical collection of LR(0) items (states).
- **DFA Generation:** Visualizes the Deterministic Finite Automaton (DFA) representing the state transitions.
- **SLR(1) Parsing Table:** Constructs the ACTION and GOTO tables and detects any shift-reduce or reduce-reduce conflicts.
- **Input String Parsing:** Traces the parsing steps (stack, input buffer, action) for a given input string.

## Theory and Algorithm Overview

Simple LR (SLR) parsing is a type of bottom-up parsing for context-free grammars. It builds upon LR(0) parsing by using FOLLOW sets to resolve shift-reduce and reduce-reduce conflicts.

The general pipeline implemented in this project is as follows:
1. **Augment the Grammar:** A new start symbol is added to the grammar (e.g., `S' -> S`).
2. **Compute FIRST and FOLLOW Sets:** Essential for determining when to reduce during parsing.
3. **Build the LR(0) Automaton:** Construct the canonical collection of LR(0) items (closure and goto operations).
4. **Construct the Parse Table:**
   - **Shift Actions:** Derived from the DFA transitions on terminal symbols.
   - **Reduce Actions:** Applied for item sets containing a completed production, but *only* for the lookahead symbols present in the FOLLOW set of the production's left-hand side non-terminal. This is the key difference from LR(0) and resolves many conflicts.
   - **GOTO Table:** Derived from DFA transitions on non-terminal symbols.
5. **Parse the Input:** A stack-based algorithm uses the table to process the input tokens from left to right, producing a rightmost derivation in reverse.

## Grammar Input Format

To use the application, enter the context-free grammar rules in the text area using the following conventions:
- Use `->` to separate the left-hand side from the right-hand side of a production.
- Example: `E -> E + T`
- Use `|` to denote multiple alternatives for the same non-terminal on a single line.
- Example: `T -> T * F | F`
- Use `e` or `epsilon` to represent an empty string production.

## Project Structure

- `app.py`: The main Flask application handling routes and coordinating the parsing pipeline.
- `modules/`: Contains the core logic for the parser.
  - `grammar.py`: Grammar representation and processing.
  - `first_follow.py`: Algorithms for computing FIRST and FOLLOW sets.
  - `lr0_items.py`: Builds the canonical collection of LR(0) items.
  - `dfa_generator.py`: Generates the DFA from the state collections.
  - `slr_table.py`: Constructs the ACTION and GOTO tables.
  - `parser_engine.py`: Simulates the parsing of an input string.
  - `validator.py`: Validates input grammar format.
- `visualizations/`: Handles generating graphical representations of the DFA.
- `templates/`: HTML templates for the web interface.
- `static/`: Static assets including CSS and generated graph images.

## Requirements

- Python 3.x
- Flask
- Graphviz (System package and Python library, required for DFA visualization)

## Installation and Execution

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SLR-Parser
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install Flask
   # Install graphviz and other dependencies as required
   ```
   *Note: Ensure the Graphviz executable is installed on your system and added to your system PATH.*

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the web interface:**
   Open a web browser and navigate to `http://localhost:5000`.
