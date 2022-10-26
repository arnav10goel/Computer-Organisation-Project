#Import codes here
import sys
from binaryencoding import *
from general_info import *
from error_checker import *
from sys import stdin

error_counter = [] #This list stores all the error statements which would get printed out.
empty_string = [" "]
#Takes assembly program input from STDIN
assembly_program = []
while True:
    try:
        assembly_line = input()
        assembly_program.append(assembly_line)
    except EOFError:
        break

#Ignores empty lines
assembly_program_final = []
for i in range(len(assembly_program)):
    if (assembly_program[i] == ''):
        pass
    else:
        assembly_program_final.append(assembly_program[i])

if(len(assembly_program_final) == 0):
    print(" ")
else:
    list_of_var_indx = []
    for i in range(len(assembly_program_final)):
        lst_line = [x for x in assembly_program_final[i].strip().split()]
        if (lst_line[0] == "var"):
            list_of_var_indx.append(i)

    for i in list_of_var_indx:
        len_var = len([x for x in assembly_program_final[i].strip().split()])
        if(len_var != 2):
            error_counter.append(f'Error: Type-Var: Illegal Variable Declaration: Expected length 2 but length {len_var} was found on line {i+1}.')

    list_of_instructions = [] #Stores list of instructions
    list_of_labelsdeclared = [] #Stores all declared labels
    list_of_labelsdeclared2 = [] #Stores all declared labels with line number

    for i in range(len(assembly_program_final)):
        lst_line = [x for x in assembly_program_final[i].strip().split()]
        first = lst_line[0]
        if (first[-1] == ":"):
            list_of_labelsdeclared.append(first[:-1])
            list_of_labelsdeclared2.append(tuple([first[:-1],i]))
            if(len(lst_line)>1):
                list_of_instructions.append(lst_line[1:]) 
            else:
                list_of_instructions.append(empty_string) #To prevent indexing problem
                error_counter.append(f'Error: Empty Label Declaration: Only keyword "{first[:-1]}" was found at line {i+1} with no instruction after it.')
        else:
            list_of_instructions.append(lst_line)

    var_count = 0
    for i in range(len(list_of_instructions)):
        first_exp = list_of_instructions[i][0]
        if first_exp == 'var':
            var_count += 1

    if(var_count != 0):
        if(var_count != (list_of_var_indx[-1]+1)):
            error_counter.append(f'Error: Type-Var: All variables are not initialised at the top of the assembly program.')

    for i in range(len(list_of_instructions)): 
        insti = list_of_instructions[i]
        first_exp = insti[0]
        if first_exp not in listofinstructions:
            error_counter.append(f'Error: Invalid Syntax: "{first_exp}"" at line {i+1} is not a recognised instruction as per the ISA')
        else:
            if(first_exp == 'var'):
                pass
            else:
            #Type of Instruction for Error Checking - Takes into account the fact that 'mov' is present in both B and C type instructions.
                if(first_exp == 'mov'):
                    if(len(insti) == 3):
                        if(insti[2][0]=='$'):
                            type_inst = opcodes['movi'][1]
                        else:
                            type_inst = opcodes['movr'][1]
                else:
                    type_inst = opcodes[first_exp][1]

                if(len(insti) != numinputs_instruction[type_inst]):
                    error_counter.append(f'Error: Invalid Syntax: Instruction {first_exp} is of type "{type_inst}" and requires "{numinputs_instruction[type_inst]}" number of arguments but on line {i+1} for this expression {len(insti)} number arguments were detected.')
                
                #For A type instructions
                if(type_inst == 'A'):
                    if(len(insti) == 4):
                        for reg in insti[1:4]:
                            if not register_validity(reg):
                                error_counter.append(f'Error: Invalid Syntax: "{reg}" at line {i+1} is not a valid register.')
                            if reg == 'FLAGS':
                                error_counter.append(f'Error: Illegal Use of Flags: FLAGS Register cannot be used with instruction {first_exp} at line number {i+1}.')
                
                #For B type instructions
                if(type_inst == 'B'):
                    if(len(insti) == 3):
                        if not register_validity(insti[1]):
                            error_counter.append(f'Error: Invalid Syntax: "{insti[1]}" at line {i+1} is not a valid register.')
                        if insti[1] == 'FLAGS':
                            error_counter.append(f'Error: Illegal Use of Flags: FLAGS Register cannot be used with instruction {first_exp} at line number {i+1}.')
                        try:
                            imm = int(insti[2][1:])
                            if not imm_validity(imm):
                                error_counter.append(f'Error: Illegal Immediate: The Immediate at line {i+1} is not of 8 bits i.e. it must lie between 0 and 255.')
                        except:
                            error_counter.append(f'Error: Illegal Immediate: Given immediate at line {i+1} is not an integer type input.')

                if(type_inst == 'C'):
                    if(len(insti) == 3):
                        if(first_exp == 'mov'):
                            if insti[2] == 'FLAGS':
                                error_counter.append(f'Error: Illegal Use of Flags: The only allowed operation with FLAGS register is "mov FLAGS Ri" where i goes from 0 to 6')
                            for reg in insti[1:3]:
                                if not register_validity(reg):
                                    error_counter.append(f'Error: Invalid Syntax: "{reg}" at line {i+1} is not a valid register.')
                        else:
                            for reg in insti[1:3]:
                                if not register_validity(reg):
                                    error_counter.append(f'Error: Invalid Syntax: "{reg}" at line {i+1} is not a valid register.')
                                if reg == 'FLAGS':
                                    error_counter.append(f'Error: Illegal Use of Flags: FLAGS Register cannot be used with instruction {first_exp} at line number {i+1}.')

                if(type_inst == 'D'):
                    if(len(insti) == 3):
                        reg = insti[1]
                        if not register_validity(reg):
                            error_counter.append(f'Error: Invalid Syntax: "{reg}" at line {i+1} is not a valid register.')
                        if reg == 'FLAGS':
                            error_counter.append(f'Error: Illegal Use of Flags: FLAGS Register cannot be used with instruction {first_exp} at line number {i+1}.')

    #Halt Error Detection
    hlt_count = 0
    hlt_index = []
    for i in range(len(list_of_instructions)-1):
        insti = list_of_instructions[i]
        first_exp = insti[0]
        if first_exp == 'hlt':
            hlt_count += 1
            hlt_index.append(i+1)
    if (hlt_count != 0):
        error_counter.append(f'Error: Multiple Halts detected at lines numbered: {hlt_index}')
    if (list_of_instructions[-1][0] != 'hlt'):
        error_counter.append(f'Error: Type: Invalid Syntax: Missing "hlt" instruction at the end of the program.')

    if(len(list_of_var_indx)==0):
        start_count = 0
    else:
        start_count = list_of_var_indx[-1]+1

    instructions_machine = [] #Stores instructions as would be stored in the machine.
    for i in range(start_count, len(assembly_program_final)):
        prog_line = [x for x in assembly_program_final[i].strip().split()]
        instructions_machine.append(prog_line)
    for i in range(start_count):
        prog_line = [x for x in assembly_program_final[i].strip().split()]
        instructions_machine.append(prog_line)

    list_of_labelsdeclared3 = [] #Stores labels declared in Machine Code
    list_of_labelsdeclared4 = [] #Stores labels declared in Machine Code with Line Number
    list_instf = [] #Final instructions in order as they would appear in Machine Code
    for i in range(len(instructions_machine)):
        lst_line = instructions_machine[i]
        first = lst_line[0]
        if (first[-1] == ":"):
            list_of_labelsdeclared3.append(first[:-1])
            list_of_labelsdeclared4.append(tuple([first[:-1],i]))
            if(len(lst_line)>1):
                list_instf.append(lst_line[1:]) 
            else:
                list_instf.append(empty_string) #To prevent indexing problem
        else:
            list_instf.append(lst_line)

    #The following For Loop prepares two lists for variable verification.
    list_of_variables_declared = [] #Names of all variables declared
    list_of_variables_declared2 = [] #Variable names with line number in Machine Code

    for i in range(len(list_instf)):
        lst_line = list_instf[i]
        first = lst_line[0]
        if(first == 'var'):
            if(len(lst_line) == 2):
                list_of_variables_declared.append(lst_line[1])
                list_of_variables_declared2.append(tuple([lst_line[1],i]))

    list_of_variables_called = [] #Stores variables called in Machine Code
    list_of_variables_called2 = [] #Stores variables called in Machine Code with their Line Number

    for i in range(len(list_instf)):
        code_line  = list_instf[i]
        first_exp = code_line[0]
        if(first_exp == "ld" or first_exp == "st"):
            if(len(code_line) == 3):
                list_of_variables_called.append(code_line[2])
                list_of_variables_called2.append(tuple([code_line[2],i+1+var_count]))

    list_of_labels_called = [] #Stores labels called in Machine Code
    list_of_labels_called2 = [] #Stores labels called in Machine Code with Line Number

    for i in range(len(list_instf)):
        code_line  = list_instf[i]
        first_exp = code_line[0]
        if(first_exp == "jmp" or first_exp == "jlt" or first_exp == "jgt" or first_exp == "je"):
            if(len(code_line) == 2):
                list_of_labels_called.append(code_line[1])
                list_of_labels_called2.append(tuple([code_line[1],i]))

    var_checker = varValid(list_of_variables_declared, list_of_variables_called)
    if(var_checker[0] == -1):
        for (x,y) in list_of_variables_declared2:
            if (x == var_checker[1]):
                error_counter.append(f'Error: Type-Var: Variable Name is not alphanumeric at line number {y+1-var_count}')

    if(var_checker[0]==-2):
        for (x,y) in list_of_variables_declared2:
            if (x == var_checker[1]):
                error_counter.append(f'Error: Type-Var: Variable Name is only numeric at line number {y+1-var_count}')

    if(var_checker[0]==-3):
        for (x,y) in list_of_variables_called2:
            if (x == var_checker[1]):
                error_counter.append(f'Error: Type-Illegal Variable Declaration: Variable called at line number {y} is NOT DEFINED')

    if(var_checker[0]==-4):
        for (x,y) in list_of_variables_declared2:
            if (x == var_checker[1]):
                error_counter.append(f'Error: Type-Var: Variable Name at line number {y+1-var_count} is a part of the ISA Syntax and cannot be used as a variable name.')

    if(var_checker[0]==-5):
        for (x,y) in list_of_variables_declared2:
            if (x == var_checker[1]):
                error_counter.append(f'Error: Type-Var: Variable Name at line number {y+1-var_count} has been declared more than once in your program')
                break

    label_checker = labelValid(list_of_labelsdeclared3, list_of_labels_called)
    if(label_checker[0] == -1):
        for (x,y) in list_of_labelsdeclared4:
            if (x == label_checker[1]):
                error_counter.append(f'Error: Type-Label: Label Name is not alphanumeric at line number {y+1+var_count}')

    if(label_checker[0]==-2):
        for (x,y) in list_of_labelsdeclared4:
            if (x == label_checker[1]):
                error_counter.append(f'Error: Type-Label: Label Name is only numeric at line number {y+1+var_count}')

    if(label_checker[0]==-3):
        for (x,y) in list_of_labels_called2:
            if (x == label_checker[1]):
                error_counter.append(f'Error: Type-Illegal Label Declaration: Label called at line number {y+1+var_count} is NOT DEFINED')

    if(label_checker[0]==-4):
        for (x,y) in list_of_labelsdeclared4:
            if (x == label_checker[1]):
                error_counter.append(f'Error: Type-Illegal Label Declaration: Label Name at line number {y+1+var_count} is a part of the ISA Syntax and cannot be used as a variable name.')

    if(label_checker[0]==-5):
        for (x,y) in list_of_labelsdeclared4:
            if (x == label_checker[1]):
                error_counter.append(f'Error: Type-Illegal Label Declaration: Label Name at line number {y+1+var_count} has been declared more than once in your program')
                break

    for (x,y) in list_of_variables_declared2:
        if x in list_of_labelsdeclared3:
            error_counter.append(f'Error: Misuse of Labels and Variables: Variable {x} declared at Line: {y+1-var_count} is already declared as a label name.')
    for (x,y) in list_of_variables_called2:
        if x in list_of_labelsdeclared3:
            error_counter.append(f'Error: Misuse of Labels and Variables: Variable {x} called at Line: {y+1-var_count} is already declared as a label name.')

    #Translation:
    if(len(error_counter) != 0):
        for i in range(len(error_counter)):
            print(error_counter[i])
    else:
        instf = []
        for i in range(len(instructions_machine)-var_count):
            inst = instructions_machine[i]
            if (inst[0][-1] == ":"):
                instf.append(inst[1:])
            else:
                instf.append(inst)
        for i in range(len(instf)):
            output_string = ""
            instruct = instf[i][0]
            if(instruct == 'mov'):
                if(instf[i][2][0]=='$'):
                    instruct = 'movi'
                else:
                    instruct = 'movr'
            type_instruct = opcodes[instruct][1]

            if(type_instruct == 'A'):
                ocode = opcodes[instruct][0]
                unused_bits = "0"*(numunusedbits_instruction[type_instruct])
                output_string = str(str(ocode) + str(unused_bits))
                for i in instf[i][1:]:
                    output_string += register_to_binary(i)

            if(type_instruct == 'B'):
                ocode = opcodes[instruct][0]
                reg = instf[i][1]
                reg_binary = register_to_binary(reg)
                imm = str(immediate_to_binary(instf[i][2][1:]))
                output_string = str(ocode + reg_binary + imm)

            if(type_instruct == 'C'):
                ocode = opcodes[instruct][0]
                unused_bits = "0"*(numunusedbits_instruction[type_instruct])
                output_string = str(str(ocode) + str(unused_bits))
                for i in instf[i][1:]:
                    output_string += register_to_binary(i)

            if(type_instruct == 'D'):
                ocode = opcodes[instruct][0]
                reg_binary = register_to_binary(instf[i][1])
                var_called = instf[i][2]
                location = ""
                for (x,y) in list_of_variables_declared2:
                    if (x==var_called):
                        location = str(memory_address_to_binary(y))
                output_string = str(ocode + reg_binary + location)

            if(type_instruct == 'E'):
                ocode = opcodes[instruct][0]
                unused_bits = "0"*(numunusedbits_instruction[type_instruct])
                output_string = str(str(ocode) + str(unused_bits))
                label_called = instf[i][1]
                location = ""
                for (x,y) in list_of_labelsdeclared4:
                    if (x == label_called):
                        location = str(memory_address_to_binary(y))
                output_string += location

            if(type_instruct == 'F'):
                ocode = opcodes[instruct][0]
                unused_bits = "0"*(numunusedbits_instruction[type_instruct])
                output_string = str(str(ocode) + str(unused_bits))
        
            print(output_string)