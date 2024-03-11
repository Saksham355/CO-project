import sys
import re
def bin_i(num,l):
    if num < 0:
        binary_repr = bin(num & 0xFFF)[3:]
        while len(binary_repr) < l:
            binary_repr = '1' + binary_repr
    
        return binary_repr
    else:
        binary_repr = bin(num)[2:]

        while len(binary_repr) < l:
            binary_repr = '0' + binary_repr
    
        return binary_repr
def reg(r):
    add = int(r[1::1])
    return bin_i(add,5)

input_path=sys.argv[1]
out_path = sys.argv[2]
with open(input_path,'r') as f:
    assemb = []
    for i in f:
        if i != " ":
            assemb.append(i)
result = []
class r_type:
    def __init__(self, func7, func3):
        self.opcode = "0110011"
        self.func3 = func3
        self.func7 = func7

class i_type:
    def __init__(self, opcode, func3):
        self.func3 = func3
        self.opcode = opcode

class s_type:
    def __init__(self, opcode, func3):
        self.func3 = func3
        self.opcode = opcode

class b_type:
    def __init__(self, func3, opcode):
        self.func3 = func3
        self.opcode = opcode

class u_type:
    def __init__(self, opcode):
        self.opcode = opcode

class j_type:
    def __init__(self, opcode):
        self.opcode = opcode

r_dict = {
    "add": r_type("0000000", "000"),
    "sub": r_type("0100000", "000"),
    "sll": r_type("0000000", "001"),
    "slt": r_type("0000000", "010"),
    "sltu": r_type("0000000", "011"),
    "xor": r_type("0000000", "100"),
    "srl": r_type("0000000", "101"),
    "or": r_type("0000000", "110"),
    "and": r_type("0000000", "111")    
}

i_dict = {
    "lw": i_type("0000011", "010"),
    "addi": i_type("0010011", "000"),
    "sltiu": i_type("0010011", "011"),
    "jalr": i_type("1100111", "000")
}

s_dict = {
    "sw": s_type("0100011", "010")
}

b_dict = {
    "beq": b_type("000", "1100011"),
    "bne": b_type("001", "1100011"),
    "blt": b_type("100", "1100011"),
    "bge": b_type("101", "1100011"),
    "bltu": b_type("110", "1100011"),
    "bgeu": b_type("111", "1100011")
}

u_dict = {
    "lui": u_type("0110111"),
    "auipc": u_type("0010111")
}

j_dict = {
    "jal": j_type("1101111")
}

ins_dict = {
    'add': 'r',
    'sub': 'r',
    'sll': 'r',
    'slt': 'r',
    'sltu': 'r',
    'xor': 'r',
    'srl': 'r',
    'or': 'r',
    'and': 'r',
    'lw': 'i',
    'addi': 'i',
    'sltiu': 'i',
    'jalr': 'i',
    'sw': 's',
    'beq': 'b',
    'bne': 'b',
    'blt': 'b',
    'bge': 'b',
    'bltu': 'b',
    'bgeu': 'b',
    'lui': 'u',
    'auipc': 'u',
    'jal': 'j'
}
reg_dict = abi_registers = {
    "zero": "x0",
    "ra": "x1",
    "sp": "x2",
    "gp": "x3",
    "tp": "x4",
    "t0": "x5",
    "t1": "x6",
    "t2": "x7",
    "s0": "x8",
    "fp": "x8",
    "s1": "x9",
    "a0": "x10",
    "a1": "x11",
    "a2": "x12",
    "a3": "x13",
    "a4": "x14",
    "a5": "x15",
    "a6": "x16",
    "a7": "x17",
    "s2": "x18",
    "s3": "x19",
    "s4": "x20",
    "s5": "x21",
    "s6": "x22",
    "s7": "x23",
    "s8": "x24",
    "s9": "x25",
    "s10": "x26",
    "s11": "x27",
    "t3": "x28",
    "t4": "x29",
    "t5": "x30",
    "t6": "x31",
    
}
ins_list = ins_dict.keys()
reg_list = reg_dict.keys()
pcounter = 0
halt = False
if(assemb[-1].strip()!="beq zero,zero,0"):
     if halt == False:
          result.append("No virtual Halt at end")
