import json
import os
import networkx as nx
import matplotlib.pyplot as plt
import graphviz
import pydotplus

# filename = "./dot files/09-Traceroutable/traceroutable.json"
# filename = "./dot files/03-L2_Flooding/Other ports/l2_flooding_other_ports.json"
# filename = "./dot files/02-Repeater/repeater_without_table.json"
# filename = "./dot files/11-Packet-Loss-Detection/loss-detection.json"
# filename = "./firewall_tofino/prog_firewall_tofino.p4"

file_path_info= open("path_info.txt",'w')


def activate_node(g, start_node):          
    stack = [start_node]

    while stack:
        node = stack.pop()
        preds = g.predecessors(node)
        stack += preds
        print('%s -> %s' % (node, preds))


def print_details(data):
    if isinstance(data,(list, tuple,set)):
        for i in data:
            print("\t",i)
    elif isinstance(data,dict):
        for i in data.keys():
            print("\t",i," : ",data[i])

def extract_actions(filename):
    data = None
    action_list = []
    with open(filename, 'r') as f:
        data = json.load(f)

    for action in data['actions']:
        action_list.append(action['name'])
    
    action_list = list(set(action_list))
    return action_list

def extract_tables_actions(filename):
    data = None
    name_to_action = {}
    with open(filename, 'r') as f:
        data = json.load(f)

    for name in data['pipelines']:
        if name["name"]=="ingress":
            for table in name["tables"]:
                if "MyIngress" in table["name"]:
                    name_to_action[table["name"]] =  [x for x in table["actions"]]

    return name_to_action

def extract_nodename_condition(filename):
    """This function creates dictionary of node
    names with its corresponding conditions."""
    data = None
    node_to_condition_map = {}
    with open(filename, 'r') as f:
        data = json.load(f)
    node_to_condition_map = {}
    for name in data['pipelines']:
        if name["name"]=="ingress":
            for condition in name['conditionals']:
                if 'source_info' in condition.keys():
                    node_to_condition_map[condition['name']] = condition['source_info']['source_fragment']
    
    return node_to_condition_map

def extract_tables_next_actions(filename):
    """This Function extracts NEXT_ACTIONS associated with
     the table from json file."""
    data = None
    table_to_next_action = {}
    with open(filename, 'r') as f:
        data = json.load(f)

    for name in data['pipelines']:
        if name["name"]=="ingress":
            for table in name["tables"]:
                table_to_next_action[table['name']] = table['next_tables']

    return table_to_next_action

def extract_conditionals(filename):
    """This function creates dictionary of conditionals with its 
    corresponding next actions based on the condition 
    evaluation "True or False"."""
    data = None
    with open(filename, 'r') as f:
        data = json.load(f)

    conditions_to_nextstep = {}
    for name in data['pipelines']:
        if name["name"]=="ingress":
            for condition in name['conditionals']:
                if 'source_info' in condition.keys():
                    conditions_to_nextstep[condition['name']] = {'true_next':condition['true_next'],'false_next':condition['false_next']}
               
    return conditions_to_nextstep



#This is a utility function. Input: Dictionary
# Returns: list of keys and values where value != None
def get_notNone_values(data):
    val = []
    key = []
    for k in data.keys():
        if data[k] is not None and data[k] != 'None' and (data[k] != 'Null' and data[k] != 'null'):
            val.append(data[k])
            key.append(k)
    return key, val
