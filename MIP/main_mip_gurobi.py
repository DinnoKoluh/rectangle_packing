import gurobipy as gp
from funs_mip import *
from gurobipy import GRB

num = 32
w, n, D = read_instance(num)
h = get_lower_height(w, D)
H = get_upper_height(w, n, D)

DX = [row[0] for row in D]
DY = [row[1] for row in D]

# Creating a new model
m = gp.Model()

# Creating variables
L = m.addVar(vtype='I', name="Height")
X = m.addMVar((n,), vtype='I', name="X_coor")
Y = m.addMVar((n,), vtype='I', name="Y_coor")
delta = m.addMVar((n, n, 4), vtype=GRB.BINARY, name='delta')
# Setting the objective function
m.setObjective(L, gp.GRB.MINIMIZE)

# Adding constraints
m.addConstr(L <= H)
m.addConstr(L >= h)
for i in range(0,n):
    m.addConstr(X[i] >= 0)
    m.addConstr(X[i] + DX[i] <= w)
    m.addConstr(Y[i] >= 0)
    m.addConstr(Y[i] + DY[i] <= L)

for i in range(0,n):
    for j in range(i+1,n):
        m.addConstr(X[i] + DX[i] <= X[j] + w*delta[i][j][0])
        m.addConstr(X[j] + DX[j] <= X[i] + w*delta[i][j][1])
        m.addConstr(Y[i] + DY[i] <= Y[j] + L*delta[i][j][2])
        m.addConstr(Y[j] + DY[j] <= Y[i] + L*delta[i][j][3])
        m.addConstr(sum(delta[i][j]) <= 3)

m.optimize()

xy = []
X = list(X.X)
X = [int(a) for a in X]

Y = list(Y.X)
Y = [int(a) for a in Y]

L = int(m.objVal)

print(X)
print(Y)
print(L)
print("Instance: "+str(num))

for x, y in zip(X,Y):
        xy.append([x,y])

write_solution((w, L, n, D, xy), num, rot=False)

visualize(num, rot=False)