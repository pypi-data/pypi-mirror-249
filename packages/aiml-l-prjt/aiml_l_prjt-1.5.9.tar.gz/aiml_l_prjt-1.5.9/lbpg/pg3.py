# pg 3

# import numpy as np 
# import pandas as pd
# data = pd.read_csv('enjoysport.csv') 
# print(data)
# concepts = np.array(data.iloc[:, 0:-11]) 
# target = np.array(data.iloc[:, -1])
# def learn(concepts, target):
#   for i,val in enumerate(target): 
#     if val == 'yes': break
#   specific_h = concepts[i].copy()
#   generic_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
#   for i, h in enumerate(concepts):
#     if target[i] == 'yes': 
#       for x in range(len(specific_h)): 
#         if h[x]!=specific_h[x]: 
#           specific_h[x] = '?' 
#           generic_h[x][x] = '?'
#     if target[i] == 'no': 
#       for x in range(len(specific_h)):
#         if h[x]!=specific_h[x]: 
#           generic_h[x][x] = specific_h[x]
#         else:
#           generic_h[x][x] = '?'
#   indices = [i for i,val in enumerate(generic_h) if val == ["?", "?","?","?","?","?"]]
#   for i in indices:
#     generic_h.remove(['?','?','?', '?','?','?']) 
#   return specific_h, generic_h
# s_final, g_final = learn(concepts, target)
# print("Final S: ", s_final, sep= "\n")
# print("Final G: ", g_final, sep= '\n')