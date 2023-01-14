import random
import sys
import os
import webbrowser
import copy
import time
from math import *
import numpy as np

from modules.open_digraph_dijkstra import open_digraph_dijkstra
from modules.open_digraph_compose import open_digraph_compose
from modules.open_digraph_affiche import open_digraph_affiche
from modules.open_digraph_registres import open_digraph_registres


class node:

	def __init__(self, identity, label, parents, children):
		'''
		identity: int; its unique id in the graph
		label: string;
		parents: int->int dict; maps a parent node's id to its multiplicity
		children: int->int dict; maps a child node's id to its multiplicity
		'''
		self.id = identity
		self.label = label
		self.parents = parents
		self.children = children

	def __str__(self):
		'''
		fonction d'affichage 
		'''
		return f'id : {self.id} , label : {self.label} , parents : {self.parents} , children : {self.children}'
	def __repr__(self):
		'''
		fonction affichage inductive
		'''
		return f'id : {self.id} , label : {self.label} , parents : {self.parents} , children : {self.children}'

	def __eq__(self, g):
		return (self.id==g.id) and (self.label==g.label) and (self.parents==g.parents) and (self.children==g.children)

	
	def copy(self) :
		'''
		return une copie du noeud
		'''
		return node(self.id, self.label, self.parents.copy(), self.children.copy())
	
	def get_id(self):

		'''
		return l'id du noeud
		'''
		return self.id
	
	def get_label(self):

		'''
		return le label du noeud
		'''
		return self.label
	
	def get_children_ids(self):
		'''
		return les clés du dictionnaire des children autrement dit les ids des children
		'''
		return list(self.children.keys())
	'''    
	def get_children_ids(self):
		return self.children
	'''
	def get_parent_ids(self):

		'''
		return les clés du dictionnaire des parents autrements dit les ids des parents
		'''
		return list(self.parents.keys())

	def set_id(self, id):
		'''
		prend en argument un id 
		et
		set/modifie l'id du noeud
		'''
		self.id=id

	def set_label(self, label):
		'''
		prend en argument un label 
		et
		set/modifie l'id du noeuf
		'''
		self.label=label

	def set_parent_ids(self, parents):
		'''
		prend en argument des ids de parents
		et
		set/modifie les parents
		'''
		self.parents=parents

	def set_children_ids(self, children):
		'''
		prend en argument des ids de children
		et
		set/modifie les children
		'''
		self.children=children

	def remove_parent_once(self,idp):
		'''
		prend un id de noeud et retire une arrete parent/enfant avec le noeud équivalent
		'''
		if idp in self.parents:
			self.parents[idp]=self.parents[idp]-1
			if self.parents[idp] <= 0 :
				self.parents.pop(idp) 

	def remove_child_once(self,idc):
		'''
		prend un id : idc
		retire une arrete enfant/parent avec le noeud équivalent
		'''
		if idc in self.children:
			self.children[idc]=self.children[idc]-1
			if self.children[idc] <= 0 : 
				self.children.pop(idc)

	def remove_parent_id(self,idp):
		'''
		prend un id : idp
		retire toutes les arretes du parent d'id idp
		'''
		if idp in self.parents.keys():
			self.parents.pop(idp)

	def remove_child_id(self,idc):
		'''
		prend un id : idc
		retire toutes les arretes du child d'id idc
		'''
		if idc in self.children.keys():
			self.children.pop(idc)

	def indegree(self):
		return sum(self.parents.values())
	
	def outdegree(self):
		return sum(self.children.values())
	
	def degree(self):
		return self.indegree()+self.outdegree()
		

