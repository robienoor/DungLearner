from itertools import product
from dungEvaluator import dungEvaluator
import logging

class dungLearner:
    # This method looks at the nodes populated by the post and the rating. Based on this it returns the ideal grounded sets.
    def __init__(self, noA, noB, noC, noD, noE, noF, rating):

        # We initialise the dung solver by instatiating the list of graph members
        self.graphMembers =  {'A' : noA,
                            'B' : noB,
                            'C' : noC,
                            'D' : noD,
                            'E' : noE,
                            'F' : noF
                            }
        
        # We group the nodes into groups based on polarity. This is so we can make sure no node of same polarity will attack eachother
        self.positiveNodes = ['A','C','E']
        self.negativeNodes = ['B','D','F']
        self.rating = rating

        # We intitialise the grounded extension to null
        self.groundedExtension = []

        # We initialise the dung solver by assuming there are no attacks between the nodes
        self.baseGraphOutward = {'A':{},
                                 'B':{},
                                 'C':{},
                                 'D':{},
                                 'E':{},
                                 'F':{}
            }

        # Make a copy of the base graph
        self.graphOutward = dict(self.baseGraphOutward)

        # Get a list of nodes populated. Need a list form of these for quick reference
        self.graphMembersList = []
        for member in self.graphMembers:
            if self.graphMembers[member] > 0:
                self.graphMembersList.append(member)
        


        for key, noOfArgs in self.graphMembers.items():
            # We want to remove any mention of a node within the graph's attack structure if they don't exist
            if noOfArgs == 0:
                # Remove the node from the overall graph
                self.graphOutward.pop(key, None)

                # Remove any mention of node within the attack structure
                for node, attacks in self.graphOutward.items():
                    if key in attacks:
                        attacks.remove(key)
        
        logging.info('Arguments per Node: ')
        logging.info(self.graphMembers)

        logging.info('Populated Nodes: ')
        logging.info(self.graphMembersList)


        self.getDesiredGroundedSet()
        self.listOfPlausibleAttacks, self.allAttackGraphs = self.generateAllDungGraphs()

    def getDesiredGroundedSet(self):
        for node, attacks in self.graphOutward.items():
            # We want to remove any mention of a nodes that wont be in the grounded extension based on polarity of rating
            if self.rating < 4:
                # Add node to the grouneded extension
                if node in self.negativeNodes:
                    self.groundedExtension.append(node)

            if self.rating > 7:
                if node in self.positiveNodes:
                    self.groundedExtension.append(node)
        
        logging.info('Desired grounded set: ')
        logging.info(self.groundedExtension)
        
    def generateAllDungGraphs(self):

        allPossibleOutwardGraphs = []

        # Build the list containing the plausible attack pairs. Eg: [A,B] means A attacks B
        fullListOfAttacks = list(product(self.graphMembersList, repeat = 2))
        listOfAttacks = list(fullListOfAttacks)

        for attack in fullListOfAttacks:
            # Nodes with the same polarity cannot attack eachother
            if((attack[0] in self.positiveNodes) and ((attack[1]) in self.positiveNodes)):
                 listOfAttacks.remove(attack)
            if((attack[0] in self.negativeNodes) and ((attack[1]) in self.negativeNodes)):
                 listOfAttacks.remove(attack)
        
        # Build a list of all possible Dung graphs. This is based on the attack list
        allAttackGraphs = list(product((1, 0), repeat = len(listOfAttacks)))
        logging.info('No of Possible Dung Graphs: ' + str(len(allAttackGraphs)))

        return listOfAttacks, allAttackGraphs

    def convertAttackGraphtoOutwardGraph(self, listOfPlausibleAttacks, attackGraph):

        graphOutward = {'A':[],
                        'B':[],
                        'C':[],
                        'D':[],
                        'E':[],
                        'F':[]
            }

        for idx, attack in enumerate(attackGraph):
            if attack == 1:
                # Find the attacking node
                attacker = (listOfPlausibleAttacks[idx])[0]
                victim = (listOfPlausibleAttacks[idx])[1]

                if attacker in graphOutward:
                    graphOutward[attacker].append(victim)

        return graphOutward

    def checkGraphPositive(self, graph):
        
        negative = False
        positive = False

        posCounter = 0
        negCounter = 0
        for node in graph:
            if node in self.positiveNodes:
                posCounter = posCounter + 1
            if node in self.negativeNodes:
                negCounter = negCounter + 1
        
        if posCounter == len(graph):
            return True

        if negCounter == len(graph):
            return False

        if ((negative == True) & (positive==True)):
            logging.WARNING('Grounded extension did not fall into a class. Something went wrong')
            return False

    def getWeightedDungGraph(self, globalAttacksList):
        
        logging.info('----Anlaysis----')

        self.overalllAttackCount = list(self.listOfPlausibleAttacks)

        groundedLists = []

        # Iterate over each attackgraph and find which ones are grounded
        for attackGraph in self.allAttackGraphs:
            graphOutward = self.convertAttackGraphtoOutwardGraph(self.listOfPlausibleAttacks, attackGraph)


            # We to create a new list of graph members. It may be the case that a node is in this post, but in the attack graph it is not attacked nor attacking. If this this the case
            # it will be trivially defended and remain in the grounded set. Need to remove such nodes 
            modifiedGraphMembers =  {'A' : 0,
                                    'B' : 0,
                                    'C' : 0,
                                    'D' : 0,
                                    'E' : 0,
                                    'F' : 0
                                    }


            for idx, attack in enumerate(attackGraph):
                if attack == 1:
                    modifiedGraphMembers[(self.listOfPlausibleAttacks[idx])[0]] += 1
                    modifiedGraphMembers[(self.listOfPlausibleAttacks[idx])[1]] += 1

            dungEval = dungEvaluator(modifiedGraphMembers['A'],
                                     modifiedGraphMembers['B'],
                                     modifiedGraphMembers['C'],
                                     modifiedGraphMembers['D'],
                                     modifiedGraphMembers['E'],
                                     modifiedGraphMembers['F'], 
                                     graphOutward)
            
            groundedExtension = dungEval.getGroundedExtensions()
            
            # If we get a grounded extension, need to check to see it is the same as the desired grounded extension
            if groundedExtension:         
                if set(groundedExtension[0]) == set(self.groundedExtension):
                    groundedLists.append(attackGraph)

        logging.info('No of correlated grounded graphs: ' + str(len(groundedLists)))

        # Instantiate empty weighted graph
        weightedGraph = [0] * len(globalAttacksList)

        # Make a sum of the grounded Lists
        if groundedLists:
            sumOfGroundedLists = [sum(row[i] for row in groundedLists) for i in range(len(groundedLists[0]))]

            # Normalise the sum values by the number of grounded extensions retrieved
            for idx, attack in enumerate(sumOfGroundedLists): 
                sumOfGroundedLists[idx] = attack / len(groundedLists)

        
            # Return the normalised weighted Dung graph in a format for the globalDung graph
            for idxGlobal, attackGlobal in enumerate(globalAttacksList):
                for idx, attack in enumerate(self.listOfPlausibleAttacks):
                    if attack == attackGlobal:
                        weightedGraph[idxGlobal] = sumOfGroundedLists[idx]


        return weightedGraph
            
             
            
       




        




                

         

            
            







        


