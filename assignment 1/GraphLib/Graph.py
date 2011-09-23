import numpy
from itertools import product

class Node:    
    
    def __init__(self,x,y,graph=None,cost=0,parent=None,goal=None,step=1,diagonals=True):
        self.x=x
        self.y=y
        self.k=cost
        self.parent=parent

        if self.parent is None:

            self.map1c=graph            
            self.diagonals=diagonals
            self.step=step

            if(goal is None):
                self.goal=None
            else:
                self.goal=goal

        else:
            self.map1c=self.parent.map1c
            self.diagonals=self.parent.diagonals
            self.goal=self.parent.goal
            self.step=self.parent.step

    def children(self):

        if self.map1c is None:
            return []
            
        res=[]
        
        for dx,dy in product([-self.step,0,self.step],repeat=2):

            tx=dx
            ty=dy
            valid=True

            if(self.x+dx<0 or self.y+dy<0):
                valid=False

            while(max(abs(tx),abs(ty))>0):

                if(self.map1c[self.x+tx,self.y+ty]!=1):
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
                if(numpy.abs(dx)+numpy.abs(dy)==self.step):
                    res.append(Node(self.x+dx,self.y+dy,cost=1,parent=self)) 
                elif(self.diagonals and (numpy.abs(dx)+numpy.abs(dy)>self.step)):
                    res.append(Node(self.x+dx,self.y+dy,cost=1.4142,parent=self)) 

        return res

    def cost(self):

        if self.parent is None:
            return self.k
        else:
            return self.parent.cost()+self.k

    def hCost(self):
        
        if self.goal is None:
            return self.cost()
        else:
            h=abs(self.goal.x-self.x)+abs(self.goal.y-self.y)
            return self.cost()+h

    def __repr__(self):
        return self.__str__()

    
    def __str__(self):
        return "Node: ("+self.x.__str__()+","+self.y.__str__()+",k="+self.hCost().__str__()+")"
            
    def __eq__(self,node):
        if(self.x==node.x and self.y==node.y):
            return True
        return False

    def __ne__(self,node):
        return not self.__eq__(node)

    def __gt__(self,node):
        return self.hCost()>=node.hCost()

    def __lt__(self,node):
        return self.hCost()<node.hCost()

    def __hash__(self):
        return self.x+(self.y*100000)
        
