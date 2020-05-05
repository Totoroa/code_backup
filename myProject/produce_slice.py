'''
Produce slice from pdg.
'''
import re
import copy

class nodes:
    def __init__(self, line_number):
        self.node_id = line_number
        self.from_node = []  #in
        self.to_node = []  #out

def get_nodes(line_pair, nodes_id):
    '''
    return a dictory of nodes.
    {node_id1: nodes1, nodes_id2: nodes2, ...}
    '''
    node_list = []
    for node in nodes_id:
        temp = nodes(node)
        for pair in line_pair:
            if pair[0] == node:
                n.to_node.append(pair[1])
            elif pair[1] == node:
                n.from_node.append(pair[0])
        temp.from_node = list(set(temp.from_node))
        temp.to_node = list(set(temp.to_node))
        node_list.append(temp)
    result = {}
    for i in node_list:
        result[i.node_id] = i
    return result

def get_slice_of_node(nodes_dict, node_id):
    '''
    nodes_dict: {node_id1: nodes1, nodes_id2: nodes2, ...}
    node_id: return the slice about node with node_id
    
    return type: list. eg: [node_id1, node_id2, ... ,node_idn]
    '''
    queue_out = [node_id]
    queue_in = [node_id]
    result = []
    
    copy_nodeDict = copy.deepcopy(nodes_dict)    
    while queue_out:
        current_node = queue_out[0]
        result.append(current_node)
        queue_out.extend(copy_nodeDict[current_node].to_node)
        copy_nodeDict[current_node].to_node = []
        
    while queue_in:
        current_node = queue_in[0]
        result.append(current_node)
        queue_in.extend(copy_nodeDict[current_node].from_node)
        copy_nodeDict[current_node].from_node = []
    
    result = list(set(result))
    return result
    
def slice_from_project(lines_numbers):
    '''
    lines_numbers(String) looks like: (29,30)(32,41)(41,42)(37,37)(32,55)
    return a dictory record each lines_numbers' slice.
    '''
    pattern = r"(\d+,\d+)"
    line_pair = []
    for i in re.findall(pattern, lines_numbers):
        temp = []
        temp.append(int(i.split(',')[0]))
        temp.append(int(i.split(',')[1]))
        if temp[0] == temp[1]:
            continue
        line_pair.append(temp)
    nodes_id = [i for j in line_pair for i in j]
    nodes_id = list(set(nodes_id))
    
    nodes_dic = get_nodes(line_pair, nodes_id)
    result = {}
    for node in nodes_id:
        tmp = get_slice_of_node(nodes_dic, node)
        result[node] = tmp
    return result