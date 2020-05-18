'''
extract functions in project's source files.
'''
import os
import parseutility2 as pu
import sys
import multiprocessing
import time

#source_path = r"C:\Users\admin\Desktop\workspace-python\gj\linux-4.14.76"
source_path = r"F:\project\project_source\linux-2.6.27.38"
project_data_path = os.path.join(os.getcwd(),"project_data", os.path.basename(source_path))
if not os.path.exists(project_data_path):
    os.makedirs(project_data_path)

def get_func(source_file_path):
    file_content = []
    with open(source_file_path, 'r') as f:
        file_content = f.readlines()
    function_list = pu.parseFile_shallow(source_file_path)
    print len(function_list)
    for functions in function_list:
        func_filaName = source_file_path.split(os.path.basename(source_path),1)[1][1:]
        func_filaName = func_filaName.replace('\\', '#~') + '$' + functions.name + '$' + str(functions.lines[0]) + '-' + str(functions.lines[1]) + '.c'
        try:
            with open(os.path.join(project_data_path, func_filaName), 'w') as ff:
                func_content = file_content[functions.lines[0]-1 : functions.lines[1]+1]
                ff.write("".join(func_content))
        except Exception,e:
            print e
            continue
    print source_file_path
    
    return

if __name__ == '__main__':    
    file_list = []
    for root, dirs, files in os.walk(source_path):
        for f in files:
            if f.endswith('.c') or f.endswith('.cpp') or f.endswith('.cc') or f.endswith('.c++') or f.endswith('.cxx'):
                file_list.append(os.path.join(root, f))
    print len(file_list)
    #existed = os.listdir(r"C:\Users\admin\Desktop\workspace-python\My_project\project_data\linux-4.14.76-1")
    #existed = [k[2:].replace('#~', '\\') for k in existed]
    #existed = [os.path.join(source_path, k).split('$',1)[0] for k in existed]
    #existed = list(set(existed))
    #file_list = [k for k in file_list if k not in existed]
    #for i in file_list:
        #print i 
    #sys.exit()
    print "file_list OK.."
    
    time1=time.time()
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=4)
    res = pool.map(get_func, file_list)
    time2=time.time()
    
    pool.close()
    pool.join()
    print('running time: ' + str(time2 - time1) + ' s')
