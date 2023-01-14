import random
import sys
import os
import webbrowser
import copy
import time

class open_digraph_dijkstra:

	def djikstra(self,src,direction=None,tgt=None):
		
		'''
		rend deux dict : 
		dist - > la distance entre src et chaque noeud
		prev - > le precedent de chaque noeud du plus coeur chemin vers src
		'''
		q=[src]
		dist = {src : 0}
		prev = {}
		while (q!=[]):

			u=(min(q,key=lambda x : dist[x]))
			if(tgt!=None and u==tgt):
				return dist,prev
			
			q.remove(u)
			if direction == None : 
				neighbors = [i for i in self.get_node_by_id(u).get_children_ids()] + [i for i in self.get_node_by_id(u).get_parent_ids()]
			if direction == 1:
				neneighbors = [i for i in self.get_node_by_id(u).get_children_ids()]
			if direction ==-1 : 
				neighbors = neighbors = [i for i in self.get_node_by_id(u).get_parent_ids()]
			for v in neighbors:
				
				if not(v in dist.keys()):
					q.append(v)
				if not(v in dist) or (dist[v]> dist[u]+1):
					dist[v]=dist[u]+1
					prev[v]=u

		return dist, prev

	def shortest_path(self,x,y):
		'''
		renvoie le plus court chemin entre x et y
		'''

		dist, prev = self.djikstra(x,tgt=y)
		chemin=[y]
		current=y
		while(current!=u):
			current=prev[current]
			chemin.append(current)
		
		return chemin[::-1]


	def ancetres_node(self,g,l):
		'''
		renvoie les ancetres d'un noeud donné
		'''
		ancetresg=self.get_node_by_id(g).get_parent_ids()
		for i in ancetresg:
			if not(i in l):
				l.append(i)
				l+=self.ancetres_node(i,l)

		return l 
		
	def ancetres_communs(self,g,g2):
		'''
		renvoie les ancetres en communs entre deux noeuds donnés 
		'''
		ancetresg=self.ancetres_node(g,[g])
		ancetresg=remove_repetition(ancetresg)
		ancetresg2=self.ancetres_node(g2,[g2])
		ancetresg2=remove_repetition(ancetresg2)
		if (not g in self.get_node_by_id(g).get_parent_ids()):
			ancetresg.remove(g)
		if (not g2 in self.get_node_by_id(g2).get_parent_ids()):
			ancetresg2.remove(g2)
		ancetrescommun=[]
		
		for i in ancetresg:
			if i in ancetresg2:
				ancetrescommun.append(i)
		
		return ancetrescommun
	def distance_ancetres(self,n1,n2):
		'''
		renvoie les distances entre chaque ancetre commun et les noeuds n1 et n2
		'''
		res={}
		k=self.ancetres_communs(n1,n2)
		
		for i in (self.ancetres_communs(n1,n2)):
			dist,prev=self.djikstra(i)
			res[i]=(dist[n1],dist[n2])
		return res

	def cofeuilles(self):
		'''
		renvoie les cofeuilles du graph
		'''
		return [i.get_id() for i in self.get_nodes() if i.get_parent_ids()==[] ]

	
	def trie_topologique(self):
		'''
		renvoie le tri topologique du graph
		'''
		copyg=self.copy()
		res=list()
		cofeuilles=copyg.cofeuilles()
		while(cofeuilles!=[]):
			
			res.append(cofeuilles)
			
			for i in cofeuilles:
				copyg.remove_node_by_id(i)
			
			cofeuilles=copyg.cofeuilles()

		if copyg.get_nodes()!=[]:
			raise Exception("graphe cyclique")
		else : 
			return res

	def profondeur_noeud(self,g):
		'''
		renvoie la profoneur d'un noeud donné du graph
		'''
		if not(g in self.get_nodes()):
			raise Exception("noeud pas dans graphe")
		for i,k in enumerate(self.trie_topologique()):
			if g.get_id() in k :
				return i+1

	def profondeur_graph(self):
		'''
		renvoie la profondeur du graph
		'''
		return len(self.trie_topologique())-1

	def longest_path(self,u,v):
		'''
		renvoie le chemin le plus court et la distance entre u et v
		'''
		trie=self.trie_topologique()
		#initialisation de dist et prev
		dist={u:0}
		prev={}
		res=[]
		trouve=False

		for i,lk in enumerate(trie):
			if trouve:
				res.append(lk)
			if u in lk : # on s'arrete quand on trouve u
				trouve=True
		flat_res = [item for sublist in res for item in sublist] # liste de tout les noeuds superieurs à u topologiquement
		i=0
		# remplie les dist et prev
		while(flat_res[i]!=v and i < len(flat_res)):
			parentsw=self.get_node_by_id(flat_res[i]).get_parent_ids()
			parentswInDist=[i for i in parentsw if i in dist.keys()]
			if parentswInDist != []:
				maxdistparent=max(parentswInDist,key=lambda x : dist[x])
				dist[flat_res[i]]=dist[maxdistparent]+1
				prev[flat_res[i]]=maxdistparent
			i=i+1
		# calcul de dist v
		parentsv=self.get_node_by_id(v).get_parent_ids()
		parentsvInDist=[i for i in parentsv if i in dist.keys()]
		if parentsvInDist != []:
				maxdistparent=max(parentsvInDist,key=(lambda x : dist[x]))
				dist[v]=dist[maxdistparent]+1
				prev[v]=maxdistparent
		#trouver le plus long chemin
		chemin=[v]
		current=v
		while(current!=u):
			current=prev[current]
			chemin.append(current)
		
		#return
		return chemin[::-1],dist[v]



def remove_repetition(l):
	res=[]
	for i in l:
		if i not in res:
			res.append(i)
	return res