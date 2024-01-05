#candidate
# import csv
f=open("candidate.csv")
csv_file = csv.reader(f)
data = list(csv_file)

specific = data[1][:-1]
general = [['?' for i in range(len(specific))] for j in range(len(specific))]
gh = [] # gh = general Hypothesis

for i in data:
    if i[-1] == "Yes":
        for j in range(len(specific)):
            if i[j] != specific[j]:
                specific[j] = "?"
                general[j][j] = "?"
    elif i[-1] == "No":
        for j in range(len(specific)):
            if i[j] != specific[j]:
                general[j][j] = specific[j]
            else:
                general[j][j] = "?"
    print(specific)
    print(general)


for i in general:
    for j in i:
        if j != '?':
            gh.append(i)
            break #Remember this
        
print("\nFinal Specific hypothesis:\n", specific)
print("\nFinal General hypothesis:\n", gh)




import numpy as np import pandas as pd
data = pd.read_csv('enjoysport.csv') print(data)
concepts = np.array(data.iloc[: , 0:-1]) target = np.array(data.iloc[:, -1])
def learn(concepts, target):
#Trying to find out the first YES row.... for i, val in enumerate(target):
if val == 'yes': break
specific_h = concepts[i]. copy()
generic_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
for i, h in enumerate(concepts): if target[i] == 'yes':
for x in range(len(specific_h)): if h[x]!=specific_h[x]:
specific_h[x] = '?' generic_h[x][x] = '?'
if target[i] == 'no':
for x in range(len(specific_h)):
    if h[x]!=specific_h[x]: generic_h[x][x] = specific_h[x]
else:
generic_h[x][x] = '?'
indices = [i for i, val in enumerate(generic_h) if val == ['?','?','?','?','?','?']]
for i in indices: generic_h.remove(['?','?','?','?','?','?'])
return specific_h, generic_h
s_final, g_final = learn(concepts, target) print("Final S: " , s_final, sep= '\n') print("Final G: " , g_final, sep= '\n')