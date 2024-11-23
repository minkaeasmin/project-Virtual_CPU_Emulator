class CPU:
    def __init__(self):
        self.registers = [0, 0, 0, 0]  # Initialize 4 registers
        self.program_counter = 0       # Initialize program counter
        self.instruction_register = None  # Holds the current instruction

    def write(self, register, value):
        """Writes a value to a specified register."""
        if 0 <= register <= 3:
            self.registers[register] = value
            print(f"Stored {value} in R{register}")
        else:
            print("Error: Invalid register number")

    def read(self, register):
        """Reads the value of a specified register."""
        if 0 <= register <= 3:
            print(f"Value in R{register}: {self.registers[register]}")
        else:
            print("Error: Invalid register number")

    def load(self, instruction):
        """Loads an instruction into the instruction register."""
        try:
            parts = instruction.split()
            operation = parts[0].upper()
            registers = list(map(int, parts[1:]))
            if operation in {"ADD", "SUB", "AND", "OR", "NOT"} and all(0 <= r <= 3 for r in registers):
                self.instruction_register = (operation, registers)
                print(f"Loaded instruction: {instruction}")
            else:
                print("Error: Invalid instruction format or registers")
        except ValueError:
            print("Error: Instruction parsing failed")

    def execute(self):
        """Executes the loaded instruction."""
        if self.instruction_register is None:
            print("Error: No instruction loaded")
            return

        operation, registers = self.instruction_register
        try:
            if operation == "ADD":
                self.registers[registers[0]] = self.registers[registers[1]] + self.registers[registers[2]]
            elif operation == "SUB":
                self.registers[registers[0]] = self.registers[registers[1]] - self.registers[registers[2]]
            elif operation == "AND":
                self.registers[registers[0]] = self.registers[registers[1]] & self.registers[registers[2]]
            elif operation == "OR":
                self.registers[registers[0]] = self.registers[registers[1]] | self.registers[registers[2]]
            elif operation == "NOT":
                self.registers[registers[0]] = ~self.registers[registers[1]]
            else:
                print("Error: Unsupported operation")
                return

            print(f"Executed instruction: {operation}")
            self.program_counter += 1
        except IndexError:
            print("Error: Invalid registers for operation")

    def run(self):
        """Interactive loop to perform CPU actions."""
        while True:
            action = input("Choose action (load, execute, write, read, exit): ").strip().lower()
            if action == "write":
                try:
                    register = int(input("Enter register number (0-3): "))
                    value = int(input("Enter value to store: "))
                    self.write(register, value)
                except ValueError:
                    print("Error: Invalid input")
            elif action == "read":
                try:
                    register = int(input("Enter register number (0-3): "))
                    self.read(register)
                except ValueError:
                    print("Error: Invalid input")
            elif action == "load":
                instruction = input("Enter instruction (e.g., ADD 0 1 2): ")
                self.load(instruction)
            elif action == "execute":
                self.execute()
            elif action == "exit":
                print("Exiting program...")
                break
            else:
                print("Error: Invalid action")


# Main Execution
if __name__ == "__main__":
    cpu = CPU()
    cpu.run()
