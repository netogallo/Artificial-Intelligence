import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
import pickle
import gzip

# Initialization: load map
f= gzip.open('map1c.p.gz','rb')
map1c= pickle.load(f)
print type(map1c), map1c.shape

# creates object map1c which is of type numpy.array
imgplot = plt.imshow(map1c, 'binary_r')
plt.show()
# The script waits till the plot is closed.

# Start and Goal points.
# The coordinates are in (row, column) format not (x,y)
start_pt=(330,316)
g1=(1068,1110)
g2=(680,800)
g3=(653,987)
goals= {g1,g2,g3}
