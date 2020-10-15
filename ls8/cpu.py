"""CPU functionality."""

import sys
print(sys.argv[0])

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xf4 # Stack pointer
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        address = 0

        # Read program
        if len(sys.argv) != 2:
            print("usage: ls8.py examples/program_name")
            sys.exit(1) # indicates what error occurred

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()

                    # ignore blank lines and everything after a `#`
                    if line == '' or line[0] == "#":
                        continue

                    # convert the binary strings to integer values to store in RAM
                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2) 
                    
                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)

                    # load value in memory
                    self.ram[address] = value
                    address += 1
                    
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[value] = address

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def push_val(self, value):
        self.reg[7] -= 1
        top_of_stack_addr = self.reg[7]
        self.ram[top_of_stack_addr] = value

    def pop_val(self):
        # get value from top of stack
        top_of_stack_addr = self.reg[7]
        value = self.ram_read(top_of_stack_addr)
        # increment the SP
        self.reg[7] += 1
        return value

    def run(self):
        """Run the CPU."""
        halted = False

        while not halted:
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            instruction = self.ram[self.pc]
            # print(instruction)
            
            if instruction == HLT:
                # print(f'HLT instruction: {instruction}')
                halted = True
                # self.pc += 1
            elif instruction == LDI:
                # print(f'LDI instruction: {instruction}')
                self.reg[operand_a] = operand_b
                # print(operand_a)
                # print(f'ldi rega: {self.reg[operand_a]}')
                # print(f'ldi opb: {operand_b}')
                # self.pc += 3
            elif instruction == PRN:
                # print(f'PRN instruction: {instruction}')
                print(self.reg[operand_a])
                # self.pc += 2
            elif instruction == MUL:
                # print(f'MUL instruction: {instruction}')
                self.alu("MUL", operand_a, operand_b)
            elif instruction == PUSH:
                # print(f'PUSH instruction: {instruction}')
                # decrement the stack pointer
                self.reg[7] -= 1
                # grab the value out of the given register
                reg_num = self.ram_read(self.pc + 1) 
                value = self.reg[reg_num] # this is what we want to push
                # copy the value onto the stack
                top_of_stack_addr = self.reg[7]
                self.ram_write(top_of_stack_addr, value)
                # pc += 2
                # print(self.ram[0xf0:0xf4])
            elif instruction == POP:
                # print(f'POP instruction: {instruction}')
                # get value from top of stack
                top_of_stack_addr = self.reg[7]
                value = self.ram_read(top_of_stack_addr)
                # store in a register
                reg_num = self.ram_read(self.pc + 1) 
                self.reg[reg_num] = value
                # increment the SP
                self.reg[7] += 1
                # pc += 2
                # print(self.ram[0xf0:0xf4])
            elif instruction == CALL:
                # get address of the next instruction after the CALL
                return_addr = self.pc + 2
                # push it on stack
                self.push_val(return_addr)
                self.ram_write(self.reg[7], return_addr)
                # get subroutine address from register
                reg_num = self.ram[self.pc + 1]
                subroutine_addr = self.reg[reg_num]
                # jump to it
                self.pc = subroutine_addr
            elif instruction == RET:
                # get return addr from top of stack
                return_addr = self.pop_val()
                # store in the PC
                self.pc = return_addr
            elif instruction == ADD:
                # print(f'ADD instruction: {instruction}')
                self.alu("ADD", operand_a, operand_b)
            else:
                print('instruction not found')
                sys.exit(1)

            # if instruction handler sets the `PC` directly, don't advance PC to next instruction
            if instruction == RET or instruction == CALL:
                pass
            else:
                inst_len = ((instruction & 0b11000000) >> 6) + 1
                # print(inst_len)
                # OR: 
                # inst_len = (instruction >> 6) + 1
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
