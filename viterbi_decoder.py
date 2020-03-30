#Viterbi Decoder

class State:

    stateTransitionTable = {'s0':['s0','s2'],
                            's1':['s0','s2'],
                            's2':['s1','s3'],
                            's3':['s1','s3']}

    encodingTransitionTable = {'s0':{'s0':0,'s2':3},
                               's1':{'s0':3,'s2':0},
                               's2':{'s1':1,'s3':2},
                               's3':{'s1':2,'s3':1}}

    
    def __init__(self, index):
        self.id = index
        self.prev = [State.stateTransitionTable[index][0],
                     State.stateTransitionTable[index][1]]

    def info (self):
        return str(self.id) + str(self.prev) + str(self.weight)

    def nextState(self, index ):
        return self.prev[index]


class Node(State):
    def __init__(self, index):
        State.__init__(self,'s'+str(index))
        self.weight = 0
        self.weightState = ''

    def findHammingDis(input):
        distance = 0

        while( input != 0 ):
            distance += input%2
            input = int(input/2)
        return distance
    
    def calculateWeight(self, x, prevStage):
        print("--calc--")
        print("node",self.id)
        
        calc0 = Node.findHammingDis(x ^ State.encodingTransitionTable[self.id][self.prev[0]])
        calc1 = Node.findHammingDis(x ^ State.encodingTransitionTable[self.id][self.prev[1]])
        
        print(self.prev[0],prevStage[self.prev[0]], calc0)
        print(self.prev[1],prevStage[self.prev[1]], calc1)
        
        calc0 += prevStage[self.prev[0]]
        calc1 += prevStage[self.prev[1]]

        self.weight = min(calc0,calc1)

        if calc0 == self.weight :
            self.weightState = self.prev[0]
        else:
            self.weightState = self.prev[1]

#        print(self.weight, self.weightState)


class Stage(Node):

    def __init__(self, index, initial = -1):
        self.index = index
        self.nodes = [Node(i) for i in range(4)]
        self.xin = 0
        self.initState = initial

    def newXin(self, x, prevStage):
        self.xin = x;
        [i.calculateWeight(x, prevStage) for i in self.nodes]

    def summarizeStage(self):
        print("--------Stage",self.index,"---------")
        dict = {}
        
        if (self.initState != -1 ):
            for i in self.nodes:
                dict[i.id] = 100
            dict[self.nodes[self.initState].id] = self.nodes[self.initState].weight
        else:
            for i in self.nodes:
                dict[i.id] = i.weight
        return(dict)



stage0 = Stage(0, 0)
stage1 = Stage(1)
stage2 = Stage(2)
stage3 = Stage(3)
stage4 = Stage(4)
stage5 = Stage(5)
#


[print(i.info()) for i in stage0.nodes]

print(stage0.summarizeStage())

stage1.newXin(0, stage0.summarizeStage())
print(stage1.summarizeStage())

stage2.newXin(1, stage1.summarizeStage())
print(stage2.summarizeStage())

stage3.newXin(1, stage2.summarizeStage())
print(stage3.summarizeStage())

stage4.newXin(2, stage3.summarizeStage())
print(stage4.summarizeStage())

stage5.newXin(2, stage4.summarizeStage())
print(stage5.summarizeStage())


print("------res------")
print(stage5.nodes[0].weight)
print(stage5.nodes[1].weight)
print(stage5.nodes[2].weight)
print(stage5.nodes[3].weight)


#


