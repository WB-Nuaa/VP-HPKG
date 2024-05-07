from enum import Enum
from operator import length_hint
import re
from turtle import dot
from get_source_des import GET_IN_OUT
import numpy as np
import os

path1 = os.path.dirname(os.path.abspath(__file__))
#边的类型
class Edge(Enum):
#control：
    control = 1
#data：
    data = 2
#call：
    fun_call = 3
#access：
    load_store = 4
#jump
    jump = 5

ins_list = ['alloca','store','load','call','br','ret','icmp','add','sub','bitcast', 'getelementptr', 'srem', 'sext', 'mul', 'select', 'phi','trunc','ashr','zext','and'] 

ins_width = {'alloca': 64, 'store':32, 'load':32, 'call':64, 'br': 1, 'ret': 32, 'icmp': 1, 'add': 32, 'sub': 32, 'bitcast': 64, 'getelementptr': 64, 'srem': 32, 'sext': 64, 'mul': 64, 'select':32, 'phi': 32, 'trunc':8, 'ashr':64, 'zext':64,'and':64}


#
Ins_type = {'ret': 'terminator', 'br': 'terminator', 'switch': 'terminator', 'indirectbr': 'terminator', 'invoke': 'terminator', 'resume': 'terminator', 'unreachable': 'terminator', 'cleanupret': 'terminator', 'catchret': 'terminator', 'catchswitch': 'terminator', 'call': 'terminator', 'add': 'int_binary', 'sub': 'int_binary', 'mul': 'int_binary', 'udiv': 'int_binary', 'sdiv': 'int_binary', 'urem': 'int_binary', 'srem': 'int_binary', 'fadd': 'float_binary', 'fsub': 'float_binary', 'fmul': 'float_binary', 'fdiv': 'float_binary', 'frem': 'float_binary', 'shl': 'logic', 'lshr': 'logic', 'ashr': 'logic', 'and': 'logic', 'or': 'logic', 'xor': 'logic', 'alloca': 'Memory', 'load': 'Memory', 'store': 'Memory', 'getelementptr': 'Memory', 'fence': 'Memory', 'trunc': 'cast_op', 'zext': 'cast_op', 'sext': 'cast_op', 'fptout': 'cast_op', 'ptrtoint': 'cast_op', 'inttoptr': 'cast_op', 'bitcast': 'cast_op', 'addrspacecast': 'cast_op', 'icmp': 'compare', 'fcmp': 'compare', 'phi': 'other', 'select': 'other', 'vaarg': 'other'}

fun_name = "" 
str2 = "BB" 

def not_empty(s):
    return s and s.strip()


dict_SDC = {}
with open(path1+"\\F_B_I.dot","r") as f:
    for line in f:
        elem = list(filter(not_empty,re.split("\n|\$",line)))
        dict_SDC[elem[0]] = elem[1]


def get_Ins_SDC(filename1 , filename2):    
    Ins_SDC = np.loadtxt(filename1, skiprows=1, dtype=str)
    Ins_other = np.loadtxt(filename2, skiprows=1, dtype=str)
    part_SDC = {}
    for i in range(Ins_SDC.shape[0]):
        if Ins_SDC[i][1] not in part_SDC.keys():
            temp = [0]*3
            temp[0] = int(Ins_SDC[i][3])
            temp[1] = int(Ins_SDC[i][3])
            temp[2] = int(Ins_SDC[i][4])
            part_SDC[Ins_SDC[i][1]] = temp
        else:
            part_SDC[Ins_SDC[i][1]][1] += int(Ins_SDC[i][3])
            part_SDC[Ins_SDC[i][1]][2] += int(Ins_SDC[i][4])
    for i in range(Ins_other.shape[0]):
        if Ins_other[i][1] not in part_SDC.keys():
            temp = [0]*3
            temp[0] = int(Ins_other[i][3])
            temp[1] = int(Ins_other[i][3])
            temp[2] = int(Ins_other[i][4])
            part_SDC[Ins_other[i][1]] = temp
        else:
            part_SDC[Ins_other[i][1]][1] += int(Ins_other[i][3])
            part_SDC[Ins_other[i][1]][2] += int(Ins_other[i][4])
    part_Ins_SDC = {} 
    keys = list(part_SDC.keys())
    for i in range(len(keys)):
        temp = [0]*2
        temp[0] = part_SDC[keys[i]][0]
        temp[1] = round((part_SDC[keys[i]][2] / part_SDC[keys[i]][1]), 4)
        part_Ins_SDC[keys[i]] = temp
    SDC = {}
    SDC_flag = {}
    keys = list(part_Ins_SDC.keys())
    for i in range(len(keys)):
        if dict_SDC[keys[i]] not in SDC.keys():
            SDC[dict_SDC[keys[i]]] = part_Ins_SDC[keys[i]]
            SDC_flag[dict_SDC[keys[i]]] = 1
        else:
            SDC[dict_SDC[keys[i]]][1] += part_Ins_SDC[keys[i]][1]
            SDC_flag[dict_SDC[keys[i]]] += 1
    keys = list(SDC_flag.keys())
    for i in range(len(keys)):
        if SDC_flag[keys[i]] > 1:
            SDC[keys[i]][1] = round(SDC[keys[i]][1]/SDC_flag[keys[i]], 4)
    return SDC

filename1 = path1+'\\cycle_result.txt'
filename2 = path1+"\\result_other.txt"

Ins_SDC = get_Ins_SDC(filename1, filename2)
BB_filename = path1+ "\\BB.dot"

dict_BB = {} #'BB0': [13, 0, 1],
BB_edge = [] #['BB0', 'BB1'], ['BB4', 'BB1'],

