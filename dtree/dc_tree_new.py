import random
import heapq
from sklearn import tree
import numpy


atrybuty=["czy_dom","przepelnienie","paliwo","zapelnienie_kolorem","typ_domku","czy_weekend"]
#true=1, false=0

# zbior uczacy
X =[[1, 1, 1, 0, 1, 1], [1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 0, 1], [0, 1, 0, 1, 1, 0], [1, 1, 1, 0, 0, 1], 
    [0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0], [1, 1, 1, 1, 0, 0], [0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1], 
    [1, 1, 0, 1, 0, 1], [1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0], [0, 1, 1, 1, 0, 1], [0, 1, 0, 1, 0, 1], [1, 1, 0, 0, 1, 0], 
    [0, 1, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0], [0, 1, 1, 0, 1, 1], [1, 1, 1, 0, 1, 1], [0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], 
    [0, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 1], [0, 1, 0, 1, 1, 0], [1, 1, 0, 1, 1, 1], [0, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 1], 
    [0, 0, 0, 1, 1, 0], [0, 0, 1, 0, 0, 1], [1, 1, 0, 1, 0, 1], [1, 1, 0, 1, 1, 1], [1, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 1], 
    [1, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1], [1, 0, 0, 0, 0, 1], [0, 0, 1, 1, 0, 1], 
    [1, 1, 1, 1, 1, 1], [1, 1, 1, 0, 0, 1], [0, 0, 1, 0, 1, 0], [1, 1, 1, 0, 1, 1], [0, 0, 1, 0, 0, 1], [1, 1, 1, 0, 0, 1], 
    [0, 0, 0, 1, 0, 0], [1, 1, 0, 1, 1, 0], [1, 1, 1, 1, 1, 0], [1, 1, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0], [0, 1, 0, 1, 1, 0], 
    [1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 1, 1], [1, 0, 0, 0, 1, 0], [1, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1], 
    [0, 1, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0], [1, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0], [1, 0, 1, 1, 1, 1], [1, 0, 1, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 0], [1, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 0], [1, 1, 0, 0, 1, 0], [1, 1, 0, 1, 1, 1], 
    [0, 0, 0, 0, 1, 0], [0, 1, 1, 1, 1, 0], [0, 1, 0, 0, 0, 1], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0], [1, 0, 0, 1, 1, 1], 
    [1, 0, 1, 1, 0, 1], [0, 0, 0, 0, 1, 1], [1, 1, 0, 1, 1, 0], [0, 1, 0, 0, 1, 0], [1, 1, 0, 1, 0, 1], [0, 0, 1, 0, 0, 1], 
    [0, 1, 1, 1, 1, 0], [1, 0, 1, 0, 0, 1], [0, 0, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1], [0, 1, 1, 1, 1, 0], [1, 0, 0, 0, 1, 1], 
    [1, 0, 1, 1, 0, 1], [0, 1, 0, 0, 1, 1], [0, 0, 1, 1, 1, 1], [1, 1, 1, 0, 1, 0], [0, 1, 0, 0, 1, 1], [1, 1, 1, 0, 1, 0], 
    [0, 1, 1, 1, 0, 0], [0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1], [0, 1, 0, 1, 1, 1], 
    [1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 0], [0, 1, 1, 0, 0, 1], [0, 0, 1, 1, 0, 0], [1, 1, 0, 1, 1, 0], [1, 0, 0, 1, 1, 0], 
    [1, 1, 0, 0, 0, 0], [1, 1, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1], 
    [1, 1, 1, 1, 0, 0], [0, 1, 0, 1, 1, 0], [0, 0, 0, 0, 0, 1], [0, 0, 1, 1, 0, 1], [1, 1, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1], 
    [1, 0, 1, 1, 0, 0], [1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 0, 0], [1, 0, 0, 1, 0, 0], [0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 0, 0], 
    [0, 1, 1, 1, 0, 1], [1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 0, 0], [0, 1, 1, 0, 0, 1], [0, 1, 0, 0, 0, 1], [1, 0, 0, 1, 1, 1], 
    [1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 1, 1], [0, 1, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0], 
    [0, 0, 1, 1, 0, 1], [0, 0, 1, 0, 1, 1], [1, 1, 1, 1, 0, 0], [0, 1, 0, 1, 1, 0], [1, 0, 1, 0, 0, 1], [0, 1, 0, 0, 1, 0], 
    [1, 1, 0, 1, 1, 0], [1, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1], [0, 0, 0, 1, 1, 0], 
    [1, 0, 0, 0, 1, 1], [0, 1, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0], [1, 1, 0, 1, 1, 0], [1, 0, 1, 1, 0, 1], [0, 1, 1, 1, 0, 0], 
    [0, 1, 1, 0, 0, 1], [1, 0, 0, 0, 1, 1], [0, 1, 0, 1, 1, 1], [1, 1, 0, 0, 1, 0], [1, 1, 1, 0, 1, 0], [0, 1, 1, 0, 1, 1], 
    [0, 0, 1, 1, 1, 0], [0, 1, 0, 1, 0, 1], [1, 0, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], 
    [1, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1], [1, 0, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0]]      

