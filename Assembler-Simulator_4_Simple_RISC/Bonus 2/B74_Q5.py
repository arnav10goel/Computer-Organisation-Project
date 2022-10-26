from math import *
print("*-*-*-*-*-Welcome to Memory Mumbo Jumbo-*-*-*-*-*-*-*-*-*-*")
mem_dict = {
    1: 1,
    2: 4,
    3: 8,
    4: 32
}
print("What is the space in your memory? (GB/KB/MB/Gb/Mb/Kb)")
memory_space = list(input().split())
# mem_num = log(int(memory_space[0]),2)
# print(mem_num)
print("1. Bit Addressable Memory")
print("2. Nibble Addressable Memory")
print("3. Byte Addressable Memory")
print("4. Word Addressable Memory")
print("How is your memory addressed? Choose between (1/2/3/4)")
mem_type = int(input())
qtype = int(input("What type of Question is it? (1/2) "))
mem_num = int(memory_space[0])
mem_denonym = memory_space[1][0].lower()
if mem_denonym == 'g':
    mem_num = mem_num*(2**30)
elif mem_denonym == 'm':
    mem_num = mem_num*(2**20)
elif mem_denonym == 'k':
    mem_num = mem_num*(2**10)

if memory_space[1][1] == 'B':
    mem_num = mem_num*8
if qtype == 1:
    instruct_len = int(input("What is the length of your instruction? "))
    reg_len = int(input("What is the length of your register? "))
    res = log(int(mem_num/mem_dict[mem_type]),2)
    if res - int(res) == 0:
        answer_a = int(res) 
    else:
        answer_a = int(res)+1
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("No of Bits needed to represent an address in this architecture is:") 
    print(answer_a)
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")  
    print("Number of bits needed by Opcode are: ")
    bits_opcode = instruct_len - reg_len - answer_a
    print(bits_opcode)
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("Number of filler bits in instruction type 2 are: ")
    filler_bit_two = answer_a - reg_len
    print(filler_bit_two)
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("Maximum number of instructions this ISA can support are: ")
    print(2**bits_opcode)
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("Maximum number of registers this ISA can support are: ")
    print(2**reg_len)
else:
    print("What type of Question in Q2 is it? (1/2)")
    qtype_2 = int(input())
    if qtype_2 == 1:
        print("How many bits CPU it is? ")
        CPU_bit = int(input())
        print("1. Bit Addressable Memory")
        print("2. Nibble Addressable Memory")
        print("3. Byte Addressable Memory")
        print("4. Word Addressable Memory")
        print("What is your memory enhanced to? Choose between (1/2/3/4)")
        mem_type_two = int(input())

        initial_pins = int(log(int(mem_num/mem_dict[mem_type]),2))+1
        if mem_type_two == 4:
            final_pins = int(log(int(mem_num/CPU_bit),2))+1
        else:
            final_pins = int(log(int(mem_num/mem_dict[mem_type_two]),2))+1

        pins_diff = final_pins - initial_pins
        if pins_diff < 0:
            print(pins_diff)
            print(f'{pins_diff} are saved.')
        else:
            print(pins_diff)
            print(f'{pins_diff} are needed more.')
    else:
        print("How many bits CPU it is? ")
        CPU_bit = int(input())
        print("How many address pins there are? ")
        num_addr_pins = int(input())
        print("1. Bit Addressable Memory")
        print("2. Nibble Addressable Memory")
        print("3. Byte Addressable Memory")
        print("4. Word Addressable Memory")
        print("How is your memory addressed? Choose between (1/2/3/4)")
        mem_type_final = int(input())
        val_needed = 0
        if mem_type_final != 4:
            val_needed = mem_dict[mem_type_final]/8
        else:
            val_needed = CPU_bit/8
        res = log(int((2**num_addr_pins)*val_needed),2)
        if res < 10:
            print(f'{res} Bytes')
        elif res >= 10 and res < 20:
            new = res - 10
            print(f'{2**new} KB')
        elif res >= 20 and res < 30:
            new = res - 20
            print(f'{2**new} MB')
        elif res >= 30:
            new = res - 30
            print(f'{2**new} GB')