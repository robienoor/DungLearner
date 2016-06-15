class post(object):

    def __init__(self, review, posExp, negExp, SymOK, SymNOK, NoSE, SE, rating, drug):

        self.review = review
        self.rating = rating
        self.drug = drug

        self.posExp = posExp
        self.negExp = negExp
        self.SymOK = SymOK
        self.SymNOK = SymNOK
        self.NoSE = NoSE
        self.SE = SE

    def getRating(self):
        return self.rating

    def getposExp(self):
        return self.posExp

    def getNegExp(self):
        return self.negExp

    def getSymOK(self):
        return self.SymOK

    def getSymNOK(self):
        return self.SymNOK

    def getNoSE(self):
        return self.NoSE

    def getSE(self):
        return self.SE

    def getReview(self):
        return self.review