##############################
#### START CREATING EDGES ####
##############################
switch_case = {}
def create_edges(filename):
    edges = []
    # Table_actions contains names of all programmer tables
    table_actions = extract_tables_actions(filename)
    #table_next_actions contains next hop for every table 
    table_next_actions = extract_tables_next_actions(filename)
    #nodename_condition maps node name to conditional step of tables.
    nodename_condition = extract_nodename_condition(filename)
    #conditional_nextstep points to next table according to condition(true_next,false_next)
    conditionals_nextstep = extract_conditionals(filename)

    for key in conditionals_nextstep.keys():
        if isinstance(conditionals_nextstep[key]['true_next'],(list, set, tuple)):
            for k1 in conditionals_nextstep[key]['true_next']:
                if k1 is not None and key != 'NoAction':
                    edges.append({"src":key,"dst":k1,"weight":0})
        else:
            if conditionals_nextstep[key]['true_next'] is not None and key != 'NoAction':
                edges.append({"src":key,"dst":conditionals_nextstep[key]['true_next'],"weight":0})

        if isinstance(conditionals_nextstep[key]['false_next'],(list, set, tuple)):
            for k1 in conditionals_nextstep[key]['false_next']:
                if k1 is not None and key != 'NoAction':
                    edges.append({"src":key,"dst":k1,"weight":0})
        else:
            if conditionals_nextstep[key]['false_next'] is not None and key != 'NoAction':
                edges.append({"src":key,"dst":conditionals_nextstep[key]['false_next'],"weight":0})

    """If Switch case is used we have to extract it from Next_action of the table."""
    #  Maps table names to their respective actions just for programmer tables.
    for key in table_next_actions.keys():
        if "MyIngress" in key:
            if key in table_actions.keys():
                for ac in table_actions[key]:
                    if key != 'NoAction':
                        edges.append({'src':key, 'dst':ac, 'weight':0})
    

    for key in table_next_actions.keys():
        vals = []
        keys, vals = get_notNone_values(table_next_actions[key])
        for k,v in zip(keys, vals):

            if "MyIngress" in k and (k!=v):
                edges.append({'src':k, 'dst':v, 'weight':0})
                switch_case[key] = {'src':k, 'dst':v, 'weight':0}
            else:
                edges.append({'src':key, 'dst':v, 'weight':0})
                switch_case[key] = {'src':key, 'dst':v, 'weight':0}

    #Remove such elements with similar 'src' and 'dst'
    for e in edges:    
        if e['src'] == e['dst']:
            edges.remove(e)

    edges.append({'src':"tbl_ret_pkt_to_sender", 'dst':"MyIngress.ret_pkt_to_sender", 'weight':0})
    edges.append({'src':"tbl_ret_pkt_to_sender_0", 'dst':"MyIngress.ret_pkt_to_sender", 'weight':0})


    return edges

##############################
##### END CREATING EDGES #####
##############################

def create_cfg(filename):

    # nodes = create_nodes(filename)
    nodes = []
    weighted_edges = create_edges(filename)    
    edge_list = []

    for e in weighted_edges:
        edge_list.append((e["src"], e["dst"], e["weight"]))
    
    """Remove duplicate edges"""
    edge_list = list(set(edge_list))


    """Remove such elements with similar 'src' and 'dst'."""
    for e in edge_list:
        if e[0] == e[1]:
            edge_list.remove(e)


    for e in edge_list:
        nodes.append(e[0])
        nodes.append(e[1])

    nodes = list(set(nodes))

    print("Total Nodes/states in graph are")
    print(len(nodes))

    print("\n")
    print("\n")
    print("\n")

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edge_list)


   

    h=G.to_undirected()
    print("Check if graph is connected or not",nx.is_connected(h))

    print("\n")
    print("\n")
    print("\n")

   
    nx.draw_shell(G, with_labels = True, arrows=True) 
    plt.show()
   

    
    topological_order = list(nx.topological_sort(G))
    rev_topological_order = list(reversed(list(nx.topological_sort(G))))

    
    leaf_vertex = [v for v, d in G.out_degree() if d == 0]
    start_vertex = [v for v, d in G.in_degree() if d==0]

    print("leaf vertexes are",leaf_vertex)

    print("\n")
    print("\n")
    print("\n")

    print("Start vertex is",start_vertex)



    path_list = []    

    ####################################
    #### START BALL-LARUS ALGORITHM ####
    ####################################
   

    weighted_edges = []
    for e in edge_list:
        weighted_edges.append({'src':e[0], 'dst':e[1], 'weight':e[2]})

    num_path = {}
    for v in rev_topological_order:
        if v in leaf_vertex:
            num_path[v] = 1
        else:
            num_path[v] = 0
            for e in G.out_edges(v):
                ind = weighted_edges.index({'src':e[0], 'dst':e[1],'weight': 0})
                weighted_edges[ind]['weight'] = num_path[v]
                num_path[v] = num_path[v] + num_path[e[1]]

    ####################################
    #### END BALL-LARUS ALGORITHM ######
    ####################################

    
    # print("entering here")
    pos_w=0
    max_path_weight_possible=0
    for i in weighted_edges:
        if i['weight']>0:
            pos_w=pos_w + 1
            # print(i)
    

    return weighted_edges, G

