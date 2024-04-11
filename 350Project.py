from pyeda.inter import *

# Define BDD variables for nodes (5 bits are enough to represent 32 nodes)
X = bddvars('x', 5)
Y = bddvars('y', 5)
Z = bddvars('z', 5)

# Function to convert nodes to BDD representation
def node_to_bdd(node, vars): 
    bits = [(node >> i) & 1 for i in range(5)] # Convert the node number to bits
    return [vars[i] if bits[i] else ~vars[i] for i in range(5)] # Convert the bits to BDD

# Define the graph's edges
def RR(i, j):
    return (i + 3) % 32 == j or (i + 8) % 32 == j

# Define all base cases of BDDs for the graph
R = expr2bdd(exprvar('False'))  
even = expr2bdd(exprvar('False')) 
prime = expr2bdd(exprvar('False'))
RR2 = expr2bdd(exprvar('False'))

for i in range(32):
    i_bdd = expr2bdd(exprvar('True')) # Start with a true expression
    for bit, var in zip(node_to_bdd(i, X), X): # Convert the node number to BDD
        i_bdd &= bit # Combine the bits

    if i % 2 == 0: # Even set
        even |= i_bdd # Add the node to the even set
    if i in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:  # Prime set
        prime |= i_bdd # Add the node to the prime set
    
    for j in range(32):
        if RR(i, j): # If there is an edge between i and j
            j_bdd = expr2bdd(exprvar('True')) 
            for bit, var in zip(node_to_bdd(j, Y), Y):  # Convert the node number to BDD
                j_bdd &= bit # Combine the bits
            R |= i_bdd & j_bdd # Add the edge to the graph

def composeRR2(r1, r2): # Function to compose two BDDs
    RR2 = (r1.compose({Y[i]: Z[i] for i in range(5)}) & r2.compose({X[i]: Z[i] for i in range(5)})).smoothing(Z) # Compose the two BDDs r1 and r2
    return RR2


# Find the transitive closure of the graph using fixed-point algorithm
H = R 
while True: 
    Hp = H # Store the previous iteration
    H = Hp | (Hp.compose({X[i]: Z[i] for i in range(5)}) & R.compose({Y[i]: Z[i] for i in range(5)})).smoothing(Z) # Update the graph
    if H.equivalent(Hp): # continute unti; graph has converged
        break 

test_cases = [
    RR(27, 3), 
    RR(16, 20), 
    even(14), 
    even(13), 
    prime(7), 
    prime(2), 
    RR2(27, 6),
    RR2(27, 9) 
]

print(test_cases)
