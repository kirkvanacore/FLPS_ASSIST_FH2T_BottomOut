from csv import reader
from numpy import genfromtxt
import numpy as np
import pandas as pd
TESTING = False
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


def main():
    checkUnique2("finalWithJS.csv","unique2.txt")

if __name__ == "__main__" and not TESTING:
    main()


