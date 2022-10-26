import sys
from sys import stdin
import matplotlib.pyplot as plt
import datetime

#Dictionary for instruction types and what instruction it is
opcodes = {
    '10000': ['add','A'],
    '10001': ['sub','A'],
    '10010': ['movi','B'],
    '10011': ['movr','C'], 
    '10100': ['ld','D'],
    '10101': ['st','D'],
    '10110': ['mul','A'],
    '10111': ['div','C'],
    '11000': ['rs','B'],
    '11001': ['ls','B'],
    '11010': ['xor','A'],
    '11011': ['or','A'],
    '11100': ['and','A'],
    '11101': ['not','C'],
    '11110': ['cmp','C'],
    '11111': ['jmp','E'],
    '01100': ['jlt','E'],
    '01101': ['jgt','E'],
    '01111': ['je','E'],
    '01010': ['hlt','F']
}

#Dictionary for decoding Register from Binary Encoding
reg_decoder = {
    '000': 'R0',
    '001': 'R1',
    '010': 'R2',
    '011': 'R3',
    '100': 'R4',
    '101': 'R5',
    '110': 'R6',
    '111': 'FLAGS'
}

def inst_type(opcode):
    inst_type = opcodes[opcode][1]
    return inst_type

def inst_name(opcode):
    inst = opcodes[opcode][0]
    return inst

def num_to_8bitbinary(num):
    return f'{int(num):08b}'

def num_to_16bitbinary(num):
    conv = bin(num)
    binary = conv[2:]
    if(len(binary) > 16):
        return binary[-16:-1]
    else:
        return ('0'*(16-len(binary)) + binary)

def binary_to_dec(binary):
    num = 0
    len_str = len(binary)
    for i in range(len_str):
        num += (int(binary[len_str - i - 1])*(2**i))
    return num

def atype_implement(inst, regcode1, regcode2, reg_dict):
    reg1 = reg_dict[reg_decoder[regcode1]]
    reg2 = reg_dict[reg_decoder[regcode2]]
    if(inst == 'add'):
        return reg1 + reg2
    elif(inst == 'sub'):
        return reg1 - reg2
    elif(inst == 'mul'):
        return reg1 * reg2
    elif(inst == 'xor'):
        return reg1 ^ reg2
    elif(inst == 'or'):
        return reg1 | reg2
    elif(inst == 'and'):
        return reg1 & reg2
    elif(inst == 'addf'):
        sixteenbit_binary_one = num_to_16bitbinary(reg1)
        sixteenbit_binary_two = num_to_16bitbinary(reg2)
        numtobeadded_one = binary_to_dec(sixteenbit_binary_one[8:16])
        numtobeadded_two = binary_to_dec(sixteenbit_binary_two[8:16])
        return numtobeadded_one+numtobeadded_two
    elif(inst == 'subf'):
        sixteenbit_binary_one = num_to_16bitbinary(reg1)
        sixteenbit_binary_two = num_to_16bitbinary(reg2)
        numtobesubbed_one = binary_to_dec(sixteenbit_binary_one[8:16])
        numtobesubbed_two = binary_to_dec(sixteenbit_binary_two[8:16])
        return numtobesubbed_one-numtobesubbed_two

def btype_implement(inst, regcode1, imm, reg_dict):
    reg1 = reg_decoder[regcode1]
    if(inst == 'movi'):
        return imm
    elif(inst == 'rs'):
        return (reg_dict[reg1] >> (imm))
    elif(inst == 'ls'):
        return (reg_dict[reg1] << (imm))

