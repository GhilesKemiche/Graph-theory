import random
import sys
import os
import webbrowser
import copy
import time

class open_digraph_compose:

	def min_id(self):
		'''
		rend l'id min present dans le graph
		'''
		return min(self.get_node_ids(),default=0)

	def max_id(self):
		'''
		rend l'id max present dans le graph
		'''
		return max(self.get_node_ids(),default=0)

	def shift_indices(self,n):
		'''
		shift tout les indices d'une certaine valeurs n donnée
		'''
		dictn={}
		for node in self.get_nodes():
			old_id=node.get_id()
			child={idc+n:node.children[idc] for idc in node.get_children_ids()}
			parent={idc+n:node.parents[idc] for idc in node.get_parent_ids()}
			node.set_parent_ids(parent)
			node.set_children_ids(child)
			node.set_id(node.get_id()+n)
			dictn[node.get_id()]=node
			
		inputs=[i+n for i in self.get_input_ids()]
		output=[i+n for i in self.get_output_ids()]
		self.set_output_ids(output)
		self.set_input_ids(inputs)
		self.nodes=dictn

	def iparralel(self,g):
		'''
		ajoute un graph donné parrallement au graph initial sans modification du graph donné
		'''
		max_id_g=g.max_id()
		min_id_g=g.max_id()
		min_id_self=self.min_id()
		max_id_self=self.max_id()
		self.shift_indices(max_id_g - min_id_self+1)
		self.set_output_ids(self.get_output_ids()+g.get_output_ids())
		self.set_input_ids(self.get_input_ids()+g.get_input_ids())
		nodez=map(lambda x : x.copy() ,g.nodes.values())
		nodes = {node.id:node for node in nodez}
		self.nodes.update(nodes)
	
	def parralel(self,g):
		'''
		renvoie un graph composé du graph initial et d'un autre donné placé parrallelement sans qu'ils soient modifiés
		'''
		new=self.__class__.origin()
		new.iparralel(self)
		new.iparralel(g)
		return new

	def icompose(self,g):
		'''
		compose deux graphes en connectant les inputs de l'un aux outputs de l'autre
		'''
		if(len(self.get_input_ids()) != len(g.get_output_ids())):
			raise Exception("nombre d'entrées différent")
		max_id_g=g.max_id()
		min_id_g=g.min_id()
		min_id_self=self.min_id()
		max_id_self=self.max_id()
		self.shift_indices(max_id_g - min_id_self+1)
		list_self_inputs=self.get_input_ids()
		list_g_outputs=g.get_output_ids()
		nodez=map(lambda x : x.copy() ,g.nodes.values())
		nodes = {node.id:node for node in nodez}
		self.nodes.update(nodes)
		
		for i in range(len(list_self_inputs)):
			self.add_edge(list_self_inputs[i],list_g_outputs[i])
		self.set_input_ids(g.get_input_ids())


	def compose(self,g):
		new=self.copy()
		newg=g.copy()
		new.icompose(newg)

		return new

	def parcours_dict(self,dict,node,k,nodes_notseen):
		if node in nodes_notseen: 
			dict[node.get_id()]=k
			nodes_notseen.remove(node)
			children_ids=node.get_children_ids()
			parents_ids=node.get_parent_ids()
			
			for i in children_ids:
				
				self.parcours_dict(dict,self.get_node_by_id(i),k,nodes_notseen)
			for j in parents_ids:
				self.parcours_dict(dict,self.get_node_by_id(j),k,nodes_notseen)


	def connected_components(self):
		dict={}
		nodes_notseen=self.get_nodes()

		k=0
		while(nodes_notseen!=[]):
			current_node=nodes_notseen[0]
			self.parcours_dict(dict,current_node,k,nodes_notseen)
			seen=[self.get_node_by_id(key) for key,v in dict.items() if v==k]
			k=k+1
			
		return (k,dict)

	

	def iparralel_list(self,*args):
		for i in args:
			self.iparralel(i)

	def parralel_list(self,*args):
		new=self.__class__.origin()
		new.iparralel(self)
		for argk in args:
			new.iparralel(argk)
		return new