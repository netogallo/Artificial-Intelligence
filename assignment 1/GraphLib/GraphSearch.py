from Graph import Node,Graph
from heapq import heappush,heappop,heapify

def dijkstra(start,goal):

    d=[]
    heapify(d)
    start.cost=0
    f=[start]

    while len(f)>0:
        
        n=heappop(f)

        #print ("Node queue: "+f.__str__())
        if(len(d)>15000):
            return f
            

        if(n==goal):
            d.append(n)
            return d

        if not n in d:
            d.append(n)
        
        children=n.children()

        for node in children:
            
            node.cost=node.cost+n.cost

            if((not (node in f)) and (not (node in d))):
                heappush(f,node)
            elif(node in f):
                if(node.cost<f[f.index(node)].cost):
                    f[f.index(node)].cost=node.cost

    return d

def astar(start,goals):

    d=[]
    heapify(d)
    start.cost=0
    f=[start]

    while len(f)>0:
        
        n=heappop(f)

        for goal in goals:
            if((abs(n.x-goal.x)+abs(n.y-goal.y))<=Graph.step):
                d.append(n)
                return (d,f)

        if not n in d:
            d.append(n)
        
        children=n.children(g=goals[0])

        for node in children:
            
            node.cost=node.cost+n.cost

            if((not (node in f)) and (not (node in d))):
                heappush(f,node)
            elif(node in f):
                if(node.cost<f[f.index(node)].cost):
                    f[f.index(node)].cost=node.cost

    return d
