#Graph Seach Test Cases
#
#This file contains the test cases for the implementation
#of A* and Dijkstra algorithmos. The do the search on a
#map of a laboratory.
#
#Question 1:
#
#There are many paths with the same cost that lead to the goal.
#That's why not every algorithm will choose the same path. The
#chosen paths depends on how the fronteer decides which node
#to expand.

import unittest
from GraphLib import Graph
from GraphLib.Graph import Node
from GraphLib.GraphSearch import graphSearch
import pickle
import gzip
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#Tests for the graph search algorithms, generates images

class TestGraphSearch(unittest.TestCase):

    map1c= pickle.load(gzip.open('map1c.p.gz','rb'))
        
    def testAStarDiagonals(self):

        #Run A* with the specified start point and goals, note that
        #the first goal in the list will be used for heuristics.

        g1=Node(1068,1110)
        g2=Node(680,800)
        g3=Node(653,987)
        
        #create a node with a goal for heuristics
        self.start_pt=Node(330,316,graph=TestGraphSearch.map1c,cost=0,parent=None,goal=g1,step=4,diagonals=True)               
        self.goals= [g1,g2,g3]

        r=graphSearch(self.start_pt,self.goals)
        
        #print(r)

        img=TestGraphSearch.map1c.copy()

        for node in r[0]:
            img[node.x,node.y]=15

        #imgplot = plt.imshow(img, 'binary_r')
        imgsave = plt.imsave('map_path_aStar_Diagonals.png',img)
        #plt.show()

        print("The cost of the search A* with diagonals: "+r[0][-1].cost().__str__())

    def testAStar(self):

        #Run A* with the specified start point and goals, note that
        #the first goal in the list will be used for heuristics.

        g1=Node(1068,1110)
        g2=Node(680,800)
        g3=Node(653,987)

        #create a start node with a goal for heuristics
        self.start_pt=Node(330,316,graph=TestGraphSearch.map1c,cost=0,parent=None,goal=g1,step=4,diagonals=False) 
        self.goals= [g1,g2,g3]

        r=graphSearch(self.start_pt,self.goals)
        
        #print(r)

        img=TestGraphSearch.map1c.copy()

        for node in r[0]:
            img[node.x,node.y]=15

        #imgplot = plt.imshow(img, 'binary_r')
        imgsave = plt.imsave('map_path_aStar.png',img)
        #plt.show()

        print("The cost of the search A* without diagonals: "+r[0][-1].cost().__str__())

    def testDijkstraDiagonals(self):

        #Run A* with the specified start point and goals, note that
        #the first goal in the list will be used for heuristics.

        g1=Node(1068,1110)
        g2=Node(680,800)
        g3=Node(653,987)

        #create a start node with a goal for heuristics
        self.start_pt=Node(330,316,graph=TestGraphSearch.map1c,cost=0,parent=None,goal=None,step=4,diagonals=True) 
        self.goals= [g1,g2,g3]

        r=graphSearch(self.start_pt,self.goals)
        
        #print(r)

        img=TestGraphSearch.map1c.copy()

        for node in r[0]:
            img[node.x,node.y]=15

        #imgplot = plt.imshow(img, 'binary_r')
        imgsave = plt.imsave('map_path_Dijkstra_Diagonals.png',img)
        #plt.show()

        print("The cost of the search Dijsktra: "+r[0][-1].cost().__str__())

    def testDijkstra(self):

        #Run A* with the specified start point and goals, note that
        #the first goal in the list will be used for heuristics.

        g1=Node(1068,1110)
        g2=Node(680,800)
        g3=Node(653,987)

        #create a start node with a goal for heuristics
        self.start_pt=Node(330,316,graph=TestGraphSearch.map1c,cost=0,parent=None,goal=None,step=4,diagonals=False) 
        self.goals= [g1,g2,g3]

        r=graphSearch(self.start_pt,self.goals)
        
        #print(r)

        img=TestGraphSearch.map1c.copy()

        for node in r[0]:
            img[node.x,node.y]=15

        #imgplot = plt.imshow(img, 'binary_r')
        imgsave = plt.imsave('map_path_Dijkstra.png',img)
        #plt.show()

        print("The cost of the search Dijsktra: "+r[0][-1].cost().__str__())

if __name__ == '__main__':
    unittest.main()
