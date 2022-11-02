from matplotlib import pyplot as plt, patches
import numpy as np
import random
from z3 import *


def read_instance(num):
    f = open('instances\ins-'+str(num)+'.txt', 'r')
    content = f.read().split()
    w = int(content[0])
    n = int(content[1])
    D = []
    for i in range(2, 2*n+2, 2):
        D.append([int(content[i]), int(content[i+1])])
    return w, n, D

def read_solution(num, rot):
    f = open('out\out-'+str(num)+'.txt', 'r')
    if rot:
        f = open('out_rots\out-'+str(num)+'.txt', 'r')
    content = f.read().split()
    w = int(content[0])
    L = int(content[1])
    n = int(content[2])
    D = []
    xy = []
    for i in range(3, 4*n+3, 4):
        D.append([int(content[i]), int(content[i+1])])
        xy.append([int(content[i+2]), int(content[i+3])])
    return w, L, n, D, xy

def write_solution(data, num, rot):
    name = 'out\out-'+str(num)+'.txt'
    if rot:
        name = 'out_rots\out-'+str(num)+'.txt'
    w, L, n, D, xy = data
    f = open(name, 'w')
    f.write(str(w)+' '+str(L)+'\n')
    f.write(str(n)+'\n')
    for i in range(0,n):
        f.write(str(D[i][0]) + ' ' + str(D[i][1]) + ' ' + str(xy[i][0]) + ' ' + str(xy[i][1]) + '\n')
    f.close()

def visualize(num, rot, *args):
    if rot:
        rots = args[0]
        print(rots)
    w, L, n, D, xy = read_solution(num, rot)
    fig = plt.figure(facecolor=(1, 1, 1))
    fig.set_figwidth(w+2)
    fig.set_figheight(L+2)
    ax = fig.add_subplot(111)
    plt.xlim([-1, w+1])
    plt.ylim([-1, L+1])
    plt.grid()
    plt.axis('equal')
    ax.set_xticks(range(-1, w+2, 1))
    ax.set_yticks(range(-1, L+2, 1))
    ax.set_axisbelow(True)

    for i in range(0,n):
        fsize = 0
        if D[i][0] / D[i][1] > 1:
            fsize = D[i][1] * 13
        else:
            fsize = D[i][0] * 10 
        ax.add_patch(patches.Rectangle((xy[i][0], xy[i][1]), D[i][0], D[i][1], 
            facecolor = [random.random(), random.random(), random.random(), 0.3], edgecolor = 'black', lw = 1.5))
        ax.text(xy[i][0] + D[i][0]/2 - D[i][0]/7, xy[i][1] + D[i][1]/2 + D[i][1]/7, 'R'+str(i+1), fontsize = fsize)
        ax.text(xy[i][0] + D[i][0]/2 - D[i][0]/4.8, xy[i][1] + D[i][1]/2 - D[i][1]/4.8, str(D[i][0])+'x'+str(D[i][1]), fontsize = fsize)
        if rot and rots[i]:
            ax.text(xy[i][0] + D[i][0]/2 - D[i][0]/5.8, xy[i][1] + D[i][1]/2 - D[i][1]/2.8, 'ROT', fontsize = fsize/2)
    ax.add_patch(patches.Rectangle((0,0), w, L, fill = False, edgecolor = 'black', lw = 2))
    if rot:
        plt.savefig('figs_rots\out-'+str(num)+'.png')
    else:
        plt.savefig('figs\out-'+str(num)+'.png')
    plt.show()

def sort_by_heights(D):
    for i in range(len(D)):
        max_index = i
        for j in range(i+1, len(D)):
            if D[j][1] >= D[max_index][1]:
                max_index = j
        temp = D[i]
        D[i] = D[max_index]
        D[max_index] = temp
    return D

def switch_order(D, i, j):
    dummy = D[i]
    D[i] = D[j]
    D[j] = dummy
    return D

def get_lower_height(w, D):
    area = 0
    for x, y in D:
        area = area + x*y
    return int(np.ceil(area/w))

def get_upper_height(w, n, D):
    xy = [None] * n
    xy[0] = [0, 0]
    sort_by_heights(D) # sorting rectangles 
    H = D[0][1] # height of first column
    stacked_xy = [] # where the coordinates of stacked rectangles will be saved
    stacked_D = [] # where the dimensions of stacked rectangles will be saved
    N = n 
    j = 0
    i = 1

    while i < n:
        if xy[i-1][0] + D[i-1][0] + D[i][0] <= w:
            xy[i] = [xy[i-1][0] + D[i-1][0], xy[i-1][1]]
            currH = xy[i][1] + D[i][1]
            k = i + 1
            while k < n:
                if D[i][0] >= D[k][0] and (H-currH) >= D[k][1]:
                    stacked_xy.append([xy[i][0], currH])
                    stacked_D.append(D[k])
                    currH = currH + D[k][1]

                    del D[k]
                    del xy[k]

                    n = n - 1
                    k = k - 1
                k = k + 1
        else:
            dummy = True
            for j in range(i+1, n):
                if xy[i-1][0] + D[i-1][0] + D[j][0] <= w:
                    switch_order(D, i, j)
                    # sort again after switching
                    D[i+1:] = sort_by_heights(D[i+1:])
                    dummy = False
                    i = i - 1
                    break
            if dummy:
                xy[i] = [0, H]
                H = H + D[i][1]
        i = i + 1
    xy.extend(stacked_xy)
    D.extend(stacked_D)
    #return w, H, N, D, xy
    return H

