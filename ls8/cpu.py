"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    

    def __init__(self):
        """Construct a new CPU."""
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.stackpointer = 0b11110011
        self.ram = [0]*255
        self.reg = [0]*8
        self.pc = [0]*2
        self.MAR = 0
        self.MDR = 1

    def load(self,program):
        """Load a program into memory."""

        address = 0
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
        address = 0
        while self.ram[address]:
            instruction = self.ram[address]
            if instruction == self.HLT:
                return
            elif instruction == self.PRN:
                address += 1
                reg_address = self.ram[address]
                reg_value = self.reg[reg_address]
                print(reg_value)
                
            elif instruction == self.LDI:
                address +=1
                reg_address = self.ram[address]
                address +=1
                value = self.ram[address]
                self.reg[reg_address] = value
            elif instruction == self.MUL:
                address +=1
                reg_a = self.ram[address]
                address +=1
                reg_b = self.ram[address] 
                self.alu('MUL',reg_a,reg_b)
            elif instruction == self.PUSH:
                address +=1
                reg_address = self.ram[address]
                self.ram[self.stackpointer] = self.reg[reg_address]
                self.stackpointer -=1
            elif instruction == self.POP:
                address +=1
                reg_address = self.ram[address]
                self.stackpointer +=1
                self.reg[reg_address] = self.ram[self.stackpointer]
                
            address +=1