# weighted_edges, graph = create_cfg(filename)

def augmentor(p4_filename, json_filename):
    import re
    # print(json_filename)
    # jsonfile = "./dot files/03-L2_Flooding/Other ports/l2_flooding_other_ports.json"
    # jsonfile = "./dot files/09-Traceroutable/traceroutable.json"
    jsonfile = json_filename

    weighted_edges, graph = create_cfg(jsonfile)



    actions = extract_actions(jsonfile)
    tables = extract_tables_actions(jsonfile)
    conditions = extract_conditionals(jsonfile)

    
    topological_order = list(nx.topological_sort(graph))    
    leaf_vertex = [v for v, d in graph.out_degree() if d == 0]
    path_list = []
    for leaf in leaf_vertex:
        for path in nx.all_simple_paths(graph, source=topological_order[0], target=leaf ):
            path_list.append(path)

    # print("\n\t path_list: ")
    # print_details(path_list)
   

    # path_weight = {}
    # count = 0
    # for path in path_list:
    #     w = 0
    #     dest_leaf="none"
    #     for p in path:
    #         dest_leaf=p
    #         if p in nodes_and_weights:
    #             w = w + nodes_and_weights[p]
    #         else:
    #             w = w + 0
    #     path_weight[count] = {'path':path, 'weight':w}
    #     # print(w,dest_leaf,path)
    #     count = count+1


    # print(nodes_and_weights['nh_avaibility_2_tmp == 1w0'])


    dump_path=[]
    dump_path.append(98817)
    dump_path.append(135874)
    dump_path.append(148225)
    dump_path.append(172930)
    dump_path.append(182194)
    dump_path.append(193001)
    dump_path.append(195317)
    dump_path.append(197631)
    dump_path.append(198420)
    dump_path.append(198424)
    dump_path.append(198426)
    dump_path.append(198429)


    check_ball_larus_encoding=[]
    for path in path_list:
        w = 0
        length=len(path)-1
        for i in range(length):
            weight_to_add=0
            for we in weighted_edges:
                src = we['src']
                dst = we['dst']
                weight = int(we['weight'])
                if src==path[i] and dst==path[i+1]:
                    weight_to_add=weight
                    break

            w = w + weight_to_add
        if w in dump_path:
            file_path_info.write(str(w))
            file_path_info.write("-->")
            file_path_info.write(str(path))
            file_path_info.write("\n")
            file_path_info.write("\n")
            file_path_info.write("\n")
        check_ball_larus_encoding.append(w)

    # print(len(check_ball_larus_encoding))
    pos_weights=0;
    zero_weights=0;




    # temp_list= list(range(0,198427))
    # print(len(check_ball_larus_encoding))
    # a=0
    # for i in temp_list:
    #     if i in check_ball_larus_encoding:
    #         a=0
    #     else:
    #         print(i)
    #         print("something wrongs")


    for we in weighted_edges:
        src = we['src']
        dst = we['dst']
        weight = int(we['weight'])
        if weight>0:
            pos_weights= pos_weights + 1;
            print(we)
        else:
            zero_weights= zero_weights + 1;

    # print(pos_weights)
    # print(zero_weights)
    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")


 
jsonfile = "./netcache.json"
p4filename = "./netcache.p4"
# p4filename = "./dot files/09-Traceroutable/traceroutable.p4"
augmentor(p4filename, jsonfile)