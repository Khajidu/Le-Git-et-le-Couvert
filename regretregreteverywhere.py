#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, sys, random, copy, numpy, pygame
from pygame.locals import *

#regret contiendra pénalités pour qui a gagné, le classement et les notes des candidats

npartis = 10
powerdistance = 1.5
veaututile = 0.3
width = 8

xcandidats=[143, 5, 124, 25, 160, 111, 168, 159, 165, 115]
ycandidats=[167, 175, 150, 178, 101, 83, 112, 170, 127, 194]
candidats = [(3 * xcandidats[i],3 * ycandidats[i]) for i in range(npartis)]#[(int(200 * random.random()) + 200 * int(3 * random.random()), int(200 * random.random()) + 200 * int(3 * random.random())) for i in range(npartis)]

pygame.init()
fenetre = pygame.display.set_mode((600,600), RESIZABLE)
continuer = 1
color=["White","Red","Blue","Green","Magenta","Cyan","Yellow","Gray","Brown","Orange"]

def finddistance(point1, point2, powerdistance):
    x1, y1 = float(point1[0]), float(point1[1])
    x2, y2 = float(point2[0]), float(point2[1])
    if powerdistance == 1:
        return abs(x2 - x1) + abs(y2 - y1)
    elif powerdistance == 2:
        return math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
    elif powerdistance == numpy.inf:
        return max(abs(x2 - x1), abs(y2 - y1))
    elif powerdistance == 0:
        return min(abs(x2 - x1), abs(y2 - y1))
    else:
        return math.pow(math.pow(abs(x2 - x1), powerdistance) + math.pow(abs(y2 - y1), powerdistance), 1.0/powerdistance)