class open_digraph(open_digraph_dijkstra,open_digraph_affiche,open_digraph_compose): # for open directed graph
	def __init__(self, inputs, outputs, nodes):
		'''
		inputs: int list; the ids of the input nodes
		outputs: int list; the ids of the output nodes
		nodes: node iter;
		'''
		self.inputs = inputs
		self.outputs = outputs
		self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict

	def __str__(self):
		'''
		fonction d'affichage 
		'''
		return f'id : {self.inputs} ,outputs : {self.outputs} nodes : {self.nodes}'

	def __repr__(self):
		'''
		fonction d'affichage inductif
		'''
		if isinstance(self, list):
			for i in self:
				__repr__(i)
		else:
			__str__(self)

	def __eq__(self, g):
		return (self.inputs == g.inputs) and (self.outputs == g.outputs ) and (self.nodes == g.nodes )



	@classmethod
	def origin(cls): 
		return cls([],[],{})

	
	def copy(self) :
		nodez=map(lambda x : x.copy() ,self.nodes.values())

		return open_digraph(self.inputs.copy(), self.outputs.copy(), nodez)

	def get_input_ids(self):
		return self.inputs

	def get_output_ids(self):
		return self.outputs

	def get_id_node_map(self):
		return self.nodes

	def get_nodes(self):
		return list(self.nodes.values())
	
	def get_node_ids(self):
		return list(self.nodes.keys())
	
	def get_node_by_id(self, id):
		if id in self.get_node_ids() :
			return self.nodes[id]
		raise Exception("Sorry, no id in the graph")
	
	def get_nodes_by_ids(self, ids):
		return [self.get_node_by_id(id) for id in ids]
	
	def set_input_ids(self, inputs):
		self.inputs=inputs
		
	def set_output_ids(self, outputs):
		self.outputs=outputs
		
	def add_input_id(self, id):
		self.inputs.append(id)
		
	def add_output_id(self, id):
		self.outputs.append(id)
		
	def new_id (self):
		'''
		crée un nouvel id
		'''
		m=0
		l=self.get_node_ids()+ self.get_input_ids() +self.get_output_ids()
		if l!=[]:
			m=l[0]
			while (m in l):
				m=m+1
		return m
	def clean(self):
		'''
		fonction qui supprime les inputs et outputs sans enfant/parent
		'''
		for node in self.get_nodes():
			if(node.get_children_ids()==[] and node.get_parent_ids()==[] and ((node.get_id() in self.get_input_ids()) or (node.get_id() in self.get_output_ids()) )):
				self.nodes.pop(node.get_id())
				if node.get_id() in self.get_input_ids():
					self.inputs.remove(node.get_id())
				if node.get_id() in self.get_output_ids():
					self.outputs.remove(node.get_id())
	def add_edge(self, src, tgt):
		'''
		ajoute une arrete qui va de tgt a src
		'''
		src_node=self.get_node_by_id(src)
		tgt_node=self.get_node_by_id(tgt)
		if tgt in src_node.parents.keys():
			src_node.parents[tgt]=src_node.parents[tgt]+1
		else :
			src_node.parents[tgt]=1
			
		if src in tgt_node.children.keys():
			tgt_node.children[src]=tgt_node.children[src]+1
		else :
			tgt_node.children[src]=1
		
	def add_node(self, label=" ", parents={},children={}):
		'''
		crée un node avec label et parents/enfants données
		'''
		id=self.new_id()
		new_node=node(id, label, {}, {})
		self.nodes[new_node.get_id()]=new_node
		for i in parents.keys() :
			for j in range(parents[i]):
				self.add_edge(new_node.get_id(), i)
			
		for i in children.keys() :
			for j in range(children[i]):
				self.add_edge(i, new_node.get_id())
		return id

	def remove_edge(self,src,tgt):
		'''
		enleve une arrete qui part de src a tgt
		'''
		tgt_node = self.get_node_by_id(tgt)
		src_node = self.get_node_by_id(src)
		tgt_node.remove_parent_once(src)
		src_node.remove_child_once(tgt)
		if tgt in self.get_input_ids():
			self.inputs.remove(tgt)
		if src in self.output_ids():
			self.outputs.remove(src)

	def remove_parallel_edges(self,src,tgt):
		'''
		retire toutes les arretes de src a tgt
		'''
		tgt_node = self.get_node_by_id(tgt)
		src_node = self.get_node_by_id(src)
		tgt_node.remove_parent_id(src)
		src_node.remove_child_id(tgt)
		if tgt in self.get_input_ids():
			self.inputs.remove(tgt)
		if src in self.get_output_ids():
			self.outputs.remove(src)
	def remove_node_by_id(self,*args):
		'''
		remove des nodes du graph
		'''

		for arg in args:
			if arg in self.get_input_ids():
				self.inputs.remove(arg)
			if arg in self.get_output_ids():
				self.outputs.remove(arg)
			if arg in self.nodes.keys():
				nodearg=self.get_node_by_id(arg)
				copy_parent=copy.copy(nodearg.parents)
				copy_children=copy.copy(nodearg.children)

				for k in copy_parent.keys():
					self.remove_parallel_edges(k,arg)
				for j in copy_children.keys():
					self.remove_parallel_edges(arg,j)
				self.nodes.pop(arg)
		self.clean()


	def input_output_in_graph(self):
		'''
		verifie que les inputs et les outputs sont dans le graph
		'''
		ids_node=self.get_node_ids()

		for i in self.inputs:
			if not(i in ids_node) :
				return False
		for j in self.outputs:
			if not(j in ids_node):
				return False
		return True

	def inputs_child_one(self):
		'''
		verifie qu'il a un enfant a une multipilicité
		'''
		ids=self.get_input_ids()
		nodes = self.get_nodes_by_ids(ids)
		for node in nodes : 
			if not(len(node.get_children_ids())==1) or not(len(node.get_parent_ids())==0):
				return False
			

			if not(node.children[node.get_children_ids()[0]]==1):
				return False
		return True

	def outputs_parent_one(self):
		'''
		verifie qu'il a un parent a une multipilicité
		'''
		ids=self.get_output_ids()
		nodes = self.get_nodes_by_ids(ids)
		for node in nodes :
			if not(len(node.get_parent_ids())==1) or not(len(node.get_children_ids())==0):
				return False

			if not(node.parents[node.get_parent_ids()[0]]==1):
				return False
		return True

	def cle_nodes_exist(self):
		'''
		chaque node a son id comme clé dans nodes
		'''
		for i in self.get_node_ids():
			if self.nodes[i].get_id()!=i :
				return False
		return True

	def same_multiple_nodes(self):
		'''
		verifie que les multiplicités des arretes sont respectés d'un noeud a l'autre 
		'''
		nodes=self.get_nodes()
		for node in nodes :
			node_id= node.get_id()
			ids_parents_node = node.get_parent_ids()
			ids_children_node = node.get_children_ids()
			for i in ids_parents_node : 
				if not((i in self.nodes)): 
					return False
				if not((node_id in self.get_node_by_id(i).get_children_ids())) :
					return False
				if  not(node.parents[i]==self.get_node_by_id(i).children[node_id]):
					return False
			for j in ids_children_node : 
				if not((j in self.nodes)):
					return False
				
				if not((node_id in self.get_node_by_id(j).get_parent_ids())) :
					return False
				if not(node.children[j]==self.get_node_by_id(j).parents[node_id]):
					return False

		return True


	def is_well_formed(self):
		'''
		verifie que le graph est bien formé
		'''
		return self.input_output_in_graph() and self.inputs_child_one() and self.outputs_parent_one() and self.cle_nodes_exist() and self.same_multiple_nodes()

	def random_id_node(self):
		return random.choice(self.get_node_ids())

	def add_node_input(self,idc, label=""):
		'''
		ajoute un input avec une arrete vers le noeud d'id idc
		'''
		if idc in self.get_input_ids():
			self.inputs.remove(idc)
		if not(idc in self.get_node_ids()):
			raise Exception("Sorry, no id in the graph")
		children_node={idc:1}
		id_node=self.new_id()
		self.add_node(label,{},children_node)
		self.set_input_ids(self.get_input_ids()+[id_node])

	def add_node_output(self,idp,label=""):
		'''
		ajoute un output avec une arrete vers le noeud d'id idp
		'''
		if idp in self.get_output_ids():
			self.outputs.remove(idp)
		if not(idp in self.get_node_ids()):
			raise Exception("Sorry , no id in the graph")
		parents_node={idp:1}
		id_node=self.new_id()
		self.add_node(label,parents_node,{})
		self.set_output_ids(self.get_output_ids()+[id_node])

	
	def is_cyclic(self):
		'''
		rend True si le graph est cyclique , False autrement
		'''
		gcopy = self.copy()
		cyclic= True
		while(cyclic):
			retire=False
			if gcopy.nodes == {} : 
				cyclic=False
				break
			nodez=copy.copy(gcopy.nodes)
			for i in nodez.values():
				if i.children=={}:
					gcopy.remove_node_by_id(i.get_id())
					retire=True
			if not(retire) : 
				break
		return cyclic 

	
	
	@classmethod
	def id_dict(self):
		dict_id={}
		nodes_ids=self.get_node_ids()
		for i in range(len(nodes_ids)):
			dict_id[node_id[i]]=i
		return dict_id

	@classmethod
	def adjacency_matrix(self):
		dict_id=self.id_dict()
		l=len(dict_id.keys())
		M=np.zeros((l,l))
		for i in self.get_nodes():
			id_i=i.get_id()
			for j in i.get_children_ids():
				M[i][j]=i.children[j]
			for k in i.get_parent_ids():
				M[i][k]=i.children[k]
		return M
	
	def connnexe_compose(self):
		k,v=self.connected_components()
		list_g=[]
		for i in range(k):
			newg=open_digraph.origin()
			seen={key:self.get_node_by_id(key) for key,value in v.items() if value==i}
			newg.nodes.update(seen)
			#inputs_g inputs deja vu
			inputs_g=[value.id for key,value in seen.items() if  (((len(value.get_children_ids())==1) and (len(value.get_parent_ids())==0)) and (value.children[value.get_children_ids()[0]]==1))]
			ouputs_g=[value.id for key,value in seen.items() if  (((len(value.get_parent_ids())==1) and (len(value.get_children_ids())==0)) and ((value.parents[value.get_parent_ids()[0]]==1)))]
			newg.set_output_ids(ouputs_g)
			newg.set_input_ids(inputs_g)
			list_g.append(newg)
		return list_g

	def fusionne_noeuds(self,id1,id2):
		'''
		fusionne deux noeuds
		'''
		if(not(id1 in self.get_node_ids()) or not(id2 in self.get_node_ids())):
			raise Exception("id pas dans le graph")
		node2=self.get_node_by_id(id2)
		node1=self.get_node_by_id(id1)
		children1=node1.children
		parents1=node1.parents
		children2=node2.children
		parents2=node2.parents
		
		for i in children2.keys():
			if i in children1.keys():
				children1[i]+=children2[i]
			else : 
				children1[i]=children2[i]
		for j in parents2.keys():
			if j in parents1.keys():
				parents1[j]+=parents2[j]
			else : 
				parents1[j]=parents2[j]
		new_id=self.new_id()
		self.add_node(node1.get_label(),parents1,children1)
		self.remove_node_by_id(id1)
		self.remove_node_by_id(id2)
		return new_id

	



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
	
