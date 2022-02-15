from os import system, name
from numpy import dtype, genfromtxt
import numpy as np
import pandas as pd


TESTING = True
PROBLEM_ID_POS = 3
USER_ID_POS = 10


def checkUnique(file,outputPath): #uses numpy
    data =  genfromtxt(file,delimiter=',',encoding='utf-8',dtype=None,names=True)
    print(data.shape)
    problemID_Col = data[0:, PROBLEM_ID_POS]
    userID_Col = data[0:, USER_ID_POS]
    print(problemID_Col)
    print(userID_Col)
    uniqueProblemID, uniqueProblemID_Counts = np.unique(problemID_Col,return_counts=True)
    uniqueUserID, uniqueUserID_Counts = np.unique(userID_Col,return_counts=True)
    print(uniqueProblemID)
    print(uniqueUserID)
    with open(outputPath,'w',encoding='utf-8') as output:
        output.write("Unique Problems IDs" + '\n')
        output.write(np.array2string(problemID_Col) + '\n')
        output.write("Unique Problems ID Counts" + '\n')
        output.write(np.array2string(uniqueProblemID_Counts) + '\n')
        output.write("Unique User IDs" + '\n')
        output.write(np.array2string(userID_Col) + '\n')
        output.write("Unique User IDs Counts" + '\n')
        output.write(np.array2string(uniqueUserID_Counts) + '\n')

def checkUnique2(file,outputPath): #uses panda
    data =  pd.read_csv(file,sep=',')
    problemID_Col = data.problem_id
    userID_Col = data.user_id
    #print(df['B'].value_counts())
    uniqueProblemID_Counts = problemID_Col.value_counts()
    uniqueUserID_Counts = userID_Col.value_counts()
    with open(outputPath,'w',encoding='utf-8') as output:
        output.write("Unique Problems ID Counts"+ '\n')
        output.write(uniqueProblemID_Counts.to_string(header=True)+ '\n')
        output.write("Unique User IDs Counts" + '\n')
        output.write(uniqueUserID_Counts.to_string(header=True)+ '\n')

def getCount(file,colName):
    data =  pd.read_csv(file,sep=',',dtype=None)
    col = data[colName]
    print(col.value_counts())

def head(file):
    data =  pd.read_csv(file,sep=',',dtype=None)
    print(data.head())

def describe(file):
    data =  pd.read_csv(file,sep=',',dtype=None)
    stat = data.describe(include='all')
    print(stat)

def clear():
  
    # for windows
    if name == 'nt':
        system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        system('clear')

def checkMissingData():
    bridgeSetUserID = set()
    bridgeSetStudentID = set()
    logSet = set()
    studySet = set()
    bridge = open("OldData/bridge.csv",'r', encoding='utf-8')
    bridge.readline()
    while (True):
        line = bridge.readline()
        if not line: # check to see if we read each line
            break
        bridgeSetUserID.add(line.split(',')[1])
        bridgeSetStudentID.add(line.split(',')[0])

    logs = open("OldData/cleaned_MAPLE_IES_study_logs.csv",'r', encoding='utf-8')
    logs.readline()
    while (True):
        line = logs.readline()
        if not line: # check to see if we read each line
            break
        logSet.add(line.split(',')[10])

    study = open("OldData/Copy of Assessment_merged_2021_07_16_state_assessment_N=4321 - Sheet1.csv",'r', encoding='utf-8')
    study.readline()
    count = 1
    while (True):
        line = study.readline()
        count += 1
        if not line: # check to see if we read each line
            break
        if line.split(',')[1] == "": print("EMPTY IN  " , count)
        studySet.add(line.split(',')[1])


    print("Missing User IDs: " + str(logSet.difference(bridgeSetUserID).union(bridgeSetUserID.difference(logSet))))
    print("Missing Student IDs: " + str(studySet.difference(bridgeSetStudentID).union(bridgeSetStudentID.difference(studySet))))
    
def info(path):
    data =  pd.read_csv(path,sep=',',dtype=None)
    while(True):
        usrInput = input("Column name, or q to quit > ")
        if usrInput.lower() == "q":
            print("Quitting")
            break
        else:
            try:
                col = data[usrInput]
                colList = col.tolist()
                colList = [str(i) for i in colList]
                usrInput2 = input("Action to perform ( 1 = maxMin, 2 = isBinary, 3 = isContinious, 4 = maxMinList, 5 = hasNullValues, 6 = checkUnique, 7 = valueCount) > ")
                if usrInput2.lower() == "2":
                    print(isBinary(colList))
                elif usrInput2.lower() == "3":
                    print(isContinuous(colList))
                elif usrInput2.lower() == "4":
                    print(maxMinVal(colList))
                elif usrInput2.lower() == "1":
                    maxMinLength(colList)
                elif usrInput2.lower() == "5":
                    print(hasNullValues(col))
                elif usrInput2.lower() == "6":
                    print(checkUnique(col))
                elif usrInput2.lower() == "7":
                    print(valueCount(colList))
                else:
                    print("Enter valid action")
            except (KeyError):
                print("Column does not exist")
            
def maxMinLength(colList):
    colList.sort(key= lambda x : len(x),reverse=True)
    print(f'Max Length: {len(colList[0])}')
    print(f'Min Length: {len(colList[-1])}')

def hasNullValues(col):
    return col.isnull().values.any()

def isBinary(list):
    for i in list:
        if not (i == "1" or i == "0"):
            print(f"Example {i}")
            return False
    return True

def isContinuous(list):
    for i in list:
        if float(i) - int(i) != 0:
            return True
    return False

def maxMinVal(list):
    list2 = []
    for i in list:
        if not i == "nan":
            list2.append(i)
    list = [float(i) for i in list2]
    list = list.sort()
    return (f"Max: {list2[-1]}, Min: {list2[0]}")

def checkUnique(list):
    return (len(set(list)) == len(list))

def valueCount(list):
    userInput = input("Enter value to count > ")
    userInput = userInput.strip()
    count = 0
    for i in list:
        if i == userInput:
            count += 1
    return f'Count for {userInput}: {count}'

def main():
    print("Nothing to do")

if __name__ == "__main__" and not TESTING:
    main()


if TESTING:
    path = "cleanedLOG_MERGED.csv"
    info(path)


