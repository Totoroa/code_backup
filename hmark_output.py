"""
vuddy get result
"""
import sys
import xlrd
import xlwt

project_hidx = r"F:\project\vuddy-master\hmark\hidx\hashmark_4_openssl-1.0.0a.hidx"
vul_hidx = r"F:\project\vuddy-master\vulnDBGen\hidx\hashmark_4_openssl.hidx"

project_len_hash = {}
project_hash_file = {}
vul_len_hash = {}
vul_hash_file = {}

f = open(project_hidx, "r")
project_all = f.readlines()
f.close()
f = open(vul_hidx, "r")
vul_all = f.readlines()
f.close()
project_all = project_all[1:]
vul_all = vul_all[1:]

flag_1 = False
for line in project_all:
    if line == '\n':
        flag_1 = True
        continue
    elif line == "=====\n":
        flag_1 = True
        continue
    if flag_1 == False:
        elem = line.split('\t')
        hash_value = elem[1:]
        project_len_hash[int(elem[0])] = hash_value[:-1]
    if flag_1 == True:
        elem = line.split('\t', 1)
        file_name = []#elem[1].split('\t')
        f = 0
        temp = ""
        for k in elem[1].split('\t'):
            if k == '':
                continue
            if f == 0:
                temp += k
                f = 1
                continue
            if f == 1:
                temp = temp +  " " + k
                file_name.append(temp)
                temp = ""
                f = 0
                continue
        project_hash_file[elem[0]] = file_name

flag_2 = False
for line in vul_all:
    if line == '\n':
        flag_2 = True
        continue
    elif line == "=====\n":
        flag_2 = True
        continue
    if flag_2 == False:
        elem = line.split('\t')
        hash_value = elem[1:]
        vul_len_hash[int(elem[0])] = hash_value[:-1]
    if flag_2 == True:
        elem = line.split('\t', 1)
        file_name = elem[1].split('./')[1:]
        vul_hash_file[elem[0]] = file_name

#print vul_hash_file['00077e84bddf13677214b8b98c58157d']
#print vul_hash_file['0087a512ee893ef30935f0eff023c41f']
#print project_hash_file['0006f1ef5ab4669f7c605b53916e5d77']
#print project_hash_file['001d5ba3200a998f952fa9b40f1494c8']
#import sys
#sys.exit()

writebook = xlwt.Workbook()#打开一个excel
sheet = writebook.add_sheet('test')#在打开的excel中添加一个sheet
sheet_line = 0

for key,value in project_len_hash.items():
    try:
        vul_value = vul_len_hash[key]
    except KeyError:
        continue
    for i in value:
        for j in vul_value:
            if i==j:
                print "Matched!!"
                if i == '\n':
                    print key,value
                    sys.exit()
                print "project file is : ", project_hash_file[i]
                print "vul file is : ", vul_hash_file[j]
                sheet.write(sheet_line, 0, "------".join(project_hash_file[i]))
                sheet.write(sheet_line, 1, "------".join(vul_hash_file[j]))
                sheet_line += 1
writebook.save('answer.xls')
