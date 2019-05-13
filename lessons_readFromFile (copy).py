import sys
import re
from copy import deepcopy
from prettytable import PrettyTable



global_days =[ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
global_dayDividedInHours = {
	# "08:00": [],
	"08:30": [],
	"09:00": [],
	"09:30": [],
	"10:00": [],
	"10:30": [],
	"11:00": [],
	"11:30": [],
	"12:00": [],
	"12:30": [],
	"13:00": [],
	"13:30": [],
	"14:00": [],
	"14:30": [],
	"15:00": [],
	"15:30": [],
	"16:00": [],
	"16:30": [],
	"17:00": [],
	"17:30": [],
	"18:00": [],
}

# if 30 minute intervals are used, follow this global hours and 
timeInterval = 30
global_hours = [
	# "08:00", 
	"08:30", "09:00", "09:30", "10:00",
	"10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30",
	"14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00",
	"17:30", 
	# "18:00"
]

# else use this one and comment the above
# timeInterval = 90
# global_hours = [
# 	# "08:00", 
# 	"08:30", "10:00",
# 	"11:00", "12:30", "13:00", 
# 	"14:30", "16:00", 
# 	"16:30", "18:00"
# 	# "18:00"
# ]

class Date:
	day = ""
	hourStart = ""
	hourEnd = ""
	def __init__(self, dayVar, hourStartVar, hourEndVar):
		self.day = dayVar
		self.hourStart = hourStartVar
		self.hourEnd = hourEndVar
	def __str__(self):
		print("[" + day + "]", "> " + hourStart + " - " + hourEnd + " <" )

class Lecture:

	def __init__(self, lineTupleVar):
		self.info = {}
		self.info["courseName"]		 = lineTupleVar[0]
		self.info["shortCourseName"] = lineTupleVar[1]
		self.info["courseCode"]		 = lineTupleVar[2]
		self.info["courseCredit"]		 = lineTupleVar[3]
		self.info["courseStatus"]		 = lineTupleVar[4]
		self.info["courseHours"]		 = lineTupleVar[5]
		self.info["coursePlace"]		 = lineTupleVar[6]
		self.info["notes"]				 = lineTupleVar[7]
		self.info["internalStatus"]		 = ""
		self.info["timeSlots"]			 = {}

		if self.info["courseHours"] == "NIL": #or self.info["courseStatus"] != "1":
			self.info["internalStatus"] = False
		else:
			self.info["internalStatus"] = True
			self.dayParser()

	def dayParser(self):
		lineVar = self.info["courseHours"]
		lineSplitted = re.sub(r"[\n\t\s]*", "", lineVar).split("*")
		for element in lineSplitted:
			elementSplitted 	= element.split(",")
			_day 				= elementSplitted[0]
			startEndSplitted 	= elementSplitted[1].split("-")
			_start 				= startEndSplitted[0]
			_end 				= startEndSplitted[1]
			# print(_day,_start,_end)

			startInMinutes = clockToMinute(_start)
			endInMinutes = clockToMinute(_end)

			# find the start of the lectures,
			# save them in periods (each period 30 minutes)
			i = startInMinutes
			periods = []
			while i < endInMinutes:
				period = minutesToClock(i)
				periods.append(period)
				i += timeInterval
			# print  (periods)

			self.info["timeSlots"][_day] = periods

	def printme(self):
		print(
			self.info["internalStatus"],
			self.info["courseName"],
			self.info["courseCode"],
			self.info["courseCredit"],
			self.info["courseStatus"]
		)
		print(
			self.info["courseHours"],
			self.info["courseImportance"],
			self.info["notes"]
		)
		print(self.info["timeSlots"])

# function for print selection for WeeklyCalendar PrettyTable object row
# printme() function of WeeklyCalendar
def whatWillBePrintedFromList(listVar):
		if listVar == []:
			return ""
		elif len(listVar) == 1:
			return listVar[0]
		else:
			return listVar


class WeeklyCalendar:

	def __init__(self,lectureListVar):
		self.lectureList = lectureListVar
		self.scheduleLectures = {}
		self.schedulePlaces = {}

		# create dictionary of days
		# each day is a list of hours dictionary
		for day in global_days:
			self.scheduleLectures[day] 	= deepcopy(global_dayDividedInHours)
			self.schedulePlaces[day] 	= deepcopy(global_dayDividedInHours)

		# insert the lectures in schedule
		for lec in self.lectureList:
			lectureName = lec.info["shortCourseName"]
			lecturePlace = lec.info["coursePlace"]
			for day in lec.info["timeSlots"]:
				for time in lec.info["timeSlots"][day]:
					self.scheduleLectures[day][time].append(lectureName)
					self.schedulePlaces[day][time].append(lecturePlace)



	def printme(self):
		t = PrettyTable(["Time"] + global_days)
		# t.add_row(['Alice', 24, 1,2,3,4])
		emptyRow = ["-----"] +  ["-----------------------"] * len(global_days)

		hIndex = 0
		for hour in global_hours:

			newRowForHour = [hour]
			for day in global_days:
				lecturesThisTimeThisDay = self.scheduleLectures[day][hour]
				whatToPrint = whatWillBePrintedFromList(lecturesThisTimeThisDay)
				if hIndex in [1,5,8,13,17]:
					newRowForHour.append(whatToPrint)
				else:
					newRowForHour.append('')
				
			nextHour = minutesToClock( (clockToMinute(hour) + timeInterval) )
			newRowForPlace = [nextHour]
			for day in global_days:
				placeThisTimeThisDay = self.schedulePlaces[day][hour]
				whatToPrint = whatWillBePrintedFromList(placeThisTimeThisDay)
				if hIndex in [1,5,8,13,17]:
					newRowForPlace.append(whatToPrint)
				else:
					newRowForPlace.append('')
			
			t.add_row(newRowForHour)
			t.add_row(newRowForPlace)
			if hIndex not in [0,1,4,5,8,9,12,13,16,17,18]:
				t.add_row(emptyRow)
			hIndex += 1
		print(t)




def lineParser(lineVar):
	# Name | Code | Credit | Status | Day1 * Day2 * ... | Importance | Notes
	strippedLine = re.sub(r"[\n\t]*", "", lineVar)
	splittedLine = strippedLine.split("|")
	name 		= splittedLine[0]
	shortName 	= splittedLine[1].strip(" ")
	code 		= splittedLine[2].strip(" ")
	credit 		= splittedLine[3].strip(" ")
	status 		= re.sub(r"[\s]*", "", splittedLine[4])
	days		= splittedLine[5].strip(" ")
	importance 	= splittedLine[6].strip(" ")
	notes 		= splittedLine[7]
	return (name, shortName, code, credit, status, days, importance, notes)

def clockToMinute(lineVar):
	hour, minute = lineVar.split(":")
	hour = int(hour)
	minute = int(minute)
	if minute == 15:
		minute = 30
	totalMinute = hour * 60 + minute
	return totalMinute

def minutesToClock(totalMinutesVar):
	# int conversion in first line is for python3
	# it somehow makes division in float
	hour = int(totalMinutesVar / 60)
	minute = totalMinutesVar % 60
	
	if hour < 10:
		strHour = "0" + str(hour)
	else:
		strHour = str(hour)

	if minute == 0:
		strMinute = "00"
	else:
		strMinute = str(minute)

	strForm = strHour + ":" + strMinute
	return strForm

def parseLinesIntoLectures(fileLinesVar):
	# clear unnecessary lines first
	cleanLines = []
	for line in fileLinesVar:
		if line == "" or len(line.strip()) == 0 or line[0] == '#':
			continue
		else:
			cleanLines.append(line)

	lectureList = []
	# go over the lines, parse them
	for line in cleanLines:
		lineTuple = lineParser(line)
		newLecture = Lecture(lineTuple)
		lectureList.append(newLecture)
	return lectureList





def returnFileHandle(fileName):
	sourceFileHandle = open(fileName, "r")
	return sourceFileHandle

def returnFileLines(fileHandle):
	lines = fileHandle.readlines()
	return lines

def ioHandler(fileName):
	return returnFileLines( returnFileHandle( fileName ) )

def main():
	if len(sys.argv) < 2 :
		print("Not enough arguments, please provide file address")
		exit()

	print("\n\n\n\n\n")
	print("\033[H\033[J")
	
	sourceFileName = sys.argv[1]
	sourceFileLines = ioHandler(sourceFileName)
	lectures = parseLinesIntoLectures(sourceFileLines)
	print("#################### Lecture List ####################")
	totalCreditSum = 0.0
	for lec in lectures:
		lecRegisterStatus = lec.info["courseStatus"]
		if lecRegisterStatus == "1":
			lecRegisterStatus = "OPEN_REG"
		else:
			lecRegisterStatus = "NOT_OPEN"

		lecDateStatus = lec.info["courseHours"]
		if lecDateStatus == "NIL":
			lecDateStatus = "NO___DATE"
		else:
			lecDateStatus = "YES__DATE"

		totalCreditSum += float(lec.info["courseCredit"])
		print(lecRegisterStatus + " ~ " + lecDateStatus + " ~ " + lec.info["courseCredit"] + " ~ " + lec.info["courseName"]   )
	print(" ")
	print("Total Credit: ", totalCreditSum)
	
	print("#################### Schedule ####################")
	cal = WeeklyCalendar(lectures)
	cal.printme()

main()