from doctest import FAIL_FAST
from unicodedata import decimal
from modules.open_digraph import *
import math 
import random
import copy

registre="1111" #le chiffre a tester( a mettre en inputs de l'encodeur)

#Premier essaie en changeant aucun bit (ca marche bien)

pop=bool_circ.hamming_enc()
graph=bool_circ.hamming_dec().compose(pop)
for node in graph.get_nodes():
	if node.get_label()!="" and node.get_label()[0]=="x":
		node.set_label(registre[int(node.get_label()[1:])])
	if node.get_label()!="" and node.get_label()[0] == "y":
		node.set_label("")
graph.display(True)
K=bool_circ(graph.get_input_ids(),graph.get_output_ids(),graph.get_nodes())
K.regles_apply()
K.display(True)


# deuxieme essaie en changeant un bit au hasard entre 0 et 6 inclus (ca marche , cela corrige effectivement l'erreur)

pop=bool_circ.hamming_enc()
outputs=pop.get_output_ids()
node_not=pop.add_node("~",pop.get_node_by_id(outputs[4]).parents.copy(),{})
node_output=pop.add_node("",{node_not:1},{})
pop.add_output_id(node_output)
pop.remove_node_by_id(outputs[4])
graph=bool_circ.hamming_dec().compose(pop)
for node in graph.get_nodes():
	if node.get_label()!="" and node.get_label()[0]=="x":
		node.set_label(registre[int(node.get_label()[1:])])
	if node.get_label()!="" and node.get_label()[0] == "y":
		node.set_label("")
graph.display(True)
K=bool_circ(graph.get_input_ids(),graph.get_output_ids(),graph.get_nodes())
K.regles_apply()
K.display(True)

#Dernier essaie en changeant 2 bit (ca ne doit pas marcher et ca ne marche effectivement pas)

pop=bool_circ.hamming_enc()
outputs=pop.get_output_ids()
node_not=pop.add_node("~",pop.get_node_by_id(outputs[5]).parents.copy(),{})
node_output=pop.add_node("",{node_not:1},{})
pop.add_output_id(node_output)
pop.remove_node_by_id(outputs[5])
outputs=pop.get_output_ids()
node_not=pop.add_node("~",pop.get_node_by_id(outputs[4]).parents.copy(),{})
node_output=pop.add_node("",{node_not:1},{})
pop.add_output_id(node_output)
pop.remove_node_by_id(outputs[4])
graph=bool_circ.hamming_dec().compose(pop)
for node in graph.get_nodes():
	if node.get_label()!="" and node.get_label()[0]=="x":
		node.set_label(registre[int(node.get_label()[1:])])
	if node.get_label()!="" and node.get_label()[0] == "y":
		node.set_label("")
graph.display(True)
K=bool_circ(graph.get_input_ids(),graph.get_output_ids(),graph.get_nodes())
K.regles_apply()
K.display(True)
