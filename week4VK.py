class ALU:
    """Arithmetic Logic Unit for performing operations."""
    def execute(self, operation, operand1, operand2=None):
        if operation == "ADD":
            return operand1 + operand2
        elif operation == "SUB":
            return operand1 - operand2
        elif operation == "LOAD":
            return operand1  # Simulates loading a value into a register
        elif operation == "HALT":
            return None
        else:
            raise ValueError(f"Unknown operation: {operation}")

class CPU:
    """Central Processing Unit."""
    def __init__(self, program):
        self.PC = 0  # Program Counter
        self.memory = []  # Memory for storing instructions
        self.IR = None  # Instruction Register
        self.registers = [0] * 8  # 8 General-purpose registers (R0 to R7)
        self.ALU = ALU()  # Arithmetic Logic Unit
        self.memory.extend(program)  # Load program into memory

    def fetch(self):
        """Fetch the next instruction."""
        if self.PC < len(self.memory):
            self.IR = self.memory[self.PC]
            self.PC += 1
        else:
            self.IR = None

    def decode_and_execute(self):
        """Decode and execute the fetched instruction."""
        if self.IR:
            parts = self.IR.split()  # Example: "ADD R1 R2 R3"
            opcode = parts[0]
            if opcode == "LOAD":
                reg_index = int(parts[1][1:])  # Extract register index (e.g., R1 -> 1)
                value = int(parts[2])  # Immediate value
                self.registers[reg_index] = self.ALU.execute(opcode, value)
            elif opcode == "ADD":
                dest_reg = int(parts[1][1:])
                src1 = int(parts[2][1:])
                src2 = int(parts[3][1:])
                self.registers[dest_reg] = self.ALU.execute(opcode, self.registers[src1], self.registers[src2])
            elif opcode == "STORE":
                reg_index = int(parts[1][1:])
                print(f"Stored value from R{reg_index}: {self.registers[reg_index]}")
            elif opcode == "HALT":
                print("HALT encountered. Stopping execution.")
                return False
            else:
                print(f"Unknown instruction: {self.IR}")
            return True
        return False

    def run(self):
        """Run the fetch-decode-execute cycle."""
        while True:
            self.fetch()
            if not self.decode_and_execute():
                break
        print("Final Register State:", self.registers)

# Example Program
program = [
    "LOAD R1 10",      # Load 10 into R1
    "LOAD R2 20",      # Load 20 into R2
    "ADD R3 R1 R2",    # R3 = R1 + R2
    "STORE R3",        # Output R3's value
    "HALT"             # Stop execution
]

# Create a CPU instance and run the program
cpu = CPU(program)
cpu.run()
