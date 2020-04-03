import re
import os
import sys
"""process the record in file:  not_matched_files.txt"""

path = r"C:\Users\admin\Desktop\workspace-python\Vuddy_vs_ReDeBug\not_matched_files.txt"
lines = []
with open(path, 'r') as f:
    lines = f.readlines()
lines = lines[1:]
#lines = [elem.replace(r"D:\test", r"F:\data\self_vul_repo") for elem in  lines]

"""TODO: process rest files"""
def normalize(alist):
    return re.sub("\s", "", "".join(alist).lower())

def process_patch(patch_lines):
    result = []  #result = [[patch_del, patch_add], [patch_del, patch_add], ...]
    patch_del = []
    patch_add = []
    flag = False
    pat = re.compile(r'@@ -(\d+,\d+) \+(\d+,\d+) @@')
    for line in patch_lines:
        if pat.search(line):
            flag = True
            if patch_del != [] and patch_add != []:
                patch = []
                patch.append(patch_del)
                patch.append(patch_add)
                result.append(patch)
            patch_del = []
            patch_add = []
            continue
        if flag:
            if line.startswith('-'):
                patch_del.append(line[1:])
            elif line.startswith('+'):
                patch_add.append(line[1:])
            else:
                patch_del.append(line)
                patch_add.append(line)
    if patch_del != [] and patch_add != []:
        patch = []
        patch.append(patch_del)
        patch.append(patch_add)
        result.append(patch)
    return result

def get_range(patch_content, file_content):
    windows = len(patch_content)
    patch_norm = normalize(patch_content)
    result = []
    if len(patch_content) > len(file_content):
        return None
    for i in range(len(file_content)-windows):
        file_norm = normalize(file_content[i:i+windows])
        if file_norm == patch_norm:
            result.append([i,i+windows])
    return result

def process(patch_content, file_content, patch_path, BM_path):
    patches = process_patch(patch_content)
    print "len(patches) = ", len(patches)
    change_list = []   #change_list = [[start_index, end_index], [start_index, end_index], ...]
    for patch in patches:    #patch = [patch_del, patch_add]
        print "###"
        patch_del = patch[0]
        patch_add = patch[1]
        if get_range(patch_del, file_content):
            print "[OLD]", patch_path, BM_path
        if get_range(patch_add, file_content):
            print "[New]", patch_path, BM_path

#line = r"D:\test\patches_and_files\CVE-2013-7448\src#~wiki.c  ###  D:\test\patches_and_files\CVE-2013-7448\(BM)src#~wiki.c"
line = r"D:\test\patches_and_files\CVE-2019-12209\pam-u2f.c  ###  D:\test\patches_and_files\CVE-2019-12209\(BM)pam-u2f.c"
file1 = line.split('  ###  ')[0]
file2 = line.split('  ###  ')[1]
patch_content = []
file_content = []
with open(file1, 'r') as f:
    patch_content = f.readlines()
with open(file2, 'r') as f:
    file_content = f.readlines()
process(patch_content, file_content, file1, file2)
sys.exit()

for line in lines:
    if line[-1] == '\n':
        line = line[:-1]
    file1 = line.split('  ###  ')[0]
    file2 = line.split('  ###  ')[1]
    patch_content = []
    file_content = []
    with open(file1, 'r') as f:
        patch_content = f.readlines()
    with open(file2, 'r') as f:
        file_content = f.readlines()
    process(patch_content, file_content, file1, file2)