def ctype_implement(inst, regcode1, regcode2, reg_dict, flag_dict):
    reg1 = reg_decoder[regcode1]
    reg2 = reg_decoder[regcode2]
    if(inst == 'not'):
        input_string = num_to_16bitbinary(reg_dict[reg1])
        output = ''
        for i in input_string:
            if i == '0':
                output += '1'
            else:
                output += '0'
        return binary_to_dec(output)
    elif(inst == 'div'):
        quotient = reg_dict[reg1] // reg_dict[reg2]
        remainder = reg_dict[reg1] % reg_dict[reg2]
        return [quotient,remainder]
    elif(inst == 'cmp'):
        if(reg_dict[reg1] == reg_dict[reg2]):
            flag_dict['E'] = '1'
        elif(reg_dict[reg1] < reg_dict[reg2]):
            flag_dict['L'] = '1'
        else:
            flag_dict['G'] = '1'
        return 0
    elif(inst == 'movr'):
        if(reg1 == 'FLAGS'):
            return (('0'*12)+ (flag_dict['V'])+ (flag_dict['L'])+ (flag_dict['G'])+ (flag_dict['E']))
        else:
            return reg_dict[reg1]

#This function assigns characters to the corresponding character and base using UNICODE values.
def valueinp(char):
    if char >= '0' and char <= '9':
        return ord(char) - ord('0')
    else:
        return ord(char) - ord('A') + 10

#This function converts the given number to its decimal form by using chrs from above function.
def AnybasetoDeci(str,base):
    lenofin = len(str)
    power = 1 
    num = 0     
    for i in range(lenofin - 1, -1, -1):
        num += valueinp(str[i]) * power
        power = power * base
    return num

#This functions converts any number input to its characters again using UNICODE values.    
def reValueinp(num): 
    if (num >= 0 and num <= 9):
        return chr(num + ord('0'))
    else:
        return chr(num - 10 + ord('A'))

#Uses reValueinp to convert fromm decimal to target base.
def fromDeci(result, base, inputNum): 
    index = 0; # Initialize index of result
    while (inputNum > 0):
        result+= reValueinp(inputNum % base)
        inputNum = int(inputNum / base)
    result = result[::-1]
    return result

#This function checks the validity of the user's input and if valid performs the CONVERSION operation.
def input_validity(srcbase,tarbase,strr):
    for i in strr:
        if i.isdigit():
            if int(i) >= srcbase:
                return "Number does not exist in the mentioned Base."
        elif i.isalpha():
            if ord(i.upper())-55 >= srcbase:
                return "Number does not exist in the mentioned Base."
    answerhold = AnybasetoDeci(strr, srcbase)
    inputNum = answerhold
    result = ""
    return str(fromDeci(result, tarbase, inputNum))

def float_to_binary(str):
    lst = []
    for i in range(len(str)):
        lst.append(str[i])

    #If the string has non-numeric terms
    for i in range(len(lst)):
        if lst[i] != '.':
            if lst[i].isdigit() == False:
                return -1
    
    #Checks if the given string is a floating point number or not
    if '.' not in lst:
        return -2      
    
    lst2 = [] 
    for i in range(len(lst)):
        if lst[i] == '.':
            break
        lst2.append(lst[i])
        lst[i] = 0

    lst3 = []
    for i in range(len(lst)):
        if lst[i] == '.' or lst[i] == 0:
            pass
        else:
            lst3.append(lst[i])
            lst[i] = 0

    #252.0 for eg must be given an error by this function as its an integer
    flag = 0
    for i in range(len(lst3)):
        if lst3[i] != '0':
            flag = 1
    if flag == 0:
        return -3

    int_part = 0
    dec_part = 0
    n = len(lst2)
    for i in range(len(lst2)):
        int_part += (10**(n-i-1)*int(lst2[i]))

    for i in range(len(lst3)):
        dec_part += (10**-(i+1))*int(lst3[i])

    int_part_bin = input_validity(10,2,lst2)
    lst_int_bin = []
    for i in int_part_bin:
        lst_int_bin.append(i)
    exp = len(lst_int_bin)-1 #Exponent of the floating point representation
    
    count = 0
    lst_dec_bin = []
    while(dec_part != 1.0):
        if(count == 5):
            break
        if(dec_part >= 1):
            dec_part = dec_part - 1
        dec_part = dec_part*2
        if(dec_part >= 1):
            lst_dec_bin.append('1')
        else:
            lst_dec_bin.append('0')
        count += 1
    
    if((len(lst_dec_bin)+len(lst_int_bin)-1) > 5):
        return -4
    else:
        a = f'{int(exp):03b}'
        lst_float = lst_int_bin[1:] + lst_dec_bin
        string_out = ''
        for i in range(len(lst_float)):
            string_out += lst_float[i]
        for i in range(5-len(lst_float)):
            string_out += '0'
        string_out = a + string_out
        return string_out


