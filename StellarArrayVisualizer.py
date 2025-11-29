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
        self.vis.log("PHASE 1: GENERATING DATA TAPE...")
        data = []
        for i in range(225):
            val = random.randint(0, 99)
            label = f"D-{i:03d}"
            if self.mode == "trading":
                label = ''.join(random.choices(string.ascii_uppercase, k=3))
                val = random.randint(0, 15)
            data.append({"val": val, "label": label, "idx": i})
        
        # Show tape
        self.vis.update_tape_display(data[:10]) # Show first few
        yield

        # 2. LOAD GRID (Tape -> Calc -> Register -> Grid)
        self.vis.log("PHASE 2: LOADING ARRAY...")
        grid_data = [[None]*15 for _ in range(15)]
        
        for item in data:
            idx = item['idx']
            val = item['val']
            label = item['label']
            
            # Calculate coordinates
            row = idx // 15
            col = idx % 15
            
            # 2a. READ TAPE
            self.vis.highlight_tape(True)
            self.vis.log(f"READ TAPE: {label} ({val})")
            yield
            self.vis.highlight_tape(False)

            # 2b. ROUTE TO CALCULATOR
            # Logic: Rows 0-4 -> Calc 0, 5-9 -> Calc 1, 10-14 -> Calc 2
            calc_id = (row // 5) % 3
            self.vis.log(f"ROUTING: Row {row} maps to CALCULATOR {calc_id}")
            self.vis.highlight_calculator(calc_id, True)
            yield

            # 2c. STORE IN REGISTER
            # Logic: (idx) % 38
            reg_id = idx % 38
            self.vis.log(f"STORING: Register {reg_id} in Calc {calc_id}")
            self.vis.highlight_register(calc_id, reg_id, True, val)
            yield
            self.vis.highlight_register(calc_id, reg_id, False, val)
            self.vis.highlight_calculator(calc_id, False)

            # 2d. COMMIT TO GRID
            self.vis.log(f"COMMIT: Transfer to Grid Node [{row},{col}]")
            color = "#333333"
            if self.mode == "trading":
                color = "#333333" # Neutral base
            self.vis.update_grid_cell(row, col, color, str(val))
            grid_data[row][col] = item
            yield

        # 3. COMPUTATION
        self.vis.log("PHASE 3: PARALLEL COMPUTATION...")
        for i in range(15):
            for j in range(15):
                item = grid_data[i][j]
                val = item['val']
                label = item['label']
                
                self.vis.update_grid_cell(i, j, "#ffcc00", str(val), "black") # Active
                
                msg = ""
                result_color = "#333333"
                
                if self.mode == "trading":
                    if val > 10:
                        msg = "BUY (Spread > 10)"
                        result_color = "#00ff00"
                    elif val < 3:
                        msg = "SELL (Spread < 3)"
                        result_color = "#ff0000"
                    else:
                        msg = "HOLD"
                
                if msg:
                    self.vis.log(f"[{i},{j}] {label}: {msg}")
                
                yield
                self.vis.update_grid_cell(i, j, result_color, str(val), "white" if result_color != "#00ff00" else "black")

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
        
        tk.Button(controls, text="START TRADING SIM", command=lambda: self.start_sim("trading"), bg="#404040", fg="white").pack(side="left", padx=5)
        
        ttk.Separator(controls, orient="vertical").pack(side="left", fill="y", padx=10)
        
        tk.Button(controls, text="⏯ PLAY/PAUSE", command=self.toggle_play, bg="#404040", fg="white").pack(side="left", padx=5)
        tk.Button(controls, text="⏭ STEP", command=self.step_once, bg="#404040", fg="white").pack(side="left", padx=5)
        
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
        self.tape_canvas = tk.Canvas(tape_frame, width=80, bg="black", highlightthickness=0)
        self.tape_canvas.pack(fill="both", expand=True, padx=5, pady=5)

        # COL 2: CALCULATORS
        calc_frame = tk.LabelFrame(main, text="CALCULATORS (PROCESSING UNITS)", bg="#121212", fg="#00ff00", font=("Courier", 10, "bold"))
        calc_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        self.calcs = []
        for i in range(3):
            cf = tk.Frame(calc_frame, bg="#1a1a1a", bd=1, relief="solid")
            cf.pack(fill="x", expand=True, pady=5, padx=5)
            tk.Label(cf, text=f"CALCULATOR {i} (Rows {i*5}-{(i*5)+4})", bg="#1a1a1a", fg="#00ffff", font=("Courier", 9)).pack(anchor="w")
            
            # Registers Grid
            reg_frame = tk.Frame(cf, bg="#1a1a1a")
            reg_frame.pack(fill="x", padx=2)
            regs = []
            for r in range(38):
                lbl = tk.Label(reg_frame, text="00", bg="#000000", fg="#444444", font=("Arial", 7), width=3, relief="flat")
                lbl.grid(row=r//19, column=r%19, padx=1, pady=1)
                regs.append(lbl)
            self.calcs.append({"frame": cf, "regs": regs})

        # COL 3: GRID
        grid_frame = tk.LabelFrame(main, text="15x15 ARRAY (MEMORY)", bg="#121212", fg="#00ff00", font=("Courier", 10, "bold"))
        grid_frame.pack(side="left", fill="both", expand=True, padx=5)
        self.grid_canvas = tk.Canvas(grid_frame, bg="black", highlightthickness=0)
        self.grid_canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Initialize Grid Cells
        self.grid_cells = {}
        self.grid_texts = {}
        # Defer drawing until resize? No, fixed size for now to be safe
        self.grid_canvas.config(width=500, height=500)

        # --- LOG ---
        log_frame = tk.Frame(self.root, bg="#121212", height=100)
        log_frame.pack(fill="x", padx=10, pady=5)
        self.log_lbl = tk.Label(log_frame, text="READY", font=("Courier", 12), fg="#00ff00", bg="black", anchor="w", padx=10)
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

    def update_grid_cell(self, r, c, color, text, text_color="white"):
        self.grid_canvas.itemconfig(self.grid_cells[(r,c)], fill=color)
        self.grid_canvas.itemconfig(self.grid_texts[(r,c)], text=text, fill=text_color)


if __name__ == "__main__":
    root = tk.Tk()
    app = StellarVisualizer(root)
    root.mainloop()
