from minizinc import Instance, Model, Solver
from funs_cp import *
import time
from datetime import timedelta

solver = Solver.lookup("chuffed")

model = Model()
model.add_string(
    """
    include "globals.mzn";
    int: h;
    int: H;
    int: n;
    int: w;
    array[1..n] of int: DX;
    array[1..n] of int: DY;
    array[1..n,1..2] of int: D;
    
    array[1..n] of var int: X;
    array[1..n] of var int: Y;
    array[1..n] of var bool: R;
    var h..H: L; % what to minimize

    constraint forall(i in 1..n) (X[i] >= 0  /\  X[i] + DX[i]*(1 - R[i]) + DY[i] * R[i] <= w /\ Y[i] >= 0 /\ Y[i] + DY[i]*(1 - R[i]) + DX[i] * R[i] <= L);
    
    constraint forall(i in 1..n, j in i+1..n) (X[i] + DX[i]*(1 - R[i]) + DY[i] * R[i] <= X[j] \/ X[j] + DX[j]*(1 - R[j]) + DY[j] * R[j] <= X[i] \/ 
        Y[i] + DY[i]*(1 - R[i]) + DX[i] * R[i] <= Y[j] \/ Y[j] + DY[j]*(1 - R[j]) + DX[j] * R[j] <= Y[i]);

    %constraint forall(i in 1..n) (X[i] >= 0 /\ if R[i] then X[i] + DY[i] <= w else X[i] + DX[i] <= w endif);
    %constraint forall(i in 1..n) (Y[i] >= 0 /\ if R[i] then Y[i] + DX[i] <= L else Y[i] + DY[i] <= L endif);

    %constraint forall(i in 1..n, j in i+1..n) (if R[i] == 0 then (if R[j] == 0 then rotation(1,1,2,2,i,j) else rotation(1,2,2,1,i,j) endif) else
    %    (if R[j] == 0 then rotation(2,1,1,2,i,j) else rotation(2,2,1,1,i,j) endif) endif);

    %predicate rotation(int: a, int: b, int: c, int:d, int:i, int:j) =
    %    X[i] + D[i,a] <= X[j] \/ X[j] + D[j,b] <= X[i] \/ Y[i] + D[i,c] <= Y[j] \/ Y[j] + D[j,d] <= Y[i];
    
    include "chuffed.mzn";

    solve 
    :: restart_linear(100) 
    minimize L;    
    %solve minimize L;    
    """
)
for num in range (7, 11):
    print("Instance: "+str(num))
    w, n, D = read_instance(num)
    h = get_lower_height(w, D)
    H = get_upper_height(w, n, D)

    DX = [row[0] for row in D]
    DY = [row[1] for row in D]

    instance = Instance(solver, model)
    instance["n"] = n #number of rectangles
    instance["w"] = w #width of container
    instance["h"] = h #lower bound of height
    instance["H"] = H #upper bound of height
    instance["DX"] = DX #X dimensions
    instance["DY"] = DY #Y dimensions
    instance["D"] = D

    t1 = time.time()
    
    result = instance.solve(timeout=timedelta(seconds = 300))

    t2 = time.time()
    print("Time needed: " + str(t2 - t1))

    L = result["L"]
    X = result["X"]
    Y = result["Y"]
    R = result["R"]
    xy = []
    for x, y in zip(X,Y):
        xy.append([x,y])
    
    newD = []
    for r, d in zip(R,D): # rotating rectangles for the output
        if r:
            newD.append([d[1], d[0]])
        else:
            newD.append(d)

    write_solution((w, L, n, newD, xy), num, rot=True)

    visualize(num, True, R)