reg_values = {
    'R0':0,
    'R1':0,
    'R2':0,
    'R3':0,
    'R4':0,
    'R5':0,
    'R6':0
}

flag_values = {
    'V':'0',
    'L':'0',
    'G':'0',
    'E':'0'
}

ls_inputs = []
while True:
    try:
        str = input()
        ls_inputs.append(str)
    except EOFError:
        break

memory_dump = ls_inputs.copy()
for i in range(256-len(ls_inputs)):
    memory_dump.append('00000000'*2)

halt = False
program_counter = 0
cycle_counter = 0

PClst = [] #Program Counter List
CClst = [] #Cycle Counter List

def output_string(program_counter, reg_values, flag_dict):
    PC = num_to_8bitbinary(program_counter)
    R0 = num_to_16bitbinary(reg_values['R0'])
    R1 = num_to_16bitbinary(reg_values['R1'])
    R2 = num_to_16bitbinary(reg_values['R2'])
    R3 = num_to_16bitbinary(reg_values['R3'])
    R4 = num_to_16bitbinary(reg_values['R4'])
    R5 = num_to_16bitbinary(reg_values['R5'])
    R6 = num_to_16bitbinary(reg_values['R6'])
    FLAG = ('0'*12) + (flag_dict['V']) + (flag_dict['L']) + (flag_dict['G']) + (flag_dict['E'])
    return f'{PC} {R0} {R1} {R2} {R3} {R4} {R5} {R6} {FLAG}'

