'''
detect vulnerabilities based on the parsed project source code.
'''
#diffCommand = "\"{0}\" -u {1} {2} > {3}_{4}.patch".format(config.diffBinary,
                                                           #vulOldFileName,
                                                           #vulNewFileName,
                                                           #vulFileNameBase,
                                                           #finalOldFuncId)
#os.system(diffCommand)


import os
import json
import bitarray

import produce_slice
import parseutility2 as pu

dpd_file_path = r""  # Path of files that record the dependence relationships of project functions' lines.
function_file_path = r""   # Path of files that store source functions.

vul_json_path = r""   # vul_repo in json format
vul_patch_path = r""
vul_func_path = r"F:\data\self_vul_repo\functions\Bad"
patched_func_path = r"F:\data\self_vul_repo\functions\Good"
vul_func_dpd_path = r"F:\data\self_vul_repo\func_lines"

show_lines_limit = 20
html_escape_dict = { '&': '&amp;', '>': '&gt;', '<': '&lt;', '"': '&quot;', '\'': '&apos;' }

bitvector_size = 2097152
bitvector = bitarray.bitarray(bloomfilter_size)
bitvector_dic = {}  # record the slice's hashvalue and the line numbers. eg: {1839273: [1,5,7,9,10], 34502394: [6,7,8,10,11,12]}

vul_dic = {}

def _html_escape(self, string):
    '''
    Escape HTML
    '''
    return ''.join(common.html_escape_dict.get(c,c) for c in string)

with open(vul_json_path, 'r') as ff:
    vul_dic = json.load(ff)
    
outfile = open('out.html', 'a')
outfile.write("""
<!DOCTYPE html>
<html>
<head>
    <title>ReDeBug - Report</title>
    <style type="text/css">
    .container { padding: 3px 3px 3px 3px; font-size: 14px; }
    .patch { background-color: #CCCCCC; border: 2px solid #555555; margin: 0px 0px 5px 0px }
    .source { background-color: #DDDDDD; padding: 3px 3px 3px 3px; margin: 0px 0px 5px 0px }
    .filepath { font-size: small; font-weight: bold; color: #0000AA; padding: 5px 5px 5px 5px; }
    .codechunk { font-family: monospace; font-size: small; white-space: pre-wrap; padding: 0px 0px 0px 50px; }
    .linenumber { font-family: monospace; font-size: small; float: left; color: #777777; }
    </style>
    <script language="javascript">
        function togglePrev(node) {
            var targetDiv = node.previousSibling;
            targetDiv.style.display = (targetDiv.style.display=='none')?'block':'none';
            node.innerHTML = (node.innerHTML=='+ show +')?'- hide -':'+ show +';
        }
        function toggleNext(node) {
            var targetDiv = node.nextSibling;
            targetDiv.style.display = (targetDiv.style.display=='none')?'block':'none';
            node.innerHTML = (node.innerHTML=='+ show +')?'- hide -':'+ show +';
        }
    </script>
</head>
<body>
<div style="width: 100%; margin: 0px auto">""")  

