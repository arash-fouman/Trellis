import numpy as np


H = [[1,1,0,0, 1,  0,0,0,0, 0],
     [1,0,1,0, 0,  0,0,0,0, 1],
     [1,0,0,1, 1,  0,0,0,0, 0],
     [0,0,0,0, 0,  1,1,0,0, 1],
     [0,0,0,0, 0,  1,0,1,0, 1],
     [0,0,0,0, 0,  1,0,0,1, 1]]


dataBits = len(H[0])
parityBits = len(H)


class Node:

    
    extrinsic = np.zeros((parityBits,dataBits))
    sigma = np.zeros(dataBits)

    def __init__(self, index, type, H):
        
        self.index = index
        self.type = type
        self.nodeConnections = [i for i in range(len(H)) if H[i]==1 ]

    def getExtrinsic( checker, nodeIndex):
        return Node.extrinsic[checker][nodeIndex]
    
    
    def print(self):
        string=", "
        return("Node index: "+ str(self.index)+" Node type: "+self.type+" check eq.: "+string.join([str(i) for i in self.nodeConnections]))


class DataNode(Node):

    def __init__(self, index, type, val, H):
        Node.__init__(self,index,type,H)
        self.dataVal = val
    
    
    def sigma( self ):

        sum = self.dataVal;
        for i in self.nodeConnections:
            sum += Node.getExtrinsic(i, self.index)
        Node.sigma[self.index] = sum
        print ("sum: ",sum)
        print (Node.sigma)
        return(np.round(sum,2))

    def print(self):
        string=", "
        return(super().print()+" Channel reading: "+str(self.dataVal))


class CheckNode(Node):
    
    def __init__(self, index, type, H):
        Node.__init__(self, index, type, H)


    def updateExtrinsic(self, dIn):

        alaki = Node.sigma-Node.extrinsic[self.index]
        alaki2 =  [alaki[i] for i in self.nodeConnections ]

        for i in range(len(alaki2)):
            if len(alaki2) == 1:
                continue
            test = np.delete(alaki2,i)
            min = CheckNode.absoluteMin(test)
            sign = CheckNode.aggrSign(test)
            Node.extrinsic[self.index][self.nodeConnections[i]] = sign*min

        print(Node.extrinsic,"\n\n")

    def absoluteMin(L):
        return np.absolute(L).min()
    def aggrSign(L):
        x = 1
        for i in L:
            x *= i
        return ( -1 if x<0 else +1)


#    def creatExtrinsic(self):
#        self.extrinsic = dict([(i, 0) for i in self.nodeConnections])
#        print(CheckNode.extrinsic[0])






#H = [[1,1,1,0,0,0,1,0,0,0,0],
#     [0,0,0,1,1,1,0,1,0,0,0],
#     [1,0,0,1,0,0,0,0,1,0,0],
#     [0,1,0,0,1,0,0,0,0,1,0],
#     [0,0,1,0,0,1,0,0,0,0,1]]

#H = [[0,1,1,1,0,0,1,0,1,0,0],
#     [0,1,0,1,0,1,0,1,0,1,0],
#     [1,1,0,1,1,0,0,0,1,1,0],
#     [0,1,1,0,1,1,0,0,0,1,1],
#     [1,1,0,1,1,0,1,1,0,0,1]]



dataBits = len(H[0])
parityBits = len(H)
eqCount = 5

H = np.array(H)
Ht = H.transpose()
x = 2
y = 4
Lc = np.array([0, x, y, 1, -100,0, x, y, -3, 100])
print(Lc)
print (Ht)


d = []
for i in range(0,dataBits):
    d.append(DataNode(i,'d',Lc[i],Ht[i]))

for i in range(dataBits,len(Ht)):
    d.append(DataNode(i,'p',Lc[i],Ht[i]))

c = []
for i in range(len(H)):
    c.append(CheckNode(i,'c',H[i]))


#for i in d:
#    print(i.print())
#

for i in c:
    print(i.print())

sigma = 0
sigma_prime = -1
for i in range(0,100):
#    print (i, sigma)
    if sigma == sigma_prime:
        break
    sigma_prime = sigma
    sigma = [d[i].sigma() for i in range(len(Ht))]

    for j in range(len(c)):
        c[j].updateExtrinsic(Lc)
print(Node.sigma[0],Node.sigma[5])
