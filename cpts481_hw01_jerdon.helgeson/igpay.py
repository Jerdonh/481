#Jerdon Helgeson
#481 HW1
#igpay Module

vowels = ['a','e','i','o','u','A','E','I','O','U']
punctuation = ['.','?',',','!',':',';']

def igpay(inString):
    """Takes a string and returns it's piglatin translation"""
    inString += '\n'
    beginningString = ""
    punct = ''
    #Check if string has punctuation and remove it for piglatin conversion
    inString = inString.strip()
    if(len(inString)>0):
        inString = inString.strip()
        if((inString[-1]) in punctuation):
            punct = inString[-1]
            inString = inString[0:-1:1]
    i = 0
    for letter in inString:
        if(letter in vowels):
            break
        else:
            beginningString += letter
            i = i+1
    endString = inString[i::1]
    if(inString == beginningString):
        pig = inString
    elif(len(beginningString) > 0):
        pig = endString + beginningString + "ay"
    else:
        pig = inString + "way"

    #Gonna handle capitalization just before returning the string
    if(inString.istitle()):
        pig = pig.capitalize()
    if(inString.isupper()):
        pig = pig.upper()
    return pig + punct
    
        


#def main():
#    igpay("testtesttest")

if __name__ == "__main__" :
    t = igpay("test")
    print(t)
    t = igpay("errand")
    print(t)
    t = igpay("why")
    print(t)
    t = igpay("Hello?")
    print(t)
