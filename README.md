# Stellar Array Simulator

## Overview
The Stellar Array Simulator is a Python-based emulation of the 700-tube Stellar Array, a fictional computational machine set in a 1946 New York lab environment. Designed for tasks like algorithmic trading and art generation, the array features 700 vacuum tubes across four calculators (three with ~166 tubes, one with 200), 150,000-bit wire storage (~15,000 commands), ~464 flip-flops (~3,712 bits), and Étoile Code (~32 commands, ~8-bit instructions). This simulator mimics the array’s core operations—data input, parallel computation on a 15x15 grid, and output—while reflecting 1946 hardware constraints like tube delays (~4 ms/operation) and I/O speeds (~100 bits/s input, ~10 bits/s output).

## Prerequisites
- Python 3.6 or higher
- No external libraries required (uses `time` and `random` from Python’s standard library)

## Installation
1. Clone or download the repository containing `StellarArray.py`.
2. Ensure Python is installed on your system.
3. Place the script in your working directory.

## Usage
1. Open a terminal or command prompt.
2. Navigate to the directory containing `StellarArray.py`.
3. Run the script:

   python StellarArray.py
4. The script will simulate processing a 15x15 grid (~225 points, ~800 bits) of random data, mimicking a task like trading signal generation. Output includes the loaded data, computed results, and total simulated time.

## Code Structure
- **StellarArray Class**:
  - `__init__`: Initializes the array with 700 tubes, four calculators, wire storage, and flip-flops.
  - `read_tape`: Simulates punched tape input at ~100 bits/s.
  - `write_output`: Simulates output to nixie tubes at ~10 bits/s.
  - `compute_15x15_grid`: Performs parallel computation on a 15x15 grid, simulating subtractions and comparisons.
  - `simulate`: Orchestrates the full simulation process (input, compute, output).
- **Main Block**: Generates random input data (~225 values) and runs the simulation.

## Example Output

Starting simulation...Data loaded in 8.00 sComputation done in 31.90 sOutput: ['Trade at [0,0]: 7', 'Trade at [1,2]: 8', ...]Total time: 39.90 s

## Limitations
- Simplified hardware emulation: Tube delays and I/O speeds are approximated.
- No real-time I/O or hardware interfacing; purely a computational simulation.
- Random data used for testing; real-world inputs (e.g., stock prices) would need manual integration.

## License
This project is unlicensed and intended for educational or experimental use, reflecting a fictional 1946 computational system.