def get_available_area(w, L, D):
    area = 0
    for x, y in D:
        area = area + x*y
    return w*L - area

def solve_problem(num):
    w, n, D = read_instance(num)
    sort_by_heights(D)
    h = get_lower_height(w, D)
    H = get_upper_height(w, n, D)
    numb = 0
    print("Height Iteration AvailableArea Width")
    X = [Int('x%s' % i) for i in range (0,n)]
    Y = [Int('y%s' % i) for i in range (0,n)]
    L = Int('L')
    while True:
        x_bound = [And(X[i] >= 0, X[i] + D[i][0] <= w) for i in range(0,n)]
        y_bound = [And(Y[i] >= 0, Y[i] + D[i][1] <= L) for i in range(0,n)]
        l_bound = [And(L >= h, L <= H)]

        rect = [If(And(i == 0, j == 1),Or(X[i] + D[i][0] <= X[j], If(D[i][1] + D[j][1] > L, False, Y[i] + D[i][1] <= Y[j])),
                    Or(X[i] + D[i][0] <= X[j], 
                    X[j] + D[j][0] <= X[i], 
                    If(D[i][1] + D[j][1] > L, False, Or(Y[i] + D[i][1] <= Y[j], Y[j] + D[j][1] <= Y[i]))))
                    for i in range(0,n) for j in range(i+1,n)]
        
        s = Solver()
        s.add(l_bound + x_bound + rect + y_bound)
        #s.set("timeout", 1000 * 60)

        if get_available_area(w, H+1, D) > 0 and s.check() == sat:
            m = s.model()
            xy = []
            for x, y in zip(X,Y):
                xy.append([m[x], m[y]])
            write_solution((w, H, n, D, xy), num, rot=False)
            print(H, numb, get_available_area(w, H, D), w)
            
            H = H - 1
            numb = numb + 1  
        else:
            return

def solve_problem_rot(num):
    w, n, D = read_instance(num)
    h = get_lower_height(w, D)
    H = get_upper_height(w, n, D)
    numb = 0
    print("Height Iteration AvailableArea Width")
    X = [Int('x%s' % i) for i in range (0,n)]
    Y = [Int('y%s' % i) for i in range (0,n)]
    L = Int('L_1')
    R = [Bool('rot%s' % i) for i in range (0,n)] # True if there is a rotation, false if there is no rotation
    rots = []
    while True:
        x_bound = [And(X[i] >= 0, Or(And(R[i], X[i] + D[i][1] <= w), And(Not(R[i]), X[i] + D[i][0] <= w))) for i in range(0,n)]
        y_bound = [And(Y[i] >= 0, Or(And(R[i], Y[i] + D[i][0] <= L), And(Not(R[i]), Y[i] + D[i][1] <= L))) for i in range(0,n)]
        #x_bound = [And(X[i] >= 0, If(R[i], X[i] + D[i][1] <= w, X[i] + D[i][0] <= w)) for i in range(0,n)]
        #y_bound = [And(Y[i] >= 0, If(R[i], Y[i] + D[i][0] <= L, Y[i] + D[i][1] <= L)) for i in range(0,n)]
        l_bound = [And(L >= h, L <= H)]
        
        short_call = lambda a, b, c, d, i, j: Or(X[i] + D[i][a] <= X[j], X[j] + D[j][b] <= X[i], Y[i] + D[i][c] <= Y[j], Y[j] + D[j][d] <= Y[i])
        '''
        short_call = lambda a, b, c, d, i, j: If(And(i == 0, j == 1),
                    Or(X[i] + D[i][a] <= X[j], If(D[i][a] + D[j][b] > L, False, Y[i] + D[i][c] <= Y[j])),
                    Or(X[i] + D[i][a] <= X[j], 
                    X[j] + D[j][b] <= X[i], 
                    If(D[i][c] + D[j][d] > L, False, Or(Y[i] + D[i][c] <= Y[j], Y[j] + D[j][d] <= Y[i]))))
        '''
        
        rect = [(Or(And(Not(R[i]), Or(And(Not(R[j]), short_call(0, 0, 1, 1,i,j)), And(R[j], short_call(0, 1, 1, 0, i, j)))), 
            And(R[i], Or(And(Not(R[j]), short_call(1,0,0,1,i,j)), And(R[j], short_call(1, 1, 0, 0, i,j)))))) for i in range(0,n) for j in range(i+1,n)]
        
        #rect = [(If(R[i] == False, If(R[j] == False, short_call(0, 0, 1, 1, i, j), short_call(0, 1, 1, 0, i, j)), 
        #        If(R[j] == False, short_call(1,0,0,1,i,j), short_call(1, 1, 0, 0, i,j)))) for i in range(0,n) for j in range(i+1,n)]
        
        #rot_call = lambda r: If(r, 1, 0)
        #rect = [Or(X[i] + D[i][0]*(1 - rot_call(R[i])) + D[i][1] * rot_call(R[i]) <= X[j], X[j] + D[j][0]*(1 - rot_call(R[j])) + D[j][1] * rot_call(R[j]) <= X[i], 
        #    Y[i] + D[i][1]*(1 - rot_call(R[i])) + D[i][0] * rot_call(R[i]) <= Y[j], Y[j] + D[j][1]*(1 - rot_call(R[j])) + D[j][0] * rot_call(R[j]) <= Y[i]) for i in range (0,n) for j in range(i+1,n)]

        s = Solver()
        s.add(l_bound + x_bound + rect + y_bound) 
        s.set("timeout", 1000 * 300)

        if get_available_area(w, H+1, D) > 0 and s.check() == sat:
            m = s.model()
            xy = []
            rots = []
            for x, y in zip(X,Y):
                xy.append([m[x], m[y]])
            newD = []
            for r, d in zip(R,D): # rotating rectangles for the output
                if m[r]:
                    newD.append([d[1], d[0]])
                    rots.append(True)
                else:
                    newD.append(d)
                    rots.append(False)
                #print(m[r], end = ' ')
            write_solution((w, H, n, newD, xy), num, rot=True)
            print(H, numb, get_available_area(w, H, newD), w)

            H = H - 1
            numb = numb + 1
            
        else:
            return rots

