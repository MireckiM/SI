
zapziel=0
zapzol=0
zapnieb=0
pomin=[]

def trashloc(point,pomin):
    next=point
    primpoint=point
    a=1
    b=-1
    mzpx=[-1,0,1]
    mzpy=[-1,0,1]
    while next==point:
        for x in mzpx:
            for y in mzpy:
                newpoint=point[0]+(mzpx[x]),point[1]+(mzpy[y])
                if newpoint[0]>=0 and newpoint[0]<=9 and newpoint[1]>=0 and newpoint[1]<=9 and newpoint!=primpoint:

                    if(tab[newpoint[0]][newpoint[1]]==3):
                        if(tabtrash[newpoint[0]][newpoint[1]]>0):
                            if(tabtrash[newpoint[0]][newpoint[1]]==1 and zapziel<1):
                                next=newpoint
                                print "Punkt docelowy ze smieciami zielonymi:" , next
                                break
                            elif(tabtrash[newpoint[0]][newpoint[1]]==2 and zapnieb<1):           
                                next=newpoint
                                print "Punkt docelowy ze smieciami niebieskimi:" , next
                                break
                            elif(tabtrash[newpoint[0]][newpoint[1]]==3 and zapzol<1):           
                                next=newpoint
                                print "Punkt docelowy ze smieciami zoltymi:" , next
                                break
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
        a=a+1
        b=b-1
        mzpx.append(a)
        mzpx.insert(0,b)
        mzpy.append(a)
        mzpy.insert(0,b)
    if zapziel==1 and zapnieb==1 and zapzol==1:
        print "Znaleziono wszystkie smieci na mapie"
    else:
        trashloc(next,zapziel,zapnieb,zapzol)


def dumploc():
    ox=[0,1,2,3,4,5,6,7,8,9]
    oy=[0,1,2,3,4,5,6,7,8,9]
    point=0,0
    f=0
    while f!=3:
        for x in ox:
            for y in oy:
                newpoint=x,y
                if(tab[newpoint[0]][newpoint[1]]==-1):
                    dziel=newpoint
                    f=f+1
                elif(tab[newpoint[0]][newpoint[1]]==-2):
                    dnieb=newpoint
                    f=f+1
                elif(tab[newpoint[0]][newpoint[1]]==-3):#
                    dzol=newpoint
                    f=f+1
    
    print "Punkt docelowy wysypisko w lokacjach: ", dziel, dnieb, dzol                            
    