def get_BB(filename):
    with open(filename,"r") as f:
        for line in f:
            elem = list(filter(not_empty,re.split("\n| ",line)))
            if "BB" in elem[0]:
                str2 = list(filter(not_empty,re.split("BB", elem[0])))
                dict_BB[str2[0]] = []
                curbb = str2[0]
                pred = 0
                succ = 0
                dict_BB[curbb].append(int(elem[1])) 
            elif elem[0] == "pred:": 
                for i in range(1,len(elem)): 
                    edge = []
                    edge.append(elem[i])
                    edge.append(curbb)
                    BB_edge.append(edge)
                    pred += 1
                dict_BB[curbb].append(pred)
            elif elem[0] == "succ:": 
                for i in range(1, len(elem)):
                    edge = []
                    edge.append(curbb)
                    edge.append(elem[i])
                    BB_edge.append(edge)
                    succ += 1
                dict_BB[curbb].append(succ)
            elif elem[0] == "funcall":
                for i in range(1, len(elem)):
                    lines = list(filter(not_empty, re.split("->", elem[i])))
                    edge = []
                    edge.append(lines[0])
                    edge.append(lines[1])
                    BB_edge.append(edge)
                    
                    
get_BB(BB_filename)



def get_index(s):
    for i in range(len(ins_list)):
        if s == ins_list[i]:
            return i


dict_Ins = {}   
dict_edge = []  

node_feature = {}

ins_num = 0
relationship = 0
flow_flag = 0

def get_key(value):
    keys = list(dict_Ins.keys())
    values = list(dict_Ins.values())
    for i in range(len(values)):
        if value == values[i]:
            return i
    return -1

alloca_load  = ['alloca','load']

with open (path1+"\\Ins_g.dot","r") as f:
    for line in f:
        elem = list(filter(not_empty,re.split("->|\n|{|\"|;",line)))
        first = list(filter(None,re.split("_| ",elem[0])))

        if len(first) == 3 and first[1] == 'cluster' and str2 not in first[2]:
            fun_name = first[2]

        elif first[0] == 'label' and str2 in first[2]:
            bb_name =  first[2]

        elif elem[0] == "dataflow":
            flow_flag = 2
            continue
        elif elem[0] == "controlflow":
            flow_flag = 1
            continue
        elif elem[0] == "bb_call":
            flow_flag = 5
        elif elem[0] == "fun_call":
            flow_flag = 3
        elif len(elem) >= 2 or ("ret" in elem[0]):
            temp = []
            rel = [] 
            rel.append(flow_flag)
            relationship = flow_flag

            for i in range(0,len(elem)):
                features = [0]*8
                features[6] = fun_name
                features[5] = bb_name
                features[7] = -1
                in_out = []
                elem1 = list(filter(not_empty,re.split(",|[ ]+",elem[i])))

                if (len(elem1) > 3 and elem1[3] in ins_list):
                    features[4] = Ins_type[elem1[3]]
                    features[0] = ins_width[elem1[3]]
                    input, output = GET_IN_OUT(elem1[3],elem[i]).get_input_output()
                    features[3] = len(input) + len(output)
                    index = get_index(elem1[3])
                    Ins_index = get_key(elem[i])
                    if Ins_index == -1:
                        str1 = str(ins_num)
                        ins_num = ins_num + 1
                        dict_Ins[str1] = elem[i]
                        node_feature[str1] = features
                    else:
                        str1 = list(dict_Ins.keys())[Ins_index]
                    temp.append(str1)
                    if ins_list[index] in alloca_load and flow_flag == 2 and len(temp) == 1:
                        rel.append(4)
                        relationship = 4
                elif (len(elem1) >= 3 and elem1[1] in ins_list):
                    features[4] = Ins_type[elem1[1]]
                    features[0] = ins_width[elem1[1]]

                    input, output = GET_IN_OUT(elem1[1],elem[i]).get_input_output()
                    features[3] = len(input) + len(output)
                    index = get_index(elem1[1])
                    Ins_index = get_key(elem[i])
                    if Ins_index == -1:
                        str1 = str(ins_num)
                        ins_num = ins_num + 1
                        dict_Ins[str1] = elem[i]
                        node_feature[str1] = features
                    else:
                        str1 = list(dict_Ins.keys())[Ins_index]
                    temp.append(str1)
                    if ins_list[index] in alloca_load and flow_flag == 2 and len(temp) == 1:
                        rel.append(4)
                        relationship = 4
            if len(temp) == 2:
                for i in range(len(rel)):
                    flag = []
                    flag.append(temp[0])
                    flag.append(temp[1])
                    flag.insert(1,rel[i])
                    dict_edge.append(flag)



def pre_suc():
    pre = 0 
    suc = 0 
    for i in range(len(dict_edge)):
        #print(dict_edge[i])
        node_feature[dict_edge[i][0]][2] += 1 
        node_feature[dict_edge[i][2]][1] += 1 

def get_node():
    return dict_Ins

def get_edge():
    return dict_edge


def get_features():
    pre_suc()
    keys = list(Ins_SDC.keys())
    ins_keys = list(dict_Ins.keys())
    ins_value = list(dict_Ins.values())
    for i in range(len(keys)):
        index = ins_value.index(keys[i])
        node_feature[ins_keys[index]][0] = Ins_SDC[keys[i]][0]
        node_feature[ins_keys[index]][7] = Ins_SDC[keys[i]][1]
    keys = list(node_feature.keys())


    return node_feature

def get_BB_info():
    return dict_BB, BB_edge


if __name__ == '__main__':
    edge = get_edge()
    print(len(edge))
    features = get_features()
    print(get_node())
    #print(get_edge())
    print(features)
    #for node, feature in features.items():