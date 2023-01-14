import random
import sys
import os
import webbrowser
import copy
import time

class open_digraph_affiche:

	def save_as_dot_file(self, path, verbose=False):
		exit_basename=path.__contains__(".dot")
		#print(exit_basename)
		if(exit_basename):
			#isExist = os.path.exists(path)
			name = os.path.basename(path)
			path=path.replace(name,"")
		else:
			name = "graph.dot"

		#print(path)
		isExist = os.path.exists(path)
		#print(isExist)
		if(isExist):
			pathf=path+"/"+name
			if(os.path.exists(pathf)):
				os.remove(pathf)
			fichier = open(pathf, "a")


		else:
			if(os.path.exists(name)):
				os.remove(name)
			fichier = open(name, "a")
		graph_name="graph_"+str(random.randint(0,10000))
		fichier.write("digraph "+graph_name+" {\n")
		if verbose:
			for node in self.nodes:
				#fichier.write(str(node)+" [label=\" label: "+self.nodes[node].get_label()+ " \\nid: " + str(node)+ "\"];\n")
				fichier.write(str(node)+" [label=\""+self.nodes[node].get_label()+"\"];")
				

		for node in self.get_nodes():
			children=node.children
			for child in children:
				for multiplicite in range(children[child]):
					fichier.write(str(node.get_id()) + " -> " + str(child) + ";\n")

		fichier.write("}\n")

		fichier.close()

	@classmethod
	def from_dot_file(cls, path) : 
		'''
		renvoie un graph a partir d'un dot file
		'''
		fichier = open(path, "r+") 
		list_ids=[]
		for ligne in fichier :
			ligne.strip()
			
			if((ligne=="") or ("{" in ligne) or ("}" in ligne) or ("digraph" in ligne) or ("[label=" in ligne ) or not("->" in ligne)):
				continue
			
			ligne=ligne.replace("\n","")
			ligne=ligne.replace(" ","")
			ligne=ligne.replace(";","")
			ligne=ligne.replace("->"," ")
			ligne_list=ligne.split()
			for i in ligne_list:
				list_ids.append(int(i))
			
			#print(ligne)
		list_ids_remove_duplicates=list(set(list_ids))
		G_new=open_digraph([],[],[node(id, "v"+str(id),{},{}) for id in list_ids_remove_duplicates])
		for i in range(0,len(list_ids)-1,2):
			G_new.add_edge(list_ids[i+1], list_ids[i])
		
	 
		fichier.close()
		
		return G_new
			
	def display (self, verbose=False):
		'''
		affiche à l'écran le graph en question
		'''
		num=str(random.randint(0,10000))
		nom=os.getcwd()+"/graph"+num
		self.save_as_dot_file( nom+".dot", verbose)
		os.system('dot -Tpdf graph'+num+'.dot -o graph'+num+'.pdf')
		webbrowser.open_new(nom+".pdf")
		os.remove(nom+".dot")
		time.sleep(1)
		os.remove(nom+".pdf")
