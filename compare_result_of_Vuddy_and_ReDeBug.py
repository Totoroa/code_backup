import sys
sys.path.append(r"F:\project\vuddy-master\vulnDBGen")
from tools import parseutility
import os
import xlrd
import xlwt
import re

root_path = r"C:\Users\admin\Desktop\openssl-1.0.0a"
def get_function_range(file_name, func_num):
    f_name = os.path.join(root_path, file_name)
    func_list = parseutility.parseFile_shallow(f_name, "caller")
    
    return func_list[func_num-1].lines

#结果生成：文件名（C:\Users\admin\Desktop\openssl-1.0.0a\ssl\s3_srvr.c）, 文件范围(111,222)，cve编号(CVE-2017-3733)
print "Processing Vuddy output..."
vuddy_data = xlrd.open_workbook(r"answer_Vuddy.xls")
sheet1 = vuddy_data.sheet_by_index(0)
vuddy_info = {}    #(文件名$cve编号)：(文件范围)
for i in range(1,sheet1.nrows):
    info = sheet1.row_values(i)
    k1_str = root_path + "\\" + info[0].split(" ")[0]
    fun_range = get_function_range(k1_str, int(info[0].split(" ")[1]))
        
    v_str = " ".join([str(elem) for elem in fun_range])
    k2_str = re.search(r"CVE-\d+-\d+", info[1]).group(0)
    k_str = k1_str + '$' + k2_str
    k_str = k_str.replace("/","\\")
    if k_str in vuddy_info.keys():
        vuddy_info[k_str].append(v_str)
    else:
        vuddy_info[k_str] = [v_str]

print "Processing ReDeBug output..."
redebug_data = xlrd.open_workbook(r"answer_ReDeBug.xls")
sheet2 = redebug_data.sheet_by_index(0)
redebug_info = {}
for j in range(1,sheet2.nrows):
    info = sheet2.row_values(j)
    k1_str = info[0].split(" ", 1)[0]
    v_str = info[0].split(" ", 1)[1]
    k2_str = re.search(r"CVE-\d+-\d+", info[1]).group(0)
    k_str = k1_str + '$' + k2_str
    if k_str in redebug_info.keys():
        redebug_info[k_str].append(v_str)
    else:
        redebug_info[k_str] = [v_str]
print "All output processed..."

for k,v in vuddy_info.items():
    vuddy_info[k] = list(set(vuddy_info[k]))
for k,v in redebug_info.items():
    redebug_info[k] = list(set(redebug_info[k]))

print "Getting result..."
 #(文件名$cve编号)：(文件范围)
result = {'both':[], 'Vuddy':[], 'ReDeBug':[]}
r_reversed_key = []

for key,value in vuddy_info.items():
    #print key
    #print value
    #sys.exit()
    for v_value in value:
        v_value = [int(elem) for elem in v_value.split(" ")]
        try:
            r_value = redebug_info[key]
            for rv in r_value:
                rv = [int(elem) for elem in rv.split(" ")]
                if v_value[0]-1 <= rv[0] and v_value[1] >= rv[1]:
                    result['both'].append(key+"$"+str(v_value)+"$"+str(rv))
                    r_reversed_key.append(key)
                else:
                    result['Vuddy'].append(key+"$"+str(v_value))
                    result['ReDeBug'].append(key+"$"+str(rv))
        except KeyError:
            result['Vuddy'].append(key+"$"+str(value))
    
    
    
    #改这里！！
    #value = [int(elem) for elem in value[0].split(" ")]
    #try:
        #r_value = redebug_info[key]
        #for rv in r_value:
            #rv = [int(elem) for elem in rv.split(" ")]
            #if value[0] <= rv[0] and value[1] >= rv[1]:
                #result['both'].append(key+"$"+str(value)+"$"+str(rv))
                #r_reversed_key.append(key)
            #else:
                #result['Vuddy'].append(key+"$"+str(value))
                #result['ReDeBug'].append(key+"$"+str(rv))
                #r_reversed_key.append(key)
    #except KeyError:
        #result['Vuddy'].append(key+"$"+str(value))
        
        #print r_value
        #r_value = [int(elem) for elem in r_value[0].split(" ")]
        #if value[0] <= r_value[0] and value[1] >= r_value[1]:
            #result['both'].append(key+"$"+str(value)+"$"+str(r_value))
            #r_reversed_key.append(key)
        #else:
            #result['Vuddy'].append(key+"$"+str(value))
            #result['ReDeBug'].append(key+"$"+str(r_value))
            #r_reversed_key.append(key)
    #except KeyError:
        #result['Vuddy'].append(key+"$"+str(value))

r_rest = [elem for elem in redebug_info.keys() if elem not in r_reversed_key]

for ii in r_rest:
    result['ReDeBug'].append(ii+"$"+str(redebug_info[ii]))

result['both'] = set(list(result['both']))
result['Vuddy'] = set(list(result['Vuddy']))
result['ReDeBug'] = set(list(result['ReDeBug']))


with open("both.txt","w") as f:
    f.write('\n'.join(result['both']))
with open("Vuddy.txt","w") as f:
    f.write('\n'.join(result['Vuddy']))
with open("ReDeBug.txt","w") as f:
    f.write('\n'.join(result['ReDeBug']))

print "OK.."
