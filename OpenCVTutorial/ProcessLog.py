from datetime import datetime
from datetime import timedelta
import sys
import os

class WorkTimeSpan:
    timeStart = None
    timeEnd = None

    def __init__(self, ts, te):
        self.timeStart = self.AdjustStartTime(ts)
        self.timeEnd = self.AdjustEndTime(te)

    def AdjustTimeToQuarter(self, dt, offset):
        minutesAdjusted = 15 * round((float(dt.minute + offset) + float(dt.second)/60) / 15)
        addHour = False
        if minutesAdjusted < 0:
            minutesAdjusted = 0
        if minutesAdjusted > 59:
            minutesAdjusted = 0
            addHour = True
        adjustedTime = datetime(dt.year, dt.month, dt.day, dt.hour, minutesAdjusted)
        if addHour:
            adjustedTime += + timedelta(hours=1)
        return adjustedTime

    def AdjustStartTime(self, dt):
        """ Rocky's customized function"""
        return self.AdjustTimeToQuarter(dt, 7.5)

    def AdjustEndTime(self, dt):
        """ Rocky's customized function"""
        return self.AdjustTimeToQuarter(dt, -7.5)

    def AdjustBreakTime(self, workTime):
        """ Rocky's customized function"""
        adjustedWorkTime = workTime
        if adjustedWorkTime > timedelta(hours=3, minutes=30):
            adjustedWorkTime -= timedelta(minutes=30)
        return adjustedWorkTime

    def CalculateWorkTime(self):
        return self.AdjustBreakTime(self.timeEnd - self.timeStart)

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
            self.currEndTime = t
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
    
    def Export(self):
        print(self.workDate)
        totalWorkTime = timedelta()
        for ws in self.workTimeSpanList:
            workTime = ws.CalculateWorkTime()
            totalWorkTime += workTime
            print(str(ws.timeStart) + " - " + str(ws.timeEnd) + " : " + str(workTime))
        print("Total work time in " + str(self.workDate) + " : " + str(totalWorkTime))
  

class EmpWorkRecord:
    
    mDailyRecord = []
    mEmployeeName = "Not set"

    def __init__(self, empName):
        self.mEmployeeName = empName
        self.mDailyRecord = []

    def Export(self):
        print(self.mEmployeeName)
        for dr in self.mDailyRecord:
            dr.Export()

    def CalculateWorkTime(self, timeLogList):    
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
                dayProcessor.AddTime(logTime, action)
            else:
                # same date, add a processor entry
                dayProcessor.AddTime(logTime, action)
        # process data of last date
        dayProcessor.Process()
        self.mDailyRecord.append(dayProcessor)

def ProcessFile(filename):
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
        empRec = EmpWorkRecord(empName)
        empRec.CalculateWorkTime(list(reversed(timeLogList)))
        empRec.Export()

if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv))
    for arg in sys.argv:
        print (str(arg))
    if len(sys.argv) < 2:
        print("Usage: python ProcessLog.py Filename")
        sys.exit()
    
    fn = sys.argv[1]
    if os.path.exists(fn):
        ProcessFile(fn)