'''

# data cleaning
def glue_rectangles(num):
    w, n, D = read_instance(num)
    glued_D = []
    max_X = max(D)
    i = 0
    while i < n:

        i = i + 1

def rotate_all(D):
    for d in D:
        temp = d[0]
        d[0] = d[1]
        d[1] = temp 

def mix_rotations(D):
    for d in D:
        if random.random() > 0.5:
            temp = d[0]
            d[0] = d[1]
            d[1] = temp 

def precedes(a1, a2):
    if not a1:
        return True
    if not a2:
        return False
    return Or(a1[0] < a2[0], And(a1[0] == a2[0], precedes(a1[1:], a2[1:])))

def my_max(vs):
    m = vs[0]
    for v in vs[1:]:
        m = If(v > m, v, m)
    return m

def rotate_rect(D, i):
    temp = D[i][0]
    D[i][0] = D[i][1]
    D[i][1] = temp
    return True

'''

'''
def solve_problem0(num):
    w, n, D = read_instance(num)
    sort_by_heights(D)
    H = get_upper_height(w, n, D)
    numb = 0
    print("Height Iteration AvailableArea Width")
    X = [Int('x%s' % i) for i in range (0,n)]
    Y = [Int('y%s' % i) for i in range (0,n)]
    while True:
        x_bound = [And(X[i] >= 0, X[i] + D[i][0] <= w) for i in range(0,n)]
        y_bound = [And(Y[i] >= 0, Y[i] + D[i][1] <= H) for i in range(0,n)]
        y_sum = [Sum(Y) <= 40]

        rect = [If(And(i == 0, j == 1),Or(X[i] + D[i][0] <= X[j], 
                                          If(D[i][1] + D[j][1] > H, False, Y[i] + D[i][1] <= Y[j])),
                    Or(X[i] + D[i][0] <= X[j], 
                    X[j] + D[j][0] <= X[i], 
                    If(D[i][1] + D[j][1] > H, False, Or(Y[i] + D[i][1] <= Y[j], Y[j] + D[j][1] <= Y[i]))))
                    for i in range(0,n) for j in range(i+1,n)]
        
            
        s = Solver()
        s.add(x_bound + rect + y_bound + y_sum)
        #s.set("timeout", 1000 * 60)
        
        if get_available_area(w, H+1, D) > 0 and s.check() == sat:
            m = s.model()
            xy = []
            for x, y in zip(X,Y):
                xy.append([m[x], m[y]])
            write_solution((w, H, n, D, xy), num)
            print(H, numb, get_available_area(w, H, D), w)
            #print([sum(a) for a in zip(*xy)])
            H = H - 1
            numb = numb + 1
        else:
            return


def solve_problem2(num):
    w, n, D = read_instance(num)
    H = get_upper_height(w, n, D.copy())
    area = 0
    for x, y in D:
        area = area + x*y
    h = int(np.ceil(area/w))
    print(H)
    print("Height Iteration AvailableArea Width")
    L = Int('L')
    X = [Int('x%s' % i) for i in range (0,n)]
    Y = [Int('y%s' % i) for i in range (0,n)]
    x_bound = [ And(X[i] >= 0, X[i] + D[i][0] <= w) for i in range(0,n)]
    y_bound = [ And(Y[i] >= 0, Y[i] + D[i][1] <= L) for i in range(0,n)]
    l_bound = [ And(L>= h, L <= H)]
    #max_el = Int('max_el')
    rect = [If(And(i == 0, j == 1),Or(X[i] + D[i][0] <= X[j], 
                                        If(D[i][1] + D[j][1] > L, False, Y[i] + D[i][1] <= Y[j])),
                Or(X[i] + D[i][0] <= X[j], 
                X[j] + D[j][0] <= X[i], 
                If(D[i][1] + D[j][1] > L, False, Or(Y[i] + D[i][1] <= Y[j], Y[j] + D[j][1] <= Y[i]))))
                for i in range(0,n) for j in range(i+1,n)]
    #L = []
    #for i in range(0,n):
    #    L.append(Y[i] + D[i][1])
    #max_el = my_max(L)
    #print(max_el)
    #print(Y[0].sort()) 
    #L = [If(Y[i] + D[i][1] > max_el, max_el = Y[i] + D[i][1]) for i in range(1,n)]
    opt = Optimize()
    opt.set("timeout", 1000 * 120)
    opt.add(l_bound + x_bound + y_bound + rect)

    
    #print(max_el)
    res = opt.minimize(L)
    
    if opt.check() == sat:
        m = opt.model()
        print(res.value())
        xy = []
        print(H)
        for x, y in zip(X,Y):
            xy.append([m[x], m[y]])
        write_solution((w, H, n, D, xy), num)
    else:
        print('unsat')
        return

def solve_problem3(num):
    w, n, D = read_instance(num)
    #area = 0
    #for x, y in D:
    #    area = area + x*y
    H = get_upper_height(w, n, D.copy())
    #H = int(np.ceil(area/w))
    numb = 0
    print("Height Iteration AvailableArea Width")
    X = [Int('x%s' % i) for i in range (0,n)]
    Y = [Int('y%s' % i) for i in range (0,n)]
    lr = [[Bool(f"lr_{i}_{j}") for j in range(n)] for i in range(n)]
    ud = [[Bool(f"ud_{i}_{j}") for j in range(n)] for i in range(n)]
    while True:
        x_bound = [ And(X[i] >= 0, X[i] + D[i][0] <= w) for i in range(0,n)]
        y_bound = [ And(Y[i] >= 0, Y[i] + D[i][1] <= H) for i in range(0,n)]
        
        prop = [If(D[i][1] + D[j][1] > H, Or(lr[i][j], lr[j][i]), Or(lr[i][j], lr[j][i], ud[i][j], ud[j][i])) for i in range(0,n) for j in range(i+1, n)]
        x_rect1 = [Or(Not(lr[i][j]), X[i] + D[i][0] <= X[j]) for i in range(0,n) for j in list(range(i+1,n))]
        x_rect2 = [Or(Not(lr[j][i]), X[j] + D[j][0] <= X[i]) for i in range(0,n) for j in list(range(i+1,n))]
        y_rect1 = [If(D[i][1] + D[j][1] > H, True, Or(Not(ud[i][j]), Y[i] + D[i][1] <= Y[j])) for i in range(0,n) for j in list(range(i+1,n))]
        y_rect2 = [If(D[i][1] + D[j][1] > H, True, Or(Not(ud[j][i]), Y[j] + D[j][1] <= Y[i])) for i in range(0,n) for j in list(range(i+1,n))]

        #delta_sum = [Sum(delta[i][j]) <= 3 for i in range(0,n) for j in range(i+1,n)]
                    
        s = Solver()
        #print(len(x_bound + y_bound + x_rect1 + x_rect2 + y_rect1 + y_rect2 + delta_sum))
        s.add(x_bound + y_bound + x_rect1 + x_rect2 + y_rect1 + y_rect2 + prop)
        #s.add(x_bound + y_bound + rect)
        #s.set("timeout", 1000 * 60)

        if get_available_area(w, H+1, D) > 0 and s.check() == sat:
            m = s.model()
            xy = []
            for x, y in zip(X,Y):
                xy.append([m[x], m[y]])
            write_solution((w, H, n, D, xy), num)
            print(H, numb, get_available_area(w, H, D), w)
            
            H = H - 1
            numb = numb + 1
            
        else:
            print('out')
            return



'''