def report(src_file_name, src_dpd_lines, vul_file_name, vul_dpd_lines):
    # TODO
    #if src_lines == 0 and vul_lines == 0, means all function lines should be considered.
    outfile.write("""
    <div class="container">
        <br />""")
    
    # patch info
    patch_ct = []
    with open(os.path.join(vul_patch_path, vul_file_name[9:]), 'r') as f:
        patch_ct = f.readlines()
    # TODU process //+ and //-.
    
    
    if len(patch_ct) > show_lines_limit:
        outfile.write("""
        <div class="patch">
            <div class="filepath">%s</div>""" % vulfunc_file_name[9:].split('$')[0]+'/'+vulfunc_file_name[9:].split('$')[1])
        outfile.write("""
            <div>
                <div class="codechunk">%s</div>
            </div>"""%_html_escape("".join(patch_ct[:show_lines_limit])))
        outfile.write("""
            <a href="javascript:;" onclick="toggleNext(this);">+ show +</a><div style="display: none">
                <div class="codechunk">%s</div>
            </div>
        </div>"""%_html_escape("".join(patch_ct[show_lines_limit:])))
    else:
        outfile.write("""
        <div class="patch">
            <div class="filepath">%s</div>""" % vulfunc_file_name[9:].split('$')[0]+'/'+vulfunc_file_name[9:].split('$')[1])
        outfile.write("""
            <div>
                <div class="codechunk">%s</div>
            </div>
        </div>"""%_html_escape("".join(patch_ct)))
    
    #source info
    source_ct = []
    with open(src_file_name, 'r') as f:
        source_ct = f.readlines()
    # TODO process dependence lines(marked to blue)
    # TODO compute the line range in src_file_name
    line_range = []
    
    if len(source_ct) > show_lines_limit:
        outfile.write("""
        <div class="source">
            <div class="filepath">%s</div>""" % os.path.basename(src_file_name))
        outfile.write("""
            <div>
                <div class="linenumber">""")
        for i in range(line_range[0], line_range[0]+show_lines_limit):
            outfile.write("""
                %d<br />""" % (i+1))
        outfile.write("""
                </div>
                <div class="codechunk">%s</div>
            </div>""" % self._html_escape("".join(source_ct[:show_lines_limit])))
        outfile.write("""
            <a href="javascript:;" onclick="toggleNext(this);">+ show +</a><div style="display: none">
                <div class="linenumber">""")
        for i in range(line_range[0]+show_lines_limit, line_range[1]):
            outfile.write("""
                %d<br />""" % (i+1))
        outfile.write("""
                </div>
                <div class="codechunk">%s</div>
            </div>
        </div>""" %_html_escape("".join(source_ct[show_lines_limit:])))
    else:
        outfile.write("""
        <div class="source">
            <div class="filepath">%s</div>""" % os.path.basename(src_file_name))
        outfile.write("""
            <div>
                <div class="linenumber">""")
        for i in range(line_range[0], line_range[1]):
            outfile.write("""
                %d<br />""" % (i+1))
        outfile.write("""
                </div>
                <div class="codechunk">%s</div>
            </div>
        </div>""" % self._html_escape("".join(source_ct)))
        
    outfile.write("""
    </div>""")

for files in os.listdir(function_file_path):
    # first, get the abstracted/normalized func_Body, to detect if the hashvalue of the func_Body is vulnerability. 
    temp = produce_slice.procude_funcBody_hash(os.path.join(function_file_path, files))
    hash_value = temp[0]
    for vulfunc_file_name, record in vul_dic.items():         #Maybe need to be changed because of vul_dic. failed to json.load()
        if record['hashvalue'][0] == hash_value:
            print files, "   Bingo(1) !"
            report(os.path.join(function_file_path, files), 0, vulfunc_file_name)
            break
    
    # if the func_Body is "not" vulnerablity, then produce slices for current function. 
    # Build a bitvector for current function, 
    else: #if 'break' executed, the else will no be executed.
        dpd_content = ""  #dpd means dependence
        func_content = []
        if not os.path.exists(os.path.join(dpd_file_path, files)):
            continue
        with open(os.path.join(dpd_file_path, files), 'r') as ff:
            temp = ff.readlines()
            dpd_content = "".join("".join(temp).split('\n'))
        dpd_dic = produce_slice.slice_from_project(dpd_content)
        
        with open(os.path.join(function_file_path, files), 'r') as ff:
            func_content = ff.readlines()
        
        # build a bitvector according to dpd_dic
        bitvector.setall(0)
        for line_num, line_dpd in dpd_dic.items():
            slice_content = produce_slice.get_slice_content(func_content, line_dpd)
            slice_content = pu.removeComment(slice_content)
            slice_content = pu.normalize(slice_content)
            slice_hash = produce_slice.fnv1a_hash(slice_content)
            bitvector[slice_hash] = 1
            bitvector_dic[slice_hash] = line_dpd
            
        #detect the vul_slice according the bitvector
        for vul_filename, records in vul_dic.items():
            if len(records['hashvalue']) == 1:
                continue
            flag = True
            matched_hash = []
            for n in records['hashvalue'][1:]:
                if bitvector[n] == 1:
                    matched_hash.append(n)
                else:
                    flag == False
                if flag == False:
                    matched_hash = []
                    break
            if flag:
                print files, "    Bingo(2) !"
                line_list = []
                for i in matched_hash:
                    line_list.extend(bitvector_dic[i])
                line_list = list(set(line_list))
                line_list.sort()
                report(os.path.join(function_file_path, files), line_list, vul_filename)
                break
outfile.write("""
</div>
</body>
</html>""")
outfile.close()