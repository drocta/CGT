"""
CGT
This file for things for combinatorial game theory, and the class of Games.

In this file, a Game is represented as a 2-tuple of lists of games.
For example, the 0 game would be represented as ([],[])
and the game star would be represented as ([([],[])],[([],[])])
.

TODO:
add a function for cleaning up a game to remove redundancy.
    Maybe make it find the form with the earliest birthday?
add the function that adds the option to skip one's turn.DONE
add a function for binary fractions
maybe add a class that can be used in place of a game in order to handle certain operations faster
(for simple things anyway)
maybe handle future TODOs with github issue tracker?
"""

import tokenizing

class ga():
    """
    This is a first attempt at making a class for games to make certain operations faster
    """
    def __init__(self,n=0,gtype='int',left=None,right=None,denompower=1):
        self.n=n
        self.left=left
        self.right=right
        self.gtype=gtype
        self.denomPower=denompower
        if(self.gtype=='binfrac'):
            if(self.denomPower==0 or self.n==0):
                self.gtype='int'
            elif(self.n%2==0):
                while(self.n%2==0 and self.denomPower>0):
                    self.denomPower-=1
                    self.n=self.n/2
                    
    def __getitem__(self,index):
        if(self.gtype=='int'):
            if(index==0):
                if(self.left is None):
                    if(self.n>0):
                        self.left=[ga(self.n -1)]
                    else:
                        self.left=[]
                return self.left
            elif(index==1):
                if(self.right is None):
                    if(self.n<0):
                        self.right=[ga(self.n + 1)]
                    else:
                        self.right=[]
                return self.right
            return "err"
        elif(self.gtype=='binfrac'):
            if(index==0):
                return [ga(n=(self.n-1)/2,gtype='binfrac',denompower=self.denomPower-1)]
            if(index==1):
                return [ga(n=(self.n+1)/2,gtype='binfrac',denompower=self.denomPower-1)]
    def __str__(self):
        return str(self.n)
    def __int__(self):
        if(self.gtype=='int'):
            return self.n
        else:
            assert False
        


def is_int(maybeint):
    try:
        int(maybeint)
        return True
    except:
        return False

def dedup(options):
    newOptions=[]
    for option in options:
        if option not in newOptions:
            newOptions.append(option)

    return newOptions

def dedup2(options):
    newOptions=[]
    for option in options:
        for option2 in newOptions:
            if(eq(option,option2)):
                break
        else:
            newOptions.append(option)
    return newOptions

def simplifyOptions(options):
    newOptions=[]
    for option in options:
        if(isinstance(option,ga)):
            newOptions.append(option)
        elif(eq(option,g0)):
            newOptions.append(g0)
        else:
            newOptions.append(option)
    return dedup2(newOptions)

def simplifyGame1(game):
    if(isinstance(game,ga)):
        return game
    return simplifyOptions(game[0]),simplifyOptions(game[1])

def simpGame2(game):
    if(isinstance(game,ga)):
        return game
    left=game[0]
    right=game[1]
    left=map(simpGame2,left)
    right=map(simpGame2,right)
    left=simplifyOptions(left)
    right=simplifyOptions(right)
    return (left,right)

def simp3(game):
    if(isinstance(game,ga)):
        return game
    if(eq(ceil(game),game)):
        return ga(n=ceil2(game),gtype='int')
    left,right=game
    newLeft,newRight=game
    for leftOption in left:
        newLeft=[simp3(newLeftOption) for newLeftOption in newLeft if not less(newLeftOption,leftOption)]
    for rightOption in right:
        newRight=[simp3(newRightOption) for newRightOption in newRight if not less(rightOption,newRightOption)]
    return simpGame2((newLeft,newRight))

def gameUnion(gameA,gameB):
    leftA,rightA=gameA
    leftB,rightB=gameB
    return leftA+leftB,rightA+rightB

def gameSum(gameA,gameB):
    if(eq(gameA,g0)):
        return gameB
    if(eq(gameB,g0)):
        return gameA
    if(isinstance(gameA,ga) and isinstance(gameB,ga)):
        if(gameA.gtype=='int' and gameB.gtype=='int'):
            return ga(gameA.n+gameB.n)#improve this.
        if(gameA.gtype=='binfrac' and gameB.gtype=='binfrac'):
            pass#this should probably be done with methods instead?
    left=[gameSum(L_A,gameB) for L_A in gameA[0]]+\
          [gameSum(L_B,gameA) for L_B in gameB[0]]
    left=dedup(left)
    right=[gameSum(R_A,gameB) for R_A in gameA[1]]+\
          [gameSum(R_B,gameA) for R_B in gameB[1]]
    right=dedup(right)
    return (left,right)

