from datetime import datetime

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
        print(line)
        print(logId, empName, logTime, action, actionType)
        print(empWorkTime[empName])
        input("Press Enter to continue...")

if __name__ == '__main__':
     Process('Export_20180218_221120.csv')