while(not halt):
    CClst.append(cycle_counter)
    PClst.append(program_counter)
    memory_line = ls_inputs[program_counter]
    opcode = memory_line[:5]
    instf_type = inst_type(opcode)
    instf = inst_name(opcode) 
    if(instf_type == 'A'):
        for (x,y) in list(flag_values.items()):
            flag_values[x] = '0'
        reg1_code = memory_line[7:10]
        reg2_code = memory_line[10:13]
        reg3_code = memory_line[13:16]
        reg3 = reg_decoder[reg3_code]
        value_output = atype_implement(instf, reg1_code, reg2_code, reg_values)
        if instf == 'add' or instf == 'mul':
            if value_output > (2**16)-1 or value_output < 0:
                flag_values['V'] = '1'
                value_output = value_output%(2**16)
                value_to_be_stored = num_to_16bitbinary(value_output)
                reg_values[reg3] = binary_to_dec(value_to_be_stored) 
            else: 
                reg_values[reg3] = value_output
        elif instf == 'sub':
            if value_output > (2**16)-1 or value_output < 0:
                flag_values['V'] = '1'
                reg_values[reg3] = 0
            else:
                reg_values[reg3] = value_output
        else:
            reg_values[reg3] = value_output        
        output = output_string(program_counter, reg_values, flag_values)
        print(output)
        program_counter += 1

    elif(instf_type == 'B'):
        for (x,y) in list(flag_values.items()):
            flag_values[x] = '0'
        reg1_code = memory_line[5:8]
        immediate_str = memory_line[8:16]
        immediate_dec = binary_to_dec(immediate_str)
        value_output = btype_implement(instf, reg1_code, immediate_dec, reg_values)
        reg_values[reg_decoder[reg1_code]] = value_output
        print(output_string(program_counter, reg_values, flag_values))
        program_counter += 1

    elif(instf_type == 'C'):
        reg1_code = memory_line[10:13]
        reg2_code = memory_line[13:16]
        value_output = ctype_implement(instf, reg1_code, reg2_code, reg_values, flag_values)
        if instf == 'not':
            for (x,y) in list(flag_values.items()):
                flag_values[x] = '0'
            reg_values[reg_decoder[reg2_code]] = value_output
        elif instf == 'div':
            for (x,y) in list(flag_values.items()):
                flag_values[x] = '0'
            reg_values['R0'] = value_output[0]
            reg_values['R1'] = value_output[1]
        elif instf == 'movr':
            if reg_decoder[reg1_code] == 'FLAGS':
                dec_value = binary_to_dec(value_output)
                reg_values[reg_decoder[reg2_code]] = dec_value
                for (x,y) in list(flag_values.items()):
                    flag_values[x] = '0'
            else:
                reg_values[reg_decoder[reg2_code]] = value_output
                for (x,y) in list(flag_values.items()):
                    flag_values[x] = '0'
        elif instf == 'cmp':
            for (x,y) in list(flag_values.items()):
                flag_values[x] = '0'
            value_output = ctype_implement(instf, reg1_code, reg2_code, reg_values, flag_values)
        print(output_string(program_counter, reg_values, flag_values))
        program_counter += 1
    elif(instf_type == 'D'):
        for (x,y) in list(flag_values.items()):
            flag_values[x] = '0'
        reg1_code = memory_line[5:8]
        reg1 = reg_decoder[reg1_code]
        memory_add_bin = memory_line[8:16]
        memory_addr = binary_to_dec(memory_add_bin)
        CClst.append(cycle_counter)
        PClst.append(memory_addr)
        if(instf == 'ld'):
            num_at_addr = memory_dump[memory_addr]
            data_to_be_stored = binary_to_dec(num_at_addr)
            reg_values[reg1] = data_to_be_stored
        elif(instf == 'st'):
            value_stored = reg_values[reg1]
            value_pushed = num_to_16bitbinary(value_stored)
            memory_dump[memory_addr] = value_pushed
        print(output_string(program_counter, reg_values, flag_values))
        program_counter += 1
    elif(instf_type == 'E'):
        memory_add_bin = memory_line[8:16]
        memory_addr = binary_to_dec(memory_add_bin)
        if(instf == 'jmp'):
            for (x,y) in list(flag_values.items()):
                flag_values[x] = '0'
            print(output_string(program_counter, reg_values, flag_values))
            program_counter = memory_addr
        elif(instf == 'jlt'):
            if(flag_values['L'] == '1'):
                for (x,y) in list(flag_values.items()):
                    flag_values[x] = '0'
                print(output_string(program_counter, reg_values, flag_values))
                program_counter = memory_addr
            else:
                for (x,y) in list(flag_values.items()):
                    flag_values[x] = '0'
                print(output_string(program_counter, reg_values, flag_values))
                program_counter += 1
        elif(instf == 'jgt'):
            if(flag_values['G'] == '1'):
                for (x,y) in list(flag_values.items()):
                    flag_values[x] = '0'
                print(output_string(program_counter, reg_values, flag_values))
                program_counter = memory_addr
            else:
                for (x,y) in list(flag_values.items()):
                    flag_values[x] = '0'
                print(output_string(program_counter, reg_values, flag_values))
                program_counter += 1
        elif(instf == 'je'):
            if(flag_values['E'] == '1'):
                for (x,y) in list(flag_values.items()):
                    flag_values[x] = '0'
                print(output_string(program_counter, reg_values, flag_values))
                program_counter = memory_addr
            else:
                for (x,y) in list(flag_values.items()):
                    flag_values[x] = '0'
                print(output_string(program_counter, reg_values, flag_values))
                program_counter += 1
    else:
        for (x,y) in list(flag_values.items()):
            flag_values[x] = '0'
        halt = True
        print(output_string(program_counter, reg_values, flag_values))
    cycle_counter += 1

for i in range(len(memory_dump)):
    print(memory_dump[i])

#Q4 - Plot between Memory Address and Cycle Counters
lst_ylabel = range(0, 264, 8)
lst_xlabel = range(0, cycle_counter, 2)
plt.scatter(CClst, PClst, c = 'blue')
plt.yticks(lst_ylabel, fontsize = 4)
plt.xticks(lst_xlabel, fontsize = 4)
plt.xlabel('Cycle Number')
plt.ylabel('Memory Address')
time = datetime.datetime.now()
plt.savefig(f'Plot - {time}.png')