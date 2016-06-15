from collections import Counter
from itertools import product

class globalDung(object):

    def __init__(self):

         # We initialise the dung solver by instatiating the list of graph members
        self.graphMembers =  {'A' : [],
                            'B' : [],
                            'C' : [],
                            'D' : [],
                            'E' : [],
                            'F' : []
                            }
        
        # We group the nodes into groups based on polarity. This is so we can make sure no node of same polarity will attack eachother
        self.positiveNodes = {'A','C','E'}
        self.negativeNodes = {'B','D','F'}

        # We intitialise the grounded extension to null
        self.groundedExtension = {}

        self.graphMembersList = list(self.graphMembers.keys())

        globalAttacksFullList = list(product(self.graphMembersList, repeat = 2))
        self.globalAttackList = list(globalAttacksFullList)


        for attack in globalAttacksFullList:
            # Nodes with the same polarity cannot attack eachother
            if((attack[0] in self.positiveNodes) and ((attack[1]) in self.positiveNodes)):
                 self.globalAttackList.remove(attack)
            if((attack[0] in self.negativeNodes) and ((attack[1]) in self.negativeNodes)):
                 self.globalAttackList.remove(attack)



        self.globalWeightedGraph = [0] * len(self.globalAttackList)

    def updateGlobalDung(self, weightedAttackGraph):

        self.globalWeightedGraph = [new + current for new, current in zip(weightedAttackGraph, self.globalWeightedGraph)]
        

    def getGlobalAttacksList(self):
        return self.globalAttackList

            

