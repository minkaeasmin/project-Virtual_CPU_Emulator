class ALU: 
    def __init__(self):
        self.custom_operations = {}

    def define_operation(self, name, function):
        """Allows user to define a custom operation."""
        self.custom_operations[name] = function

    def execute(self, operation, operand1, operand2=None): 
        if operation in self.custom_operations:
            return self.custom_operations[operation](operand1, operand2)
        elif operation == "ADD": 
            return bin(int(operand1, 2) + int(operand2, 2))[2:]  # Binary addition
        elif operation == "SUB": 
            return bin(int(operand1, 2) - int(operand2, 2))[2:]  # Binary subtraction
        elif operation == "LOAD": 
            return operand1 
        elif operation == "HALT": 
            return None 
        else: 
            raise ValueError(f"Unknown operation: {operation}") 

class IODevice: 
    @staticmethod 
    def read_input(): 
        decimal_value = int(input("Enter a value (decimal): "))  # Prompt user for input
        return bin(decimal_value)[2:] 

    @staticmethod 
    def display_output(value): 
        print(f"Output (binary): {value}") 

MEMORY_SIZE = 1024 
memory = ['0'] * MEMORY_SIZE  # Initialize memory with binary zeros

def write_memory(address, value): 
    if 0 <= address < MEMORY_SIZE: 
        memory[address] = value 
    else: 
        raise ValueError("Invalid memory address") 

def read_memory(address): 
    if 0 <= address < MEMORY_SIZE: 
        return memory[address] 
    else: 
        raise ValueError("Invalid memory address") 

class CPU:
    def __init__(self, program): 
        self.PC = 0  # Program Counter 
        self.memory = program  # Load program into memory 
        self.IR = None  # Instruction Register 
        self.registers = ['0'] * 8  # 8 General-purpose registers (R0 to R7) 
        self.ALU = ALU()  # Arithmetic Logic Unit 
        self.input_memory_address = 200  # Starting address for storing inputs 
        self.call_stack = []  # Stack for subroutine calls 

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
            print(f"Executing: {self.IR}")  # Modified output format
            
            if opcode == "LOAD": 
                reg_index = int(parts[1][1:]) 
                value = bin(int(parts[2]))[2:]  # Convert decimal to binary
                self.registers[reg_index] = value 

            elif opcode in ["ADD", "SUB"] or opcode in self.ALU.custom_operations:
                dest_reg = int(parts[1][1:]) 
                src1 = int(parts[2][1:]) 
                src2 = int(parts[3][1:]) 
                self.registers[dest_reg] = self.ALU.execute(
                    opcode, self.registers[src1], self.registers[src2]
                ) 

            elif opcode == "STORE": 
                reg_index = int(parts[1][1:]) 
                memory_address = int(parts[2]) 
                write_memory(memory_address, self.registers[reg_index]) 

            elif opcode == "INPUT": 
                reg_index = int(parts[1][1:]) 
                input_value = IODevice.read_input() 
                self.registers[reg_index] = input_value 

            elif opcode == "OUTPUT": 
                reg_index = int(parts[1][1:]) 
                print(f"Register {parts[1]} (binary): {self.registers[reg_index]}")  # Cleaner output format
                IODevice.display_output(self.registers[reg_index]) 

            elif opcode == "JUMP":
                if len(parts) != 2:
                    raise ValueError(f"JUMP instruction requires 1 operand, got: {self.IR}")
                target_address = int(parts[1])
                self.PC = target_address

            elif opcode == "JUMPZ":
                if len(parts) != 2:
                    raise ValueError(f"JUMPZ instruction requires 1 operand, got: {self.IR}")
                target_address = int(parts[1])
                if to_decimal(self.registers[0]) == 0:  # Check R0 for zero
                    self.PC = target_address

            elif opcode == "CALL":
                if len(parts) != 2:
                    raise ValueError(f"CALL instruction requires 1 operand, got: {self.IR}")
                target_address = int(parts[1])
                self.call_stack.append(self.PC)  # Push return address onto stack
                self.PC = target_address

            elif opcode == "RET":
                if not self.call_stack:
                    print("Call stack is empty, cannot return.")
                    return False  # Stop execution
                self.PC = self.call_stack.pop()  # Pop return address from stack

            elif opcode == "HALT":
                return False  # Stop execution

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
        print("Final Register State (binary):", self.registers)

    def profile_execution(self):
        """Profile the CPU to identify bottlenecks."""
        import time
        start_time = time.time()
        self.run()  # Run the fetch-decode-execute cycle
        end_time = time.time()
        print(f"Execution Time: {end_time - start_time:.6f} seconds")  # Display time taken to run the program


# Utility functions
def to_binary(value):
    """Convert a decimal value to binary (string)."""
    return bin(value)[2:]

def to_decimal(binary_str):
    """Convert a binary string to decimal value."""
    if all(bit in '01' for bit in binary_str):
        return int(binary_str, 2)
    else:
        raise ValueError(f"Invalid binary string: {binary_str}")

MEMORY_SIZE = 1024
memory = [0] * MEMORY_SIZE

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


# Assembler Functionality
def assemble(instructions):
    """Convert assembly code to machine code."""
    machine_code = []
    for instruction in instructions:
        parts = instruction.split()
        opcode = parts[0]
        if opcode in ["LOAD", "STORE", "INPUT", "OUTPUT", "ADD", "SUB", "JUMP", "JUMPZ", "CALL", "RET", "HALT"]:
            machine_code.append(instruction)
        else:
            raise ValueError(f"Unknown instruction: {opcode}")
    return machine_code


# Main Program
if __name__ == "__main__":
    assembly_code = [
        "LOAD R1 10",      # Load decimal 10 into R1
        "LOAD R2 20",      # Load decimal 20 into R2
        "ADD R3 R1 R2",    # R3 = R1 + R2
        "STORE R3 100",    # Store the value in R3 into memory at address 100
        "CALL 5",          # Call subroutine at line 5
        "INPUT R4",        # Take input in decimal, convert to binary, and store in R4
        "OUTPUT R4",       # Display the binary value of R4
        "RET",             # Return from subroutine
        "LOAD R5 0",       # Load 0 into R5 as a loop counter
        "LOAD R6 5",       # Load 5 into R6 as the loop limit
        "SUB R7 R6 R5",    # R7 = R6 - R5
        "JUMPZ 10",        # If R7 == 0, jump to HALT
        "JUMP 4",          # Otherwise, jump back to INPUT
        "HALT"             # Stop execution
    ]

    # Assemble and run the program
    program = assemble(assembly_code)
    cpu = CPU(program)
    cpu.profile_execution()

    # After execution, check the contents of memory
    print("Memory[100] (binary):", read_memory(100))  # Output: binary result