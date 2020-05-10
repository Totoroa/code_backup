'''process vul_repo_backup-test.json'''

import re

path = r"C:\Users\admin\Desktop\workspace-python\My_project\vul_repo_backup-test.json"

a = []
with open(path, 'r') as f:
    a = f.readlines()
b = a[0]

file_list = []
pattern = re.compile("\"\(BadFunc\)CVE-\d+-\d+.*?\.c\"")
file_list = pattern.findall(b)
file_list = [k[1:-1] for k in file_list]
file_list = list(set(file_list))