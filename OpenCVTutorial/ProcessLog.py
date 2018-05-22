from datetime import datetime

class WorkTimeSpan:
    timeStart = None
    timeEnd = None

    def __init__(self, ts, te):
        self.timeStart = ts
        self.timeEnd = te

    def CalculateWorkTime(self):
        return self.timeEnd - self.timeStart

class DayProcessor:
    """ process work time of an employee in one day """
    workDate = None
    workTimeSpanList = []   # list of all time spans in this day
    
    currStartTime = None
    currEndTime = None

    def __init__(self, currDate):
        self.workDate = currDate
        self.workTimeSpanList = []
        self.currStartTime = None
        self.currEndTime = None
        self.dayMinTime = datetime.combine(self.workDate, datetime.min.time())
        self.dayMaxTime = datetime.combine(self.workDate, datetime.max.time())

    def AddTime(self, t, action):
        if action == "Punch In":
            self.currStartTime = t
        elif action == "Punch Out":
            self.currEndTimeTime = t
            # initialize as if work start from midnight
            workTimeSpan = WorkTimeSpan(self.dayMinTime, self.currEndTime)
            if self.currStartTime:
                # a valid time span is added
                workTimeSpan = WorkTimeSpan(self.currStartTime, self.currEndTime)
            self.workTimeSpanList.append(workTimeSpan)
            self.currStartTime = None   # reset
            self.currEndTime = None
            
    def AddTimeSpan(self, ts, te):
        timeSpan = WorkTimeSpan(ts, te)
        self.workTimeSpanList.append(timeSpan)

    def Process(self):
        # if there's punch in without punch out, assume it end at the end of day
        if self.currStartTime:
            # a valid time span is added
            workTimeSpan = WorkTimeSpan(self.currStartTime, self.dayMaxTime)
            self.workTimeSpanList.append(workTimeSpan)
                
        print(self.workDate)
        for ws in self.workTimeSpanList:
            print(str(ws.timeStart) + " - " + str(ws.timeEnd) + " : " + str(ws.CalculateWorkTime()))

def CalculateWorkTime(timeLogList):
    currDate = timeLogList[0][1].date()
    dayProcessor = DayProcessor(currDate)
    
    for timeLog in timeLogList:
        # print(timeLog)
        logTime = timeLog[1]
        logDate = logTime.date()
        action = timeLog[2]
        if logDate != currDate:
            # date changed, calculate total time of this day            
            dayProcessor.Process()
            # reset day processor
            currDate = logDate
            dayProcessor = DayProcessor(currDate)
        else:
            # same date, add a processor entry
            dayProcessor.AddTime(logTime, action)

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
     Process('input.csv')
