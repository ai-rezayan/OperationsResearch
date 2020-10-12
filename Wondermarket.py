

#WonderMarket

from gurobipy import *



#Sets

Stores = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]
DistributionCenters = ["DC0", "DC1", "DC2"]

#Data

#The cost of transporting one truckload from each distribution centre(column) to each store(row):
CT = [
     [2081,	2462,	2958,	1911,	2735,	1805,	2139,	2795,	1456,	2707],
	[1094,	1267,	1996,	1091,	1520,	1016,	1200,	1880,	912,	2100],
	[1418,	1604,	2877,	2566,	2113,	2578,	2570,	2900,	2478,	3379]
    ]

#The weekly demand at the ten stores, in truckloads in each five scenarios:
WD = [12, 12, 10, 21, 6, 10, 12, 11, 8, 14]


#S and D and N are established for iterations in later code:
S = range(len(Stores))
D = range(len(DistributionCenters))

#Model

m = Model("Wonder Market")

#Variables

X = {(s,d): m.addVar() for s in S for d in D}

#Objective
    
m.setObjective(quicksum(CT[d][s]*X[s,d] for d in D for s in S),GRB.MINIMIZE)

#Meeting the weekly demand(Communication 1)
for s in S:
    m.addConstr(quicksum(X[s,d] for d in D) == WD[s] )

#Capacity limitation at the distribution centres(Communication 2)

CD = [48, 63, 57]
for d in D:
    m.addConstr(quicksum(X[s,d] for s in S) <= CD[d])
    
#Two distribution centres on the north side of the river
#actually share a labour pool(Communication 3)
F = range(1,3)
m.addConstr(quicksum(X[s,f] for s in S for f in F) <= 85)
 
m.optimize()
for s in S:
        print(X[s,0].x, X[s,1].x, X[s,2].x)