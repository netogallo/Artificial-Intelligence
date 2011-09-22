import unittest
from GraphLib import Graph,Node,astar

#Tests for the graph search algorithms, generates images

class TestGraphSearch(unittest.TestCase):

    def setUp(self):
        f= gzip.open('map1c.p.gz','rb')
        Graph.map1c= pickle.load(f)
        self.start_pt=Node(330,316)
        g1=Node(1068,1110)
        g2=Node(680,800)
        g3=Node(653,987)
        self.goals= [g1,g2,g3]

        
    def testAStarDiagonals(self):

        Graph.diagonals=True
        Graph.step=4
        
        #Run A* with the specified start point and goals, note that
        #the first goal in the list will be used for heuristics.
        r=astar(self.start_pt,self.goals)
        
        print r
