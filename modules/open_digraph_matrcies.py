import random
import sys
import os
import webbrowser
import copy
import time



def random_rand_list(n,bound):
    return [int(random.randrange(0,bound)) for i in range(n)]

def random_int_matrix(n,bound,null_diag=True):
    M=[random_rand_list(n,bound) for i in range(n)]
    if null_diag:
        for i in range(n):
            M[i][i]=0
    return M


def random_symetric_int_matrix(n,bound,null_diag=True):
    
    if null_diag :
        M=random_int_matrix(n,bound)
    else:
        M=M=random_int_matrix(n,bound, false)
    for i in range(n-1):
        for j in range(i+1,n):
            M[i][j]=M[j][i]
    return M
        
            
def random_oriented_int_matrix(n, bound,null_diag=True):
    
    M=random_int_matrix(n,bound, null_diag)
    for i in range(n-1):
        for j in range(i+1,n):
            if (int(random.randrange(0,bound)) %2==0):
                M[i][j]=0
            else :
                M[j][i]=0
    return M

def random_triangular_int_matrix(n, bound, null_diag=True) :
    M=[]
    for i in range(n):
        M.append([])
        for j in range(n) :
            if (i>j) or (i==j and null_diag) :
                M[i].append(0)
            else :
                M[i].append(int(random.randrange(0,bound)))
    return M





def random_graph(n, bound, inputs=0, outputs=0, form="free"):
    
    if form=="free":
        M= random_int_matrix(n,bound,null_diag=False)
    elif form=="DAG":
        M=random_triangular_int_matrix(n,bound)
    elif form=="oriented":
        M= random_oriented_int_matrix(n,bound)
    elif form=="loop-free":
        M= random_int_matrix(n,bound)
    elif form=="undirected":
        M= random_symetric_int_matrix(n,bound,null_diag=False)
    elif form=="loop-free undirected":
        M=random_symetric_int_matrix(n,bound)
    G=graph_from_adjacency_matrix(M,n)
    for i in range(inputs):
        id_child=G.random_id_node()
        while(id_child in G.get_input_ids()):
            id_child=G.random_id_node()
        G.add_node_input(id_child)
    for i in range(outputs):
        id_parent=G.random_id_node()
        while(id_parent in G.get_output_ids()):
            id_parent=G.random_id_node()
        G.add_node_output(id_parent)
    return G