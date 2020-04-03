import os
import  re

'''process bbb, delete .highlight and \n\n'''
def del_highlight(file_path):
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    if len(lines) == 0:
        print "#################3",file_path
        return False
    if lines[0].startswith('.highlight'):
        lines = lines[67:]
        lines[0] = lines[0][86:]
        with open(file_path, 'w') as f:
            f.write("".join(lines))
        return True
    else:
        return False

def is_odd(num):    #jishu return True,else false
    if num%2 == 1:
        return True
    else:
        return False

def delete_last_blank(alist):
    while True:
        if len(alist) == 0:
            break
        if alist[-1] == '\n':
            alist = alist[:-1]
        else:
            break
    return alist

def is_need_to_delete(file_path):
    lines = []
    flag = False
    with open(file_path, 'r') as f:
        lines = f.readlines()
    if lines == []:
        print "[+]", file_path, "is null"
        return False
    lines = delete_last_blank(lines)
    if not '\n' in lines:
        return False
    for index in range(len(lines)-1):
        if '/*' in lines[index]:
            flag = True
        if '*/' in lines[index]:
            flag = False
        if flag:
            continue
        if index == 0 and lines[index] == '\n':
            if lines[index+1] == '\n':
                continue
            else:
                return False
        if lines[index] == '\n':
            if lines[index-1] == '\n' or lines[index+1] == '\n':
                continue
            else:
                return False
    return True

def del_extra_line(file_path):
    if not is_need_to_delete(file_path):
        return 
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    flag = False
    new_lines = []
    for line in lines:
        if line != '\n':
            new_lines.append(line)
            continue
        if line == '\n' and flag == False:
            new_lines.append(line)
            flag = True
            continue
        if line == '\n' and flag == True:
            flag = False
            continue
    with open(file_path, 'w') as f:
        f.write("".join(new_lines))
    print file_path, 'processed Ok..'

def normalize(alist):
    return re.sub("\s", "", "".join(alist).lower())
    
"""process the patched files"""
def reverse_patched_files(patch_file_path, BM_file_path):
    change_list = []
    patch_content = []
    file_content = []
    pattern = re.compile(r'@@ -(\d+,\d+) \+(\d+,\d+) @@')
    with open(patch_file_path, 'r') as f:
        patch_content = f.readlines()
    with open(BM_file_path, 'r') as f:
        file_content = f.readlines()
        
    temp_del_patch = []
    temp_add_patch = []
    old_start = -1
    old_range = -1
    new_start = -1
    new_range = -1
    flag = False
    for patch_line in patch_content:
        if pattern.search(patch_line):
            flag = True
            if len(temp_del_patch) != 0 and len(temp_add_patch) != 0:
                if normalize(temp_del_patch) == normalize(file_content[old_start:old_start+old_range]):
                    print "[OLD]", patch_file_path, BM_file_path, "matched !"
                elif normalize(temp_add_patch) == normalize(file_content[new_start:new_start+new_range]):
                    print "[NEW]", patch_file_path, BM_file_path, "matched !"
                    temp = []  # record [start_index, range, content_to_add]
                    temp.append(new_start)
                    temp.append(new_range)
                    temp.append(temp_del_patch)
                    change_list.append(temp)
                    
                    #with open(os.path.join(os.path.dirname(BM_file_path), "(AM)"+os.path.basename(patch_file_path)), 'w') as f:
                        #f.write("".join(file_content))
                    #file_content[new_start:new_start+new_range] = temp_del_patch
                    #with open(BM_file_path,'w') as f:
                        #f.write("".join(file_content))
                    print "processed !"
                else:
                    print "[-][-][-]", patch_file_path, BM_file_path, "not matched !!!"
                    with open('not_matched_files.txt','a') as f:
                        f.write(patch_file_path+"  ###  "+BM_file_path+"\n")
                    #print "normalize(temp_del_patch):\n", normalize(temp_del_patch)
                    #print "\nnormalize(file_content[old_start:old_start+old_range]):\n", normalize(file_content[old_start:old_start+old_range])
                    #print "\nnormalize(temp_add_patch):\n", normalize(temp_add_patch)
                    #print "\nnormalize(file_content[new_start:new_start+new_range]):\n", normalize(file_content[new_start:new_start+new_range])
                    #print old_start, old_range, new_start, new_range
                    
            temp_del_patch = []
            temp_add_patch = []
            old_start = int(pattern.search(patch_line).group(1).split(',')[0])-1
            old_range = int(pattern.search(patch_line).group(1).split(',')[1])
            new_start = int(pattern.search(patch_line).group(2).split(',')[0])-1
            new_range = int(pattern.search(patch_line).group(2).split(',')[1]) 
            continue
        if flag:
            if patch_line.startswith('+'):
                temp_add_patch.append(patch_line[1:])
            elif patch_line.startswith('-'):
                temp_del_patch.append(patch_line[1:])
            else:
                temp_add_patch.append(patch_line)
                temp_del_patch.append(patch_line)
    if len(temp_del_patch) != 0 and len(temp_add_patch) != 0:
        if normalize(temp_del_patch) == normalize(file_content[old_start:old_start+old_range]):
            print "[OLD]", patch_file_path, BM_file_path, "matched !"
        elif normalize(temp_add_patch) == normalize(file_content[new_start:new_start+new_range]):
            print "[NEW]", patch_file_path, BM_file_path, "matched !"
            temp = []  # record [start_index, range, content_to_add]
            temp.append(new_start)
            temp.append(new_range)
            temp.append(temp_del_patch)
            change_list.append(temp)
            print "processed !"
        else:
            print "[-][-][-]", patch_file_path, BM_file_path, "not matched !!!"
    change_list.sort(reverse=True) 
    for i in change_list:  #i: [start_index, range, content_to_add]
        file_content[i[0]:i[0]+i[1]] = i[2]
    with open(BM_file_path,"w") as f:
        f.write("".join(file_content))
            #print "normalize(temp_del_patch):\n", normalize(temp_del_patch)
            #print "\nnormalize(file_content[old_start:old_start+old_range]):\n", normalize(file_content[old_start:old_start+old_range])
            #print "\nnormalize(temp_add_patch):\n", normalize(temp_add_patch)
            #print "\nnormalize(file_content[new_start:new_start+new_range]):\n", normalize(file_content[new_start:new_start+new_range])
            #print old_start, old_range, new_start, new_range            

reverse_patched_files(r"D:\test\aaa\CVE-2019-1010293\core#~arch#~arm#~mm#~tee_mmu.c", r"D:\test\aaa\CVE-2019-1010293\(BM)core#~arch#~arm#~mm#~tee_mmu.c")

count = 0
for root, dirs, files in os.walk(r"D:\test\aaa"):
    for ff in files:
        if ff.startswith('(BM)'):
            patch_file_path = os.path.join(root, ff[4:])
            if os.path.exists(patch_file_path):
                reverse_patched_files(patch_file_path, os.path.join(root, ff))
                count += 1
        
print "number of changed files: ", count
print "Over.."
