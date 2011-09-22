import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
import pickle
import gzip
from itertools import product

class Graph:
    
    map1c=None
    w=numpy.sqrt(2)
    diagonals=True
    step=4    

class Node:    
    
    def __init__(self,x,y,cost=0,goal=None):
        self.x=x
        self.y=y
        self.cost=cost

        if(goal is None):
            self.goal=0
        else:
            self.goal=abs(goal.x-self.x)+abs(goal.y-self.y)

    def children(self,g=None):

        if Graph.map1c is None:
            return []
            
        res=[]
        
        for dx,dy in product([-Graph.step,0,Graph.step],repeat=2):

            tx=dx
            ty=dy
            valid=True

            if(self.x+dx<0 or self.y+dy<0):
                valid=False

            while(max(abs(tx),abs(ty))>0):

                if(Graph.map1c[self.x+tx,self.y+ty]!=1):
                    valid=False
                    break

                if(tx>0):
                    tx=tx-1
                elif(tx<0):
                    tx=tx+1

                if(ty>0):
                    ty=ty-1
                elif(ty<0):
                    ty=ty+1
            

            if(valid):
                if(numpy.abs(dx)+numpy.abs(dy)==Node.step):
                    res.append(Node(self.x+dx,self.y+dy,cost=1,goal=g)) 
                elif(Graph.diagonals and (numpy.abs(dx)+numpy.abs(dy)>Node.step)):
                    res.append(Node(self.x+dx,self.y+dy,cost=1.4142,goal=g))

        return res

    def __repr__(self):
        return self.__str__()

    
    def __str__(self):
        return "Node: ("+self.x.__str__()+","+self.y.__str__()+",k="+(self.cost+self.goal).__str__()+")"
            
    def __eq__(self,node):
        if(self.x==node.x and self.y==node.y):
            return True
        return False

    def __ne__(self,node):
        return not self.__eq__(node)

    def __gt__(self,node):
        return self.cost+self.goal>=node.cost+node.goal

    def __lt__(self,node):
        return self.cost+self.goal<node.cost+node.goal

    def __hash__(self):
        return self.x+(self.y*100000)
        
