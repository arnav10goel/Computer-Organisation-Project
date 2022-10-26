#This File parses information into its respective Binary Encoding
from registers import *
from general_info import *

def register_to_binary(register):
    #Parses Register Encoding for Given Register Name
    return registers_binary[register]

def immediate_to_binary(num):
    #Binary value for given immediate
    return f'{int(num):08b}'

def opcode_retriever(instruction):
    #Returns the opcode for the instruction passed as an argument
    return opcodes[instruction][0]

def memory_address_to_binary(location):
    #Binary Value for Given Memory Address
    return f'{int(location):08b}'
