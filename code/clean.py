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


def testLoad(file):
    data =  genfromtxt(file,delimiter=",",encoding='utf-8',dtype=None,names=True)
    #data = pd.read_csv(file)
    print(data)

def sortCSV(path,colName):
    df = pd.read_csv(path,sep=',',dtype=None)
    df.sort_values(by=[colName])
    df.to_csv(path)

def main():
    #checkUnique("cleaned_MAPLE_IES_study_logs.csv")
    removeWhiteSpaceCSV()

if __name__ == "__main__" and (not TESTING):
    main()

if TESTING:
    #expandJS("test.csv")
    sortCSV("cleanedLOG_MERGED.csv","num")
    #checkUnique3("finalWithJS.csv")
    
    #checkUnique2("htmlAndWhiteSpaceFix.csv")

