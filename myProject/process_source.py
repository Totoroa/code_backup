'''
extract functions in project's source files.
'''
import os
import parseutility2 as pu

source_path = r"C:\Users\admin\Desktop\workspace-python\gj\linux-4.14.76"
project_data_path = os.path.join(os.getcwd(),"project_data", os.path.basename(source_path))
if not os.path.exists(project_data_path):
    os.mkdir(project_data_path)

total = 0
for root, dirs, files in os.walk(source_path):
    for f in files:
        if f.endswith('.c') or f.endswith('.cpp') or f.endswith('.cc') or f.endswith('.c++') or f.endswith('.cxx'):
            total += 1
idx = 1
for root, dirs, files in os.walk(source_path):
    for f in files:
        if f.endswith('.c') or f.endswith('.cpp') or f.endswith('.cc') or f.endswith('.c++') or f.endswith('.cxx'):
            file_content = []
            with open(f, 'r') as ff:
                file_content = ff.readlines()
            
            function_list = pu.parseFile_deep(os.path.join(root, f))
            for functions in function_list:
                func_location = os.path.join(root, f)
                func_location = func_location.replace('\\', '#~') + '$' + functions.name
                with open(func_location, 'w') as ff:
                    func_content = file_content[functions.lines[0]-1 : functions.lines[1]+1]
                    ff.write("".join(func_content))
        print f, " completed. ", idx, "/", total
        idx += 1
print "Ok.."