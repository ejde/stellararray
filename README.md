# Stellar Array Simulator

## Overview
The Stellar Array is a fictional 1946 computational machine designed as a **massive parallel pre-computation device**. Unlike general-purpose computers (like the ENIAC) which process one thing at a time, the Stellar Array is specialized for processing entire 15x15 grids of data at once. It utilizes a unique architecture of 700 vacuum tubes distributed across four distinct calculation units.

Its primary function is to ingest large datasets, map them onto a memory grid, and perform simultaneous parallel operations—like comparing stock prices or checking neutron flux levels—before a final aggregation step.

## How It Works: A Deep Dive
Imagine you are a scientist in 1946. You don't have a microchip; you have vacuum tubes, which are hot, expensive, and burn out if you use too many. You need to compare 225 numbers (a 15x15 grid) instantly. How do you do it?

### 1. The Input: The "Time-Travel" Tape
The Stellar Array doesn't have "RAM" like a modern computer where you can jump around randomly. It reads from a **Punched Tape** that moves in one direction.
*   **Structure**: The tape is organized into **Blocks**.
    *   **Block A (The Past)**: This block contains the "Baseline" data (e.g., stock prices at 9:00 AM). The machine reads this first and "memorizes" it.
    *   **Block B (The Present)**: This block contains the live data (e.g., stock prices at 9:01 AM).
*   **The Trick**: The machine doesn't store Block B. As Block B streams through the reader, the machine *immediately* subtracts it from the memorized Block A. It calculates the difference "on the fly" before the data is lost forever.

### 2. The Code: "Wire Storage"
There is no hard drive. The "program" is literally hard-wired.
*   **Étoile Code**: Instructions are stored on **Wire Storage** (a precursor to magnetic core memory).
*   **The Logic**: The code is simple. It tells the machine: "When you see a number from the tape, send it to Row 5, Column 3, and subtract it from what's already there. If the result is bigger than 5, turn on the light."

### 3. Communication: The "Striped" Architecture
This is the genius of the Stellar Array. If you tried to connect 225 memory cells to one central processor, you'd need thousands of tubes for the switching logic—too many!
Instead, the designers used **Striping**:
*   They split the 15x15 grid into three horizontal slices (5 rows each).
*   **Calculator 0** owns Rows 0–4.
*   **Calculator 1** owns Rows 5–9.
*   **Calculator 2** owns Rows 10–14.

**Why? Speed.**
When the tape reader sends a signal for "Row 7", Calculator 0 and 2 don't even wake up. Only Calculator 1 listens. This allows the machine to route data 3x faster than a single processor could manage.

### 4. Output: The Aggregator (Calculator 3)
Calculators 0, 1, and 2 are "dumb." They only know about their own 5 rows. They can't see the big picture.
*   When a Calculator finds an interesting result (e.g., "Price spread > 5"), it fires a **Thyratron** (a gas-filled tube acting as a switch).
*   **Calculator 3** (The Aggregator) sits above the others. It scans these Thyratrons.
*   If it sees enough firing, or a specific pattern of fires, it triggers the final **Nixie Tube Display** or punches a result card.

## Technical Specifications (Summary)
- **Total Vacuum Tubes**: 700
- **Memory**: 464 Flip-Flops (Storing the 15x15 grid).
- **Speed**: ~100 bits/second (Tape Reader limit).

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