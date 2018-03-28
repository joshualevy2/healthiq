
import csv
import sys

# TODO erase first line of data
# Assumption one 24 hour period of simulation

foodDataFile = "Food.tsv"
exerciseDataFile = "Exercise.tsv"

activityData = {}
foodData = {}
exerciseData = {}

def loadActivityData(activityDataFileName):
    with open(activityDataFileName) as activityTsv:
       activityFile = csv.reader(activityTsv, dialect="excel-tab")
       for activityItem in activityFile:
       	   # If there is already an item, add tuple to the list, if not create list w/1 tuple
           try:
       	   	   activityList = activityData[str(activityItem[1])]
       	   	   activityList.append((activityItem[0],activityItem[2]))
       	   except KeyError:
               activityData[str(activityItem[1])] = [(activityItem[0],activityItem[2])]

def loadExerciseData():
    with open(exerciseDataFile) as exerciseTsv:
       exerciseFile = csv.reader(exerciseTsv, dialect="excel-tab")
       for exerciseItem in exerciseFile:
            exerciseData[exerciseItem[1]] = exerciseItem[2]	


def loadFoodData():
    with open(foodDataFile) as foodTsv:
       foodFile = csv.reader(foodTsv, dialect="excel-tab")
       for foodItem in foodFile:
            foodData[foodItem[1]] = foodItem[2]	

loadExerciseData()
loadFoodData()

#print(sys.argv[1])
loadActivityData(sys.argv[1])

#print(activityData)
#print(foodData)
#print(exerciseData)

bg = 80.0
glycation = 0.0
activeFoodList = []
activeExerciseList = []


# TODO more than 2 hour impact

for currentMinute in range(0, ((24*60)-1)):
    if bg > 150:
        glycation = glycation+1
    try:
	    activityList = activityData[str(currentMinute)]
    except KeyError:
        activityList = None

    print("At %s bg is %f and glycation is %f    " % (currentMinute, bg, glycation), end="") 
    # TODO 2 hour  

    if activityList != None:
        for activity in activityList:
          print(activity)
          if activity[0] == "Exercise":
            print("At %s did %s" % (currentMinute,activity[1]))
            exercise = exerciseData[activity[1]]
            activeExerciseList.append((currentMinute, exercise))
    		#print(exercise            bg = bg - int(exercise)
          elif activity[0] == "Eat":
            print("At %s ate %s" % (currentMinute,activity[1]))
            food = foodData[activity[1]]
            activeFoodList.append((currentMinute, food))

    else:
        print("")

    normalize = True
    # Apply active food
    # TODO remove old records
    for activeFood in activeFoodList:
    	if currentMinute < activeFood[0]+120:
    		bg = bg + float(activeFood[1])/120.0
    		normalize = False
    
    # Apply active exercise    
    for activeExercise in activeExerciseList:
    	if currentMinute < activeExercise[0]+60:
    		bg = bg - float(activeExercise[1])/60.0
    		normalize = False
 
    if normalize:
        if bg != 80:
            if bg > 80:
                bg = bg-1
            if bg < 80:
                bg = bg+1
    	






