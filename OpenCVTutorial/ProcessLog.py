from datetime import datetime

def CalculateWorkTime(timeLogList):
    currDate = timeLogList[0][1].date()
    print(currDate)
    timeStart = None
    timeEnd = None
    for timeLog in timeLogList:
        print(timeLog)

def Process(filename):
    empWorkTime = {}
    for line in open(filename):
        logId, empName, logTime, action, actionType = line.rstrip().split(',')
        # 20180217 02:47:06
        logTime = datetime.strptime(logTime, '%Y%m%d %H:%M:%S')
        if empName in empWorkTime:
            empWorkTime[empName].append((logId, logTime, action, actionType))
        else:            
            empWorkTime[empName] = [(logId, logTime, action, actionType)]

    for empName, timeLogList in empWorkTime.items():
        print(empName)
        CalculateWorkTime(list(reversed(timeLogList)))

if __name__ == '__main__':
     Process('Export_20180218_221120.csv')