def graph_from_adjacency_matrix(M,n):
	graph=open_digraph([],[],[node(i,"v"+str(i),{},{}) for i in range(n)])
	l=graph.get_node_ids()
	for i in range(n):
		for j in range(n):
			for k in range(M[i][j]):
				graph.add_edge(l[j], l[i])
	for i in graph.get_nodes():
		if i.get_children_ids()==[] and len(i.get_parent_ids())==1 and i.parents[i.get_parent_ids()[0]]==1:
			graph.outputs.append(i.get_id())
		if i.get_parent_ids()==[] and len(i.get_children_ids())==1 and i.children[i.get_children_ids()[0]]==1:
			graph.inputs.append(i.get_id())
	return graph 

	
	




class bool_circ(open_digraph,open_digraph_registres):
	
	def __init__(self,inputs, outputs, nodes):

		self.inputs = inputs
		self.outputs = outputs
		self.nodes = {node.id:node for node in nodes} 
		self.identify={}
		if not(self.is_well_formed_circ()):
			raise Exception("n'est pas un circuit boolean")

	def get_identify(self):
		return self.identify		


	@classmethod
	def origin(cls): 
		return cls([],[],[])

	def is_well_formed_circ(self):
		if not(self.is_well_formed):
			return False
		for node in self.nodes.values():
			if (node.label== "1" or node.label== "0")and not(node.get_id() in self.get_input_ids()):
				return False
			if node.label=="" and not(node.indegree()==1) : 
				return False 
			if (node.label=="&" or node.label=="|" or node.label=="^") and not(node.outdegree()==1):
				return False
			if (node.label=="~") and not(node.indegree()==1) and not(node.outdegree()==1):
				return False
		return not(self.is_cyclic())  

	

	def parse_parentheses_bis(self,s):
		g = open_digraph([],[1],[node(0,"",{},{1:1}),node(1,"",{0:1},{})])
		current_node=0
		s2=""
		for char in s :
			if char=='(':
				current_node_n=g.get_node_by_id(current_node)
				if current_node_n.get_label()=="":
					current_node_n.set_label(current_node_n.get_label()+s2)
				k=current_node
				current_node=g.new_id()
				g.add_node("",{},{k:1})
				s2=""
			elif char ==')':
				current_node_n=g.get_node_by_id(current_node)
				current_node_n.set_label(current_node_n.get_label()+s2)
				current_node=current_node_n.get_children_ids()[0]
				s2=""
			else : 
				s2+=char
		res=bool_circ(g.inputs,g.outputs,g.get_nodes())
		
		res.fusionne_nodes_graph()
		res.insert_copies()



		return res
	def insert_copies(self):
		'''
		insert les copies necessaires a parse parentheses
		'''
		resnodes=self.get_nodes()
		
		for i in range(len(resnodes)):
			if resnodes[i].get_label()!="" and resnodes[i].get_label()!="&" and resnodes[i].get_label()!="|" and resnodes[i].get_label()!="" and resnodes[i].get_label()!="^" and resnodes[i].get_label()!="~":
				self.identify[resnodes[i].get_label()]=resnodes[i].get_id()
				new_id=self.new_id()
				self.add_node("",{},{resnodes[i].get_id():1})
				self.add_input_id(new_id)
				resnodes[i].set_label("")
		



	def fusionne_nodes_graph(self):
		'''
		fusionnes les noeufs du graphs similaires
		'''
		resnodes=self.get_nodes()
		for i in range(len(resnodes)):
			# si le noeud n'est pas un operateur
			if resnodes[i].get_label()!="&" and resnodes[i].get_label()!="|" and resnodes[i].get_label()!="" and resnodes[i].get_label()!="^" and resnodes[i].get_label()!="~":

				for j in range(i+1,len(resnodes)):
					if resnodes[i].get_label()==resnodes[j].get_label():
						print(resnodes[i].get_id(),resnodes[j].get_id())

						id_n=self.fusionne_noeuds(resnodes[i].get_id(),resnodes[j].get_id())
						resnodes[i]=self.get_node_by_id(id_n)
						resnodes[j].set_label("") # changement de label pour ne pas refusionner un noeud qui a été supprimé (affectation None ne fonctionne pas)

	
	def parse_parentheses(self,*args):
		'''
		genere un graph a partir de strings
		'''
		G = bool_circ.origin()
		for argk in args:
			
			G.iparralel(G.parse_parentheses_bis(argk))
		
		G.fusionne_nodes_graph()
		G.insert_copies()

		return G

	@classmethod
	def random_bool_circ(cls,n,bound,inputs,outputs):
		'''
		rend un boul circ avec n noeud au minimum, bound max d'arretes , un nombre 'inputs' d'inputs et 'outputs' d'outputs
		'''
		M = random_triangular_int_matrix(n,bound)
		graph = graph_from_adjacency_matrix(M,n)

		while(len(graph.get_input_ids()) > inputs):
			inputs_graph = graph.get_input_ids()
			random_inputs = random.sample(inputs_graph,k = 2)
			new_id = graph.new_id()
			graph.add_node(graph.get_node_by_id(random_inputs[0]).get_label() + graph.get_node_by_id(random_inputs[1]).get_label(),{},{random_inputs[0]:1,random_inputs[1]:1})
			graph.inputs.pop(random_inputs[0])
			graph.inputs.pop(random_inputs[1])
			new_id2 = graph.new_id()
			graph.add_node(graph.get_node_by_id(random_inputs[0]).get_label() + graph.get_node_by_id(random_inputs[1]).get_label() + "bis",{},{new_id:1})
			graph.inputs.append(new_id2)
		while(len(graph.get_input_ids()) < inputs):
			nodes_not_inputs = [node for node in graph.get_node_ids() if node not in graph.get_input_ids()]
			random_nodes = random.sample(nodes_not_inputs,k = 1)
			new_id = graph.new_id()
			graph.add_node(graph.get_node_by_id(random_nodes[0]).get_label() + "input",{},{random_nodes[0]:1})
			graph.inputs.append(new_id)
		while(len(graph.get_output_ids()) > outputs):
			outputs_graph=graph.get_output_ids()
			random_outputs = random.sample(outputs_graph, k = 2)
			new_id=graph.new_id()
			graph.add_node(graph.get_node_by_id(random_outputs[0]).get_label() + graph.get_node_by_id(random_outputs[1]).get_label(),{random_outputs[0]:1,random_outputs[1]:1},{})
			graph.outputs.pop(random_outputs[0])
			graph.outputs.pop(random_outputs[1])
			graph.inputs.pop(random_inputs[1])
			new_id2 = graph.new_id()
			graph.add_node(graph.get_node_by_id(random_outputs[0]).get_label() + graph.get_node_by_id(random_outputs[1]).get_label() + "bis",{},{new_id:1})
			graph.outputs.append(new_id2)
		while(len(graph.get_output_ids()) < outputs):
			nodes_not_outputs = [node for node in graph.get_node_ids() if node not in graph.get_output_ids()]
			random_nodes = random.sample(nodes_not_inputs,k = 1)
			new_id = graph.new_id()
			graph.add_node(graph.get_node_by_id(random_nodes[0]).get_label() + "output",{random_nodes[0]:1},{})
			graph.outputs.append(new_id)

		op_binaires=["&","|"]
		nodes=graph.get_nodes()
		for node in nodes:
			if(node.indegree() == 1 and node.outdegree() == 1):
				node.set_label("~")
			if(node.indegree() == 1 and node.outdegree() > 1):
				node.set_label("")
			if(node.indegree() > 1 and node.outdegree() == 1):
				node.set_label(random.sample(op_binaires,k = 1)[0])
			if(node.indegree() > 1 and node.outdegree() > 1):
				id_uop=graph.new_id()
				graph.add_node(random.sample(op_binaires,k = 1)[0],node.parents,{})
				graph.add_node("",{id_uop:1},node.children)
				graph.remove_node_by_id(node.get_id())



		return bool_circ(graph.get_input_ids(),graph.get_output_ids(),graph.get_nodes())
	

	@classmethod
	def hamming_enc(cls):
		G=cls.origin()
		node_x0=G.add_node("x0")
		node_x0_copie=G.add_node("",{node_x0:1},{})
		node_x1=G.add_node("x1")
		node_x1_copie=G.add_node("",{node_x1:1},{})
		node_x2=G.add_node("x2")
		node_x2_copie=G.add_node("",{node_x2:1},{})
		node_x3=G.add_node("x3")
		node_x3_copie=G.add_node("",{node_x3:1},{})
		G.add_input_id(node_x0)
		G.add_input_id(node_x1)
		G.add_input_id(node_x2)
		G.add_input_id(node_x3)
		node_xor_013=G.add_node("^",{node_x3_copie:1,node_x1_copie:1,node_x0_copie:1},{})
		node_xor_023=G.add_node("^",{node_x3_copie:1,node_x2_copie:1,node_x0_copie:1},{})
		node_xor_123=G.add_node("^",{node_x3_copie:1,node_x1_copie:1,node_x2_copie:1},{})
		node_copie_xor_013=G.add_node("",{node_xor_013:1},{})
		node_copie_xor_023=G.add_node("",{node_xor_023:1},{})
		node_copie_xor_123=G.add_node("",{node_xor_123:1},{})
		node_copie_output_x0=G.add_node("",{node_x0_copie:1},{})
		node_copie_output_x1=G.add_node("",{node_x1_copie:1},{})
		node_copie_output_x2=G.add_node("",{node_x2_copie:1},{})
		node_copie_output_x3=G.add_node("",{node_x3_copie:1},{})
		G.add_output_id(node_copie_output_x3)
		G.add_output_id(node_copie_output_x2)
		G.add_output_id(node_copie_output_x1)
		G.add_output_id(node_copie_output_x0)
		G.add_output_id(node_copie_xor_013)
		G.add_output_id(node_copie_xor_023)
		G.add_output_id(node_copie_xor_123)

		return G

	@classmethod
	def hamming_dec(cls):
		G=cls.origin()
		node_x0=G.add_node("y0")
		node_x1=G.add_node("y1")
		node_x2=G.add_node("y2")
		node_x2_copie=G.add_node("",{node_x2:1},{})
		node_x3=G.add_node("y3")
		node_x4=G.add_node("y4")
		node_x4_copie=G.add_node("",{node_x4:1},{})
		node_x5=G.add_node("y5")
		node_x5_copie=G.add_node("",{node_x5:1},{})
		node_x6=G.add_node("y6")
		node_x6_copie=G.add_node("",{node_x6:1},{})
		G.add_input_id(node_x0)
		G.add_input_id(node_x1)
		G.add_input_id(node_x2)
		G.add_input_id(node_x3)
		G.add_input_id(node_x4)
		G.add_input_id(node_x5)
		G.add_input_id(node_x6)
		node_xor0246=G.add_node("^",{node_x0:1,node_x2_copie:1,node_x4_copie:1,node_x6_copie:1},{})
		node_xor0246_copie=G.add_node("",{node_xor0246:1},{})
		node_xor1256=G.add_node("^",{node_x1:1,node_x2_copie:1,node_x5_copie:1,node_x6_copie:1},{})
		node_xor1256_copie=G.add_node("",{node_xor1256:1},{})
		node_xor3456=G.add_node("^",{node_x3:1,node_x4_copie:1,node_x5_copie:1,node_x6_copie:1},{})
		node_xor3456_copie=G.add_node("",{node_xor3456:1},{})
		node_not_xor3456=G.add_node("~",{node_xor3456_copie:1},{})
		node_and_xor_not3=G.add_node("&",{node_not_xor3456:1,node_xor1256_copie:1,node_xor0246_copie:1},{})
		node_xor_and3_xor=G.add_node("^",{node_and_xor_not3:1,node_x2_copie:1},{})
		node_xor_and3_xor_r=G.add_node("r0",{node_xor_and3_xor:1},{})
		G.add_output_id(node_xor_and3_xor_r)
		node_not_1256=G.add_node("~",{node_xor1256_copie:1},{})
		node_and_xor_not2=G.add_node("&",{node_xor0246_copie:1,node_not_1256:1,node_xor3456_copie:1},{})
		node_xor_and2_xor=G.add_node("^",{node_and_xor_not2:1,node_x4_copie:1},{})
		node_xor_and2_xor_r=G.add_node("r1",{node_xor_and2_xor:1},{})
		G.add_output_id(node_xor_and2_xor_r)
		node_not_0246=G.add_node("~",{node_xor0246_copie:1},{})
		node_and_xor_not1=G.add_node("&",{node_xor1256_copie:1,node_not_0246:1,node_xor3456_copie:1},{})
		node_xor_and1_xor=G.add_node("^",{node_and_xor_not1:1,node_x5_copie:1},{})
		node_xor_and1_xor_r=G.add_node("r2",{node_xor_and1_xor:1},{})
		G.add_output_id(node_xor_and1_xor_r)
		node_and_xor_f=G.add_node("&",{node_xor1256_copie:1,node_xor0246_copie:1,node_xor3456_copie:1},{})
		node_xor_xor_f=G.add_node("^",{node_and_xor_f:1,node_x6_copie:1})
		node_xor_xor_f_r=G.add_node("r3",{node_xor_xor_f:1},{})
		G.add_output_id(node_xor_xor_f_r)

		return G





