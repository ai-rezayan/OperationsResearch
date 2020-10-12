#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:11:17 2019

@author: amirebrahimrezaeian
"""

import numpy as np
#The profit for each type of fridge
profit = [131, 164, 170]

#
Expected = [
        [0.0,	0.3,	3.5,	4.4,	4.6],   #Alaska
	    [0.0	,   0.5,  	2.8,	3.8,	4.1],   #Elsa
        [0.0,	1.9,	3.1,	3.5,	3.8]    #Lumi
        ]   
#The function for communication 1:
def Profit(s,t):
    if t == 3:
        return(0,0)
    return max((Expected[t][x]*profit[t] + Profit(s-x,t+1)[0], x) for x in range(min(4,s)+1))

#The probability of demand for each type of fridge
Demand =[
        [0.00,	0.16,	0.20,	0.31,	0.24,	0.09],
        [0.11, 	0.17,	0.29,	0.25,	0.18,	0.00],
        [0.09,	0.20,	0.32,	0.24,	0.15,	0.00]
        ]

#Warehouse space rental cost for each type of the fridge
warehouse = 30

#The function for communication 2:
def Profit2(f,t,w):
   if t == 4:
       return(0,0)

   return max((
           sum(Demand[f][d]*(profit[f]*min(d+1,x+w)+Profit2(f,t+1,max(0,x+w-(d+1)))[0]) for d in range(6))-warehouse*(w+x)
           ,x)
                for x in range(7))

#Summing over the types of fridges at at Profit2(f,0,0):
def Profit2a(a,b):
    return Profit2(0,a,b)+Profit2(1,a,b)+Profit2(2,a,b),Profit2(0,a,b)[0]+Profit2(1,a,b)[0]+Profit2(2,a,b)[0]    
    
#The function to calculate the probability of ordering fridges    
def Prob(f1,f2,f3):
    
    return Demand[0][f1-1]*Demand[1][f2-1]*Demand[2][f3-1]

#Defining a function for calculating the delivery cost
def Deliv(f1,f2,f3):
    if f1 + f2 + f3 > 7:
        return 300
    else:
        return 150
#Creating 3-D zero matrixes for delivery costs and probabilities(using numpy)
deliv_tab = np.zeros((7,7,7))
prob_tab = np.zeros((7,7,7))


#Populating the matrices with the values from the functions
for f1 in range(7):
    for f2 in range(7):
        for f3 in range(7):
            deliv_tab[f1,f2,f3] = Deliv(f1,f2,f3)
            prob_tab[f1,f2,f3] = Prob(f1,f2,f3)

# Creating a 5-D matrix for storing the weeks and warehouse of each type and the 4-array Profit3 function               
profit3_tab = np.zeros((5,10,10,10,4))


#Defining the main function
def Profit3(t,w1,w2,w3):
    
#Creating variables with low values for initialization   
    best = -999
    x1_best = 0
    x2_best = 0
    x3_best = 0
    
#Looping over the number of each fridge type we are ordering to compute the maximum profit for any given week and warehouse storage
    for x1 in range(7-w1):
        for x2 in range(7-w2):
            for x3 in range(min(7-w3, 14-x1-x2)):
                totalprofit = 0
                for f1 in range(1,7):
                    for f2 in range(1,7):
                        for f3 in range(1,7):
                            totalprofit += prob_tab[f1,f2,f3]*(profit[0]*min(f1,x1+w1)      #Calculating the profit for each probability
                            + profit[1]*min(f2,x2+w2) 
                            + profit[2]*min(f3,x3+w3) 
                            + profit3_tab[t+1,-f1+max(f1,x1+w1),-f2+max(f2,x2+w2),-f3+max(f3,x3+w3)][0]) 
                totalprofit -= deliv_tab[x1,x2,x3]+warehouse*(w1+w2+w3+x1+x2+x3)
                if totalprofit > best:
                    best = totalprofit
                    x1_best = x1
                    x2_best = x2
                    x3_best = x3
    return [best, x1_best, x2_best, x3_best]

#This function is considering all the possibilites of weeks and warehouse storages of our Profit table and returning
#the the desired one, profit_3(0,0,0,0)
def wrapper():
    for t in range(0, 4):
        profit3_tab[t, 9, 9, 9] = [-999,0,0,0]
    for w1 in range(9):
        for w2 in range(9):
            for w3 in range(9):
                profit3_tab[4, w1, w2, w3] = [0,0,0,0]
    for t in range(0, 3):
        for w1 in range(9):
            for w2 in range(9):
                for w3 in range(9):
                    profit3_tab[3-t, w1, w2, w3] = Profit3(3-t,w1,w2,w3)
                    print(3-t, w1, w2, w3, profit3_tab[3-t, w1, w2, w3][0])
    profit3_tab[0, 0, 0, 0] = Profit3(0,0,0,0)
    return profit3_tab[0, 0, 0, 0]
    

    
    
    


    



