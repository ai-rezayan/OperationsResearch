#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:45:56 2019

@author: amirebrahimrezaeian
"""
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


#Capacity limitation at the distribution centres(Communication 2)
CD = [48, 63, 57]

#The weekly demand at the ten stores:
WD = [12, 12, 10, 21, 6, 10, 12, 11, 8, 14]

#The weekly demand at the ten stores, in truckloads in each five scenarios:
WS = [
      [13,	12,	10,	21,	23,	10,	12,	11,	8,	14],
      [12,  12, 10,	21,	6,	10,	12,	12,	8,	25],
      [12,	12,	10,	21,	18,	10,	12,	15,	8,	14],
      [12,	12,	10,	30,	16,	10,	12,	11,	9,	14],   
      [12,	12,	10,	21,	6,	10,	12,	31,	8,	14]
      ]
#S and D are established for iterations in later code:
S = range(len(Stores))
D = range(len(DistributionCenters))

#Model

m = Model("Wonder Market")

#Variables

#Adding the variable for the ratio of the truckloads delivered to each store:
X = {(d,s): m.addVar() for d in D for s in S}

#Objective
m.setObjective(quicksum(CT[d][s]*X[d,s]*WD[s] for d in D for s in S),GRB.MINIMIZE)

#Meeting the weekly demand(Communication 1)
for s in S:
    m.addConstr(quicksum(X[d,s]*WD[s] for d in D) == WD[s] )

#Constraint on the capacity demand of each distribution centre:
for d in D:
    m.addConstr(quicksum(X[d,s]*WD[s] for s in S) <= CD[d])
    
#Two distribution centres on the north side of the river
#actually share a labour pool(Communication 3)
F = range(1,3)
m.addConstr(quicksum(X[f,s]*WD[s] for s in S for f in F) <= 88)
for t in range(5):
    m.addConstr(quicksum(X[f,s]*WS[t][s] for s in S for f in F) <= 88)
    
#Keep the ratios in a way that it works for 5 other scenarios(Communication4)
for d in D:
    for t in range(5):
        m.addConstr(quicksum(X[d,s]*WS[t][s] for s in S) <= CD[d] )
  
m.optimize()

#Printing out the number of truckloads from each distribution centre(column)
#to each store(row):
for s in S:
    print(X[0,s].x*WD[s], X[1,s].x*WD[s], X[2,s].x*WD[s])
print("\nRounded answers: \n")    
for s in S:
    print(round(X[0,s].x*WD[s],2), round(X[1,s].x*WD[s],2), round(X[2,s].x*WD[s],2)) 
print("\n OPTIMAL COST: %g" %m.objVal)    