import sys
def hexa(decim):
    start = 0x00010000
    offset = 4 
    hex_value = start + (decim * offset)
    return format(hex_value,'08x')
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

def convert_bin(num):
    return "0b"+bin_i(num,32)

def decimal(binary):
    length = len(binary)
    if binary[0] == '1':
        binary = ''.join('1' if bit == '0' else '0' for bit in binary)
        decimal = -1 * ((int(binary, 2) + 1) % (1 << length))  
    else:
        decimal = int(binary, 2)  
    return decimal
def unsigned(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return decimal
opcode = {
    "0110011":"r",
    "0000011":"i",
    "0010011":"i",
    "1100111":"i",
    "0100011":"s",
    "1100011":"b",
    "0110111":"u",
    "0010111":"u",
    "1101111":"j"
}
i_func3 = {
    "010": "lw",
    '000':'addi',
    "011": "sltiu",
    "000": "jalr"
}
b_func3 = {
    "000": "beq",
    "001": "bne",
    "100": "blt",
    "101": "bge",
    "110": "bltu",
    "111": "bgeu"
}
r_func3 = {
    "001": "sll",
    "010": "slt",
    "011": "sltu",
    "100": "xor",
    "101": "srl",
    "110": "or",
    "111": "and"
}
regist = {
    '00000': 0, '00001': 0, '00010': 256, '00011': 0, '00100': 0,
    '00101': 0, '00110': 0, '00111': 0, '01000': 0, '01001': 0,
    '01010': 0, '01011': 0, '01100': 0, '01101': 0, '01110': 0,
    '01111': 0, '10000': 0, '10001': 0, '10010': 0, '10011': 0,
    '10100': 0, '10101': 0, '10110': 0, '10111': 0, '11000': 0,
    '11001': 0, '11010': 0, '11011': 0, '11100': 0, '11101': 0,
    '11110': 0, '11111': 0
}
input_file= sys.argv[1]
with open(input_file,'r') as s:
    program_memory = []
    for l in s:
        program_memory.append(l)        
data_memory=[0 for i in range(32)]

pc=0
with open(sys.argv[2],'w') as s:
    while(pc//4 < len(program_memory)):
        b = False
        l = program_memory[pc//4].strip()
        op = l[-7::1]
        inst_type = opcode[op]
        if(l=="00000000000000000000000001100011"):
            line=""
            for i in regist:
                    line = line+convert_bin(regist[i])+" "
            line=convert_bin(pc)+" "+line.strip()
            s.write(line+"\n")
            break

        if(inst_type == 'r'):
            pc+=4
            func_3 = l[-15:-12:1]
            if(func_3=="000"):
                func_7 = l[0:8:1]
                if(func_7=="00000000"):
                    inst = "add"
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    regist[rd] = regist[r1]+regist[r2] 
                else:
                    inst = "sub"
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    regist[rd] = regist[r1]-regist[r2]
                
            else:
                inst = r_func3[func_3]
                if inst == "slt":
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    if regist[r1]<regist[r2]:
                        regist[rd] = 1
                
                        
                elif inst == "sltu":
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    r1_binary = bin_i(r1,5)
                    r2_binary = bin_i(r2,5)
                    r1_unsigned = unsigned(r1_binary)
                    r2_unsigned = unsigned(r2_binary)
                    if r1_unsigned < r2_unsigned:
                        regist[rd] = 1
                    
                elif inst == "xor":
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    regist[rd] = regist[r1] ^ regist[r2]
                    
                elif inst == "and":
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    regist[rd] = regist[r1] & regist[r2]
                
                elif inst == "or":
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    regist[rd] = regist[r1] | regist[r2]
                
                elif inst == "sll":
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    shift = regist[r2] & 0b11111
                    regist[rd] = regist[r1] << shift
                
                elif inst == "srl":
                    rd = l[-12:-7:1]
                    r1 = l[-20:-15:1]
                    r2 = l[-25:-20:1]
                    shift = regist[r2] & 0b11111
                    regist[rd] = regist[r1] >> shift        
                 
        elif(inst_type=="b"):
            func_3=l[17:20]
            reg2=l[7:12]
            reg1=l[12:17]
            imm=decimal(l[0]+l[-8]+l[1:7]+l[-12:-8]+"0")
            if(b_func3[func_3]=="beq"):
                if(regist[reg1]==regist[reg2]):
                    pc+=imm
                else:
                    pc+=4
            elif(b_func3[func_3]=="bne"):
                if(regist[reg1]!=regist[reg2]):
                    pc+=imm
                else:
                    pc+=4  
            elif(b_func3[func_3]=="bge"):
                if(regist[reg1]>=regist[reg2]):
                    pc+=imm
                else:
                    pc+=4
            elif(b_func3[func_3]=="bgeu"):
                r1=bin_i(regist[reg1],12)
                r2=bin_i(regist[reg2],12)
                if(unsigned(r1)>=unsigned(r2)):
                    pc+=imm
                else:
                    pc+=4   
            elif(b_func3[func_3]=="blt"):
                if(regist[reg1]<regist[reg2]):
                    pc+=imm
                else:
                    pc+=4    
            elif(b_func3[func_3]=="bltu"):
                r1=bin_i(regist[reg1],12)
                r2=bin_i(regist[reg2],12)
                if(unsigned(r1)<unsigned(r2)):
                    pc+=imm
                else:
                    pc+=4   
        elif(inst_type == 'j'):
            rd = l[-12:-7:1]
            regist[rd] = pc+4
            immi = imm=l[0]+l[12:20]+l[11]+l[1:11]+"0"
            pc = pc+decimal(immi)
            pc=bin_i(pc,32)
            pc=pc[0:31]+'0'
            pc=decimal(pc)
            
        elif(inst_type=='i'):
            imm=l[0:12:1]
            rs1=l[12:17:1]
            func_3=l[17:20:1]
            rd=l[20:25:1]
            if(i_func3[func_3]=="lw"):
                pc+=4
                regist[rd]=data_memory[regist[rs1]+decimal(imm)-65536]
            elif(func_3=="000" and op=="0010011"):
                pc+=4
                regist[rd]=regist[rs1]+decimal(imm)
            elif(i_func3[func_3]=="sltiu"):
                pc+=4
                rs1_num=unsigned(rs1)
                imm_num=unsigned(imm)
                if(rs1_num<imm_num):
                    regist[rd]=1
            elif(func_3=="000" and op=="1100111"):
                if(rd=='00000'):
                    regist[rd]=0
                else:
                    regist[rd]=pc+4
                pc=regist[rs1]+decimal(imm)
                pc=bin_i(pc,32)
                pc=pc[0:31]+'0'
                pc=decimal(pc)
            
        elif(inst_type == 's'):
            pc+=4
            imm1 = l[0:7:1]
            imm2 = l[-12:-7:1]
            imm = imm1+imm2
            num = decimal(imm)
            rs1_num = regist[l[7:12:1]]
            tot_ind = rs1_num
            data_memory[(regist[l[12:17:1]]-65536+num)//4]=tot_ind
        
        if(inst_type=='u'):
            pc+=4
            imm = l[0:20]+"000000000000"
            
            if(op == "0110111"):
                regist[l[-12:-7:1]] = decimal(imm)   
            elif(op =="0010111" ):
                        regist[l[-12:-7:1]]=pc-4+decimal(imm)
        line=""
        for i in regist:
                line = line+convert_bin(regist[i])+" "
        if b == False:
            line=convert_bin(pc)+" "+line.strip()
        else:
            line = convert_bin(temp)+" "+line.strip()
        s.write(line+"\n")
    for i in range(len(data_memory)):
            lin2 = ""
            lin2 = lin2+ '0x'+(hexa(i)) + ':' + convert_bin(data_memory[i])
            s.write(lin2+'\n')
