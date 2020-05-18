'''
produce vulnerability slice.
'''
import os
import json
import sys
import datetime

import produce_slice
import parseutility2 as pu
import fix

vul_func_path = r"F:\data\self_vul_repo\functions\Bad"
vul_func_lines = r"F:\data\self_vul_repo\func_lines"
result_fileName = "vul_repo.json"

#bloomfilter_size = 2097152
#bitarray.bitarray(common.bloomfilter_size)

written = {}

total = 0
for root, dirs, files in os.walk(vul_func_path):
    for f in files:
        if f.endswith('.c') and f in fix.file_list:
            total += 1

start_time = datetime.datetime.now()
idx = 1
for root, dirs, files in os.walk(vul_func_path):
    for f in files:
        if f.endswith('.c') and f in fix.file_list:
            #if idx <= 7810:
                #idx += 1
                #continue
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
                idx += 1
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
            written[f]['lineNumber'] = [0]
            written[f]['lineId'] = [0]
            
            #print "44444444444"
            
            #存储函数切片的hash值
            for keys,values in dpd_dic.items():
                if keys in del_line_number:
                    values.sort()
                    print "node_id:", keys
                    print "dpd_id", values
                    slice_content = produce_slice.get_slice_content(func_content, values)
                    slice_content = pu.removeComment(slice_content)
                    slice_content = pu.normalize(slice_content)
                    written[f]['value'].append(slice_content)
                    written[f]['hashvalue'].append(produce_slice.fnv1a_hash(slice_content))
                    written[f]['lineNumber'].append("-".join([str(nb) for nb in values]))
                    written[f]['lineId'].append(keys)
            
            try:
                with open(r'emm.txt', 'a') as fff:
                    fff.write(f)
                    fff.write(' $$hashvalue$$ ')
                    fff.write(" ".join([str(nb) for nb in written[f]['hashvalue']]))
                    fff.write(" $$value$$ ")
                    fff.write(" ".join(written[f]['value']))
                    fff.write(" $$lineNumber$$ ")
                    fff.write(" ".join([str(nb) for nb in written[f]['lineNumber']]))
                    fff.write(" $$lineId$$ ")
                    fff.write(" ".join([str(nb) for nb in written[f]['lineId']]))
                    fff.write('\n\n')
                
                #with open(r"emm.json", "a") as fff:
                    #fff.write('\"' + f + '\": ')
                    #json.dump(written[f], fff)
                    #fff.write(", ")
            except UnicodeDecodeError:
                print "write file <emm.txt> failed."
                written.pop(f)
            
            print "completed. ", idx, "/", total
            print "---------------------------------------------------------------------"
            idx += 1
try:
    with open(result_fileName,"w") as result_f:
        json.dump(written, result_f, encoding='gbk')
        print "Okay .."
except BaseException:
    print "write file <", result_fileName, "> failed !"
        
end_time = datetime.datetime.now()
print "Running time:", (end_time - start_time).seconds, "s"