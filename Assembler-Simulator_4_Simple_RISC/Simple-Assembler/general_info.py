#Dictionary to lookup Opcodes and their corresponding instruction type.
opcodes = {
    'add': ['10000','A'],
    'sub': ['10001','A'],
    'movi': ['10010','B'],
    'movr': ['10011','C'], #self-note to ensure mov register and mov immediate are differentiated by assembler
    'ld': ['10100','D'],
    'st': ['10101','D'],
    'mul': ['10110','A'],
    'div': ['10111','C'],
    'rs': ['11000','B'],
    'ls': ['11001','B'],
    'xor': ['11010','A'],
    'or': ['11011','A'],
    'and': ['11100','A'],
    'not': ['11101','C'],
    'cmp': ['11110','C'],
    'jmp': ['11111','E'],
    'jlt': ['01100','E'],
    'jgt': ['01101','E'],
    'je': ['01111','E'],
    'hlt': ['01010','F'],
}

#General Info
listofinstructions = ['hlt', 'je', 'jgt', 'jlt', 'jmp', 'cmp', 'not', 'and', 'or', 'xor', 'ls', 'rs', 'div', 'mul', 'st', 'ld', 'mov', 'sub', 'add', 'var']
listofinstructions_final = ['hlt', 'je', 'jgt', 'jlt', 'jmp', 'cmp', 'not', 'and', 'or', 'xor', 'ls', 'rs', 'div', 'mul', 'st', 'ld', 'movr', 'movi', 'sub', 'add']
valid_syntax = ['hlt', 'je', 'jgt', 'jlt', 'jmp', 'cmp', 'not', 'and', 'or', 'xor', 'ls', 'rs', 'div', 'mul', 'st', 'ld', 'mov', 'sub', 'add', 'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']
listofregisters = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'FLAGS']