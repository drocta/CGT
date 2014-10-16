def tokenizeSingleToken(inStringList,token,ignore=""):
    outStringList=[]
    for part in inStringList:
        if(part==ignore):
            outStringList.append(part)
        else:
            partParts=part.partition(token)
            if(partParts[0]!=""):outStringList.append(partParts[0])
            if(partParts[1]!=""):
                outStringList.append(partParts[1])
            if(partParts[2]!=""):
                outStringList.extend(tokenizeSingleToken([partParts[2]],token))
    return outStringList
def tokenizeMultiToken(inStringList,tokenList):
    outStringList=inStringList
    for token in tokenList:
        outStringList=tokenizeSingleToken(outStringList,token)
    return outStringList

                
