# Automaton Test Tool

A comprehensive Python library and web application for working with finite automata, including DFA and NFA simulation, visualization, and conversion algorithms.

## Features

🤖 **Core Automata Support**
- Deterministic Finite Automata (DFA)
- Nondeterministic Finite Automata (NFA)
- Epsilon (λ) transitions
- Complete state and transition management

⚡ **Simulation Engines**
- DFA step-by-step simulation
- NFA simulation with epsilon closure
- Interactive step-by-step execution
- Batch string testing

🔄 **Conversion Algorithms**
- NFA to DFA conversion (subset construction)
- State explosion analysis
- Equivalence verification

🌐 **REST API**
- Flask-based HTTP API
- CORS-enabled for frontend integration
- Comprehensive automaton operations

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sebas1541/automaton-test-tool.git
   cd automaton-test-tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the example script**
   ```bash
   python example.py
   ```

4. **Start the API server**
   ```bash
   python -m backend.app
   ```
   The API will be available at `http://localhost:5000`

## Usage Examples

### Creating a Simple DFA

```python
from backend.models import State, Transition, Automaton
from backend.algorithms import DFASimulator

# Create states
q0 = State("q0", (100, 100), is_final=False)
q1 = State("q1", (200, 100), is_final=True)

# Create transitions
t1 = Transition(q0, q1, "a")
t2 = Transition(q1, q1, "a")
t3 = Transition(q1, q0, "b")

# Create DFA
dfa = Automaton(
    states={q0, q1},
    transitions={t1, t2, t3},
    initial_state=q0,
    final_states={q1},
    alphabet={"a", "b"}
)

# Simulate
simulator = DFASimulator(dfa)
result = simulator.is_accepted("aaa")  # True
```

### NFA with Epsilon Transitions

```python
from backend.algorithms import NFASimulator

# Create NFA with epsilon transitions
nfa = Automaton(...)  # ... states and transitions with epsilon

# Simulate
nfa_sim = NFASimulator(nfa)
result = nfa_sim.is_accepted("ab")
```

### NFA to DFA Conversion

```python
from backend.algorithms import NFAToDFAConverter

# Convert NFA to equivalent DFA
converter = NFAToDFAConverter()
dfa, conversion_steps = converter.convert(nfa)

# Analyze conversion
analysis = converter.analyze_conversion(nfa)
print(f"State explosion ratio: {analysis['conversion_metrics']['state_explosion_ratio']}")
```

## API Endpoints

### Base URL: `http://localhost:5000/api`

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/health` | GET | Health check |
| `/automaton/create` | POST | Create automaton from JSON |
| `/automaton/simulate/dfa` | POST | Simulate DFA execution |
| `/automaton/simulate/nfa` | POST | Simulate NFA execution |
| `/automaton/convert/nfa-to-dfa` | POST | Convert NFA to DFA |
| `/automaton/analyze` | POST | Analyze automaton properties |
| `/automaton/test-strings` | POST | Test multiple strings |

### Example API Usage

```bash
# Create an automaton
curl -X POST http://localhost:5000/api/automaton/create \
  -H "Content-Type: application/json" \
  -d '{
    "states": [
      {"id": "q0", "position": [100, 100], "is_final": false},
      {"id": "q1", "position": [200, 100], "is_final": true}
    ],
    "transitions": [
      {"from_state_id": "q0", "to_state_id": "q1", "symbol": "a"}
    ],
    "initial_state_id": "q0",
    "final_state_ids": ["q1"],
    "alphabet": ["a", "b"]
  }'

# Simulate DFA
curl -X POST http://localhost:5000/api/automaton/simulate/dfa \
  -H "Content-Type: application/json" \
  -d '{
    "automaton": { ... },
    "input_string": "aaa"
  }'
```

## Project Structure

```
automaton-test-tool/
├── backend/
│   ├── models/           # Core data structures
│   │   ├── state.py      # State representation
│   │   ├── transition.py # Transition representation
│   │   └── automaton.py  # Automaton container
│   ├── algorithms/       # Simulation and conversion algorithms
│   │   ├── dfa_simulator.py     # DFA simulation
│   │   ├── nfa_simulator.py     # NFA simulation
│   │   └── nfa_to_dfa.py        # NFA to DFA conversion
│   ├── api/              # REST API endpoints
│   │   └── routes.py     # Flask routes
│   └── app.py            # Main Flask application
├── frontend/             # Future TypeScript + D3.js frontend
├── example.py            # Usage examples
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Architecture

### Core Components

1. **Models** (`backend/models/`)
   - `State`: Represents automaton states with position, labels, and final status
   - `Transition`: Represents transitions between states with symbols
   - `Automaton`: Container managing states, transitions, and automaton properties

2. **Algorithms** (`backend/algorithms/`)
   - `DFASimulator`: Deterministic simulation with step-by-step tracking
   - `NFASimulator`: Nondeterministic simulation with epsilon closure
   - `NFAToDFAConverter`: Subset construction algorithm implementation

3. **API** (`backend/api/`)
   - RESTful endpoints for all automaton operations
   - JSON serialization/deserialization
   - CORS support for frontend integration

### Key Features

- **Type Safety**: Full type hints throughout the codebase
- **Clean Architecture**: Separation of concerns with clear interfaces
- **Comprehensive Testing**: Example scripts demonstrating all features
- **Educational Focus**: Step-by-step simulation for learning
- **Production Ready**: Robust error handling and validation

## Development

### Running Tests
```bash
python example.py
```

### Starting Development Server
```bash
python -m backend.app
```

### API Documentation
Visit `http://localhost:5000/` for endpoint information.

## Future Enhancements

- 🎨 TypeScript + D3.js frontend for visual automaton editing
- 📊 Advanced visualization and animation
- 🔧 Additional automaton types (PDA, Turing machines)
- 🧪 Comprehensive test suite
- 📚 Interactive tutorials and examples

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Authors

- **Sebastian Canon Castellanos** - Initial work and implementation

---

*Built with ❤️ for automata theory education and research*