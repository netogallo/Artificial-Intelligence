#
# The BN is represented by a DAG using the graph_tool python library which
# uses Boost C++ bindings for fast execution of several graph-theory algorithms. 
# http://http://projects.skewed.de/graph-tool/
# Install this library.
#
# The BN can be initialized by reading an XMLBIF file:
# Format description: http://www.cs.cmu.edu/~fgcozman/Research/InterchangeFormat/
#
# Using this BN, implement either the Variable-Elimination or the Likelihood-Weighting Algorithm.
# Use the provided alarm.xmlbif file for testing
# More information about the network can be found in alarm_name_details.txt and 
#  ALARM_BMIR-1988-0239.pdf
#
# To check your answers:
# From http://aispace.org/bayes/ download bayes.jar v5.1.9. It can be run using "java -jar bayes.jar"
# This applet answers queries using the variable-elimination algorithm.
# Video tutorials on its usage are given on the web-site
# In the applet goto: File > Load Sample Problem > Diagnosis Problem 
# to load the problem corresponding to alarm.xmlbif
#
# Author: Kaustubh Pathak
#
import numpy
import pickle
import gzip
import math
import sys
import xml.dom.minidom as xd # part of Python standard lib
import graph_tool.all as gt

class RandomVariableNode(object):
    """ Stores the following information regarding a DRV node in a BN: 
        1. name: Name of this RV X.
        2. values: possible values taken by the RV X.
        3. cpt: The CPT representing P(X | P_1, P_2, ..., P_n). The CPT is a numpy.ndarray and can be
           accessed by indices cpt[p_1i, p_2j, ..., x_k]. Note that the last index corresponds to the RV X.
        4. vertex: This is the vertex in the graph_tool graph which contains this RV.
           The loop: for e in vertex.in_edges() will loop over parent edges in the order P_1, P_2, ..., P_n
    """
    def __init__(self, graph_vertex= None):
        self.name="None"
        self.values=[]
        self.cpt= numpy.array([]);
        self.vertex= graph_vertex
    def __str__(self):
        return self.name
    def __repr__(self):
        s= "Name: %s, Values=%s" % (self.name, self.values)
        return s
    def validateCPT(self, epsilon=1e-12):
        """ Returns True if the CPT satisfies its summation constraints.
        """
        should_b_1s= self.cpt.sum(len(self.cpt.shape)-1)
        cpt_error= (numpy.absolute(should_b_1s - numpy.ones(should_b_1s.shape))).sum()
        return (cpt_error < epsilon)

    def prettyPrintCPT(self, graph):
        """ Prints the CPT on stdout in an easily understood format.
        """
        sys.stdout.write("\n")
        sys.stdout.write("-"*80)
        sys.stdout.write("\nCPT \n")
        flat_it= self.cpt.flat
        while True:
            coords= flat_it.coords
            p= self.cpt[coords]
            ix= 0
            sys.stdout.write("Given(")
            for e in self.vertex.in_edges(): 
                parent_vertex= e.source()
                prv= graph.vertex_properties["rv"][parent_vertex]
                sys.stdout.write(" " + prv.name + "=" + prv.values[coords[ix]])
                ix += 1
            sys.stdout.write(" ) For( " + self.name + "="+ self.values[coords[ix]] + " )")
            sys.stdout.write("= %2.4f\n"% (p))
            flat_it.next()
            if flat_it.index == len(flat_it):
                break
            
        
class JBN(object):
    """ A Bayesian Network based on graph-tool.
        Can be loaded from an XMLBIF file.
        The RVs are stored in the graph's vertex property "rv".
    """
    def __init__(self):
        self.graph= gt.Graph(directed=True)
        self.name= None
        rvprop = self.graph.new_vertex_property("object") 
        self.graph.vertex_properties["rv"] = rvprop   
        self.vertex_name_dict={} 
    
        
    def load(self, dom):
        """ loads an object created by xml.dom.minidom.parse
        """
        xbn= dom.getElementsByTagName("NETWORK")[0]
        self.handleNetwork(xbn)

    def handleNetwork(self, dom_nw):
        for node in dom_nw.childNodes:
            if node.nodeName == "NAME":
                self.name= node.childNodes[0].data
                print "The network name is: ", self.name
            elif node.nodeName == "VARIABLE":
                self.handleVariable(node)
            elif node.nodeName == "DEFINITION":
                self.handleDefinition(node)
        
    def handleVariable(self, dom_var):
        v = self.graph.add_vertex()
        rv= RandomVariableNode(v)
        self.graph.vertex_properties["rv"][v]= rv
        
        for node in dom_var.childNodes:
            if node.nodeName == "NAME":
                rv.name= node.childNodes[0].data
                self.vertex_name_dict[rv.name]= v
            elif node.nodeName == "OUTCOME":
                val_name= node.childNodes[0].data
                val_name= val_name.encode('ascii', 'ignore')
                rv.values.append(val_name)
        print rv  
             
    def handleDefinition(self, dom_def):
        v= None
        given_rvs= []
        cpt_dims= [] 
        for_node_name= None
        for node in dom_def.childNodes:
            if node.nodeName == "FOR":
                for_node_name= node.childNodes[0].data
                v= self.vertex_name_dict[for_node_name]
                rv= self.graph.vertex_properties["rv"][v]
            elif node.nodeName == "GIVEN":
                given_node_name= node.childNodes[0].data
                gv= self.vertex_name_dict[given_node_name]
                grv= self.graph.vertex_properties["rv"][gv]
                given_rvs.append(grv)                
                cpt_dims.append(len(grv.values))
                self.graph.add_edge(gv, v)
            elif node.nodeName == "TABLE":
                cpt_dims.append(len(rv.values))
                table_str= node.childNodes[0].data
                table_vals_str= table_str.split()
                n= len(table_vals_str)
                assert(n == numpy.prod(cpt_dims))
                rv.cpt= numpy.zeros(n)
                for ix in range(n):
                    rv.cpt[ix]= float(table_vals_str[ix])
                rv.cpt.resize(tuple(cpt_dims))
                if (not rv.validateCPT()):
                    raise ValueError('Invalid CPT for' + for_node_name)
                rv.prettyPrintCPT(self.graph)
 
#                       
if __name__== '__main__': 
    """Unit testing
    """
    
    dom = xd.parse("alarm.xmlbif")
    bn= JBN()
    bn.load(dom)
    # visualize the BN graph
    gt.graph_draw(bn.graph, size=(15,15), output="bn.pdf", 
            vprops={"label":bn.graph.vertex_properties["rv"]}, layout="dot", vcolor="white", overlap=False, splines=True,
            ratio="compress", penwidth=2.0)