def gameMul(gameA,gameB):
    left=[]
    left+=[reduce(gameSum,[gameMul(AL,gameB),gameMul(gameA,BL),gameNeg(gameMul(AL,BL))]) for AL in gameA[0] for BL in gameB[0]]
    left+=[reduce(gameSum,[gameMul(AR,gameB),gameMul(gameA,BR),gameNeg(gameMul(AR,BR))]) for AR in gameA[1] for BR in gameB[1]]
    right=[]
    right+=[reduce(gameSum,[gameMul(AL,gameB),gameMul(gameA,BR),gameNeg(gameMul(AL,BR))]) for AL in gameA[0] for BR in gameB[1]]
    right+=[reduce(gameSum,[gameMul(gameA,BL),gameMul(AR,gameB),gameNeg(gameMul(AR,BL))]) for AR in gameA[1] for BL in gameB[0]]
    #right not yet implemented. for positive integers it should be blank though?
    return (left,right)

def gameNeg(game):
    left=map(gameNeg,game[1])
    right=map(gameNeg,game[0])
    return (left,right)

def pp(game):
    """
    Pretty Prints a game.
    TODO:
        representation of binary fractions
        representation of nimbers :check! (mostly)
    """
    if(game==None):
        return ''
    if(isinstance(game,ga)):
        return str(game)
    if(game==g0):
        return '0'
    if(len(game[0])==0 and len(game[1])==0):
        return '0'
    if(game==([g0],[g0])):
        return '*'
    if(len(game[0])==1 and game[1]==[] and\
           is_int(pp(game[0][0])) and\
           int(pp(game[0][0]))>=0):
        return str(int(pp(game[0][0]))+1)
    if(len(game[1])==1 and game[0]==[] and\
           is_int(pp(game[1][0])) and\
           int(pp(game[1][0]))<=0):
        return str(int(pp(game[1][0]))-1)
    if(len(game[0])==len(game[1])):
        halfLen=len(game[0])
        if(numbersAreEqual(game,nim(halfLen))):
           return '*'+str(halfLen)
    return '{'+\
           ','.join(map(pp,game[0]))+\
           '|'+\
           ','.join(map(pp,game[1]))+\
           '}'

def intToGame(n):
    assert(n==int(n))
    if(n==0):
        return g0
    if(n>0):
        return ([intToGame(n-1)],[])
    if(n<0):
        return ([],[intToGame(n+1)])
ig=intToGame

def d(int1,int2):
    return ([ig(int1)],[ig(int2)])

def intToNimber(n):
    assert(n==int(n))
    assert(n>=0)
    if(n==0):
        return g0
    prevNimber=intToNimber(n-1)
    nimberHalf=[prevNimber]+prevNimber[0]
    return (nimberHalf,nimberHalf)
nim=intToNimber

def binFrac(power,numerator=1):
    if(numerator==0):
        return g0
    if(power==0):
        return intToGame(numerator)
    assert(power>=0)
    if(numerator%2==0):
        return binFrac(power-1,numerator/2)
    return ([binFrac(power-1,(numerator-1)/2)],[binFrac(power-1,(numerator+1)/2)])


#------------------------------------
g0=([],[])
g1=([g0],[])
star=([g0],[g0])
up=([g0],[star])
down=([star],[g0])
#------------------------------------

def leftFirstWin(game):
    if(game[0]==[]):
        return False
    for subgame in game[0]:
        if(not leftFirstWin(gameNeg(subgame))):
            return True
    return False

rightFirstWin=lambda game:leftFirstWin(gameNeg(game))
lfs=leftFirstWin
rfs=rightFirstWin


def lessOrEqual(gameX,gameY):
    for xL in gameX[0]:
        if(lessOrEqual(gameY,xL)):
            return False
    for yR in gameY[1]:
        if(lessOrEqual(yR,gameX)):
            return False
    return True

def less(gameX,gameY):
    return lessOrEqual(gameX,gameY) and not lessOrEqual(gameY,gameX)

greaterOrEqual = lambda gameX,gameY:lessOrEqual(gameY,gameX)

#----------------------------------

def birthday(game):
    return max(map(birthday,game[0]+game[1])+[-1])+1
b=birthday

def isSymmetric(game):
    game=simp3(game)
    left,right=game
    for leftOption in left:
        if not isNimber(leftOption):
            return False
        for rightOption in right:
            if(eq(leftOption,rightOption)):
                break
        else:
            return False#left option does not occur in right
    raise("ok idk what to do with this. ???")

#ok whatever doing this the easy and slow way
def isNimber(game):
    """Stupid and naive method to check if a game is a nimber, and determine which one it is if so"""
    if(sign(game)!='*'):
        return False,0
    gameDay=birthday(game)
    for i in range(gameDay+1):
        if(eq(game,nim(i))):
            return True,i
    return False,0

def gameIsZero(game):
    if(leftFirstWin(game) or rightFirstWin(game)):
        return False
    else:
        return True

def gamesAreEqual(gameA,gameB):
    if(gameIsZero(gameSum(gameA,gameNeg(gameB)))):
        return True
    else:
        return False

