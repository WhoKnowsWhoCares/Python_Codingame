import sys
import math
import random
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

width, height, my_id = [int(i) for i in input().split()]
myCoord = [-1, -1]
lastCoord = [-1, -1]
priorityField = [[0]*width for i in range(height)]
myBombs = 0
myBombRange = 3
flagToRecalculatePriority = True
# tillMyBomb = 0
# enemyCoord = []
allBombs = []
allBoxes = []
allWalls = []
# dangerFlag = False
# deadlockFlag = False

fence = 'X'
emptyBox = '0'
rangeBox = '1'
bombBox = '2'

#find all coordinates of the bombs in string
def parceMap(priorityField, string, row):
    global allBoxes, allWalls
    boxes = []
    if string.find(emptyBox) != -1:
        boxes += [[x, row, 0] for x in range(len(string)) if string[x] == emptyBox]
    if string.find(rangeBox) != -1:
        boxes += [[x, row, 1] for x in range(len(string)) if string[x] == rangeBox]
    if string.find(bombBox) != -1:
        boxes += [[x, row, 2] for x in range(len(string)) if string[x] == bombBox]
    walls = []
    if string.find(fence) != -1:
        walls += [[x, row, 0] for x in range(len(string)) if string[x] == fence]

    for box in boxes:
        priorityField[row][box[0]] = -100
    for wall in walls:
        priorityField[row][wall[0]] = -100
    allBoxes += boxes
    allWalls += walls
    # print("cordinates: "+str(bombs), file=sys.stderr)
    # print("cordinates: "+str(walls), file=sys.stderr)
    return priorityField

#find an enemy
def statistics(entity_type, owner, x, y, param_1, param_2):
    global myCoord, allBombs, myBombs, myBombRange, lastCoord
    if entity_type == 0:
        if owner == my_id:
            if lastCoord != myCoord: lastCoord = myCoord
            myCoord = [x, y]
            myBombs = param_1
            myBombRange = param_2
            print("you are in: %d,%d and you have %d bombs with range %d" % (x, y, param_1, param_2), file=sys.stderr)
        else:
            print("Danger! Your enemy is on: %d,%d with %d bombs and %d bomb range" % (x, y, param_1, param_2), file=sys.stderr)
    if entity_type == 1:
        if owner == my_id:
            print("your bomb planted: %d,%d till explosion: %d, range: %d" % (x, y, param_1, param_2), file=sys.stderr)
        else:
            print("Danger! Your enemy's bomb is on: %d,%d till explosion: %d, range: %d" % (x, y, param_1, param_2), file=sys.stderr)
        allBombs.append([x, y, param_1, param_2])
    else:
        print("Wow here is a present! %d, %d" % (x, y), file=sys.stderr)

#place bomb in string, while you start from x, y
def plantBomb(bombs, x, y):
    if bombs[y] is None:
        print("Can't plant in this row, no bombs...", file=sys.stderr)
        return plantBomb(bombs, x, (y+1) % 11)
    print("start planting...", file=sys.stderr)
    flag = 23
    x = int(x)
    placeToGo = [0, y]
    distanceBomb = flag
    for i in bombs[y]:
        if abs(x - i) < distanceBomb:
            distanceBomb = abs(x - i)
            placeToGo[0] = i
    if distanceBomb != flag:
        if placeToGo[0] < x:
            placeToGo[0] += min(myBombRange-1, distanceBomb)
        else:
            placeToGo[0] -= min(myBombRange-1, distanceBomb)
    print("plan to place: "+str(placeToGo), file=sys.stderr)
    if myBombs > 0 and myCoord == placeToGo:
        print("BOMB "+str(placeToGo[0])+" "+str(placeToGo[1]))
    elif myBombs == 0:
        run()
    else:
        print("MOVE "+str(placeToGo[0])+" "+str(placeToGo[1]))
    return placeToGo

#get some bonuses in a free time
def getBonuses():
    return

#can i get here and where?
def available(points, start, bombs, deep):
    if deep <= 0: return points
    nearest = []
    field = list(points)
    if not int(start[1]-1) < 0:
        newPoint = (priorityField[start[2]][start[1]-1], start[1]-1, start[2])
        nearest.append(newPoint)
    if not int(start[1]+1) > height:
        newPoint = (priorityField[start[2]][start[1]+1], start[1]+1, start[2])
        nearest.append(newPoint)
    if not int(start[2]-1) < 0:
        newPoint = (priorityField[start[2]-1][start[1]], start[1], start[2]-1)
        nearest.append(newPoint)
    if not int(start[2]+1) > width:
        newPoint = (priorityField[start[2]+1][start[1]], start[1], start[2]+1)
        nearest.append(newPoint)
    print("nearest: "+str(nearest), file=sys.stderr)
    # print("points: "+str(priorityField), file=sys.stderr)
    for check in nearest:
        if check[0] >= 0 and (field is None or check not in field):
            # field.append(check)
            print("one more checked: "+str(check), file=sys.stderr)
            if bombs[check[2]][check[1]] == 0:
                field.append(check)
            field = available(field, check, bombs, deep - 1)
    return field

