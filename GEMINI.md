# Stellar Array Simulator

## Project Overview
The **Stellar Array** is a simulator for a fictional 1946 computational machine designed for **massive parallel pre-computation**. Unlike sequential computers of its era (like ENIAC), the Stellar Array is architected to perform simultaneous grid-based operations using a unique "striped" memory architecture across multiple vacuum-tube calculator units.

This project contains:
1.  A **Python Simulator** that models the hardware constraints, timing, and logical operations.
2.  A **Python Visualizer** (Tkinter) that provides a step-by-step view of the data flow.
3.  A **Web Demo** (HTML/JS) offering a browser-based visualization of the trading algorithm.
4.  Documentation for the fictional assembly language (**Étoile Code**).

## Architecture
The machine simulates a system with **700 Vacuum Tubes** distributed as follows:
*   **Grid Memory**: A 15x15 matrix (225 nodes) storing values in flip-flops.
*   **Striped Processing**: Data is split across three parallel **Calculator Units** based on row index:
    *   Calculator 0: Rows 0-4
    *   Calculator 1: Rows 5-9
    *   Calculator 2: Rows 10-14
*   **Aggregator**: A fourth unit that sweeps results for final output.

## Key Files

### Core Python Components
*   **`StellarArray.py`**: The main simulation engine. It defines the hardware specs (tubes, registers, wire storage) and implements the four computation modes. It calculates simulated execution time based on hardware operations (e.g., tape read speed vs. tube switching speed).
*   **`StellarArrayVisualizer.py`**: A Tkinter-based GUI that visually demonstrates the machine's operation. It highlights the active components (Tape, Calculator, Grid) as data flows through the system.

### Web Implementation
*   **`stellar_web/index.html`** & **`app.js`**: A lightweight, browser-based version of the visualizer, primarily focused on the "Trading" simulation mode. Open `index.html` in a browser to run it.

### Documentation
*   **`TRADING_CODE_EXAMPLE.md`**: Explains the low-level "Étoile Code" assembly language used by the machine, specifically detailing the logic for the differential arbitrage algorithm.

## Installation & Usage

### Prerequisites
*   Python 3.6+ (No external dependencies required for the Python scripts).

### Running the Simulator (CLI)
To run the core logic simulator which executes all 4 modes (AEC, CEA, Trading, Art) and reports simulated timings:
```bash
python StellarArray.py
```

### Running the Visualizer (GUI)
To launch the interactive graphical interface:
```bash
python StellarArrayVisualizer.py
```
*   **Controls**: Use "Play/Pause" or "Step" to advance the simulation.
*   **Speed**: Adjust the speed slider to slow down the visualization for educational purposes.

### Running the Web Demo
Simply open `stellar_web/index.html` in any modern web browser. No server is required.

## Simulation Modes
The simulator supports four distinct computational tasks:
1.  **AEC (Atomic Energy Commission)**: Analyzing neutron flux distributions.
2.  **CEA (Commissariat à l'énergie atomique)**: Monitoring reactor pressure/temperature criticality.
3.  **Trading**: Detecting arbitrage opportunities (spreads) across a 15x15 market grid.
4.  **Art**: Generating procedural patterns based on sine-wave interference.

## Development Notes
*   **Code Style**: The Python code uses standard library features only.
*   **Architecture adherence**: All logical operations in the code attempt to respect the physical constraints of the fictional 1946 hardware (e.g., striping data by rows to specific calculator units). Changes to logic should preserve this architectural "flavor".
