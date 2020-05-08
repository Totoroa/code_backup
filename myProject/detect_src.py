'''
detect vulnerabilities based on the parsed project source code.
'''
import os
import json
import bitarray

import produce_slice
import parseutility2 as pu

dpd_file_path = r""  # Path of files that record the dependence relationships of project functions' lines.
function_file_path = r""   # Path of files that store source functions.
vul_json_path = r""   # vul_repo in json format

bitvector_size = 2097152
bitvector = bitarray.bitarray(bloomfilter_size)
bitvector_dic = {}  # record the slice's hashvalue and the line numbers. eg: {1839273: [1,5,7,9,10], 34502394: [6,7,8,10,11,12]}

vul_dic = {}
with open(vul_json_path, 'r') as ff:
    vul_dic = json.load(ff)

def report(src_file_name, src_lines, vul_file_name):
    # TODO
    #if src_lines == 0, means all function lines should be considered.
    return

for files in os.listdir(function_file_path):
    # first, get the abstracted/normalized func_Body, to detect if the hashvalue of the func_Body is vulnerability. 
    temp = produce_slice.procude_funcBody_hash(os.path.join(function_file_path, files))
    hash_value = temp[0]
    for vulfunc_file_name, record in vul_dic.items():
        if record['hashvalue'][0] == hash_value:
            print files, "   Bingo !"
            report(os.path.join(function_file_path, files), 0, vulfunc_file_name)
            break
    
    # if the func_Body is "not" vulnerablity, then produce slices for current function. 
    # Build a bitvector for current function, 
    else: #if 'break' executed, the else will no be executed.
        dpd_content = ""  #dpd means dependence
        func_content = []
        if not os.path.exists(os.path.join(dpd_file_path, files)):
            continue
        with open(os.path.join(dpd_file_path, files), 'r') as ff:
            temp = ff.readlines()
            dpd_content = "".join("".join(temp).split('\n'))
        dpd_dic = produce_slice.slice_from_project(dpd_content)
        
        with open(os.path.join(function_file_path, files), 'r') as ff:
            func_content = ff.readlines()
        
        # build a bitvector according to dpd_dic
        bitvector.setall(0)
        for line_num, line_dpd in dpd_dic.items():
            slice_content = produce_slice.get_slice_content(func_content, line_dpd)
            slice_content = pu.normalize(slice_content)
            slice_hash = produce_slice.fnv1a_hash(slice_content)
            bitvector[slice_hash] = 1
            bitvector_dic[slice_hash] = line_dpd
            
        #detect the vul_slice according the bitvector
        for vul_filename, records in vul_dic.items():
            if len(records['hashvalue']) == 1:
                continue
            flag = True
            matched_hash = []
            for n in records['hashvalue'][1:]:
                if bitvector[n] == 1:
                    matched_hash.append(n)
                else:
                    flag == False
                if flag == False:
                    matched_hash = []
                    break
            if flag:
                print files, "    Bingo !"
                line_list = []
                for i in matched_hash:
                    line_list.extend(bitvector_dic[i])
                line_list = list(set(line_list))
                line_list.sort()
                report(os.path.join(function_file_path, files), line_list, vul_filename)
                break
                