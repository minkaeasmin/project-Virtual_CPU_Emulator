
class ALU:
    """Arithmetic Logic Unit for performing operations."""
    def execute(self, operation, operand1, operand2=None):
        if operation == "ADD":
            return operand1 + operand2
        elif operation == "SUB":
            return operand1 - operand2
        elif operation == "LOAD":
            return operand1
        elif operation == "HALT":
            return None
        else:
            raise ValueError(f"Unknown operation: {operation}")

class IODevice:
    """Simulated I/O Device for input and output."""
    @staticmethod
    def read_input():
        return int(input("Enter a value: "))

    @staticmethod
    def display_output(value):
        print(f"Output: {value}")

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
            parts = self.IR.split()
            opcode = parts[0]
            if opcode == "LOAD":
                reg_index = int(parts[1][1:])
                value = int(parts[2])
                self.registers[reg_index] = self.ALU.execute(opcode, value)
            elif opcode == "ADD":
                dest_reg = int(parts[1][1:])
                src1 = int(parts[2][1:])
                src2 = int(parts[3][1:])
                self.registers[dest_reg] = self.ALU.execute(opcode, self.registers[src1], self.registers[src2])
            elif opcode == "STORE":
                reg_index = int(parts[1][1:])
                memory_address = int(parts[2])
                write_memory(memory_address, self.registers[reg_index])
                print(f"Stored value from R{reg_index} into Memory[{memory_address}]: {self.registers[reg_index]}")
            elif opcode == "INPUT":
                reg_index = int(parts[1][1:])
                self.registers[reg_index] = IODevice.read_input()
            elif opcode == "OUTPUT":
                reg_index = int(parts[1][1:])
                IODevice.display_output(self.registers[reg_index])
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

# Memory Management
MEMORY_SIZE = 1024
memory = [0] * MEMORY_SIZE

class SegmentDescriptor:
    def __init__(self, base, limit):
        self.base = base
        self.limit = limit

segment_table = [SegmentDescriptor(0, 512), SegmentDescriptor(512, 512)]

def read_memory(address):
    if 0 <= address < MEMORY_SIZE:
        return memory[address]
    else:
        raise ValueError("Invalid memory address")

def write_memory(address, value):
    if 0 <= address < MEMORY_SIZE:
        memory[address] = value
    else:
        raise ValueError("Invalid memory address")

def read_memory_segmented(segment, offset):
    if 0 <= segment < len(segment_table) and 0 <= offset < segment_table[segment].limit:
        return read_memory(segment_table[segment].base + offset)
    else:
        raise ValueError("Invalid segment or offset")

def write_memory_segmented(segment, offset, value):
    if 0 <= segment < len(segment_table) and 0 <= offset < segment_table[segment].limit:
        write_memory(segment_table[segment].base + offset, value)
    else:
        raise ValueError("Invalid segment or offset")

# Unified Example Program
program = [
    "LOAD R1 10",      # Load 10 into R1
    "LOAD R2 20",      # Load 20 into R2
    "ADD R3 R1 R2",    # R3 = R1 + R2
    "STORE R3 100",    # Store R3's value into memory address 100
    "INPUT R4",        # Take input and store in R4
    "OUTPUT R4",       # Display the value of R4
    "HALT"             # Stop execution
]

# Initialize CPU and run
cpu = CPU(program)
cpu.run()

# Memory Operations Example (Using Same Context)
print("Memory[100]:", read_memory(100))  # Output: 30 (from the CPU program execution)

write_memory_segmented(0, 50, read_memory(100))  # Store the result (30) in segmented memory
print("Segmented Memory[0, 50]:", read_memory_segmented(0, 50))  # Output: 30
