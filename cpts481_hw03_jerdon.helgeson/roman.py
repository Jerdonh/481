#JERDON HELGESON
#11376111
#481 hw3
#Roman Module


numerals = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000,"N":0}
extNumerals = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'),
               (90, 'XC'),(50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'),
               (4, 'IV'), (1, 'I')]
invNumerals = {"IV":4,"IX":9,"XL":40,"XC":90,"CD":400,"CM":900}
nOrder = ["M","D","C","L","X","V","I","N"]


class Roman:
    #numerals = {"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}
    num = None
    value = None
    
    def __init__(self, nm):
        if(isinstance(nm,str)):
            self.num = nm
        elif(isinstance(nm,int)):
            self.setNum(nm)
        self.setValue(nm)

    

    """
    ~~~~~~~~~~~~~~~~~~~~~~~Roman Operator Overloads~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    

    def __add__(self,other):
        if(isinstance(other, Roman)):
            return Roman(self.value + other.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return Roman(self.value + other)

    def __radd__(self,other):
        if(isinstance(other, Roman)):
            return Roman(self.value + other.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return Roman(self.value + other)

    def __sub__(self,other):
        if(isinstance(other, Roman)):
            return Roman(self.value - other.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return Roman(self.value - other)
    """
    def __rsub__(self,other):
        if(isinstance(other, roman)):
            return roman(other.value - self.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return roman(other - self.value)
    """
    def __mul__(self,other):
        if(isinstance(other, Roman)):
            return Roman(self.value * other.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return Roman(self.value * other)

    def __rmul__(self,other):
        if(isinstance(other, Roman)):
            return Roman(self.value * other.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return Roman(self.value * other)
    
    def __truediv__(self,other):
        if(isinstance(other, Roman)):
            return (Roman(self.value // other.value), Roman(self.value % other.value))
        elif(isinstance(other, int) or isinstance(other,float)):
            return (Roman(self.value // other), Roman(self.value % other))

    def __floordiv__(self,other):
        if(isinstance(other, Roman)):
            return Roman(self.value // other.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return Roman(self.value // other)

    def __pow__(self,other):
        if(isinstance(other, Roman)):
            return Roman(self.value ** other.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return Roman(self.value ** other)

    def __rpow__(self,other):
        if(isinstance(other, Roman)):
            return Roman(other.value ** self.value)
        elif(isinstance(other, int) or isinstance(other,float)):
            return Roman(other ** self.value)

    def __eq__(self, other):
        if(isinstance(other, Roman)):
            return other.value == self.value
        elif(isinstance(other, int) or isinstance(other,float)):
            return other == self.value

    def __ne__(self, other):
        if(isinstance(other, Roman)):
            return other.value != self.value
        elif(isinstance(other, int) or isinstance(other,float)):
            return other != self.value

    def __lt__(self, other):
        if(isinstance(other, Roman)):
            return self.value < other.value
        elif(isinstance(other, int) or isinstance(other,float)):
            return self.value < other

    def __le__(self, other):
        if(isinstance(other, Roman)):
            return self.value <= other.value
        elif(isinstance(other, int) or isinstance(other,float)):
            return self.value <= other

    def __gt__(self, other):
        if(isinstance(other, Roman)):
            return self.value > other.value
        elif(isinstance(other, int) or isinstance(other,float)):
            return self.value > other

    def __ge__(self, other):
        if(isinstance(other, Roman)):
            return self.value >= other.value
        elif(isinstance(other, int) or isinstance(other,float)):
            return self.value >= other

    def __neg__(self):
        return Roman(-self.value)
        
    


    """
    ~~~~~~~~~~~~~~~~~~~~~~~Roman Attribute Setters~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    

    def setNum(self, val):
        """ convert int val to the corrosponding Numeral """
        num = ''
        if(val < 0):
            num = "-"
            val = -val
        elif(val == 0):
            self.num = "N"
            return
        val2 = val
        while val2 > 0:
            for i, r in extNumerals:
                while val2 >= i:
                    num += r
                    val2 -= i
        self.num = num    

    def setValue(self, nm):
        """convert the given numeral or given input to value"""
        if(isinstance(nm,int)):
            if(nm >= 2000000):
                raise ValueError("ValueError: Roman Numeral Exceeds 2000000")
            self.value = nm
        elif(isinstance(nm,str)):
            if(len(nm) < 1):
                print("nm value doesn't exist")
            elif(len(nm) == 1 and nm in numerals):
                self.value = numerals[nm]    
            else:
                nmL = self.listafyNums(nm)
                #print(nmL)
                if(nmL == False):
                    print("Invalid Numeral Syntax")
                elif(self.numsInOrder(nmL)):
                    #if the numerals are in order
                    temp = self.setValHelper(nmL, True)
                    if(temp >= 2000000):
                        print("TESTTESTTESTTEST")
                        raise ValueError("ValueError: Roman Numeral Exceeds 2000000")
                    else:
                        self.value = temp
                else:
                    #if the numerals are not in order
                    #print("\n\n \t NUMERALS NOT IN ORDER \n \n")
                    temp = self.setValHelper(nmL, False)
                    if(temp >= 2000000):
                        print("TESTTESTTESTTEST")
                        raise ValueError("ValueError: Roman Numeral Exceeds 2000000")    
                    else:
                        self.value = temp
        

    """
    ~~~~~~~~~~~~~~~~~~~~~~~Roman Numeral as input Methods~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

    def setValHelper(self, nm, order):
        if(order):
            #base case is a single numeral
            if(len(nm) == 1 and len(nm[0]) == 1):
                return numerals[nm[0]]
            #secondary case is a single numeral with parenthesis
            elif(len(nm) == 1 and len(nm[0]) >= 3):
                nm[0] = nm[0].strip("(")
                nm[0] = nm[0].strip(")")
                return 1000 * self.setValHelper(nm[0], True)
            else:
                return numerals[nm[0]] + self.setValHelper(nm[1:], True)
        else:
            if(len(nm) > 1):
                if((nm[0] + nm[1]) in invNumerals):
                    if(len(nm) > 2):
                        order = self.numsInOrder(nm[2:])
                        return invNumerals[(nm[0]+nm[1])] + self.setValHelper(nm[2:], order)
                    else:
                        return invNumerals[(nm[0]+nm[1])]

    

    def listafyNums(self, nm):
        nmL = []
        i = 0
        
        while(i < len(nm)):
            if(nm[i] == '('):
                tempStr = ""
                closed = False
                while(i < len(nm)):
                    tempStr += nm[i]
                    if(nm[i] == ")"):
                        closed = True
                        break
                    i+=1
                if(closed == True):
                    nmL.append(tempStr)
                else:
                    print("invalid Roman Numeral input")
                    return False
            else:
                nmL.append(nm[i])
            i+=1
        return nmL
                    
    def numsInOrder(self, nmL):
        i = 0
        N = nmL[i]
        for n in nOrder:
            #print("O = ", n, "  N = ", N)
            if(i >= len(nmL)):
                pass
            elif(n in nmL and nmL[i] != n):
                return False
            else:
                while(i < len(nmL) and nmL[i] == n):
                    i +=1
                    if(i >= len(nmL)):
                        break
                    N = nmL[i]
                    #print("         N = ", N)

        return True

        
        
        
    """
    ~~~~~~~~~~~~~~~~~~~~~~~Roman Output Methods~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    
    def __str__(self):
        return str(self.num)# + " = " + str(self.value)
        """if(isinstance(self.num,str)):
            return str(self.num) + " = " + str(self.value)
        elif(isinstance(self.num,int)):
            return str(self.num) + " = " + str(self.value)"""
        
    def __repr__(self):
        return "Roman(" + str(self.num) + " = " + str(self.value) + ")"        
        
        


for i in range(1001):
    globals()[(Roman(i)).num] = Roman(i)


