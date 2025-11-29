# Stellar Array Trading Algorithm Example

This document illustrates the low-level "code" used by the Stellar Array for the Trading Simulation. It is divided into two parts: the **Program** (loaded into Wire Storage) and the **Data** (fed via Punched Tape).

## 1. Wire Storage (Program Code)
The Stellar Array uses **Étoile Code**, a specialized instruction set for parallel matrix operations. The following sequence is loaded into the 150,000-bit wire storage to execute the Trading Algorithm.

### Operation: Arbitrage Detection (Spread > 5)

```assembly
; HEADER
; SEQ_ID: 0x4F (Trading)
; ARCH: 15x15_STD

; --- INITIALIZATION ---
0001: SYS_RST              ; Reset all Vacuum Tubes and Flip-Flops
0002: IO_MODE_TAPE         ; Set Input Source to High-Speed Tape Reader
0003: MAP_STRIPE_STD       ; Enable Standard Striping (Rows 0-4->C0, 5-9->C1, 10-14->C2)

; --- INGEST PHASE ---
0004: LOAD_GRID_WAIT       ; Start Tape Reader. Wait until all 225 nodes are filled.
                           ; (Hardware handles the modulo-38 register routing automatically)

; --- PARALLEL COMPUTATION PHASE ---
; The following instructions execute on Calculators 0, 1, and 2 simultaneously.

0005: P_LOAD_CONST 0x05    ; Load constant '5' into the Accumulator Shadow Register
0006: P_COMP_GT            ; Compare: Register[i] > Accumulator
                           ; If True: Set corresponding Flip-Flop High (1)
                           ; If False: Set corresponding Flip-Flop Low (0)

; --- AGGREGATION PHASE ---
; Executed by Calculator 3 (The Master Unit)

0007: M_SCAN_GRID          ; Scan the 15x15 Flip-Flop Array for High (1) bits
0008: BR_ZERO 0011         ; Branch to 0011 if no High bits found

0009: IO_MODE_NIXIE        ; Set Output to Nixie Display
0010: M_OUT_ADDR_VAL       ; Output the Address [Row,Col] and Value of all High nodes
                           ; Format: "TICKER-[Row][Col]: BUY"

0011: HALT                 ; End of Program
```

## 2. Input Tape (Data Stream)
The input tape contains the raw market data. Since the program logic is pre-loaded, the tape only needs to carry the values.

**Physical Format**: 5-hole paper tape (Baudot-style encoding).
**Logical Format**: Stream of 8-bit Integers (0-255).

### Example Tape Segment

| Sequence | Binary (Holes) | Hex | Decimal | Meaning / Mapping |
| :--- | :--- | :--- | :--- | :--- |
| **Start** | `11111111` | `FF` | - | **Start of Data Block** |
| 1 | `00000011` | `03` | 3 | Node [0,0] (Spread=3) $\rightarrow$ Calc 0, Reg 0 |
| 2 | `00001000` | `08` | 8 | Node [0,1] (Spread=8) $\rightarrow$ Calc 0, Reg 1 |
| 3 | `00000001` | `01` | 1 | Node [0,2] (Spread=1) $\rightarrow$ Calc 0, Reg 2 |
| ... | ... | ... | ... | ... |
| 225 | `00000100` | `04` | 4 | Node [14,14] (Spread=4) $\rightarrow$ Calc 2, Reg 37 |
| **End** | `11111111` | `FF` | - | **End of Data Block** |

### Execution Result
Based on the code above:
1.  **Node [0,0]** (Value 3): `3 > 5` is False. Flip-Flop stays 0.
2.  **Node [0,1]** (Value 8): `8 > 5` is True. Flip-Flop sets to 1.
3.  **Output**: The Master Scan detects Node [0,1] is High and prints the buy signal.
