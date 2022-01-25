from numpy import dtype, genfromtxt
import numpy as np
import pandas as pd
from csv import reader
import re
import os

TESTING = True
FREQ = 5000
VERBOSE = True
HTML_POS = 5
JS_POSITION = 15 # 15 col in data
JS_BODY_WEIRD = JS_POSITION + 3

def hasDoubleWhiteSpace(line):
    return bool(re.search(r"\s\s", line))

def removeWhiteSpace(line):
    return re.sub(' +', ' ', line)

def removeComma(line):
    return re.sub('#','HASH', re.sub(',+', ';', line))

# Assumming the line starts with a number for ID, will work in most cases
def hasCorrectFormatting(line, numCols):
    firstVal = line.split(",")[0].strip()
    firstIsDigit = firstVal.isdigit()
    #consistentCols = len(line.split(",")) == numCols
    return firstIsDigit

def removeHTML_Tags(line):
    patt = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 
    return re.sub(patt, '', line)

def removeWhiteSpaceCSV():
    numCols = 0
    with open("htmlAndWhiteSpaceFix.csv", "w", encoding='utf-8') as outputFile:
        with open("htmlFix.csv", "r", encoding='utf-8') as data :
            counter = 0
            while(True):
                line = data.readline()
                if not line: # check to see if we read each line
                    print("Reached EOF")
                    break
                counter +=1

                if counter ==1: # ignore header
                    numCols = len(line.split(","))
                    outputFile.write(line)
                    continue

                logCount(counter)

                if hasDoubleWhiteSpace(line) and (line):
                    while(True):
                        nextLine = data.readline()
                        if hasDoubleWhiteSpace(nextLine):
                            line = line + nextLine
                        else: 
                            break
                    line = removeWhiteSpace(line)
                outputFile.write(line)
        data.close()
    outputFile.close()



def logCount(counter):
    if VERBOSE:
        if (counter % FREQ == 0):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Read " + str(counter) + " lines")

def fixHTMLformatting(path, output="htmlFix.csv"):
    outputFile = open(output,"w", encoding='utf-8')
    data = open(path,"r", encoding='utf-8')
    counter = 0
    numCols = 0
    isMultiLine = False
    nextLine = ""
    shouldReadNextLine = True

    while(True):
        if shouldReadNextLine:
            line = data.readline()
        else:
            line = nextLine

        if not line:
            print("Reached EOF")
            break

        counter += 1

        if counter == 1:
            numCols = len(line.split(","))
            outputFile.write(line) # write header
            continue # skip processing header
        logCount(counter) # logging lines read

        if hasCorrectFormatting(line,numCols):
            while(True):
                nextLine = data.readline()

                if not nextLine: # checking eof
                    if isMultiLine:
                        outputFile.write(removeHTML_Tags(line)+'\n')
                    else:
                        outputFile.write(removeHTML_Tags(line))
                    shouldReadNextLine = True
                    break

                if hasCorrectFormatting(nextLine,numCols):
                    if isMultiLine:
                        outputFile.write(removeHTML_Tags(line)+'\n')
                    else:
                        outputFile.write(removeHTML_Tags(line))
                    shouldReadNextLine = False
                    break
                else: 
                    isMultiLine = True
                    shouldReadNextLine = True
                    line = line.rstrip() + nextLine.strip()
    outputFile.close()
    data.close()


def expandJS(path, output="expanded.csv"):
    outputFile = open(output,'w', encoding='utf-8')
    dataFile = open(path,'r',encoding='utf-8')
    data = reader(dataFile)
    counter = 0
    for line in data:
        counter +=1
        if counter == 1: #skip header processing
            del line[JS_POSITION]
            for i in range(9):
                line.insert(JS_POSITION+i,"JS_COL_"+str(i))
            outputFile.write(",".join(line)+'\n') # write header
            continue
        logCount(counter)
        js = line[JS_POSITION] 
        del line[JS_POSITION]
        for i, jsItem in enumerate(js.split(' - ')):
            line.insert(JS_POSITION+i,jsItem.strip("{ }"))
        
        outputFile.write(",".join(line)+'\n')

    print("Reached EOF")

def checkUnique(path,output="final.csv"):
    outputFile = open(output,'w', encoding='utf-8')
    dataFile = open(path,'r',encoding='utf-8')
    data = reader(dataFile)
    counter = 0
    for line in data:
        counter+=1
        logCount(counter)
        noCommaHTML = removeComma(line[5])
        del line[5]
        line.insert(5,noCommaHTML)
        noCommaJS = removeComma(line[15])
        del line[15]
        line.insert(15,noCommaJS)
        del line[18]
        noCommaJS_3 = removeComma(noCommaJS.split("-")[3]).strip()
        line.insert(18,noCommaJS_3)
        outputFile.write(",".join(line)+'\n')
    outputFile.close()
    dataFile.close

def checkUnique2(path,output="finalWithJS.csv"):
    outputFile = open(output,'w', encoding='utf-8')
    dataFile = open(path,'r',encoding='utf-8')
    data = reader(dataFile)
    counter = 0
    for line in data:
        counter+=1
        if counter == 1:
            continue
        logCount(counter)
        html = removeComma(line[HTML_POS])
        js = removeComma(line[JS_POSITION])
        jsBody = removeComma(line[JS_BODY_WEIRD])
        del line[HTML_POS]
        line.insert(HTML_POS,html)
        del line[JS_POSITION]
        line.insert(JS_POSITION,js)
        del line[JS_BODY_WEIRD]
        line.insert(JS_BODY_WEIRD,jsBody)
        outputFile.write(",".join(line)+'\n')


    outputFile.close()
    dataFile.close

def checkUnique3(path,output="logCheckUnique3.csv"):
    outputFile = open(output,'w', encoding='utf-8')
    dataFile = open(path,'r',encoding='utf-8')
    counter = 0
    while(True):
        line = dataFile.readline()
        if not line:
            print("Reached EOF")
            break
        counter += 1
        logCount(counter)
        numCols = len(line.split(','))
        if (numCols != 28):
            outputFile.write(line)
    outputFile.close()
    dataFile.close()

def head(file, endIndex = 100):
    inputFile = open(file,'r',encoding='utf-8')
    data = reader(inputFile)
    counter = 0
    for line in data:
        counter += 1
        if counter < endIndex:
            print("".join(line))
        else:
            break

def testLoad(file):
    data =  genfromtxt(file,delimiter=",",encoding='utf-8',dtype=None)
    #data = pd.read_csv(file)
    print(data)

def main():
    #checkUnique("cleaned_MAPLE_IES_study_logs.csv")
    removeWhiteSpaceCSV()

if __name__ == "__main__" and (not TESTING):
    main()

if TESTING:
    #expandJS("test.csv")
    testLoad("finalWithJS.csv")
    #checkUnique3("finalWithJS.csv")
    
    #checkUnique2("htmlAndWhiteSpaceFix.csv")

