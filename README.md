# 🤖 Automaton Test Tool

A comprehensive Python-based tool for creating, visualizing, and testing finite automata (DFA and NFA).

## ✨ Features

- **Interactive Visualization**: Beautiful automaton graphs using Graphviz
- **DFA & NFA Support**: Create and test both deterministic and non-deterministic automata
- **Real-time Simulation**: Test strings with instant accept/reject feedback
- **Step-by-Step Execution**: Trace automaton execution step by step
- **NFA to DFA Conversion**: Convert NFAs to equivalent DFAs automatically
- **Sample Templates**: Quick-start with pre-built example automata
- **Clean Architecture**: Well-organized backend with domain-based packages

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open in Browser**: Navigate to `http://localhost:8501`

4. **Get Started**: Click "Sample DFA" or "Sample NFA" to load an example

## 🏗️ Architecture

```
automaton-test-tool/
├── streamlit_app.py          # Main Streamlit application
├── backend/
│   ├── algorithms/
│   │   ├── dfa/             # DFA simulation logic
│   │   ├── nfa/             # NFA simulation logic
│   │   └── conversion/      # NFA to DFA conversion
│   └── models/              # Data models
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎯 Usage

### Creating Automatons
- Use the sidebar to configure states, alphabet, and transitions
- Set initial and final states
- Add transitions using the interactive form

### Testing Strings
- Enter a test string in the input field
- Click "Run Simulation" for instant results
- Use "Step-by-Step Simulation" for detailed execution trace

### Advanced Features
- **NFA Conversion**: Convert any NFA to an equivalent DFA
- **Visual Feedback**: Color-coded accept/reject results
- **Real-time Updates**: Changes reflect immediately in the graph

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Visualization**: Graphviz (professional graph rendering)
- **Backend**: Pure Python with clean domain architecture
- **Libraries**: NetworkX, Matplotlib, Plotly

## 📝 Examples

The app includes sample automata:
- **Sample DFA**: Accepts strings ending with "01"
- **Sample NFA**: Accepts strings containing "01"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.