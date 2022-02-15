import pandas as pd

# df.info()

logData = pd.read_csv("log.csv",encoding='utf-8',dtype=None)
actionData = pd.read_csv("actionLevel.csv",encoding='utf-8',dtype=None)
bridge = pd.read_csv("bridge.csv",encoding='utf-8',dtype=None)
temp = pd.merge(logData, bridge, on=["user_id"])
result = pd.merge(temp, actionData, on=["student_id"])
result.to_csv("cleanedLOG_MERGED.csv",sep=',',index=False)
