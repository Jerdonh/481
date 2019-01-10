#JERDON HELEGESON
#REACT Module


"""
***************************************************************************
                \/         Prerequisite Code        \/
***************************************************************************
"""

class Particle:

    def __init__(self, sym, chg, massNumber):
        self.sym = sym
        self.chg = chg
        self.massNumber = massNumber

    def __str__(self):
        return self.sym

    def __repr__(self):
        className = self.__class__.__name__
        return "{}({!r}, {!r}, {!r})".format(
            className, self.sym, self.chg, self.massNumber)

    def __add__(self, other):
        return (self, other)

    def __radd__(self, other):
        return (other, self)

class Nucleus(Particle):
    def __str__(self):
        return "({}){}".format(self.massNumber, self.sym)


em = Particle("e-", -1, 0)       # an electron
ep = Particle("e+", 1, 0)        # a positron
p = Particle("p", 1, 1)          # a proton
n = Particle("n", 0, 1)          # a neutron
nu_e = Particle("nu_e", 0, 0)    # a neutrino
gamma = Particle("gamma", 0, 0)  # a gamma particle

d = Nucleus("H", 1, 2)    # hydrogen
li6 = Nucleus("Li", 3, 6) # lithium
he4 = Nucleus("He", 2, 4) # helium


"""
***************************************************************************
                   \/           My Code          \/
***************************************************************************                                
"""


class Reaction:
    def __init__(self,lhs,rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.checkRules()
        
    def checkRules(self):
        cDiff = self.checkCharge()
        if(cDiff != 0):
            raise UnbalancedCharge(cDiff)
        mDiff = self.checkMass()
        if(mDiff != 0):
            raise UnbalancedNumber(mDiff)   

    def checkCharge(self):
        lCharge = 0
        rCharge = 0
        if(isinstance(self.lhs, Particle)):
            lCharge = self.lhs.chg
        else:
            for c in self.lhs:
                lCharge += c.chg
        if(isinstance(self.rhs, Particle)):
            rCharge = self.rhs.chg
        else:
            for c in self.rhs:
                rCharge += c.chg
        return abs(lCharge - rCharge) 

    def checkMass(self):
        lMass = 0
        rMass = 0
        if(isinstance(self.lhs, Particle)):
            lMass = self.lhs.massNumber
        else:
            for c in self.lhs:
                lMass += c.massNumber
        if(isinstance(self.rhs, Particle)):
            rMass = self.rhs.massNumber
        else:
            for c in self.rhs:
                rMass += c.massNumber
        return abs(lMass - rMass)

    def __str__(self):
        output = ""
        if(isinstance(self.lhs, Particle)):
            output = output + "(" + str(self.lhs.massNumber) + ")" + str(self.lhs.sym) + "-> "
        else:
            for c in self.lhs:
                output = output +  "(" + str(c.massNumber) + ")" + str(c.sym) + " + "
            output = output[0:-2] + "-> "
        if(isinstance(self.rhs, Particle)):
            output = output + "(" + str(self.rhs.massNumber) + ")" + str(self.rhs.sym) + "-> "
        else:
            for c in self.rhs:
                output = output +  "(" + str(c.massNumber) + ")" + str(c.sym) + " + "
        return output[0:-3]

    

class ChainReaction():

    def __init__(self, name):
        self.name = name
        self.chain = [] #list of reactions
        self.netReaction = "" #for now empty str

    def addReaction(self, rctn):
        self.chain.append(rctn)
        self.constructNet()

    def constructNet(self):
        netRhs = []
        netLhs = []
        
        #1.merge all lhs'
        for l in self.chain:
            if(isinstance(l.lhs, Particle)):
                netLhs.append(l.lhs)
            else:
                for p in l.lhs:
                    netLhs.append(p)
        #2.merge all rhs'
        for r in self.chain:
            if(isinstance(r.rhs,Particle)):
                netRhs.append(r.rhs)
            else:
                for p in r.rhs:
                    netRhs.append(p)
        #3.cancel out duplicates on each side
        for rc in netLhs:
            if rc in netRhs:
                netLhs.remove(rc)
                netRhs.remove(rc)
        for rc in netRhs:
            if rc in netLhs:
                netLhs.remove(rc)
                netRhs.remove(rc)
        
        #4.build the net reaction out of updated left and right lists
        net = ""
        for nR in netLhs:
            #for nPr in nR: #if each value in netRhs is a reaction and not a particle
            net = net + nR.__str__() + " + "
        net = net[0:-2] + "-> "
        for nL in netRhs:
            #for nPl in nL: #if each value in netLhs is a reaction and not a particle
            net = net + nL.__str__() + " + "
        net = net[0:-3]
        self.netReaction = net
        
    def __str__(self):
        oput = self.name + "chain: \n"
        oput += self.netReaction
        return oput
    

class UnbalancedCharge(Exception):
    """raised when sum of charges on the left hand side are not equal to the sum of charges on the right hand side
    --diff is the difference between charges--"""
    def __init__(self,diff):
        print("Unbalanced Charge Raised: ", diff)
    

class UnbalancedNumber(Exception):
    """raised when sum of mass numbers on the left hand side are not equal to the sum of mass numbers on the right hand side
    --diff is the difference between mass numbers--"""
    def __init__(self,diff):
        print("Unbalanced Mass Raised: ", diff)


if __name__ == '__main__':
    print("Test1 - Reaction:",Reaction((li6, d), (he4, he4)),"\n")

    try:
        print(Reaction((p,d),(he4,he4)))
    except UnbalancedCharge:
        print("Test2 - Unbalanced Charge Error Caught")
    except UnbalancedNumber:
        print("Test2 - Unbalanced Number Error Caught")
    
    print()    
    print("Test3 - Reaction with +:",Reaction(li6 + d, he4 + he4),"\n")
    he3 = Nucleus ( "He" , 2 , 3)
    chnPP = ChainReaction ( " proton - proton ( branch I ) " )
    for rctn in (Reaction(( p , p ) , (d , ep , nu_e )) ,
		Reaction(( p , p ) , (d , ep , nu_e )),
		Reaction(( d , p ) , ( he3 , gamma )) ,
		Reaction(( d , p ) , ( he3 , gamma )) ,
		Reaction(( he3 , he3 ) , ( he4 , p , p ))):
        chnPP.addReaction(rctn)
    print("Test4 - ChainReaction:\n",chnPP)
    
    
    

    
