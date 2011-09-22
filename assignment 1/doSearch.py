from Graph import Node,Graph
from GraphSearch import dijkstra,astar
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import ndarray
import pickle
import gzip


s=Node(Graph.start_pt[0],Graph.start_pt[1])
g=Node(Graph.g1[0],Graph.g1[1])
#g=Node(321,323)
#g=Node(500,323)

#p=dijkstra(s,g)
b=astar(s,g)

p=b[0]

#img=ndarray(shape=(1201,1201),dtype='float32') 
img=Graph.map1c.copy()
#img.fill(0)
for node in p:
    img[node.x,node.y]=15

imgplot = plt.imshow(img, 'binary_r')
imgsave = plt.imsave(img, 'aStar.png')
plt.show()