else:

    for s in assemb:
        if s == " ":
            pcounter +=1
            
            continue
        if ':' in s:
            pcounter +=1
            s = s.split(": ")
            s = s[1]
        else:
            pcounter +=1
            s = s.strip()
        c_split = s.split(" ")
        ins = c_split[0]
        if(s == "beq zero,zero,0" and pcounter != len(assemb)):
            halt = True
            result.append("Virtual Halt Error at: "+ str(pcounter))
            break
        if(ins not in ins_list):
            result.append("Error at line: "+ str(pcounter)+" instruction type not supported")
            break
        type = ins_dict[ins]
        #r
        if (type == 'r'):
            memory = c_split[1]    
            memory = memory.split(",")
            code = r_dict[ins]
            if(memory[2].strip() not in reg_list or memory[1] not in reg_list or memory[0] not in reg_list):
                result.append("Error at line: "+ str(pcounter)+" register not found")
                break
            rs2 = reg(reg_dict[memory[2].strip()])
            rs1 = reg(reg_dict[memory[1]])
            rd = reg(reg_dict[memory[0]])
            result.append(code.func7+rs2+rs1+code.func3+rd+code.opcode)
            
            
        #i  jalr ra,a5,-07
        elif(type== 'i'):
            memory = c_split[1]
            if'(' in memory:

                memory = memory[:len(memory)-1:]
                memory = memory.split(',')
                memory.append( memory[1].split("(")[0])
                memory[1] = memory[1].split("(")[1]
                if(-2**11>int(memory[2].strip()) or int(memory[2].strip())>(2**11)-1):
                    result.append("Error at line: "+ str(pcounter)+" immidiate length out of bound")
                    break
                imm = bin_i(int(memory[2].strip()),12)
                if(memory[1] not in reg_list or memory[0] not in reg_list):
                    result.append("Error at line:"+str(pcounter)+" register not found")
                    break
                rr = reg(reg_dict[memory[1]])
                rs1 = reg(reg_dict[memory[0]])
                code = i_dict[ins]
                binary = imm+rr+code.func3+rs1+code.opcode

                result.append(binary)
            else:
                memory = memory.split(",")
                if(-2**11>int(memory[2].strip()) or int(memory[2].strip())>(2**11)-1):
                    result.append("Error at line: "+str(pcounter)+" immidiate length out of bound")
                    break
                imm = bin_i(int(memory[2].strip()),12)
                if(memory[1] not in reg_list or memory[0] not in reg_list):
                    result.append("Error at line: "+str(pcounter)+" register not found")
                    break
                rr = reg(reg_dict[memory[1]])
                rs1 = reg(reg_dict[memory[0]])
                code = i_dict[ins]
                binary = imm+rr+code.func3+rs1+code.opcode
                result.append(binary)
        elif(type== 's'):
            memory = c_split[1]
            memory = memory[:len(memory)-1:]
            memory = memory.split(',')
            memory.append( memory[1].split("(")[0])
            memory[1] = memory[1].split("(")[1]
            if(-2**11>int(memory[2].strip()) or int(memory[2].strip())>(2**11)-1):
                    result.append("Error at line: "+str(pcounter)+" immidiate length out of bound")
                    break
            imm = bin_i(int(memory[2]),12)
            imm1 = imm[0:7:1]
            imm2 = imm[7::1]

            code = s_dict[ins]
            if(memory[1] not in reg_list or memory[0] not in reg_list):
                    result.append("Error at line: "+str(pcounter)+" register not found")
                    break
            binary = imm1 + reg(reg_dict[memory[0]]) +reg(reg_dict[memory[1]])+ code.func3 + imm2 +code.opcode
            result.append(binary)
            
        elif(type == 'b'):
            memory = c_split[1]
            memory = memory.split(",")
            label = memory[2].strip()
            label_c = 0
            for l in assemb:
                l=l.split(':')
                if l[0]==label:
                    break
                else:
                    label_c+=1
            if label_c>=len(assemb):
                label = int(memory[2])
            else:
                label = (label_c-pcounter)*4
            if(-2**11>label or label>(2**11)-1):
                    result.append("Error at line: "+str(pcounter)+" label length out of bound")
                    break
            imm = bin_i(label,12)
            imm1 = imm[0:7:1]
            imm2 = imm[7:12:1]
            if(memory[1] not in reg_list or memory[0] not in reg_list):
                    result.append("Error at line: "+str(pcounter)+" register not found")
                    break
            rs1= reg(reg_dict[memory[1]])
            rs2= reg(reg_dict[memory[0]])
            code = b_dict[ins]
            binary = imm1 +rs1+rs2+code.func3+imm2+code.opcode
            result.append(binary)
        elif(type == 'u'):
            memory = c_split[1]
            memory = memory.split(",")
            if(-2**19>int(memory[1]) or int(memory[1])>(2**19)-1):
                    result.append("Error at line: "+str(pcounter)+" immidiate length out of bound")
                    break
            imm = bin_i(int(memory[1].strip()),32)
            imm1 = imm[0:20:1]
            if(memory[0] not in reg_list):
                    result.append("Error at line: "+str(pcounter)+" register not found")
                    break
            rs1= reg(reg_dict[memory[0]])
            code = u_dict[ins]
            binary = imm1 +rs1+code.opcode
            result.append(binary)
        elif(type == 'j'):
            memory = c_split[1]
            if'(' in memory:

                memory = memory[:len(memory)-1:]
                memory = memory.split(',')
                memory.append( memory[1].split("(")[0])
                memory[1] = memory[1].split("(")[1]
            else:
                memory = memory.split(",")
            if(-2**19>int(memory[1].strip()) or int(memory[1].strip())>(2**19)-1):
                    result.append("Error at line: "+str(pcounter)+" immidiate length out of bound")
                    break
            imm = bin_i(int(memory[1].strip()),20)
            imm1 = imm[8:19:1]
            if(memory[0] not in reg_list):
                    result.append("Error at line: "+str(pcounter)+" register not found")
                    break
            rs1= reg(reg_dict[memory[0]])
            code = j_dict[ins]
            imm2 = imm[0:9:1]
            binary = imm1+imm2+rs1+code.opcode
            result.append(binary)          
s = open(out_path, 'w') 
for i in range(len(result)-1):
    res = result.pop(0)
    if res.strip():  
        s.write(res + '\n')
s.write(result.pop(0))
s.close()
