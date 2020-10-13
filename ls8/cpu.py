"""CPU functionality."""

import sys
print(sys.argv[0])

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        address = 0

        # Read program
        if len(sys.argv) != 2:
            print("usage: ls8.py examples/program_name")
            sys.exit(1) # indicates what error occurred

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == '':  # ignore blanks
                        continue
                    val = int(num, 2)
                # for line in f:
                #     line = line.strip()

                #     # ignore blank lines and everything after a `#`
                #     if line == '' or line[0] == "#":
                #         continue

                #     # convert the binary strings to integer values to store in RAM
                #     try:
                #         str_value = line.split("#")[0]
                #         value = int(str_value, 2) 
                    
                #     except ValueError:
                #         print(f"Invalid number: {str_value}")
                #         sys.exit(1)

                    # load value in memory
                    self.ram[address] = val
                    address += 1
                    
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value):
        self.ram[self.pc] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= reg_b
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        halted = False
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)

        while not halted:
            instruction = self.ram[self.pc]
            # print(instruction)
            
            if instruction == HLT:
                print(f'HLT instruction: {instruction}')
                halted = True
                # self.pc += 1
            elif instruction == LDI:
                print(f'LDI instruction: {instruction}')
                self.reg[operand_a] = operand_b
                print(operand_a)
                print(f'ldi rega: {self.reg[operand_a]}')
                print(f'ldi opb: {operand_b}')
                # self.pc += 3
            elif instruction == PRN:
                print(f'PRN instruction: {instruction}')
                print(self.reg[operand_a])
                # self.pc += 2
            elif instruction == MUL:
                print(f'MUL instruction: {instruction}')
                self.alu("MUL", operand_a, operand_b)
            else:
                print('instruction not found')
                sys.exit(1)

            inst_len = ((instruction & 0b11000000) >> 6) + 1
            # OR: inst_len = f(instruction >> 6) + 1
            self.pc += inst_len

            # read instruction layout!!!
            # * AND takes two arguments (takes 3 bytes) bc 10 are first 2 #'s in operand - get them out
            #   0b10100010
            # & 0b11000000
            # ------------
            #   0b10000000
            # then shift right 1: >> 1 (or >> 6 ?)
            # * HLT doesn't take any arguments 

    # make a dictionary of functions for stretch goal (step 9)