def irv(x0, y0):
    candidates = copy.deepcopy(candidats)
    distances = []
    notes = []
    classements = []
    regretclassement = 0
    regretnotes = 0
    regretelu = 0
    regretelucarre = 0
    regreteluabsolu = 0
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances.append([finddistance ((x, y), candidat, powerdistance) for candidat in candidats])
            notes.append([int(max(0, 6 - distance / (1500* random.random()))) for distance in distances[-1]])
            sorteddistances = sorted(distances[-1])
            classements.append([sorteddistances.index(distance) + 1 for distance in distances[-1]])
            classement = copy.deepcopy(classements[-1])
            if random.random() <= veaututile:
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    classement[0] = 1
                    classement[1] = npartis
                    for i in range(2, npartis):
                        classement[i] = classement[i] + 1 if classement[i] < classements[-1][0] else classement[i]
                        classement[i] = classement[i] - 1 if classement[i] > classements[-1][1] else classement[i]
                else:
                    classement[1] = 1
                    classement[0] = npartis
                    for i in range(2, npartis):
                        classement[i] = classement[i] + 1 if classement[i] < classements[-1][1] else classement[i]
                        classement[i] = classement[i] - 1 if classement[i] > classements[-1][0] else classement[i]
    scores = [0 for candidat in candidats]
    for p in range(len(candidats)):
        scores[p] = len([index for index in range(len(classements)) if classements[index][p] == 1])
    votes = [0 for candidat in candidats]
    classementfinal = [0 for candidat in candidates]
    note = len(candidats)
    eliminate = []
    while len(candidates) > 2:
        s = min([scores[p] for p in range(len(candidats)) if p not in eliminate])
        eliminated = scores.index(s)
        votes[eliminated] = s
        eliminate.append(eliminated)
        classementfinal[eliminated] = note
        note -= 1
        candidate = [p for p in range(len(candidates)) if scores[p] == s][0]
        candidates = [candidat for candidat in candidates if candidat != candidates[candidate]]
        for p in range(len(candidats)):
            scores[p] = len([index for index in range(len(classements)) if classements[index][p] == min([classements[index][i] for i in range(len(candidats)) if i not in eliminate])])
    candidate = [p for p in range(len(candidates)) if scores[p] >= scores[1 - p]][0]
    finalist = [p for p in range(len(candidates)) if candidates[p] != candidats[candidate]][0]
    first = candidats.index(candidates[candidate])
    votes[first] = scores[first]
    classementfinal[first] = 1
    second = candidats.index(candidates[finalist])
    votes[second] = scores[second]
    classementfinal[second] = 2
    elu = first
    fenetre.set_at((x0, y0), pygame.Color(color[elu]))
    if (x0, y0) in candidats:
        fenetre.set_at((x0, y0), pygame.Color("Black"))
    regretclassement += max([1.0 * sum([abs(classementfinal[i] - classements[y1 + x1 * width][i]) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretnotes += max([1.0 * sum([abs(notes[y1 + x1 * width][i] - int(6.0 * votes[i] / width ** 2)) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretelu += max([1.0 * sum([(distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regretelucarre += max([sum([(1.0 * (distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20) ** 2 / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regreteluabsolu +=  1.0 * sum([distances[y1 + x1 * width][elu] / 20 / width ** 2 for x1 in range(width) for y1 in range(width)])
    return float(regretclassement), float(regretnotes), float(regretelu), float(regretelucarre), float(regreteluabsolu)

def votedevaleur(x0, y0):
    votes = [0 for candidat in candidats]
    distances = []
    notes = []
    classements = []
    regretclassement = 0
    regretnotes = 0
    regretelu = 0
    regretelucarre = 0
    regreteluabsolu = 0
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances.append([finddistance ((x, y), candidat, powerdistance) for candidat in candidats])
            notes.append([int(max(0, 6 - distance / (1500* random.random()))) for distance in distances[-1]])
            sorteddistances = sorted(distances[-1])
            classements.append([sorteddistances.index(distance) + 1 for distance in distances[-1]])
            distance0 = numpy.random.normal(100, 30, 1)[0]
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 6
                else:
                    votes[1] += 6
            for p in range(p0, len(candidats)):
                votes[p] += notes[-1][p]
    sortedvotes = sorted(votes, reverse=True)
    classementfinal = [sortedvotes.index(vote) + 1 for vote in votes]
    elu = classementfinal.index(1)
    fenetre.set_at((x0, y0), pygame.Color(color[elu]))
    if (x0, y0) in candidats:
        fenetre.set_at((x0, y0), pygame.Color("Black"))
    regretclassement += max([1.0 * sum([abs(classementfinal[i] - classements[y1 + x1 * width][i]) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretnotes += max([1.0 * sum([abs(notes[y1 + x1 * width][i] - int(1.0 * votes[i] / width ** 2)) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretelu += max([1.0 * sum([(distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regretelucarre += max([sum([(1.0 * (distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20) ** 2 / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regreteluabsolu +=  1.0 * sum([distances[y1 + x1 * width][elu] / 20 / width ** 2 for x1 in range(width) for y1 in range(width)])
    return float(regretclassement), float(regretnotes), float(regretelu), float(regretelucarre), float(regreteluabsolu)

def chiasma(x0, y0):
    jugements = [[] for candidat in candidats]
    distances = []
    notes = []
    classements = []
    regretclassement = 0
    regretnotes = 0
    regretelu = 0
    regretelucarre = 0
    regreteluabsolu = 0
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances.append([finddistance ((x, y), candidat, powerdistance) for candidat in candidats])
            notes.append([max(0, 6 - distance / (1500* random.random())) for distance in distances[-1]])
            sorteddistances = sorted(distances[-1])
            classements.append([sorteddistances.index(distance) + 1 for distance in distances[-1]])
            distance0 = numpy.random.normal(100, 30, 1)[0]
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    jugements[1].append(0)
                    jugements[0].append(6)
                else:
                    jugements[0].append(0)
                    jugements[1].append(6)
            for p in range(p0, len(candidats)):
                jugements[p].append(notes[-1][p])
    jugement = []
    for p in range(len(candidats)):
        grades = sorted(jugements[p], reverse=True)
        cumulative = [1.0 * grade * width ** 2 / 6 for grade in grades]
        diff = [abs(cumulative[i] - i) for i in range(width ** 2)]
        jugement.append(((width ** 2 - list(reversed(diff)).index(min(diff))) * 6.0 / width ** 2, grades[len(grades) / 2], sum(grades)))
    sortedvotes = sorted(jugement, key = lambda l: (-l[0], -l[1], -l[2]))
    classementfinal = [sortedvotes.index(j) + 1 for j in jugement]
    elu = classementfinal.index(1)
    fenetre.set_at((x0, y0), pygame.Color(color[elu]))
    if (x0, y0) in candidats:
        fenetre.set_at((x0, y0), pygame.Color("Black"))
    regretclassement += max([1.0 * sum([abs(classementfinal[i] - classements[y1 + x1 * width][i]) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretnotes += max([1.0 * sum([abs(notes[y1 + x1 * width][i] - int(1.0 * jugement[i][0] / width ** 2)) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretelu += max([1.0 * sum([(distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regretelucarre += max([sum([(1.0 * (distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20) ** 2 / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regreteluabsolu +=  1.0 * sum([distances[y1 + x1 * width][elu] / 20 / width ** 2 for x1 in range(width) for y1 in range(width)])
    return float(regretclassement), float(regretnotes), float(regretelu), float(regretelucarre), float(regreteluabsolu)

def jugementmajoritaire(x0, y0):
    jugements = [[] for candidat in candidats]
    distances = []
    notes = []
    classements = []
    regretclassement = 0
    regretnotes = 0
    regretelu = 0
    regretelucarre = 0
    regreteluabsolu = 0
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances.append([finddistance ((x, y), candidat, powerdistance) for candidat in candidats])
            notes.append([int(max(0, 6 - distance / (1500* random.random()))) for distance in distances[-1]])
            sorteddistances = sorted(distances[-1])
            classements.append([sorteddistances.index(distance) + 1 for distance in distances[-1]])
            distance0 = numpy.random.normal(100, 30, 1)[0]
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    jugements[1].append(0)
                    jugements[0].append(6)
                else:
                    jugements[0].append(0)
                    jugements[1].append(6)
            for p in range(p0, len(candidats)):
                jugements[p].append(notes[-1][p])
    jugement = []
    for p in range(len(candidats)):
        grades = sorted(jugements[p], reverse=True)
        reversedgrades = sorted(jugements[p])
        if len(grades) != 0:
            note = grades[len(grades)/2]
            jugement.append((note, grades.index(note), reversedgrades.index(note)))
        else:
            jugement.append(0, grades.index(0), reversedgrades.index(0))
    sortedvotes = sorted(jugement, key = lambda l: (-l[0], l[1] < l[2], -l[1] if l[1] >= l[2] else l[2]))
    classementfinal = [sortedvotes.index(j) + 1 for j in jugement]
    elu = classementfinal.index(1)
    fenetre.set_at((x0, y0), pygame.Color(color[elu]))
    if (x0, y0) in candidats:
        fenetre.set_at((x0, y0), pygame.Color("Black"))
    regretclassement += max([1.0 * sum([abs(classementfinal[i] - classements[y1 + x1 * width][i]) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretnotes += max([1.0 * sum([abs(notes[y1 + x1 * width][i] - int(1.0 * jugement[i][0] / width ** 2)) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretelu += max([1.0 * sum([(distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regretelucarre += max([sum([(1.0 * (distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20) ** 2 / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regreteluabsolu +=  1.0 * sum([distances[y1 + x1 * width][elu] / 20 / width ** 2 for x1 in range(width) for y1 in range(width)])
    return float(regretclassement), float(regretnotes), float(regretelu), float(regretelucarre), float(regreteluabsolu)

def jugementmajoritaireaffine(x0, y0):
    jugements = [[] for candidat in candidats]
    distances = []
    notes = []
    classements = []
    regretclassement = 0
    regretnotes = 0
    regretelu = 0
    regretelucarre = 0
    regreteluabsolu = 0
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances.append([finddistance ((x, y), candidat, powerdistance) for candidat in candidats])
            notes.append([int(max(0, 6 - distance / (1500* random.random()))) for distance in distances[-1]])
            sorteddistances = sorted(distances[-1])
            classements.append([sorteddistances.index(distance) + 1 for distance in distances[-1]])
            distance0 = numpy.random.normal(100, 30, 1)[0]
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    jugements[1].append(0)
                    jugements[0].append(6)
                else:
                    jugements[0].append(0)
                    jugements[1].append(6)
            for p in range(p0, len(candidats)):
                jugements[p].append(notes[-1][p])
    jugement = []
    for p in range(len(candidats)):
        grades = sorted(jugements[p], reverse=True)
        reversedgrades = sorted(jugements[p])
        if len(grades) != 0:
            note = grades[len(grades)/2]
            jugement.append((note, grades.index(note), reversedgrades.index(note)))
        else:
            jugement.append(0, grades.index(0), reversedgrades.index(0))
    nvotes = width ** 2
    sortedvotes = sorted(jugement, key = lambda l: (-l[0], -(nvotes / 2 - l[2]) / (nvotes - l[1] - l[2])))
    classementfinal = [sortedvotes.index(j) + 1 for j in jugement]
    elu = classementfinal.index(1)
    fenetre.set_at((x0, y0), pygame.Color(color[elu]))
    if (x0, y0) in candidats:
        fenetre.set_at((x0, y0), pygame.Color("Black"))
    regretclassement += max([1.0 * sum([abs(classementfinal[i] - classements[y1 + x1 * width][i]) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretnotes += max([1.0 * sum([abs(notes[y1 + x1 * width][i] - int(1.0 * jugement[i][0] / width ** 2)) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretelu += max([1.0 * sum([(distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regretelucarre += max([sum([(1.0 * (distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20) ** 2 / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regreteluabsolu +=  1.0 * sum([distances[y1 + x1 * width][elu] / 20 / width ** 2 for x1 in range(width) for y1 in range(width)])
    return float(regretclassement), float(regretnotes), float(regretelu), float(regretelucarre), float(regreteluabsolu)

def approbation(x0, y0):
    votes = [0 for candidat in candidats]
    distances = []
    notes = []
    classements = []
    regretclassement = 0
    regretnotes = 0
    regretelu = 0
    regretelucarre = 0
    regreteluabsolu = 0
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances.append([finddistance ((x, y), candidat, powerdistance) for candidat in candidats])
            notes.append([int(max(0, 6 - distance / (1500* random.random()))) for distance in distances[-1]])
            sorteddistances = sorted(distances[-1])
            classements.append([sorteddistances.index(distance) + 1 for distance in distances[-1]])
            distance0 = numpy.random.normal(200, 50, 1)[0]
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                else:
                    votes[1] += 1
            for p in range(p0, len(candidats)):
                if distances[-1][p] < distance0:
                    votes[p] += 1
    sortedvotes = sorted(votes, reverse=True)
    classementfinal = [sortedvotes.index(vote) + 1 for vote in votes]
    elu = classementfinal.index(1)
    fenetre.set_at((x0, y0), pygame.Color(color[elu]))
    if (x0, y0) in candidats:
        fenetre.set_at((x0, y0), pygame.Color("Black"))
    regretclassement += max([1.0 * sum([abs(classementfinal[i] - classements[y1 + x1 * width][i]) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretnotes += max([1.0 * sum([abs(notes[y1 + x1 * width][i] - int(6.0 * votes[i] / width ** 2)) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretelu += max([1.0 * sum([(distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regretelucarre += max([sum([(1.0 * (distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20) ** 2 / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regreteluabsolu +=  1.0 * sum([distances[y1 + x1 * width][elu] / 20 / width ** 2 for x1 in range(width) for y1 in range(width)])
    return float(regretclassement), float(regretnotes), float(regretelu), float(regretelucarre), float(regreteluabsolu)

def untour(x0, y0):
    votes = [0 for candidat in candidats]
    distances = []
    notes = []
    classements = []
    regretclassement = 0
    regretnotes = 0
    regretelu = 0
    regretelucarre = 0
    regreteluabsolu = 0
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances.append([finddistance ((x, y), candidat, powerdistance) for candidat in candidats])
            notes.append([int(max(0, 6 - distance / (1500* random.random()))) for distance in distances[-1]])
            sorteddistances = sorted(distances[-1])
            classements.append([sorteddistances.index(distance) + 1 for distance in distances[-1]])
            if random.random() <= veaututile:
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                else:
                    votes[1] += 1
            else:
                p = distances[-1].index(min(distances[-1]))
                votes[p] += 1
    sortedvotes = sorted(votes, reverse=True)
    classementfinal = [sortedvotes.index(vote) + 1 for vote in votes]
    elu = classementfinal.index(1)
    fenetre.set_at((x0, y0), pygame.Color(color[elu]))
    if (x0, y0) in candidats:
        fenetre.set_at((x0, y0), pygame.Color("Black"))
    regretclassement += max([1.0 * sum([abs(classementfinal[i] - classements[y1 + x1 * width][i]) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretnotes += max([1.0 * sum([abs(notes[y1 + x1 * width][i] - int(6.0 * votes[i] / width ** 2)) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretelu += max([1.0 * sum([(distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regretelucarre += max([sum([(1.0 * (distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20) ** 2 / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regreteluabsolu +=  1.0 * sum([distances[y1 + x1 * width][elu] / 20 / width ** 2 for x1 in range(width) for y1 in range(width)])
    return float(regretclassement), float(regretnotes), float(regretelu), float(regretelucarre), float(regreteluabsolu)

def deuxtours(x0, y0, candidats, veaututile):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
            if random.random() <= veaututile:
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                else:
                    votes[1] += 1
            else:
                for candidat in candidats:
                    distance = finddistance((x, y), candidat, powerdistance)
                    distances.append(distance)
                p = distances.index(min(distances))
                votes[p] += 1
    p1 = votes.index(max(votes))
    votes[p1] = 0
    p2 = votes.index(max(votes))
    deuxiemetour = [candidats[p1], candidats[p2]]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            for candidat in deuxiemetour:
                distance = finddistance((x, y), candidat, powerdistance)
                distances.append(distance)
    if distances[0] < distances[1]:
        p = p1
    else:
        p = p2
    return p

def bordouille(x0, y0):
    votes = [0 for candidat in candidats]
    distances = []
    notes = []
    classements = []
    regretclassement = 0
    regretnotes = 0
    regretelu = 0
    regretelucarre = 0
    regreteluabsolu = 0
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances.append([finddistance ((x, y), candidat, powerdistance) for candidat in candidats])
            notes.append([int(max(0, 6 - distance / (1500* random.random()))) for distance in distances[-1]])
            sorteddistances = sorted(distances[-1])
            classements.append([sorteddistances.index(distance) + 1 for distance in distances[-1]])
            classement = copy.deepcopy(classements[-1])
            if random.random() <= veaututile:
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    classement[0] = 1
                    classement[1] = npartis
                    for i in range(2, npartis):
                        classement[i] = classement[i] + 1 if classement[i] < classements[-1][0] else classement[i]
                        classement[i] = classement[i] - 1 if classement[i] < classements[-1][1] else classement[i]
                else:
                    classement[1] = 1
                    classement[0] = npartis
                    for i in range(2, npartis):
                        classement[i] = classement[i] + 1 if classement[i] < classements[-1][1] else classement[i]
                        classement[i] = classement[i] - 1 if classement[i] < classements[-1][0] else classement[i]
            for i in range(npartis):
                votes[i] += npartis - classement[i]
    sortedvotes = sorted(votes, reverse=True)
    classementfinal = [sortedvotes.index(vote) + 1 for vote in votes]
    elu = classementfinal.index(1)
    fenetre.set_at((x0, y0), pygame.Color(color[elu]))
    if (x0, y0) in candidats:
        fenetre.set_at((x0, y0), pygame.Color("Black"))
    regretclassement += max([1.0 * sum([abs(classementfinal[i] - classements[y1 + x1 * width][i]) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretnotes += max([1.0 * sum([abs(notes[y1 + x1 * width][i] - int(6.0 / (npartis - 1) * votes[i] / width ** 2)) for x1 in range(width) for y1 in range(width)]) / width ** 2 for i in range(npartis)])
    regretelu += max([1.0 * sum([(distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regretelucarre += max([sum([(1.0 * (distances[y1 + x1 * width][i] - distances[y1 + x1 * width][elu]) / 20) ** 2 / 20 / width ** 2 for x1 in range(width) for y1 in range(width)]) for i in range(npartis)])
    regreteluabsolu +=  1.0 * sum([distances[y1 + x1 * width][elu] / 20 / width ** 2 for x1 in range(width) for y1 in range(width)])
    return float(regretclassement), float(regretnotes), float(regretelu), float(regretelucarre), float(regreteluabsolu)

regrets = [0 for i in range(5)]
for x in range(0, 600, 3):
    for y in range(0, 600, 3):
        regret = chiasma(x, y)
        regrets = [regrets[i] + regret[i] for i in range(len(regrets))]
print [regrets[i] / 200 ** 2 if i != 3 else math.sqrt(regrets[i] / 200 ** 2) for i in range(len(regrets))]

pygame.display.flip()
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
