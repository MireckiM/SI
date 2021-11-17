from sklearn import tree
clf = tree.DecisionTreeClassifier()    

 
#[height, hair-length, voice-pitch]                                             
X = [ [180, 15,0],                                                              
      [167, 42,1],                                                              
      [136, 35,1],                                                              
      [174, 15,0],                                                              
      [141, 28,1]]                                                              

Y = [1,0,0,1,0]

clf = clf.fit(X, Y)                                                             
prediction = clf.predict([[193, 37,1]])                                         
if prediction == [0]:
    print "kobieta"
if prediction ==[1]:
    print "mezczyzna"   
