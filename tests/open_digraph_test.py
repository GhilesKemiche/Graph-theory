import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.open_digraph import *


class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1:1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1:1})
        self.assertIsInstance(n0, node)

class NodeTest(unittest.TestCase):
    def setUp(self):
        self.n0 = node(0, 'a', [], [1])
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')
    def testcopy(self):
        self.assertIsNot(self.n0, self.n0.copy())

class GraphTest(unittest.TestCase):
    def setUp(self):
        
        self.ad_node_2 = node(3,"hamid_1",{},{2:1})
        self.ad_node = node(2,"hamid_2",{3:1, 16:2},{16:1})
        self.ad_node_3 = node(16,"hamid_3",{2:1},{2:2, 19:1})
        self.ad_node_4 = node(19,"hamid_4",{16:1},{})
        self.ad_node_5 = node(21,"hamid_33",{16:1},{2:1})
        self.ad_node_2_2 = node(3,"hamid_1",{},{2:1})
        self.ad_node_2_1 = node(2,"hamid_2",{3:1, 16:2},{16:1})
        self.ad_node_2_3 = node(16,"hamid_3",{2:1},{2:2, 19:1})
        self.ad_node_2_4 = node(19,"hamid_4",{16:1},{})
        self.ad_node_2_5 = node(21,"hamid_33",{16:1},{2:1})
        self.ad_node_test=node(20,"hamid_test",{},{})
        self.graph = open_digraph([3],[19],[self.ad_node,self.ad_node_2, self.ad_node_3, self.ad_node_4])
        self.graph_3 = open_digraph([3,100],[19],[self.ad_node,self.ad_node_2, self.ad_node_3, self.ad_node_4])
        self.graph_4=  open_digraph([3,20],[19],[self.ad_node,self.ad_node_2, self.ad_node_3, self.ad_node_4,self.ad_node_test])
        self.graph_2 = open_digraph([3],[19],[self.ad_node_2_1,self.ad_node_2_2, self.ad_node_2_3, self.ad_node_2_4, self.ad_node_2_5])
    def test_is_well_formed(self):
        '''graph respectant toutes les conditions'''
        self.assertTrue(self.graph.is_well_formed())
        '''mauvaise arrete/multiplicitÃ© differente'''
        self.assertFalse(self.graph_2.is_well_formed())
        '''graph dont lequel un des inputs n'existe pas dans le graph '''
        self.assertFalse(self.graph_4.is_well_formed())
        '''input sans child'''
        self.assertFalse(self.graph_3.is_well_formed())
       
        
    def test_ajooute_retire_noeud(self):
        self.graph.add_node("hamid_ajoute",{16:3}, {2:1})
        self.assertTrue(self.graph.is_well_formed())
        self.graph.remove_node_by_id(2)
        self.assertTrue(self.graph.is_well_formed())
      
    def test_ajoute_entree_sortie(self):
        self.graph.add_node_input(2)
        self.assertTrue(self.graph.is_well_formed())
        self.graph.add_node_output(19)
        self.assertTrue(self.graph.is_well_formed())
    def test_ajoute_retire_arrete(self):
        self.graph.add_edge(2,16)
        self.assertTrue(self.graph.is_well_formed())
        self.graph.remove_parallel_edges(2,16)
        self.assertTrue(self.graph.is_well_formed())

    def test_shift_indices(self):
        n=10
        ids=self.graph.get_node_ids()
        self.graph.shift_indices(n)
        ids_shif=self.graph.get_node_ids()
       #on tetste si les anciens ids +n soient egal aux nouveaux ids 
        self.assertEqual(ids_shif, list(map(lambda x:x+n, ids)))

    def test_iparralel_list(self):
        max=self.graph.max_id()
        min=self.graph.min_id()
        g=self.graph.copy()
        f=self.graph.copy()
        f_prime=f.copy()
        g_prime=g.copy()
        self.graph.iparralel_list(g, f) 
        self.assertTrue(set(f.get_node_ids()).issubset(set(self.graph.get_node_ids())))
        self.assertTrue(set(f.get_input_ids()).issubset(set(self.graph.get_input_ids())))
        self.assertTrue(set(f.get_output_ids()).issubset(set(self.graph.get_output_ids())))
        self.assertTrue(set([i + max - min +1 for i in g.get_node_ids() ]).issubset(set(self.graph.get_node_ids())))
        self.assertTrue(set([i + max - min +1 for i in g.get_input_ids() ]).issubset(set(self.graph.get_input_ids())))
        self.assertTrue(set([i + max - min +1 for i in g.get_output_ids() ]).issubset(set(self.graph.get_output_ids())))
        self.assertTrue(g== g_prime)
        self.assertTrue(f== f_prime)

    def test_djikstra(self):
        self.assertTrue(self.graph.is_well_formed())
        self.dist,self.prev=self.graph.djikstra(3)
        self.assertTrue(self.dist[2]==1 and self.prev[2]==3)
        self.assertTrue(self.dist[16]==2 and self.prev[16]==2)

    def test_parallel_list(self):
        max=self.graph.max_id()
        min=self.graph.min_id()
        g=self.graph.copy()
        f=self.graph.copy()
        f_prime=f.copy()
        g_prime=g.copy()
        res=self.graph.parralel_list(g, f)
        self.assertTrue(set(f.get_node_ids()).issubset(set(res.get_node_ids())))
        self.assertTrue(set(f.get_input_ids()).issubset(set(res.get_input_ids())))
        self.assertTrue(set(f.get_output_ids()).issubset(set(res.get_output_ids())))
        self.assertTrue(g==g_prime)
        self.assertTrue(f==f_prime)

        
        

if __name__ == '__main__': # the following code is called only when
    unittest.main() # precisely this file is run