Y = [0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1,
     0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1,
     0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0,
     0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0]


clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

#prediction=clf.predict([[1,0,1,0,1,0]])
#print (prediction)






zapziel=0
zapzol=0
zapnieb=0
pomin=[]
pominkolor=[]

def locate(point,pominlokacje,pominkolor):
    next=point
    primpoint=point
    a=1
    b=-1
    mzpx=[-1,0,1]
    mzpy=[-1,0,1]
    while True:
        for x in mzpx:
            for y in mzpy:
                newpoint=point[0]+(mzpx[x]),point[1]+(mzpy[y])
                if newpoint[0]>=0 and newpoint[0]<=9 and newpoint[1]>=0 and newpoint[1]<=9 and newpoint!=primpoint:
                    if tab[newpoint[0]][newpoint[1]]==3 and tab[newpoint[0]][newpoint[1]] not in pominlokacje :
                        if tabtrash[newpoint[0]][newpoint[1]]>0 :
                            if tabtrash[newpoint[0]][newpoint[1]]==1 and tabtrash[newpoint[0]][newpoint[1]] not in pominkolor :
                                return newpoint
                                break
                            elif tabtrash[newpoint[0]][newpoint[1]]==2 and tabtrash[newpoint[0]][newpoint[1]] not in pominkolor :           
                                return newpoint
                                break
                            elif tabtrash[newpoint[0]][newpoint[1]]==3 and tabtrash[newpoint[0]][newpoint[1]] not in pominkolor:           
                                return newpoint
                                break
                        else:
                            pass
                    elif tab[newpoint[0]][newpoint[1]]<0 and tab[newpoint[0]][newpoint[1]] not in pominlokacje :
                        return newpoint
                        break
                        
                else:
                    pass
        a=a+1
        b=b-1
        mzpx.append(a)
        mzpx.insert(0,b)
        mzpy.append(a)
        mzpy.insert(0,b)

def dec_smieciarka(point,czy_dom,przepelnienie,paliwo,zapziel,zapnieb,zapzol,typ_domku,czy_weekend):
    pominlokacje=[]
    pominkolor=[]
    if zapziel==1 and zapnieb==1 and zapzol==1:
        przepelnienie=1
        pominlokacje.append(3)
    else:
        pominlokacje.append(-1)
        pominlokacje.append(-2)
        pominlokacje.append(-3)
    if zapziel==1:
        pominkolor.append(1)
    if zapnieb==1:
        pominkolor.append(2)
    if zapzol==1:
        pominkolor.append(3)
    
    location=locate(point,pominlokacje,pominkolor)


    dec_table=[czy_dom,przepelnienie,paliwo,zap_kol,typ_domku,czy_weekend]
    prediction=clf.predict([[dec_table]])
    if prediction
    



















