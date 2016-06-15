import itertools
import logging

# The aim of this class is to take in a Dung graph and evaluate the winning grounded extension

class dungEvaluator:

    # Define the nodes of each graph
    def __init__(self, noA, noB, noC, noD, noE, noF, dungGraphOutward):

        self.dungGraphMembers = {'A' : noA,
                            'B' : noB,
                            'C' : noC,
                            'D' : noD,
                            'E' : noE,
                            'F' : noF
                            }
        
        

        self.dungBaseGraphOutWard = dungGraphOutward

        self.dungGraphOutward = self.dungBaseGraphOutWard.copy()

        for key, noOfArgs in self.dungGraphMembers.items():
            # We want to remove any mention of a node within the graphs if they exists
            if noOfArgs == 0:
                # Remove the node from the overall graph
                self.dungGraphOutward.pop(key, None)

                # Remove any mention of node within the attack structure
                for node, attacks in self.dungGraphOutward.items():
                    if key in attacks:
                        attacks.remove(key)

    def getConflictFreeSets(self):
        
        listOfNodes = list(self.dungGraphOutward.keys())
        listOfArgSets = []

        # Generate all combinations of node sets. This represents all the possible argument sets
        for i in range(1, len(listOfNodes) + 1):
            argSet = [list(x) for x in itertools.combinations(listOfNodes, i)]
            listOfArgSets.extend(argSet)
        

        conflictedSets = []
        # Remove all of the conflict sets
        for argSet in listOfArgSets:
        # At this stage we have the arg set        
            conflictFlag = False
         
            for node in argSet:
                for deepNode in argSet:
                    if deepNode in self.dungGraphOutward[node]:
                        conflictedSets.append(argSet)
                        conflictFlag = True
                        break
                if conflictFlag: break

        nonConflictedSets = [argSet for argSet in listOfArgSets if argSet not in conflictedSets]
        return nonConflictedSets

    def getAdmissibleSets(self):

        nonConflictedSets = self.getConflictFreeSets()
        nonAdmissibleSets = []

        for set in nonConflictedSets:
            setNonAdmissFlag = False

            hitlist = []
            for node in set:
                targets = self.dungGraphOutward[node]
                for target in targets: hitlist.append(target)
            

            for attacker, victims in self.dungGraphOutward.items():
                for node in set:

                    if node in victims:
                        if attacker not in hitlist:
                            # Then set is not protected. Delete the set from the list
                            nonAdmissibleSets.append(set)
                            setNonAdmissFlag = True
                            break

                if setNonAdmissFlag: break

        admissibleSets = [set for set in nonConflictedSets if set not in nonAdmissibleSets]
        return admissibleSets

    def getCompleteExtentions(self):
        
        admissibleSets = self.getAdmissibleSets()
        # Need to find trivially defended arguments:
        triviallyDefendedNodes = []

        for node, values in self.dungGraphOutward.items():
            triviallySafe = False

            for attacker, victims in self.dungGraphOutward.items(): 
                if node not in victims:
                    triviallySafe = True
                else:
                    triviallySafe = False
                    break
            
            if triviallySafe: triviallyDefendedNodes.append(node)

        completeExtensions = []
        for admisSet in admissibleSets:
            argGraph = self.dungGraphOutward.copy()

            hitlist = []
            for node in admisSet:
                targets = self.dungGraphOutward[node]
                for target in targets: hitlist.append(target)
            
            for target in hitlist:
                argGraph.pop(target, None)

            defendedSet = list(argGraph.keys())
            if set(defendedSet) == set(admisSet):
                completeExtensions.append(admisSet)
                

        return completeExtensions

    def getGroundedExtensions(self):

        completeExtensions = self.getCompleteExtentions()

        minimalSets = []

        for compSet in completeExtensions:
            minSet = True
            for compSetTwo in completeExtensions:
                 result = self.sublistExists(compSet, compSetTwo)
                 if not result:  minSet = False

            if minSet: minimalSets.append(compSet)

        if len(minimalSets) > 1:
            logging.WARNING('We got more than one grounded extension. Taking the first one')

        return minimalSets

    def sublistExists(self, list, sublist):
        for i in range(len(list)-len(sublist)+1):
            if sublist == list[i:i+len(sublist)]:
                return True 
        return False 