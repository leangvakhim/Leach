import matplotlib.pyplot as plt
import random
import os

os.system('clear')

# Field Dimensions - x and y maximum (in meters)
xm = 100
ym = 100

# x and y Coordinates of the Sink
sink = {
    'x': 0.5 * xm,
    'y': 0.5 * ym
}

# Number of Nodes in the field
n = 100


# Optimal Election Probability of a node
# to become cluster head
p=0.1

# Energy Model (all values in Joules)
# Initial Energy 
Eo=0.5 
# Eelec=Etx=Erx
ETX=50*0.000000001 
ERX=50*0.000000001 
# Transmit Amplifier types
Efs=10*0.000000000001 
Emp=0.0013*0.000000000001 
# Data Aggregation Energy
EDA=5*0.000000001 

# Values for Hetereogeneity
# Percentage of nodes than are advanced
m=0.1 
# \alpha
a=1 

#maximum number of rounds
rmax=9999

# Computation of do
do = (Efs/Emp) ** 0.5

# Creation of the random Sensor Network
plt.figure(1)
for i in range(1, n+1):
    S={}
    XR={}
    YR={}
    S[i]['xd'] = random.random() * xm
    XR[i] = S[i]['xd']
    S[i]['yd'] = random.random() * ym
    YR[i] = S[i]['yd']
    S[i]['G']=0
    # initially there are no cluster heads only nodes
    S[i]['type'] = 'N'

    temp_rnd0 = i
    # Random Election of Normal Nodes
    if temp_rnd0 >= m*n+1:
        S[i]['E'] = Eo
        S[i]['ENERGY'] = 0
        plt.plot(S[i]['xd'], S[i]['yd'], 'o')
    
    # Random Election of Advanced Nodes
    if temp_rnd0 < m*n+1:
        S[i]['E'] = Eo*(1+a)
        S[i]['ENERGY'] = 1
        plt.plot(S[i]['xd'], S[i]['yd'], '+')

S[n+1]['xd'] = sink['x']
S[n+1]['yd'] = sink['y']
plt.plot(S[n+1]['xd'],S[n+1]['yd'],'x')  

# First Iteration
plt.figure(1) 
# counter for CHs
countCHs=0 
# counter for CHs per round
rcountCHs=0 
cluster=1 

countCHs
rcountCHs=rcountCHs+countCHs
flag_first_dead=0

for r in range(rmax + 1):
    print(r)

    # Operation for epoch
    if r % round(1 / p) == 0:
        for i in range(n):
            S[i]['G'] = 0
            S[i]['cl'] = 0

    plt.clf()

    # Number of dead nodes
    dead=0
    # Number of dead Advanced Nodes
    dead_a=0
    # Number of dead Normal Nodes
    dead_n=0

    # counter for bit transmitted to Bases Station and to Cluster Heads
    packets_TO_BS=0
    packets_TO_CH=0
    # counter for bit transmitted to Bases Station and to Cluster Heads 
    # per round
    PACKETS_TO_CH = {}
    PACKETS_TO_BS = {}
    PACKETS_TO_CH[r+1]=0
    PACKETS_TO_BS[r+1]=0

    plt.figure(1)

    for i in range(n):
        if S[i]['E'] <= 0:
            plt.plot(S[i]['xd'], S[i]['yd'], marker='.', color='red')
            dead = dead + 1
            if S[i]['ENERGY'] == 1:
                dead_a = dead_a + 1
            else:
                dead_n = dead_n + 1

        if S[i]['E'] > 0:
            S[i]['type'] = 'N'
            if S[i]['ENERGY'] == 0:
                plt.plot(S[i]['xd'], S[i]['yd'], marker='o')
            if S[i]['ENERGY'] == 1:
                plt.plot(S[i]['xd'], S[i]['yd'], marker='+')

    plt.plot(S[n+1]['xd'],S[n+1]['yd'],'x')

    STATISTICS = {}
    DEAD = {}
    DEAD_N = {}
    DEAD_A = {}
    STATISTICS[r+1]['DEAD']=dead
    DEAD[r+1]=dead
    DEAD_N[r+1]=dead_n
    DEAD_A[r+1]=dead_a

    if dead == 1:
        if flag_first_dead == 0:
            first_dead = r
            flag_first_dead = 1

    countCHs=0
    cluster=1

    for i in range(n):
        if S[i]['G'] > 0:
            temp_rand = random.random()
            if S[i]['G'] <= 0:
                if temp_rand <= (p/(1-p * (r % round(1/p)))):
                    countCHs=countCHs+1
                    packets_TO_BS=packets_TO_BS+1
                    PACKETS_TO_BS[r+1]=packets_TO_BS

                    S[i]['type'] = 'C'
                    S[i]['G'] = round(1/p) - 1
                    C={}
                    C[cluster]['xd'] = S[i]['xd']
                    C[cluster]['yd'] = S[i]['yd']
                    plt.plot(S[i]['xd'], S[i]['yd'], marker='*', color='k')

                    distance = ((S[i]['xd'] - S[n+1]['xd']) ** 2 + (S[i]['yd'] - S[n+1]['yd']) ** 2) ** 0.5
                    C[cluster]['distance'] = distance
                    C[cluster]['id'] = i
                    X = {}
                    X[cluster] = S[i]['xd']
                    Y = {}
                    Y[cluster] = S[i]['yd']
                    cluster = cluster + 1
                    
                    # Calculation of Energy dissipated
                    distance
                    if distance > do:
                        S[i]['E'] = S[i]['E'] - ((ETX + EDA)* 4000 + Emp*4000*(distance**4))
                    if distance <= do:
                        S[i]['E'] = S[i]['E'] - ((ETX + EDA)* 4000 + Efs*4000*(distance**2))

    STATISTICS[r+1].CLUSTERHEADS=cluster-1
    CLUSTERHS={}
    CLUSTERHS[r+1]=cluster-1

    # Election of Associated Cluster Head for Normal Nodes
    for i in range(n):
        if S[i]['type'] == 'N' and S[i]['E'] > 0:
            if cluster - 1 >= 1:
                min_dis = (S[i]['xd'] - S[n+1]['xd']) ** 2 + (S[i]['yd'] - S[n+1]['yd']) ** 0.5
                min_dis_cluster = 1
                for c in range(1, cluster):
                    temp = min(min_dis, (S[i]['xd'] - C[c]['xd']) ** 2 + (S[i]['yd'] - C[c]['yd']) ** 0.5)
                    if temp < min_dis:
                        min_dis = temp
                        min_dis_cluster = c

                # Energy dissipated by associated Cluster Head
                min_dis
                if min_dis > do:
                    S[i]['E'] = S[i]['E'] - ((ETX + EDA)* 4000 + Emp*4000*(min_dis**4))
                if min_dis <= do:
                    S[i]['E'] = S[i]['E'] - ((ETX + EDA)* 4000 + Efs*4000*(min_dis**2))
                
                # Energy dissipated
                if min_dis > 0:
                    S[C[min_dis_cluster]['id']]['E'] = S[C[min_dis_cluster]['id']]['E'] - ((ERX + EDA)* 4000)
                    PACKETS_TO_CH[r+1] = n - dead - cluster + 1

                S[i]['min_dis'] = min_dis
                S[i]['min_dis_cluster'] = min_dis_cluster


    countCHs
    rcountCHs=rcountCHs+countCHs




