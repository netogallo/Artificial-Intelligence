from Graph import Node
from heapq import heappush,heappop,heapify

#Note: This algoritm uses either Dijkstra or A*
#it all depends if the start node has a defined goal
#which can be used to calculate the heuristic cost
def graphSearch(start,goals):

    d=[]
    heapify(d)
    #start.cost=0
    f=[start]
    heapify(f)

    while len(f)>0:
        
        n=heappop(f)

        for goal in goals:
            if((abs(n.x-goal.x)+abs(n.y-goal.y))<=start.step):
                d.append(n)
                return (d,f)

        if not n in d:
            d.append(n)
        
        children=n.children()
        #print(children)

        for node in children:
            
            if((not (node in f)) and (not (node in d))):
                heappush(f,node)
            elif(node in f):
                if(node.cost()<f[f.index(node)].cost()):
                    f[f.index(node)]=node

    return d
