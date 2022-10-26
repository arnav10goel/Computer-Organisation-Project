#Dictionary to store no. of registers per instruction
numreg_instruction = {
    'A':3,
    'B':1,
    'C':2,
    'D':1,
    'E':0,
    'F':0
}

#Dictionary to store no. of immediates per instruction
numimm_instruction = {
    'A':0,
    'B':1,
    'C':0,
    'D':0,
    'E':0,
    'F':0
}

#Dictionary to store no. of inputs per instruction type
numinputs_instruction = {
    'A':4,
    'B':3,
    'C':3,
    'D':3,
    'E':2,
    'F':1
}

#Dictionary to store no. of unused bits per instruction type
numunusedbits_instruction = {
    'A':2,
    'B':0,
    'C':5,
    'D':0,
    'E':3,
    'F':11
}

#Dictionary to store no. of memory addresses per instruction type
nummemadd_instruction = {
    'A':0,
    'B':0,
    'C':0,
    'D':1,
    'E':1,
    'F':0
}

