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

#Now considering all Distribution Centres:
DistributionCenters = ["DC0", "DC1", "DC2","DC3","DC4","DC5","DC6"]

#Data

# Pooled Capacity limitation at the distribution centres
CD = [48, 63, 57,19, 45, 77, 77]

#Considering all distribution centres:
#The cost of transporting one truckload from each distribution centre(column) to each store(row):
CT = [
    [2081,	2462,	2958,	1911,	2735,	1805,	2139,	2795,	1456,	2707],
	[1094,	1267,	1996,	1091,	1520,	1016,	1200,	1880,	912,	2100],
	[1418,	1604,	2877,	2566,	2113,	2578,	2570,	2900,	2478,	3379],
    [1506,	1146,	1945,	2241,	1371,	2304,	2020,	2147,	2423,	2654],
    [2321,	2105,	1381,	1096,	1774,	1255,	1152,	1077,	1542,	716],
    [2766,	2752,	2059,	1588,	2391,	1641,	1674,	1772,	1804,	1181],
    [1469,	1802,	2505,	1550,	2107,	1389,	1714,	2370,	1087,	2392]
    ]

#The weekly demand at the ten stores:
WD = [12, 12, 10, 21, 6, 10, 12, 11, 8, 14]

#Different weekly demand scenarios we are required to meet
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

#Adding a binary variable to decide which new distribution centre should be used:
Y = {d: m.addVar(vtype=GRB.BINARY) for d in D}

#Objective
m.setObjective(quicksum(CT[d][s]*X[d,s]*WD[s] for d in D for s in S),GRB.MINIMIZE)

#Adding constraints for choosing one new distribution centre and choosing 4 in total:
m.addConstr(quicksum(Y[d] for d in range(3,7)) == 1)
m.addConstr(quicksum(Y[d] for d in D) == 4)

#Adding constraints for only delivering from the distribution centres chosen:
for s in S:
    DCused = {d: m.addConstr(Y[d] >= X[d,s]) for d in D}

#Constraint on the ratios
for s in S:
  
#Communication 5 requiring only one distribution center for each store
#Using a Special Ordered Set constraint:    
    m.addSOS(GRB.SOS_TYPE1, [X[0,s],X[1,s],X[2,s],X[3,s],X[4,s],X[5,s],X[6,s]])

#Meeting the weekly demand(Communication 1)
for s in S:
    m.addConstr(quicksum(X[d,s]*WD[s] for d in D) == WD[s])

#Constraint on the capacity demand of each distribution centre:
for d in D:
    m.addConstr(quicksum(X[d,s]*WD[s] for s in S) <= CD[d])
    
#Keep the ratios in a way that it works for 5 other scenarios(Communication4)
#Having the same distribution ratio for different scenarios
for d in D:
    for t in range(5):
        m.addConstr(quicksum(X[d,s]*WS[t][s] for s in S) <= CD[d] )
   
m.optimize()

#Printing out the number of truckloads from each distribution centre(column)
#to each store(row):
#Using round function to print discrete number of truckloads(without decimals)
for s in S:
        print(round(X[0,s].x*WD[s]), round(X[1,s].x*WD[s]), round(X[2,s].x*WD[s]),round(X[3,s].x*WD[s]),
              round(X[4,s].x*WD[s]),round(X[5,s].x*WD[s]),round(X[6,s].x*WD[s]))
print("\n OPTIMAL COST: %g" %m.objVal)    
