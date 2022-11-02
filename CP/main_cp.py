from minizinc import Instance, Model, Solver
from funs_cp import *
import time
from datetime import datetime, timedelta

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
    
    array[1..n] of var int: X;
    array[1..n] of var int: Y;
    var h..H: L; % what to minimize
    
    constraint forall(i in 1..n) (X[i] >= 0 /\ X[i] + DX[i] <= w);
    constraint forall(i in 1..n) (Y[i] >= 0 /\ Y[i] + DY[i] <= L);

    %constraint geost_nonoverlap_k(X, DX, Y, DY);
    constraint diffn(X, Y, DX, DY);
    %constraint forall(i in 1..n, j in i+1..n) (X[i] + DX[i] <= X[j] \/ X[j] + DX[j] <= X[i] \/ Y[i] + DY[i] <= Y[j] \/ Y[j] + DY[j] <= Y[i]);
    
    include "chuffed.mzn";

    solve 
    :: restart_linear(100) 
    minimize L;    
    %solve minimize L;
    """
)
for num in range (5, 6):
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

    t1 = time.time()
    
    result = instance.solve(timeout=timedelta(seconds = 300))

    t2 = time.time()
    print("Time needed: " + str(t2 - t1))

    L = result["L"]
    X = result["X"]
    Y = result["Y"]
    xy = []
    for x, y in zip(X,Y):
        xy.append([x,y])

    write_solution((w, L, n, D, xy), num, rot=False)

    visualize(num, rot=False)
