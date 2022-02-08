import pandas as pd
import numpy as np

def loadColumnList(file):
    with open(file,'r') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            lines[i] = line.strip('\n')
    f.close()
    return lines



def makeString(dataTuple):
    tempList = []
    for item in dataTuple:
        tempList.append(str(item))
    return ",".join(tempList)

def meanListDescriptive(col,df):
    series = df[col].describe()
    return (df[col].notnull().sum(),str(series.get("mean")),str(series.get("std")),str(series.get("50%")),str(series.get("25%")),str(series.get("75%")),str(series.get("max")),str(series.get("min")),"","")

def checkUniqueDescriptive(col,df):
    return (df[col].notnull().sum(),"","","","","","","",df[col].nunique(),"")

def filter(valueCount):
    if valueCount is None:
        return ""
    else:
        return valueCount

def binaryListDescriptive(col,df):
    valueCounts = df[col].value_counts()
    print(valueCounts.keys())
    return (df[col].notnull().sum(),"","","","","","","","",valueCounts.get(float(1.0)))

def generalDescriptive(col,df):
    return (df[col].notnull().sum(),"","","","","","","","","")

#dataTuple is (count,mean,sd,meadian,25%,75%,max,min,numberOfUniqueValues,numberOfTrue)
def writeLineData(colName,dataTuple,outputFile):
    outputFile.write(colName+','+ makeString(dataTuple)+'\n')

def runDescriptives(inputFile,outputFile):
    checkUnique = loadColumnList("uniqueCheck.txt")
    meanList = loadColumnList("meanList.txt")
    binaryList= loadColumnList("binaryList.txt")
    headerCol = "_,count,mean,std,meadian,25%,75%,max,min,numberOfUniqueValues,numberOfTrue"
    df = pd.read_csv(inputFile)
    output = open(outputFile,'w',encoding='utf-8')
    output.write(headerCol+'\n')
    for column in df.columns:
        dataTuple = ()
        if column in checkUnique:
            dataTuple = checkUniqueDescriptive(column,df)
        elif column in meanList:
            dataTuple = meanListDescriptive(column,df)
        elif column in binaryList:
            dataTuple = binaryListDescriptive(column,df)
        else:
            dataTuple = generalDescriptive(column,df)
        writeLineData(column,dataTuple,output)
    output.close()
    print("Done")

 





if __name__ == "__main__":
    runDescriptives("cleanedLOG_MERGED.csv","descriptives.csv")