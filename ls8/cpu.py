"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        #Operation Codes
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.ADD = 0b10100000
        #StackPointer Starting Address
        self.stackpointer = 0b11110011
        #Initialise RAM
        self.ram = [None]*255
        #Initialise 8 Registers
        self.reg = [0]*8
        self.reg[7] = 0b11110100
        #Initialise Internal Registers
        self.pc = 0
        self.IR = None
        self.MAR = None
        self.MDR = None
        self.FL = 0

    def load(self,program):
        """Load a program into memory."""
        address = 0
        #Loading in the program in to the RAM
        with open(program) as file:
            for line in file.readlines():
                #print(f'line {line},length :{len(line)}')
                if line.startswith("#") or len(line) == 1:
                    pass
                else:
                    line_instruction = line[:8]
                    instruction = int(line_instruction,2)
                    #print(instruction)
                    #print(f'address:{address}')
                    self.ram[address] = instruction
                    address += 1

            
            


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self,address):
        return self.ram[address]

    def ram_write(self,address,value):
        self.ram[address] = value
        

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
        
        while True:
            instruction = self.ram[self.pc]
            #print(f'instruction:{instruction}')
            if instruction == self.HLT:
                return
            elif instruction == self.PRN:
                self.pc += 1
                reg_address = self.ram[self.pc]
                reg_value = self.reg[reg_address]
                print(reg_value)
                
            elif instruction == self.LDI:
                self.pc +=1
                reg_address = self.ram[self.pc]
                self.pc +=1
                value = self.ram[self.pc]
                self.reg[reg_address] = value
            elif instruction == self.MUL:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('MUL',reg_a,reg_b)
            elif instruction == self.ADD:
                self.pc +=1
                reg_a = self.ram[self.pc]
                self.pc +=1
                reg_b = self.ram[self.pc] 
                self.alu('ADD',reg_a,reg_b)
            elif instruction == self.PUSH:
                self.pc +=1
                reg_address = self.ram[self.pc]
                self.ram[self.stackpointer] = self.reg[reg_address]
                self.stackpointer -=1
            elif instruction == self.POP:
                self.pc +=1
                reg_address = self.ram[self.pc]
                self.stackpointer +=1
                self.reg[reg_address] = self.ram[self.stackpointer]
            elif instruction == self.CALL:
                self.pc +=1
                register_value = self.reg[self.ram[self.pc]]
                self.pc +=1
                self.ram[self.stackpointer] = self.pc
                self.stackpointer -=1
                self.pc = register_value
                #reduce pc value by 1 to counter the effect of pc incrementer
                self.pc -=1
            elif instruction == self.RET:
                self.stackpointer +=1
                stack_value = self.ram[self.stackpointer]
                self.pc = stack_value
                #reduce pc value by 1 to counter the effect of pc incrementer
                self.pc -=1
                
                
            self.pc +=1