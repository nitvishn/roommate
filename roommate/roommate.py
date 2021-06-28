# -*- coding: utf-8 -*-
"""
Created on Fri May  5 10:04:01 2017

@author: nvishnu
"""


def getData(fileName):
    file = open(fileName, 'r')

    def splitData(string):
        subject = ""
        for char in string:
            if((char == ':')):
                break
            subject += char
        string = string[len(subject) + 1:]
        string = string.split(',')
        actualData = []
        for name in string:
            name = name.replace(',', '')
            name = name.replace('\n', '')
            name = name.replace(' ', '')
            actualData.append(name)

        subject = subject.replace(',', '')
        subject = subject.replace('\n', '')
        subject = subject.replace(' ', '')
        return (subject, actualData)
    personData = {}
    for line in file:
        data = splitData(line)
        personData[data[0]] = data[1]
    return personData


def getPoints(room, prefs):
    points = 0
    for person in room:
        for other_person in room:
            if(person == other_person):
                continue
            if(other_person in prefs[person]):
                points += 1
    return points


def get_best_rooms(perms, prefs):
    best_rooms = perms.pop()
    best_score = getPoints(best_rooms, prefs)
    for rooms in perms:
        points = getPoints(rooms, prefs)
        if(points > best_score):
            best_score = points
            best_rooms = rooms
    return best_rooms


def roomCombination(people):
    possible_rooms = set()
    for person in people:
        for mate1 in people:
            for mate2 in people:
                if(frozenset([person, mate1, mate2]) in possible_rooms):
                    continue
                possible_rooms.add(frozenset([person, mate1, mate2]))
    return possible_rooms


def printRooms(rooms):
    roomno = 1
    for room in rooms:
        print("Room #" + str(roomno))
        for person in room:
            print(person)
        print()
        roomno += 1


def getRoomsWithoutPeople(people, rooms):
    newRooms = set()
    for room in rooms:
        success = True
        for person in people:
            if(person in room):
                success = False
        if(success):
            newRooms.add(room)
    return newRooms


def getRoomPoints(rooms, data):
    roomPoints = {}
    for room in rooms:
        roomPoints[room] = getPoints(room, data)
    return roomPoints


data = getData('roomData.txt')
people = list(data.keys())
chosen = []
rooms = roomCombination(people)
roomPoints = getRoomPoints(rooms, data)
while(rooms != set()):
    roomPoints = getRoomPoints(rooms, data)
    chosen.append(list(max(roomPoints, key=roomPoints.get)))
    rooms = getRoomsWithoutPeople(chosen[-1], rooms)

loners = []
for room in chosen:
    if(len(room) == 1):
        loners.append(room[0])
        chosen.remove(room)
chosen.append(loners)
printRooms(chosen)