#escape from fire
def saveYourSoul():
    bombs = sorted(allBombs, key=lambda x: x[2])
    myPoint = (priorityField[myCoord[1]][myCoord[0]], myCoord[0], myCoord[1])
    availablePoints = [myPoint]
    bombField = [[0]*width for i in range(height)]
    for bomb in bombs:
        bombField[bomb[1]][bomb[0]] = 1
    # ignore all walls and boxes
    bombField = setPriority(bombField, bombs)
    # print("Bombs range: "+str(bombField), file=sys.stderr)
    availablePoints = available(availablePoints, myPoint, bombField, 5)
    return availablePoints

#create stack places for bombs
def choosePlaceForBomb():
    availablePoints = saveYourSoul()
    availablePoints = sorted(availablePoints, key=lambda x: x[0], reverse=True)
    print(availablePoints, file=sys.stderr)
    return availablePoints[0]

#set priority on the field
def setPriority(priorityField, boxes):
    if boxes is None: return
    for box in boxes:
        for i in range(1, myBombRange):
            if box[0]-i >= 0:
                if priorityField[box[1]][box[0]-i] >= 0: priorityField[box[1]][box[0]-i] += 1
                else: break
        for i in range(1, myBombRange):
            if box[0]+i < width:
                if priorityField[box[1]][box[0]+i] >= 0: priorityField[box[1]][box[0]+i] += 1
                else: break
        for i in range(1, myBombRange):
            if box[1]-i >= 0:
                if priorityField[box[1]-i][box[0]] >= 0: priorityField[box[1]-i][box[0]] += 1
                else: break
        for i in range(1, myBombRange):
            if box[1]+i < height:
                if priorityField[box[1]+i][box[0]] >= 0: priorityField[box[1]+i][box[0]] += 1
                else: break
    return priorityField

#chnge priority for the future explosion
def changePriority(x, y, recurs):
    priorityField[y][x] = 0
    for i in range(1, myBombRange):
        if x-i >= 0:
            if [x-i, y] in allBoxes and recurs:
                changePriority(x-i, y, False)
                break
            if recurs: priorityField[y][x-i] = 0
            else: priorityField[y][x-i] = max(0, priorityField[y][x-i] - 1)
    for i in range(1, myBombRange):
        if x+i < width:
            if [x+i, y] in allBoxes and recurs:
                changePriority(x+i, y, False)
                break
            if recurs: priorityField[y][x+i] = 0
            else: priorityField[y][x+i] = max(0, priorityField[y][x+i] - 1)
    for i in range(1, myBombRange):
        if y-i >= 0:
            if [x, y-i] in allBoxes and recurs:
                changePriority(x, y-i, False)
                break
            if recurs: priorityField[y-i][x] = 0
            else: priorityField[y-i][x] = max(0, priorityField[y-i][x] - 1)
    for i in range(1, myBombRange):
        if y+i < height:
            if [x, y+i] in allBoxes and recurs:
                changePriority(x, y+i, False)
                break
            if recurs: priorityField[y+i][x] = 0
            else: priorityField[y+i][x] = max(0, priorityField[y+1][x] - 1)

# game loop
while True:
    allBoxes = []
    priorityField = [[0]*width for i in range(height)]
    for i in range(height):
        row = input()
        priorityField = parceMap(priorityField, row, i)
    entities = int(input())
    allBombs.clear()

    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        statistics(entity_type, owner, x, y, param_1, param_2)

    priorityField = setPriority(priorityField, allBoxes)

    if flagToRecalculatePriority:
        place = choosePlaceForBomb()
        print("Best place to plant: "+str(place), file=sys.stderr)
        flagToRecalculatePriority = False

    if myBombs > 0 and myCoord[0] == place[1] and myCoord[1] == place[2]:
        print("BOMB "+str(myCoord[0])+" "+str(myCoord[1]))
        allBombs.append([myCoord[0], myCoord[1], 8, myBombRange])
        changePriority(myCoord[0], myCoord[1], False)
        place = choosePlaceForBomb()
        print("New place to go: "+str(place), file=sys.stderr)
    else:
        print("MOVE "+str(place[1])+" "+str(place[2]))


