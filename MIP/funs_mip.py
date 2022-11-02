from matplotlib import pyplot as plt, patches
import random
import numpy as np

def read_instance(num):
    f = open('instances\ins-'+str(num)+'.txt', 'r')
    content = f.read().split()
    w = int(content[0])
    n = int(content[1])
    D = []
    for i in range(2, 2*n+2, 2):
        D.append([int(content[i]), int(content[i+1])])
    return w, n, D

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


   