def remove_repetition(l):
	res=[]
	for i in l:
		if i not in res:
			res.append(i)
	return res


def tab_vrt(s):
	'''
	on donne une chaine et ca renvoie la table de vert associee
	'''
	ligne=len(s)
	if (not log2(ligne)==float(int(log2(ligne)))):
		raise Exception("la chaine ne represente pas une puissance de deux, la table n'est pas valide ")

	colonne=log2(ligne)
	l=[]
	
	for i in range(ligne):
		k=bin(i)
		k=k[2:]
		k='0'*(int(colonne)-len(k))+k
		col=[]
		
		for j in range(int(colonne)):
			col.append(k[j])

		
		col.append(s[i])
		
		l.append(col)

	return l

def circ_ligne(l):
	'''
	on lui donne une ligne de la table de verite et ça renvoie la chaine de carecterer correspondante 
	'''
	s=""
	if l[-1]=='1':
		for i in range(len(l)-1):
			if l[i]=='0':
				if not(i==len(l)-2):
					s+='(~(x'+str(i)+'))&'
				else :
					s+='(~(x'+str(i)+'))'
			else :
				if not(i==len(l)-2):
					s+='(x'+str(i)+')&'
				else :
					s+='(x'+str(i)+')'
		s='('+s+')'	
	return s

def tab_vrt_vers_graph(s):
	'''

	transforme un string de tab de verité en string de variables utilisable

	'''
	tab=tab_vrt(s)
	ss=""
	for i in range(len(tab)) :
		if tab[i][-1]=='1':
			if not(i==len(tab)-1):
				ss+=circ_ligne(tab[i])+'|'
			else :
				ss+=circ_ligne(tab[i])
	ss='('+ss+')'
	
	return ss