import random
import heapq
from sklearn import tree
import numpy


przyklady=[]
dec=[]

n=raw_input()
n=int(n)
for j in range(n):
    przyklad=[]
    czy_dom=random.randint(0,1)
    przyklad.append(czy_dom)
    przep=random.randint(0,1)
    przyklad.append(przep)
    paliwo=random.randint(0,1)
    przyklad.append(paliwo)
    zap_kol=random.randint(0,1)
    przyklad.append(zap_kol)
    typ_dom=random.randint(0,1)
    przyklad.append(typ_dom)
    typ_dnia=random.randint(0,1)
    przyklad.append(typ_dnia)
    przyklady.append(przyklad)

    if czy_dom==0:
        if przep==1:
            dec.append(1)
        else:
            if paliwo==0:
                dec.append(1)
            else:
                dec.append(0)
    else:
        if przep==1:
            dec.append(0)
        else:
            if paliwo==0:
                dec.append(0)
            else:
                if zap_kol==1:
                    dec.append(0)
                else:
                    if typ_dom==0:
                        if typ_dnia==1:
                            dec.append(0)
                        else:
                            dec.append(1)
                    else:
                        dec.append(1)

print przyklady

print dec

print len(przyklady)
print len(dec)
