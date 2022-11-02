There are four files in the 'src' folder. The 'main_mip_minizinc.py' file is used for the base model (cplex solver), the 'main_mip_minizinc_rot.py' 
is used for the rotational model (cplex solver), the 'main_mip_gurobi.py' is used for the base model (gurobi_solver), and the file 'funs_mip.py' 
contains all the functions used to solve the problem. As already mentioned in the report I was not able to get the licensed gurobi solver as I had
no access to the University WiFi but I was able to test the model on the first 3 instances and it works. So, in the end I will be using the cplex
solver which has a much worse performance than gurobi.

IMPORTANT: All the files from the 'src' folder should be in the same folder where the folders 'out', 'figs', 'out_rots', 'figs_rots' and 
'instances' are, as they read/write the solutions from these folders.

The needed libraries are: gurobipy, minizinc, datetime, matplotlib, time. 