#
# The BN is represented by a DAG using the graph_tool python library which
# uses Boost C++ bindings for fast execution of several graph-theory algorithms. 
# http://projects.skewed.de/graph-tool/
# Install this library.
#
# The BN can be initialized by reading an XMLBIF file:
# Format description: http://www.cs.cmu.edu/~fgcozman/Research/InterchangeFormat/
#
#
# Author: Kaustubh Pathak
#
import numpy
import math
import random
import sys
import copy
import xml.dom.minidom as xd # part of Python standard lib
import graph_tool.all as gt
import operator

class Factor(object):
    """ A Factor providing facilities for point-wise multiplications with other
        factors and marginalization.
    """
    def __init__(self, a_table, names_list):
        """ names_list contains the names of the nodes in the order of the indices
            they have in the numpy.ndarray table. 
        """
        assert(((a_table.shape is None) and (names_list is None))or(len(a_table.shape) == len(names_list)))
        self.table= copy.deepcopy(a_table)
        self.ordered_names= copy.deepcopy(names_list)
        self.names= dict()
        count= 0
        for name in self.ordered_names:
            self.names[name]= count
            count += 1
         
    def __getitem__(self, name):
        return self.names[name]
            
    def has(self, name):
        return (name in self.names)
    
    def coords(self, names_dict):
        """ Returns a tuple of indices corresponding to the name-value pairs in 
        names_dict. For example, if the indices in self.table have names 
        'a', 'b', 'c' (in this order) and the table has shape (3,4,2). If
        names_dict= {b:3, c:0, a:2, d:5}, then the returned tuple will be (2,3,0).
        Note that the 'd' value was ignored.
        """
        nr_to_be_assigned= len(self.table.shape)
        c= numpy.zeros(nr_to_be_assigned)
        for (name, name_ix_value) in names_dict.iteritems():
            if self.has(name):
                c[self[name]]= name_ix_value 
                nr_to_be_assigned -= 1
        assert(nr_to_be_assigned == 0) # all indices were assigned
        return tuple(c)

        
    def __mul__(self, other):
        """ Point-wise multiplication of two factors over all common names.
        """
        self_scalar= len(self.ordered_names) == 0
        other_scalar= len(other.ordered_names) == 0
        
        ks= set(self.ordered_names)
        ko= set(other.ordered_names)
        if (self_scalar and other_scalar):
            scalar_factor= Factor(numpy.zeros([]), [])
            scalar_factor.table= self.table*other.table
            return scalar_factor
            
        # print "assertion: ", ks, ko, self_scalar, other_scalar
        assert(self_scalar or other_scalar or (not ks.isdisjoint(ko)))
        
        # Verification test ----------------------
        names_common= list(ks.intersection(ko))
        for name in names_common:
            nself= self.table.shape[self[name]]
            nother= other.table.shape[other[name]]
            if (nself != nother):
                print "something amiss:"
                print self.names, self.table.shape
                print other.names, other.table.shape
            assert(nself == nother)
        #-----------------------------------------
        
        names_all= list(ks.union(ko))
        name_shapes= range(len(names_all))
        
        for n_ix in range(len(names_all)):
            name= names_all[n_ix]
            if self.has(name):
                name_shapes[n_ix]= self.table.shape[self[name]]
            else:
                name_shapes[n_ix]= other.table.shape[other[name]]
            
        factor= Factor(numpy.zeros(tuple(name_shapes)), names_all)
        
        flat_itr= factor.table.flat
        while True:
            f_coords= flat_itr.coords
            
            dict_name_coords= {} 
            for name in factor.names.keys():
                dict_name_coords[name]= f_coords[factor.names[name]]
            
            s1= self.table[self.coords(dict_name_coords)]
            s2= other.table[other.coords(dict_name_coords)]
            factor.table[f_coords]= s1*s2
            flat_itr.next()
            if flat_itr.index == len(flat_itr):
                break
        
        return factor
    
    def normalize(self):
        s= self.table.sum()
        self.table= self.table/s
    
    def marginalize(self, name):
        """ Returns a factor with one dimension less, namely that of the RV "name" 
            which will be summed out.
        """
        assert(self.has(name))
        f_table= self.table.sum(axis=self.names[name])
        f_names= []
        
        for i_name in self.ordered_names:
            if i_name != name:
                f_names.append(i_name)
                
        return Factor(f_table, f_names)
    
    def reduce(self, evidence_dict):
        """ evidence_dict is a map from evidence-RV-name to evidence-RV-value as value-index.
            Reduces the size of this factor so that only entries corresponding to the evidence are retained.
            The evidence-variables are removed from the returned factor
        """    
        ordered_names_remaining= []
        slices= []
        removal_needed= False
        
        for name in self.ordered_names:
            if name in evidence_dict:
                removal_needed= True
                slices.append(slice(evidence_dict[name], evidence_dict[name]+1))
            else:
                slices.append(slice(None))
                ordered_names_remaining.append(name)
        
        if removal_needed:
            table_remaining= self.table[slices].squeeze()
            factor= Factor(table_remaining, ordered_names_remaining)
            return factor
        else:
            return self        
        
        
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
        self.values_dict={}
        self.cpt= numpy.array([]);
        self.vertex= graph_vertex
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        s= "Name: %s, Values=%s" % (self.name, self.values)
        return s
    
    def __hash__(self):
        return hash(self.name)
    
    def factor(self, graph, evidence_dict= None):
        """ Returns a Factor object created from this node's CPT.
            evidence_dict is a map from evidence-RV-name to evidence-RV-value as value-index.
            Reduces the size of this factor so that only entries corresponding to the evidence are retained.
            The evidence-variables are removed from this factor
        """
        names= []
        shape= []
        for e in self.vertex.in_edges(): 
            parent_vertex= e.source()
            prv= graph.vertex_properties["rv"][parent_vertex]
            names.append(prv.name)
            shape.append(len(prv.values))
            
        names.append(self.name)
        shape.append(len(self.values))
        
        factor= Factor(self.cpt, names)
        
        if evidence_dict is not None:
            factor= factor.reduce(evidence_dict)
            
        return factor

        
    def validateCPT(self, epsilon=1e-11):
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
        
    def eliminateVariableFromFactors(self, factors, y):
        """ y is the name of the hidden RV to remove by marginalization.
        """
        y_factors= []
        for f in factors:
            if f.has(y):
                y_factors.append(f)
        
        if len(y_factors) > 0:  
            first_factor= y_factors[0]      
            h= first_factor
            factors.remove(first_factor)
            for f in y_factors[1:]:
                factors.remove(f)
                h= h*f
            g= h.marginalize(y)
            factors.append(g)
    
    def variableElimination(self, dict_q_names_factor, rvs_Y, evidence_dict, factors):
        for rv_y in rvs_Y:
            self.eliminateVariableFromFactors(factors, rv_y.name)
            #print "\n*Eliminated hidden RV:", rv_y.name
            
        #print "Finished eliminating all hidden RVs. Only factors involving query RVs remain:" 
        #for ix_f in range(len(factors)):
        #    print "f[", ix_f, "]=", factors[ix_f].ordered_names, "\n"

        # The product of the remaining factors form a JPD of the query RVs.
        # We now get marginalized pmfs for each query RV.
        for q in dict_q_names_factor.keys():
            q_set= set(); q_set.add(q) 
            other_qs_set= set(dict_q_names_factor.keys()).difference(q_set)
            q_factors= copy.deepcopy(factors) 
            for other_q in other_qs_set:
                self.eliminateVariableFromFactors(q_factors, other_q)
            h= q_factors[0]
            for f in q_factors[1:]:
                h= h*f
            h.normalize()
            dict_q_names_factor[q]= h
            
          
    def posteriorQuery(self, dict_q_names_factor, dict_e_names_values):
        """ Queries of type P(Q_1,...,Q_k | e_1,...,e_m)
        """
        dict_q_names_rv= {}
        rvs_Y= []
        rvs_all= []
        factors= []
        evidence_dict= {}
        top_sort_vertices = gt.topological_sort(self.graph) 
        # stictly speaking topological sorting is not needed here- any ordering will do.
        rv_prop= self.graph.vertex_properties["rv"]
        
        for vertex in top_sort_vertices:
            rv= rv_prop[self.graph.vertex(vertex)]
            rvs_all.append(rv)
            if rv.name in dict_e_names_values:
                evidence_dict[rv.name]= rv.values_dict[dict_e_names_values[rv.name]]
            elif rv.name in dict_q_names_factor:
                dict_q_names_factor[rv.name]= rv
                dict_q_names_rv[rv.name]= rv
            else: 
                rvs_Y.append(rv)
                
        for rv in rvs_all:
            factors.append(rv.factor(self.graph, evidence_dict))
         
        self.variableElimination(dict_q_names_factor, rvs_Y, evidence_dict, factors) 
        return dict_q_names_rv  
    
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
                rv.name= node.childNodes[0].data.encode('ascii', 'ignore') 
                self.vertex_name_dict[rv.name]= v
            elif node.nodeName == "OUTCOME":
                val_name= node.childNodes[0].data
                val_name= val_name.encode('ascii', 'ignore')
                rv.values.append(val_name)
                rv.values_dict[val_name]= len(rv.values)-1
        print rv  
             
    def handleDefinition(self, dom_def):
        v= None
        given_rvs= []
        cpt_dims= [] 
        for_node_name= None
        for node in dom_def.childNodes:
            if node.nodeName == "FOR":
                for_node_name= node.childNodes[0].data.encode('ascii', 'ignore')
                v= self.vertex_name_dict[for_node_name]
                rv= self.graph.vertex_properties["rv"][v]
            elif node.nodeName == "GIVEN":
                given_node_name= node.childNodes[0].data.encode('ascii', 'ignore')
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
class Evidence(dict):
    """
    A collection of RVs which form the evidence vector. Provides convenience
    functions for sampling. 
    """
    def __init__(self, a_graph):
        dict.__init__(self)
        self.graph= a_graph
        self.top_sort_vertices = gt.topological_sort(self.graph) 
        # stictly speaking topological sorting is not needed here- any ordering will do.
        
    def add(self, rv_name):
        self[rv_name]= None
    
    def sample(self):
        rv_prop= self.graph.vertex_properties["rv"]
        print "-"*70
        print "Evidence:"
        
        for vx in self.top_sort_vertices:
            rv= rv_prop[self.graph.vertex(vx)]
            if self.has_key(rv.name):
                val= random.choice(rv.values)
                self[rv.name]= val
                print "E[%s]= %s" % (rv.name, val)

    def sampleLine(self,line,order):
        
        s=line.replace('\n','').split(',')
        self.clear()

        for i in range(0,len(s)):

            try:
                if order[i]!=None:                    
                    if s[i]!='?':
                        self.add(order[i])
                        self[order[i]]=s[i]

            except IndexError:
                0

