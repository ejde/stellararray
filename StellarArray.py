import time
import random

class StellarArray:
    def __init__(self):
        # Simulate 700 tubes: 3 calculators at 166 tubes, 1 at 200
        self.tubes = 700
        self.calculators = [
            {"tubes": 166, "registers": [0] * 38},  # ~300 bits, 8-bit registers
            {"tubes": 166, "registers": [0] * 38},
            {"tubes": 166, "registers": [0] * 38},
            {"tubes": 200, "registers": [0] * 38}
        ]
        # 150,000-bit wire (~15,000 commands), ~464 flip-flops (~3,712 bits)
        self.wire = [0] * 150000  # Simplified as a list
        self.flip_flops = [0] * 3712  # 464 flip-flops, 8 bits each
        self.time_delay = 0  # Track simulated time (seconds)

    def read_tape(self, data):
        # Simulate punched tape input (~100 bits/s)
        bits = len(data) * 8  # Assuming 8 bits per value
        self.time_delay += bits / 100  # ~8 s for 800 bits
        return data

    def write_output(self, data):
        # Simulate nixie/output (~10 bits/s for tape, instant for nixie)
        bits = len(data) * 8
        self.time_delay += bits / 10  # ~80 s for 800 bits
        print(f"Output: {data}")

    def compute_15x15_grid(self, data):
        # Simulate 15x15 grid computation (~225 points)
        grid = [[0 for _ in range(15)] for _ in range(15)]
        # Parallelize across 3 calculators (stocks 1-5, 6-10, 11-15)
        for i in range(15):
            for j in range(15):
                calc_idx = (i // 5) % 3  # Assign to calculators 0, 1, 2
                # Simulate SUB operation (e.g., price difference)
                reg_idx = (i * 15 + j) % 38
                self.calculators[calc_idx]["registers"][reg_idx] = data[i * 15 + j]
                grid[i][j] = self.calculators[calc_idx]["registers"][reg_idx]
                self.time_delay += 0.004  # ~4 ms per operation

        # Fourth calculator aggregates (~225 comparisons)
        results = []
        for i in range(15):
            for j in range(15):
                # Simulate CMP operation (threshold = 5)
                self.time_delay += 0.001  # ~1 ms per comparison
                if grid[i][j] > 5:  # Simplified threshold
                    results.append(f"Trade at [{i},{j}]: {grid[i][j]}")
        self.time_delay += 22  # ~22 s for subroutine calls
        return results

    def simulate(self, input_data):
        print("Starting simulation...")
        # Step 1: Load data
        data = self.read_tape(input_data)
        print(f"Data loaded in {self.time_delay:.2f} s")

        # Step 2: Compute 15x15 grid
        results = self.compute_15x15_grid(data)
        print(f"Computation done in {self.time_delay:.2f} s")

        # Step 3: Output results
        self.write_output(results)
        print(f"Total time: {self.time_delay:.2f} s")

# Test the simulator
if __name__ == "__main__":
    # Simulate 15x15 grid input (~225 prices, ~800 bits)
    input_data = [random.randint(0, 10) for _ in range(225)]  # Simplified prices
    array = StellarArray()
    array.simulate(input_data)
