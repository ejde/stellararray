# Stellar Array Trading Algorithm Example

This document illustrates the low-level "code" used by the Stellar Array for the Trading Simulation. It demonstrates a **Differential Calculation** (Price at $t_{i+j}$ - Price at $t_i$).

## 1. Wire Storage (Program Code)
The Stellar Array uses **Étoile Code**. The following sequence performs a two-pass operation: first loading the baseline prices, then streaming the current prices to calculate the spread in real-time.

### Operation: Differential Arbitrage (Price($t_{i+j}$) - Price($t_i$) > 5)

```assembly
; HEADER
; SEQ_ID: 0x50 (Trading_Diff)
; ARCH: 15x15_STD

; --- INITIALIZATION ---
0001: SYS_RST              ; Reset all Vacuum Tubes
0002: MAP_STRIPE_STD       ; Enable Standard Striping

; --- PHASE 1: LOAD BASELINE (Time Ti) ---
0003: IO_MODE_TAPE         ; Select Input
0004: LOAD_GRID_LATCH      ; Read 225 values from Tape Block A.
                           ; Store directly into Flip-Flop Grid (Memory Bank).
                           ; These are the "Opening Prices".

; --- PHASE 2: COMPUTE SPREAD (Time Ti+j) ---
; The Array now reads the second block (Current Prices).
; Instead of storing them, it immediately subtracts the Memory value.

0005: P_LOAD_CONST 0x05    ; Load Threshold '5' into Accumulator Shadow
0006: P_STREAM_OP_SUB      ; Begin Streaming Computation:
                           ;   For each incoming Value V_curr (from Tape):
                           ;   1. Fetch V_base from corresponding Grid Node [r,c]
                           ;   2. Compute: ACC = V_curr - V_base
                           ;   3. Compare: ACC > 0x05
                           ;   4. If True: Fire Thyratron (Signal Output)
                           ;      (Note: A Thyratron is a gas-filled tube used here as a high-speed latch/switch to store the "Hit" state)
                           ;   5. If False: Suppress

; --- AGGREGATION PHASE ---
; As the Thyratrons fire, the Master Unit aggregates the signals.

0007: M_LATCH_RESULTS      ; Capture the fired Thyratrons into the Output Buffer
0008: IO_MODE_NIXIE        ; Select Output
0009: M_OUT_ADDR_DIFF      ; Print Ticker and Calculated Spread for hits
                           ; Format: "TICKER-[Row][Col]: +[Spread]"

0010: HALT                 ; End of Cycle
```

## 2. Input Tape (Data Stream)
The tape must now contain **two distinct blocks** of data.

**Physical Format**: 5-hole paper tape.
**Logical Format**: Block A (Baseline) followed by Block B (Current).

### Example Tape Segment

| Sequence | Value (Hex) | Decimal | Context | Operation Performed |
| :--- | :--- | :--- | :--- | :--- |
| **Start A** | `FF` | - | **Start Block A ($t_i$)** | - |
| 1 | `0A` | 10 | Node [0,0] Price | **STORE** $\rightarrow$ Grid[0,0] = 10 |
| 2 | `14` | 20 | Node [0,1] Price | **STORE** $\rightarrow$ Grid[0,1] = 20 |
| ... | ... | ... | ... | ... |
| **End A** | `FF` | - | **End Block A** | - |
| **Start B** | `FE` | - | **Start Block B ($t_{i+j}$)** | - |
| 226 | `0C` | 12 | Node [0,0] Price | **SUB**: $12 - 10 = 2$. ($2 \ngtr 5$). **NO ACTION**. |
| 227 | `1D` | 29 | Node [0,1] Price | **SUB**: $29 - 20 = 9$. ($9 > 5$). **SIGNAL BUY**. |
| ... | ... | ... | ... | ... |
| **End B** | `FE` | - | **End Block B** | - |

### Execution Result
1.  **Node [0,0]**: Price rose from 10 to 12. Spread is +2. Below threshold. Ignored.
2.  **Node [0,1]**: Price rose from 20 to 29. Spread is +9. Above threshold.
3.  **Output**: `TICKER-[0][1]: +9`
