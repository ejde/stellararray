import time
import random
import math

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
                reg_idx = (i * 15 + j) % 38
                self.calculators[calc_idx]["registers"][reg_idx] = data[i * 15 + j]
                grid[i][j] = self.calculators[calc_idx]["registers"][reg_idx]
                self.time_delay += 0.004  # ~4 ms per operation
        return grid

    def aec_computation(self, neutron_data):
        # Simulate AEC computation (e.g., neutron multiplication factor k for Los Alamos)
        print("Starting AEC computation...")
        data = self.read_tape(neutron_data)  # ~225 neutron counts, ~800 bits
        grid = self.compute_15x15_grid(data)  # Compute differences

        # Calculate k (neutron multiplication factor) using fourth calculator
        k = 0
        for i in range(15):
            for j in range(15):
                # Simplified k calculation: sum neutron counts, normalize
                k += grid[i][j]
                self.time_delay += 0.001  # ~1 ms per operation
        k = k / (15 * 15)  # Average neutron count
        self.time_delay += 22  # ~22 s for comparisons
        result = f"Neutron multiplication factor k: {k:.2f}"
        self.write_output([result])
        return result

    def cea_computation(self, reactor_data):
        # Simulate CEA computation (e.g., 15x15 reactor criticality)
        print("Starting CEA computation...")
        data = self.read_tape(reactor_data)  # ~225 temperature/pressure points
        grid = self.compute_15x15_grid(data)

        # Calculate criticality (simplified: average temp/pressure)
        criticality = 0
        for i in range(15):
            for j in range(15):
                criticality += grid[i][j]
                self.time_delay += 0.001
        criticality = criticality / (15 * 15)
        self.time_delay += 22  # ~22 s for comparisons
        result = f"Reactor criticality index: {criticality:.2f}"
        self.write_output([result])
        return result

    def trading_computation(self, price_data):
        # Simulate trading computation (e.g., arbitrage on 15x15 grid)
        print("Starting trading computation...")
        data = self.read_tape(price_data)  # ~225 prices (NYSE vs. Curb)
        grid = self.compute_15x15_grid(data)

        # Identify arbitrage opportunities (spread > 5)
        trades = []
        for i in range(15):
            for j in range(15):
                self.time_delay += 0.001  # ~1 ms per comparison
                if grid[i][j] > 5:  # Simplified threshold
                    trades.append(f"Trade at [{i},{j}]: Spread {grid[i][j]}")
        self.time_delay += 22  # ~22 s for subroutine calls
        self.write_output(trades)
        return trades

    def art_generation(self, pattern_data):
        # Simulate art generation (e.g., fractal patterns for MoMA exhibit)
        print("Starting art generation...")
        data = self.read_tape(pattern_data)  # ~225 values for fractal angles
        grid = self.compute_15x15_grid(data)

        # Generate fractal-like pattern (simplified: sine-based angles)
        artwork = []
        for i in range(15):
            for j in range(15):
                angle = math.sin(grid[i][j] * 0.1) * 360  # Map to 0-360 degrees
                self.time_delay += 0.001
                artwork.append(f"Point [{i},{j}]: Angle {angle:.1f}°")
        self.time_delay += 22  # ~22 s for processing
        self.write_output(artwork)
        return artwork

    def simulate(self, input_data, computation_type):
        print("Starting simulation...")
        self.time_delay = 0  # Reset delay
        if computation_type == "aec":
            result = self.aec_computation(input_data)
        elif computation_type == "cea":
            result = self.cea_computation(input_data)
        elif computation_type == "trading":
            result = self.trading_computation(input_data)
        elif computation_type == "art":
            result = self.art_generation(input_data)
        else:
            raise ValueError("Unknown computation type")
        print(f"Total time: {self.time_delay:.2f} s")
        return result

# Test the simulator with different computations
if __name__ == "__main__":
    array = StellarArray()
    # Test data: 15x15 grid (~225 points)
    neutron_data = [random.randint(0, 10) for _ in range(225)]  # AEC: Neutron counts
    reactor_data = [random.randint(20, 80) for _ in range(225)]  # CEA: Temp/pressure
    price_data = [random.randint(0, 10) for _ in range(225)]  # Trading: Price diffs
    pattern_data = [random.randint(0, 360) for _ in range(225)]  # Art: Angles

    # Run simulations
    print("\n=== AEC Simulation ===")
    array.simulate(neutron_data, "aec")
    print("\n=== CEA Simulation ===")
    array.simulate(reactor_data, "cea")
    print("\n=== Trading Simulation ===")
    array.simulate(price_data, "trading")
    print("\n=== Art Simulation ===")
    array.simulate(pattern_data, "art")