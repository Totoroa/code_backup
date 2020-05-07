'''
split the folders to smaller.
'''

import os
import shutil

func_path = r"F:\data\self_vul_repo\functions\Bad"
move_path = func_path.split('\\')[-1]
max_size = 10 #MB

def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)
    return round(fsize, 2)  #MB

if __name__ == '__main__':
    number = 0
    total_size = 0
    for f in os.listdir(func_path):
        file_path = os.path.join(func_path, f)
        cur_path = os.path.join(func_path, move_path+str(number))
        if not os.path.exists(cur_path):
            os.mkdir(cur_path)
        if os.path.isfile(file_path):
            if total_size < max_size:
                total_size += get_FileSize(file_path)
                shutil.move(file_path, os.path.join(cur_path, f))
                print total_size
            else:
                number += 1
                cur_path = os.path.join(func_path, move_path+str(number))
                if not os.path.exists(cur_path):
                    os.mkdir(cur_path)
                total_size = get_FileSize(file_path)
                shutil.move(file_path, os.path.join(cur_path, f))
                
    print "Ok.."