def numbersAreEqual(numberA,numberB):
    return lessOrEqual(numberA,numberB) and lessOrEqual(numberB,numberA)
eq=numbersAreEqual

def sign(game):
    p0=lessOrEqual(g0,game)
    n0=lessOrEqual(game,g0)
    if(p0):
        if(n0):
            return '0'
        return '1'
    if(n0):
        return '-1'
    return '*'

##def ceil(game):
##    i=g0
##    while(less(i,game)):
##        i=([i],[])
##    return int(pp(i))

def ceil(game):
    i=g0
    gameSign=sign(game)
    if(gameSign != '-1'):
        while(not lessOrEqual(game,i)):
            i=([i],[])
    else:
        while(lessOrEqual(game,i)):
            i=([],[i])
        i=i[1][0]
    return i
    
def ceil2(game):
    i=g0
    gameSign=sign(game)
    if(gameSign != '-1'):
        while(not lessOrEqual(game,i)):
            i=([i],[])
    else:
        while(lessOrEqual(game,i)):
            i=([],[i])
        i=i[1][0]
    return int(pp(i))

#-------------------------------------------

def f(game):
    f_map_left=map(f,game[0])
    f_map_right=map(f,game[1])
    newLeft=f_map_left+[(f_map_left,f_map_right)]
    newRight=f_map_right+[(f_map_left,f_map_right)]
    return (newLeft,newRight)


#--------------------------------------------

def parseExp(expr):
    expr=expr.lstrip()
    if(expr==""):
        return None
    if(expr[0]=='{'):
        pass#not yet implemented
    elif(expr=='*'):
        return star
    elif(expr[0]=='*' and is_int(expr[1:])):
        return nim(int(expr[1:]))
    elif(expr=="up"):
        return up
    elif(expr=="down"):
        return down
    elif(is_int(expr)):
        return ig(int(expr))
    else:
        print "not yet implemented"
        return None

svars={'a':g0,'b':g1,'c':ig(5)}
functionLookup={'ceil':lambda game:ig(ceil2(game)),'f':f,'sign':lambda game:parseExp(sign(game))}
def parseInp(inp):
    tokens=tokenizing.tokenizeMultiToken([inp],['{',',','|','}','+','-',' ','X','eq']+\
                                         [functionName for functionName in functionLookup])
    tokens=[token for token in tokens if token!=',' and token!=' ']
    return tokens

def read_from_tokens(tokens,prev=None):
    if(len(tokens)==0):
        return None
    if(tokens[0]=='{'):
        left,right=([],[])
        tokens.pop(0)
        while(len(tokens)!=0 and tokens[0]!='|'):
            left.append(read_from_tokens(tokens,prev))
        if(len(tokens)==0):
            return left,right
        tokens.pop(0)
        while(len(tokens)!=0 and tokens[0]!='}'):
            right.append(read_from_tokens(tokens,prev))
        if(len(tokens)==0):
            return left,right
        tokens.pop(0)
        return left,right
    elif(tokens[0]=='-'):
        tokens.pop(0)
        return gameNeg(read_from_tokens(tokens,prev))
    elif(tokens[0]=='+'):
        tokens.pop(0)
        return gameSum(read_from_tokens(tokens,prev),read_from_tokens(tokens,prev))
    elif(tokens[0]=='X'):
        tokens.pop(0)
        return gameMul(read_from_tokens(tokens,prev),read_from_tokens(tokens,prev))
    elif(tokens[0]=='eq'):
        tokens.pop(0)
        if(eq(read_from_tokens(tokens,prev),read_from_tokens(tokens,prev))):
            return g1
        else:
            return g0
    elif(tokens[0] in functionLookup):
        functionToUse=functionLookup[tokens[0]]
        tokens.pop(0)
        return simp3(functionToUse(read_from_tokens(tokens,prev)))
    elif(tokens[0]=='_'):
        tokens.pop(0)
        if(prev!=None):
            return prev
        else:
            return g0
    elif(tokens[0] =="set"):
        tokens.pop(0)
        varToUse=tokens.pop(0)
        valueToUse=read_from_tokens(tokens,prev)
        svars[varToUse]=valueToUse
        return valueToUse
    elif(tokens[0] in svars):
        varToUse=tokens.pop(0)
        return svars[varToUse]
    else:
        out=parseExp(tokens[0])
        tokens.pop(0)
        return out
    
            

def cgtshell():
    inp=""
    thingy=g0
    print """
Welcome to cgtshell.
Enter an expression to evaluate it. enter quit to quit"""
    while(inp!="quit"):
        thingy=read_from_tokens(parseInp(inp),prev=thingy)
        if(thingy!=None):
            thingy=simp3(thingy)
            print pp(thingy)
        inp=raw_input("==>:")
    print "Goodbye."
    return

