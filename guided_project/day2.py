import sys

# print(sys.argv[1])
# sys.exit()

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4

memory = [0] * 256

# Variables are called "registers".
# * There are a fixed number
# * They have preset names: R0, R1, R2, R3 ... R7
#
# Registers can each hold a single byte

register = [0] * 8  # [0,0,0,0,0,0,0,0]


day2 = "/Users/adrienneemick/Desktop/Lambda/web32cs/Computer-Architecture/guided_project/day2.py"
prog1 = "/Users/adrienneemick/Desktop/Lambda/web32cs/Computer-Architecture/guided_project/prog1.txt"

address = 0

# Read program
if len(sys.argv) != 2:
    print("usage: day2.py progname")
    sys.exit(1) # indicates what error occurred

try:
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()

            if line == '' or line[0] == "#":
                continue
            
            try:
                str_value = line.split("#")[0]
                value = int(str_value, 10) # specify base for project today: int(str_value, 2)
            
            except ValueError:
                print(f"Invalid number: {str_value}")
                sys.exit(1)

            # load value in memory
            memory[address] = value
            address += 1
            
except FileNotFoundError:
    print(f"File not found: {sys.argv[1]}")
    sys.exit(2)


# Start execution at address 0

# Keep track of the address of the currently-executing instruction
pc = 0   # Program Counter, pointer to the instruction we're executing

halted = False

while not halted:
	instruction = memory[pc]

	if instruction == PRINT_BEEJ:
		print("Beej!")
		pc += 1

	elif instruction == HALT:
		halted = True
		pc += 1

	elif instruction == SAVE_REG:
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		register[reg_num] = value
		pc += 3

	elif instruction == PRINT_REG:
		reg_num = memory[pc + 1]
		print(register[reg_num])
		pc += 2

	else:
		print(f"unknown instruction {instruction} at address {pc}")
		sys.exit(1)


# Bitwise Operators
# -----------------

# Boolean
# AND used to turn bits off, OR to turn on
# Tos compliment - handles negative numbers

# A   B   A and B     &
# ---------------
# F   F     F 
# F   T     F
# T   F     F
# T   T     T 

# A   B   A or B      | "pipe"
# ---------------
# F   F     F 
# F   T     T 
# T   F     T 
# T   T     T 

# A   not A           ~
# ---------
# T    F 
# F    T 

# T = 1
# F = 0


# Bonus program: an adder written using only bitwise operations.
# ripple_carry_adder.py 

# def ripple_carry_add(a, b):
# 	"""
# 	8-bit ripple carry adder.
# ​
# 	Adds two 8-bit numbers for an 8-bit result.
# ​
# 	Returns tuple (result, carry)
# ​
# 	If the result overflows 8 bits, the carry flag is set to 1.
# 	"""
# ​
# 	# Get individual bits of the numbers
# ​
# 	a0 = (a >> 0) & 1
# 	a1 = (a >> 1) & 1
# 	a2 = (a >> 2) & 1
# 	a3 = (a >> 3) & 1
# 	a4 = (a >> 4) & 1
# 	a5 = (a >> 5) & 1
# 	a6 = (a >> 6) & 1
# 	a7 = (a >> 7) & 1
# ​
# 	b0 = (b >> 0) & 1
# 	b1 = (b >> 1) & 1
# 	b2 = (b >> 2) & 1
# 	b3 = (b >> 3) & 1
# 	b4 = (b >> 4) & 1
# 	b5 = (b >> 5) & 1
# 	b6 = (b >> 6) & 1
# 	b7 = (b >> 7) & 1
# ​
# 	result = 0
# ​
# 	c = 0  # Initial carry in
# ​
# 	# Add bit 0
# 	s = a0 ^ b0 ^ c
# 	c = (a0 & b0) | (c & (a0 ^ b0))
# 	result |= s << 0
# ​
# 	# Add bit 1
# 	s = a1 ^ b1 ^ c
# 	c = (a1 & b1) | (c & (a1 ^ b1))
# 	result |= s << 1
# ​
# 	# Add bit 2
# 	s = a2 ^ b2 ^ c
# 	c = (a2 & b2) | (c & (a2 ^ b2))
# 	result |= s << 2
# ​
# 	# Add bit 3
# 	s = a3 ^ b3 ^ c
# 	c = (a3 & b3) | (c & (a3 ^ b3))
# 	result |= s << 3
# ​
# 	# Add bit 4
# 	s = a4 ^ b4 ^ c
# 	c = (a4 & b4) | (c & (a4 ^ b4))
# 	result |= s << 4
# ​
# 	# Add bit 5
# 	s = a5 ^ b5 ^ c
# 	c = (a5 & b5) | (c & (a5 ^ b5))
# 	result |= s << 5
# ​
# 	# Add bit 6
# 	s = a6 ^ b6 ^ c
# 	c = (a6 & b6) | (c & (a6 ^ b6))
# 	result |= s << 6
# ​
# 	# Add bit 7
# 	s = a7 ^ b7 ^ c
# 	c = (a7 & b7) | (c & (a7 ^ b7))
# 	result |= s << 7
# ​
# 	return (result, c)
# ​
# if __name__ == "__main__":
# 	# Test adding all combinations of numbers from 0-255:
# 	for a in range(0, 256):
# 		for b in range(0, 256):
# 			r, c = ripple_carry_add(a, b)
# 			assert(r + c * 256 == a + b)