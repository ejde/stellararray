import tkinter as tk
from tkinter import ttk
import time
import random
import math
import threading
import string

class SimulationEngine:
    def __init__(self, mode, visualizer):
        self.mode = mode
        self.vis = visualizer
        self.step_generator = self._simulation_generator()
        self.is_complete = False

    def step(self):
        if not self.is_complete:
            try:
                next(self.step_generator)
            except StopIteration:
                self.is_complete = True
                self.vis.log("SIMULATION COMPLETE.")
                self.vis.status_var.set("STATUS: COMPLETE")

    def _simulation_generator(self):
        # 1. GENERATE DATA
        self.vis.log("INIT: GENERATING DATA TAPES (BLOCK A & B)...")
        self.vis.update_output_display([])
        
        # Tape A: Baseline
        tape_a = []
        # Tape B: Current Stream
        tape_b = []
        
        output_log = []

        is_trading = (self.mode == "trading")
        
        for i in range(225):
            # Baseline
            val_a = random.randint(10, 50)
            label_a = f"A-{i:03d}"
            
            # Current (Stream)
            # Create some variance for trading
            if is_trading:
                # 20% chance of big spread
                if random.random() < 0.2:
                    change = random.randint(6, 15)
                else:
                    change = random.randint(-2, 4)
                val_b = val_a + change
                label_b = f"B-{i:03d}"
            else:
                 val_b = random.randint(0, 99)
                 label_b = f"B-{i:03d}"
                 
            tape_a.append({"val": val_a, "label": label_a, "idx": i})
            tape_b.append({"val": val_b, "label": label_b, "idx": i})

        # --- PHASE 1: INGEST (BLOCK A - BASELINE) ---
        self.vis.log("PHASE 1 START: INGESTING BASELINE DATA (BLOCK A)\nSystem is reading Block A from the tape to load the 'Opening Prices' into Memory.\nAction: Read Tape -> Route -> Store in Flip-Flop Grid.")
        
        # Display Tape A with explicit block header if possible (simplified here)
        self.vis.update_tape_display(tape_a[:10])
        yield

        # Grid state to store baseline
        grid_memory = [[0]*15 for _ in range(15)]
        
        last_calc_id = -1

        for item in tape_a:
            idx = item['idx']
            val = item['val']
            label = item['label']
            
            row = idx // 15
            col = idx % 15
            calc_id = (row // 5) % 3
            reg_id = idx % 38
            
            # --- CONTEXT SWITCH EXPLANATION ---
            if calc_id != last_calc_id:
                if last_calc_id != -1:
                    self.vis.log(f"ARCHITECTURAL SWITCH: CHANGING CALCULATOR UNIT\nMoving from Rows {last_calc_id*5}-{(last_calc_id*5)+4} to Rows {calc_id*5}-{(calc_id*5)+4}.\nReason: The Grid is 'Striped' across 3 parallel units to allow simultaneous access.")
                    self.vis.highlight_calculator(calc_id, True)
                    yield
                    self.vis.highlight_calculator(calc_id, False) # Flash new unit
                last_calc_id = calc_id

            # 1a. READ TAPE
            self.vis.highlight_tape(True)
            self.vis.update_tape_display([item]) 
            self.vis.log(f"STEP 1: READ TAPE (BLOCK A)\nReading value {val} ({label}).\nNext: Determining destination Calculator based on Row {row}.")
            
            yield
            
            # 1b. ROUTE for Storage
            self.vis.highlight_calculator(calc_id, True)
            self.vis.update_calc_header(calc_id, f"CALC {calc_id}: ROUTING...")
            self.vis.log(f"STEP 2: ROUTING\nRow {row} routes to CALCULATOR {calc_id} (Responsible for Rows {calc_id*5}-{(calc_id*5)+4}).\nValue is latched into Register Bank.")
            yield
            
            # 1c. LATCH GRID
            self.vis.highlight_register(calc_id, reg_id, True, val)
            grid_memory[row][col] = val
            self.vis.update_grid_cell(row, col, "#222222", str(val), "#666666")
            self.vis.log(f"STEP 3: STORAGE\nValue {val} is latched into Grid Node [{row},{col}].\nAction Complete.")
            
            yield
            
            # Cleanup step visualization
            self.vis.highlight_tape(False)
            self.vis.highlight_calculator(calc_id, False)
            self.vis.highlight_register(calc_id, reg_id, False, val)

        self.vis.log("PHASE 1 COMPLETE: MEMORY LOADED\nThe entire 15x15 Grid is now populated with Baseline Data.\nThe system is ready for the Streaming Computation phase.")
        yield

        # --- PHASE 2: STREAM & COMPUTE (BLOCK B - CURRENT) ---
        self.vis.log("PHASE 2 START: STREAMING COMPUTATION (BLOCK B)\nSystem will read Block B (Current Prices) and compare them REAL-TIME against Memory.\nCrucial: Block B is NOT stored. It is subtracted on the fly.")
        
        # Reset calculators
        self.vis.reset_visuals()

        for item in tape_b:
            idx = item['idx']
            val_curr = item['val']
            label = item['label']
            
            row = idx // 15
            col = idx % 15
            calc_id = (row // 5) % 3
            
            # Fetch Baseline from Memory
            val_base = grid_memory[row][col]
            
            # 2a. READ TAPE
            self.vis.highlight_tape(True)
            self.vis.update_tape_display([item])

            # 2b. PARALLEL COMPUTE
            # Visualize the "Stream" hitting the Calculator
            self.vis.highlight_calculator(calc_id, True)
            
            # Logic
            diff = val_curr - val_base
            op_str = f"{val_curr} - {val_base} = {diff:+d}"
            self.vis.update_calc_header(calc_id, f"CALC {calc_id}: {op_str}")
            
            # Highlight Grid Cell involved
            self.vis.update_grid_cell(row, col, "#ffcc00", str(val_base), "black")
            
            self.vis.log(f"COMPUTATION CYCLE: Node [{row},{col}]\n1. Tape supplies Current Value: {val_curr}\n2. Grid supplies Baseline Value: {val_base}\n3. Calculator {calc_id} computes Spread: {diff}")
            
            yield
            
            # 2c. OUTPUT DECISION
            msg = ""
            cell_color = "#222222"
            text_color = "#666666"
            
            if is_trading:
                if diff > 5:
                    msg = f"BUY {label} (+{diff})"
                    cell_color = "#004400" # Green tint
                    text_color = "#00ff00"
                    
                    # --- AGGREGATOR STEP ---
                    self.vis.log(f"DECISION: BUY SIGNAL FIRED! Spread +{diff} > 5.\nThyratron at [{row},{col}] fires.")
                    self.vis.highlight_aggregator(True)
                    self.vis.update_aggregator_status(f"SIGNAL DETECTED: [{row},{col}]")
                    yield
                    
                    self.vis.log(f"AGGREGATION: Calculator 3 sweeps the signal and sends to Output.")
                    output_log.append(f"[{row},{col}] +{diff}")
                    if len(output_log) > 18: output_log.pop(0) # SCROLL
                    self.vis.update_output_display(output_log)
                    
                    yield
                    self.vis.highlight_aggregator(False)
                    self.vis.update_aggregator_status("WAITING FOR SIGNAL...")
                    
                else:
                    cell_color = "#222222"
                    self.vis.log(f"DECISION: NO ACTION\nSpread +{diff} is below threshold.\nSignal suppressed.")
            
            # Reset cell
            self.vis.update_grid_cell(row, col, cell_color, str(val_base), text_color)
            self.vis.highlight_tape(False)
            self.vis.highlight_calculator(calc_id, False)
            self.vis.update_calc_header(calc_id, f"CALC {calc_id} (IDLE)")

        self.vis.log("SIMULATION COMPLETE.")




class StellarVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Stellar Array Architecture (1946)")
        self.root.geometry("1400x900")
        self.root.configure(bg="#121212")

        self.engine = None
        self.running = False
        self.speed = 0.1 # Seconds per step
        
        self.setup_ui()

    def setup_ui(self):
        # --- HEADER ---
        header = tk.Frame(self.root, bg="#121212")
        header.pack(fill="x", padx=10, pady=10)
        tk.Label(header, text="STELLAR ARRAY ARCHITECTURE", font=("Courier", 20, "bold"), fg="#00ff00", bg="#121212").pack(side="left")
        self.status_var = tk.StringVar(value="STATUS: IDLE")
        tk.Label(header, textvariable=self.status_var, font=("Courier", 14), fg="#ffcc00", bg="#121212").pack(side="right")

        # --- CONTROLS ---
        controls = tk.Frame(self.root, bg="#202020", pady=5)
        controls.pack(fill="x", padx=10)
        
        tk.Button(controls, text="START TRADING SIM", command=lambda: self.start_sim("trading")).pack(side="left", padx=5)
        
        ttk.Separator(controls, orient="vertical").pack(side="left", fill="y", padx=10)
        
        tk.Button(controls, text="⏯ PLAY/PAUSE", command=self.toggle_play).pack(side="left", padx=5)
        tk.Button(controls, text="⏭ STEP", command=self.step_once).pack(side="left", padx=5)
        
        tk.Label(controls, text="SPEED:", fg="white", bg="#202020").pack(side="left", padx=(20,5))
        self.speed_scale = tk.Scale(controls, from_=0.01, to=1.0, resolution=0.01, orient="horizontal", bg="#202020", fg="white", length=150)
        self.speed_scale.set(0.1)
        self.speed_scale.pack(side="left")

        # --- MAIN DISPLAY ---
        main = tk.Frame(self.root, bg="#121212")
        main.pack(expand=True, fill="both", padx=10, pady=10)

        # COL 1: TAPE
        tape_frame = tk.LabelFrame(main, text="INPUT TAPE", bg="#121212", fg="#00ff00", font=("Courier", 10, "bold"))
        tape_frame.pack(side="left", fill="y", padx=5)
        self.tape_canvas = tk.Canvas(tape_frame, width=140, bg="black", highlightthickness=0)
        self.tape_canvas.pack(fill="both", expand=True, padx=5, pady=5)

        # COL 2: CALCULATORS
        calc_frame = tk.LabelFrame(main, text="CALCULATORS (PROCESSING UNITS)", bg="#121212", fg="#00ff00", font=("Courier", 10, "bold"))
        calc_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.calcs = []
        for i in range(3):
            cf = tk.Frame(calc_frame, bg="#1a1a1a", bd=1, relief="solid")
            cf.pack(fill="x", expand=True, pady=5, padx=5)
            header_lbl = tk.Label(cf, text=f"CALCULATOR {i} (Rows {i*5}-{(i*5)+4})", bg="#1a1a1a", fg="#00ffff", font=("Courier", 9))
            header_lbl.pack(anchor="w")
            
            # Registers Grid
            reg_frame = tk.Frame(cf, bg="#1a1a1a")
            reg_frame.pack(fill="x", padx=2)
            regs = []
            for r in range(38):
                lbl = tk.Label(reg_frame, text="00", bg="#000000", fg="#444444", font=("Arial", 7), width=3, relief="flat")
                lbl.grid(row=r//10, column=r%10, padx=1, pady=1)
                regs.append(lbl)
            self.calcs.append({"frame": cf, "regs": regs, "header": header_lbl})

        # CALCULATOR 3 (AGGREGATOR)
        agg_frame = tk.Frame(calc_frame, bg="#1a1a1a", bd=1, relief="solid")
        agg_frame.pack(fill="x", expand=True, pady=5, padx=5)
        agg_header = tk.Label(agg_frame, text="CALCULATOR 3 (AGGREGATOR)", bg="#1a1a1a", fg="#ff00ff", font=("Courier", 9))
        agg_header.pack(anchor="w")
        self.aggregator = {"frame": agg_frame, "header": agg_header}
        
        # Aggregator Status
        self.agg_status = tk.Label(agg_frame, text="WAITING FOR SIGNAL...", bg="#000000", fg="#444444", font=("Courier", 10))
        self.agg_status.pack(fill="x", padx=5, pady=5)

        # COL 3: GRID
        grid_frame = tk.LabelFrame(main, text="15x15 ARRAY (MEMORY)", bg="#121212", fg="#00ff00", font=("Courier", 10, "bold"))
        grid_frame.pack(side="left", fill="both", expand=True, padx=5)
        self.grid_canvas = tk.Canvas(grid_frame, bg="black", highlightthickness=0)
        self.grid_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # COL 4: OUTPUT (NIXIE)
        out_frame = tk.LabelFrame(main, text="OUTPUT (NIXIE)", bg="#121212", fg="#00ff00", font=("Courier", 10, "bold"))
        out_frame.pack(side="left", fill="y", padx=5)
        self.out_canvas = tk.Canvas(out_frame, width=150, bg="black", highlightthickness=0)
        self.out_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize Grid Cells
        self.grid_cells = {}
        self.grid_texts = {}
        # Defer drawing until resize? No, fixed size for now to be safe
        self.grid_canvas.config(width=500, height=500)

        # --- SYSTEM EXPLANTION LOG ---
        log_frame = tk.LabelFrame(self.root, text="SYSTEM OPERATIONS LOG", bg="#121212", fg="#00ff00", font=("Courier", 10, "bold"), height=120)
        log_frame.pack(fill="x", padx=10, pady=5)
        self.log_lbl = tk.Label(log_frame, text="READY", font=("Courier", 14), fg="#00ff00", bg="black", anchor="nw", justify="left", padx=10, pady=5)
        self.log_lbl.pack(fill="both", expand=True)

    def start_sim(self, mode):
        self.engine = SimulationEngine(mode, self)
        self.running = False
        self.status_var.set("STATUS: READY - PRESS PLAY OR STEP")
        self.draw_grid_layout()
        self.reset_visuals()

    def toggle_play(self):
        if not self.engine: return
        self.running = not self.running
        if self.running:
            self.status_var.set("STATUS: RUNNING")
            self.run_loop()
        else:
            self.status_var.set("STATUS: PAUSED")

    def step_once(self):
        if not self.engine: return
        self.running = False
        self.status_var.set("STATUS: PAUSED (STEPPED)")
        self.engine.step()

    def run_loop(self):
        if self.running and self.engine and not self.engine.is_complete:
            self.engine.step()
            delay = int(self.speed_scale.get() * 1000)
            self.root.after(delay, self.run_loop)

    # --- VISUALIZATION HELPERS ---
    def log(self, msg):
        self.log_lbl.config(text=f"> {msg}")

    def draw_grid_layout(self):
        self.grid_canvas.delete("all")
        w = 500
        cell = w / 15
        for i in range(15):
            for j in range(15):
                x1, y1 = j*cell, i*cell
                x2, y2 = x1+cell-2, y1+cell-2
                self.grid_cells[(i,j)] = self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill="#111111", outline="")
                self.grid_texts[(i,j)] = self.grid_canvas.create_text((x1+x2)/2, (y1+y2)/2, text="", fill="white", font=("Arial", 8))

    def reset_visuals(self):
        for calc in self.calcs:
            calc['frame'].config(bg="#1a1a1a")
            for reg in calc['regs']:
                reg.config(bg="#000000", text="00")

    def update_tape_display(self, data):
        self.tape_canvas.delete("all")
        y = 10
        for item in data:
            self.tape_canvas.create_text(40, y, text=f"{item['label']}:{item['val']}", fill="white", font=("Courier", 10))
            y += 20

    def update_output_display(self, items):
        self.out_canvas.delete("all")
        y = 10
        for item in items:
            color = "#00ff00" if "BUY" in item else "white"
            self.out_canvas.create_text(5, y, text=item, fill=color, anchor="w", font=("Courier", 10))
            y += 20

    def highlight_tape(self, on):
        self.tape_canvas.config(bg="#333333" if on else "black")

    def highlight_calculator(self, calc_id, on):
        color = "#333333" if on else "#1a1a1a"
        self.calcs[calc_id]['frame'].config(bg=color)

    def highlight_register(self, calc_id, reg_id, on, val):
        reg = self.calcs[calc_id]['regs'][reg_id]
        if on:
            reg.config(bg="#00ff00", fg="black", text=str(val))
        else:
            reg.config(bg="#333333", fg="white") # Keep value visible but dim

    def update_calc_header(self, calc_id, text):
        self.calcs[calc_id]['header'].config(text=text)

    def update_grid_cell(self, r, c, color, text, text_color="white"):
        self.grid_canvas.itemconfig(self.grid_cells[(r,c)], fill=color)
        self.grid_canvas.itemconfig(self.grid_texts[(r,c)], text=text, fill=text_color)

    def highlight_aggregator(self, on):
        color = "#330033" if on else "#1a1a1a"
        self.aggregator['frame'].config(bg=color)

    def update_aggregator_status(self, text):
        self.agg_status.config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    app = StellarVisualizer(root)
    root.mainloop()
