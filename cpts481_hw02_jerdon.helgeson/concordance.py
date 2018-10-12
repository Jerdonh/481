#JERDON HELGESON
#481 HW2
#concordance Module

import pprint
pp = pprint.PrettyPrinter(indent = 1, compact = True)
punctuation = ['.','?',',','!',':',';']

def wordStripper(word):
    """Strips words of punctuation"""
    for p in punctuation:
        if(p in word):
            word = word.replace(p,"")
    return word

def concordance(f, unique = True):
    """creates a concordance of words from a txt file f"""
    concord = {}
    lineCounter = 1
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        sline = line.split(" ")
        for word in sline:
            if(word == ""):
                pass #do nothing with nothing
            else:
                word2 = word.lower()
                word2 = wordStripper(word2)
                if(unique == True):
                    if(word2 in concord):
                        if(lineCounter in concord[word2]):
                            pass
                        else:
                            concord[word2].append(lineCounter)
                    else:
                        concord[word2] = [lineCounter]
                else:
                    if word2 in concord:
                        concord[word2].append(lineCounter)
                    else:
                        concord[word2] = [lineCounter]
        lineCounter += 1
    return concord
    
if __name__ == "__main__" :
    f = open("test",'r')
    concord = concordance(f)
    print("Concordance of test.txt with Unique = True")
    pp.pprint(concord)
    f.close()
    f = open("test","r")
    concord = concordance(f,False)
    print("Concordance of test.txt with Unique = False")
    pp.pprint(concord)
    f.close()
