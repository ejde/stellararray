# Stellar Array Simulator

## Overview
The Stellar Array is a fictional 1946 computational machine designed as a **massive parallel pre-computation device**. Unlike general-purpose computers (like the ENIAC), the Stellar Array is specialized for grid-based matrix operations, utilizing a unique architecture of 700 vacuum tubes distributed across four distinct calculation units.

Its primary function is to ingest large datasets via punched tape, map them onto a 15x15 memory grid, and perform simultaneous parallel operations (comparisons, differentials, pattern matching) before a final aggregation step. This "pre-computation" architecture allows it to process complex fields (like stock spreads or neutron flux gradients) significantly faster than sequential accumulators of the era.

## Technical Specifications

### Hardware Architecture
- **Total Vacuum Tubes**: 700
    - **Calculator Units 0-2**: 166 tubes each (Primary Parallel Processors).
    - **Calculator Unit 3**: 200 tubes (Aggregator & Control Logic).
- **Memory**:
    - **Wire Storage**: 150,000 bits (~18.75 KB), used for instruction sequences and look-up tables.
    - **Flip-Flops**: 464 units (~3,712 bits), serving as high-speed registers for the active 15x15 grid.
- **I/O**:
    - **Input**: High-speed punched tape reader (~100 bits/s).
    - **Output**: Nixie tube display array (~10 bits/s).

### Operational Workflow

The Stellar Array operates in a strict four-phase cycle, which this simulator emulates:

1.  **Ingest (Tape Read)**:
    Data is read sequentially from the punched tape. Each datum represents a value for a specific node in the 15x15 grid.

2.  **Route & Stripe (The "Stellar" Mapping)**:
    The array does not use a single central memory bank. Instead, data is **striped** across three parallel Calculators to maximize throughput:
    - **Rows 0-4** (75 nodes) $\rightarrow$ **Calculator 0**
    - **Rows 5-9** (75 nodes) $\rightarrow$ **Calculator 1**
    - **Rows 10-14** (75 nodes) $\rightarrow$ **Calculator 2**
    
    Incoming data is routed in real-time to the appropriate Calculator's register bank (modulo 38 addressing) before being latched into the Flip-Flop grid.

3.  **Parallel Pre-Computation**:
    Once the grid is loaded, all three Calculators trigger simultaneously. They perform local operations on their assigned rows independent of each other.
    - *Example (Trading)*: All 225 nodes compare their values against a threshold (e.g., spread > 5) instantly.
    - *Example (AEC)*: Differential gradients are calculated between adjacent nodes.

4.  **Aggregation**:
    The fourth Calculator (200 tubes) sweeps the results from the three parallel units to compute the final system state (e.g., "Criticality Index" or "Buy Signals").

## Installation & Usage
1.  **Prerequisites**: Python 3.6+ (Standard Library only).
2.  **Run the Simulator**:
    ```bash
    python StellarArray.py
    ```
3.  **Run the Visualizer** (Recommended):
    ```bash
    python StellarArrayVisualizer.py
    ```
    The visualizer provides a step-by-step interactive view of the Tape $\rightarrow$ Calculator $\rightarrow$ Grid data flow.

## Simulation Modes
- **AEC (Atomic Energy Commission)**: Neutron flux distribution analysis.
- **CEA (Commissariat à l'énergie atomique)**: Reactor pressure/temperature criticality.
- **Trading**: Arbitrage opportunity detection across 15x15 market grids.
- **Art**: Procedural pattern generation based on sine-wave interference.

## License
Unlicensed / Educational Use.

