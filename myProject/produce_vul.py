'''
produce vulnerability slice.
'''
import os
import json
import sys
import datetime

import produce_slice
import parseutility2 as pu

vul_func_path = r"F:\data\self_vul_repo\functions\Bad"
vul_func_lines = r"F:\data\self_vul_repo\func_lines"

#bloomfilter_size = 2097152
#bitarray.bitarray(common.bloomfilter_size)

written = {}

total = 0
for root, dirs, files in os.walk(vul_func_path):
    for f in files:
        if f.endswith('.c'):
            total += 1

start_time = datetime.datetime.now()
idx = 1
for root, dirs, files in os.walk(vul_func_path):
    for f in files:
        if f.endswith('.c'):
            print f, "  start."
            func_content = []
            with open(os.path.join(root, f), 'r') as ff:
                func_content = ff.readlines()
            # get the line number of '-'
            del_line_number = []
            for index, lines in enumerate(func_content):
                if lines.endswith('//-\n'):
                    del_line_number.append(index+1)
            #print del_line_number            
            if not os.path.exists(os.path.join(vul_func_lines, f)):
                continue
            dpd_content = ""  #dpd means dependence
            with open(os.path.join(vul_func_lines, f), 'r') as ff:
                temp = ff.readlines()
                dpd_content = "".join("".join(temp).split('\n'))
            
            #print "1111111"
            
            #存储函数体的hash值
            dpd_dic = produce_slice.slice_from_project(dpd_content)
            #print "222222222"
            written[f] = {}
            written[f]['hashvalue'] = []
            written[f]['hashvalue'].append(produce_slice.procude_funcBody_hash(os.path.join(root, f))[0])
            #print "33333333333"
            written[f]['value'] = []
            written[f]['value'].append(produce_slice.procude_funcBody_hash(os.path.join(root, f))[1])
            
            #print "44444444444"
            
            #存储函数切片的hash值
            for keys,values in dpd_dic.items():              
                if keys in del_line_number:
                    print "node_id:", keys
                    print "dpd_id", values
                    slice_content = produce_slice.get_slice_content(func_content, values)
                    slice_content = pu.normalize(slice_content)
                    written[f]['value'].append(slice_content)
                    written[f]['hashvalue'].append(produce_slice.fnv1a_hash(slice_content))
            print "completed. ", idx, "/", total
            print "---------------------------------------------------------------------"
            idx += 1
with open(r"vul_repo.json","w") as result_f:
    json.dump(written,result_f)
    print "Okay .."
end_time = datetime.datetime.now()

print "Running time:", (end_time - start_time).seconds