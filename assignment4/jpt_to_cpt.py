# In this example, we show how to compute a 
# Conditional Probability Table (CPT) P(A|B) from a given
# Joint Probability Table (JPT) P(A,B)
from numpy import *

# A=[a_0, a_1, a_2, a_3]
# B=[b_0, b_1, b_2] 
# This is a joint distribution table P(A,B): A varies along a colum and B along a row.
# e.g. P(a_3, b_0)= 0.15 
p_a_and_b= array([[0.1, 0.01, 0.05], [0.2, 0.19, 0.05], [0.05, 0.05, 0.06], [0.15, 0.05, 0.04]])
N_a= p_a_and_b.shape[0]
N_b= p_a_and_b.shape[1]

print "|A|= %d, |B|= %d" % (N_a, N_b)
print "The given JPT P(A, B) is: \n", p_a_and_b
print "The sum of all probabilities in JPT= ", p_a_and_b.sum()

# p_b is the table P(B)= sum_over_A{P(A,B)} 
p_b= zeros((N_b,1))
print "Doing marginalization to find P(B)" 
for b_i in range(N_b):
    p_b[b_i]= sum(p_a_and_b[:,b_i])
 
print "The table P(B) is:"  
print p_b
print "Sum of all elements of P(b)= ", sum(p_b)

# Compute the CPT P(A|B) using the product-rule P(A|B)= P(A,B)/P(B)
p_a_given_b= zeros(p_a_and_b.shape)
for b_i in range(N_b):
    p_a_given_b[:, b_i]=  p_a_and_b[:, b_i]/p_b[b_i]

print "Computed CPT P(A|B)" 
print p_a_given_b
print "Summing over A's in P(A|B) gives:"
for b_i in range(N_b):
    print "Sum_A P(A|b_%d)= %f" % (b_i, sum(p_a_given_b[:, b_i]))  