if __name__== '__main__': 
    """Unit testing
    """

    dom = xd.parse("nbc_mushroom.xmlbif")
    bn= JBN()
    bn.load(dom)
    dict_q_names_factor= {}
    dict_q_names_factor["decision"]= None

    dict_e_names_values= Evidence(bn.graph)
    dict_e_names_values.add("odor")
    dict_e_names_values.add("spore-print-color")
    dict_e_names_values.add("gill-color")
    dict_e_names_values.add("ring-type") 
    dict_e_names_values.add("stalk-surface-above-ring")
    dict_e_names_values.add("stalk-surface-below-ring")
    dict_e_names_values.add("stalk-color-above-ring")
    dict_e_names_values.add("stalk-color-below-ring")
    dict_e_names_values.add("gill-size")
    dict_e_names_values.add("population")
    dict_e_names_values.add("bruises")
    dict_e_names_values.add("habitat")
    #dict_e_names_values.add("stalk-root") # has missing values
    dict_e_names_values.add("gill-spacing")
    dict_e_names_values.add("cap-shape")
    dict_e_names_values.add("ring-number")
    dict_e_names_values.add("cap-color")
    dict_e_names_values.add("cap-surface")
    dict_e_names_values.add("veil-color")
    dict_e_names_values.add("gill-attachment")
    dict_e_names_values.add("stalk-shape")
    #dict_e_names_values.add("veil-type") # has the same value in all examples

    N_samples= 5
    
    for i in range(N_samples):
        dict_e_names_values.sample()
        dict_q_names_rv= bn.posteriorQuery(dict_q_names_factor, dict_e_names_values)
    
        print "\n*** The final PMFs for the query RVs for the evidence are: (SORTED by decreasing likelihood)"
        sorted_q_dict = sorted(dict_q_names_factor.iteritems(), key=lambda t: t[1].table[0], reverse=True)
        for (q_name, q_factor) in sorted_q_dict:
            for ix in range(len(q_factor.table)):
                sys.stdout.write('\t P(%s=%s | evidence)=%f\n' % (q_name, dict_q_names_rv[q_name].values[ix], q_factor.table[ix]))
            # print q_name, dict_q_names_factor[q_name].values, q_factor.table
    
#    # visualize the BN graph
    gt.graph_draw(bn.graph, size=(15,15), output="bn.pdf", 
            vprops={"label":bn.graph.vertex_properties["rv"]}, layout="dot", vcolor="white", overlap=False, splines=True,
            ratio="compress", penwidth=2.0)
