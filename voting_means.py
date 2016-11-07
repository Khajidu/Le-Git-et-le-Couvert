#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, sys, random, copy, numpy, pygame
from pygame.locals import *

npartis = 8
powerdistance = 1
veaututile = 0.5
width = 5

def finddistance(point1, point2, powerdistance):
    x1, y1 = float(point1[0]), float(point1[1])
    x2, y2 = float(point2[0]), float(point2[1])
    if powerdistance == 1:
        return abs(x2 - x1) + abs(y2 - y1)
    elif powerdistance == 2:
        return math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
    elif powerdistance == 0:
        return max(abs(x2 - x1), abs(y2 - y1))
    else:
        return math.pow(math.pow(abs(x2 - x1), powerdistance) + math.pow(abs(y2 - y1), powerdistance), 1.0/powerdistance)

def irv(x0, y0, candidats):
    score = {}
    scores = {}
    candidates = copy.deepcopy(candidats)
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            for p in range(len(candidats)):
                distance = finddistance((x, y), candidats[p], powerdistance)
                distances.append(distance)
            sorteddistances = sorted(distances)
            for p in range(len(candidats)):
                score[(int(x),int(y),p)] = sorteddistances.index(distances[p]) + 1
    for p in range(len(candidats)):
        candidat = candidats[p]
        scores[candidat] = len([(x, y) for x in range(int(x0) - width, int(x0)) for y in range(int(y0) - width, int(y0)) if score[(x,y,p)] == 1])
    while len(candidats) > 2:
        s = min(scores[candidat] for candidat in candidats)
        candidate = [candidat for candidat in candidats if scores[candidat] == s][0]
        candidats = [candidat for candidat in candidats if candidat != candidate]
    candidate = [candidat for candidat in candidats if scores[candidat] >= (float(width) ** 2) / 2][0]
    return candidates.index(candidate)

def irvveaututile(x0, y0, candidats, veaututile):
    if random.random() <= veaututile:
        return irv(x0, y0, candidats)
    score = {}
    scores = {}
    candidates = copy.deepcopy(candidats)
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            for p in range(len(candidats)):
                distance = finddistance((x, y), candidats[p], powerdistance)
                distances.append(distance)
            sorteddistances = sorted(distances)
            if distances[0] < distances[1]:
                score[(int(x),int(y),0)] = 1
                score[(int(x),int(y),1)] = len(candidats)
            else:
                score[(int(x),int(y),0)] = len(candidats)
                score[(int(x),int(y),1)] = 1
            for p in range(2, len(candidats)):
                score[(int(x),int(y),p)] = sorteddistances.index(distances[p]) + 1
    for p in range(len(candidats)):
        candidat = candidats[p]
        scores[candidat] = len([(x, y) for x in range(int(x0) - width, int(x0)) for y in range(int(y0) - width, int(y0)) if score[(x,y,p)] == 1])
    while len(candidats) > 2:
        s = min(scores[candidat] for candidat in candidats)
        candidate = [candidat for candidat in candidats if scores[candidat] == s][0]
        candidats = [candidat for candidat in candidats if candidat != candidate]
    candidate = [candidat for candidat in candidats if scores[candidat] >= (float(width) ** 2) / 2][0]
    return candidates.index(candidate)

def votedevaleur(x0, y0, candidats):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
            for p in range(len(candidats)):
                distance = finddistance((x, y), candidats[p], powerdistance)
                votes[p] += int(distance/distance0)
    return votes.index(min(votes))

def votedevaleurveaututile(x0, y0, candidats, veaututile):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[1] += int(850/distance0)
                else:
                    votes[0] += int(850/distance0)
            for p in range(p0, len(candidats)):
                distance = finddistance((x, y), candidats[p], powerdistance)
                votes[p] += int(distance/distance0)
    return votes.index(min(votes))

def jugementmajoritaire(x0, y0, candidats):
    jugements = [[] for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
            for p in range(len(candidats)):
                distance = finddistance((x, y), candidats[p], powerdistance)
                jugements[p].append(int(distance/distance0))
    jugement = []
    for p in range(len(candidats)):
        notes = sorted(jugements[p])
        note = notes[len(notes)/2]
        jugement.append(note)
    return jugement.index(min(jugement))

def jugementmajoritaireveaututile(x0, y0, candidats, veaututile):
    jugements = [[] for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    jugements[1].append(int(850/distance0))
                    jugements[0].append(0)
                else:
                    jugements[0].append(int(850/distance0))
                    jugements[1].append(0)
            for p in range(p0, len(candidats)):
                distance = finddistance((x, y), candidats[p], powerdistance)
                jugements[p].append(int(distance/distance0))
    jugement = []
    for p in range(len(candidats)):
        notes = sorted(jugements[p])
        if len(notes) != 0:
            note = notes[len(notes)/2]
            jugement.append(note)
        else:
            jugement.append(0)
    return jugement.index(min(jugement))

def approbation(x0, y0, candidats):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
            for p in range(len(candidats)):
                distance = finddistance((x, y), candidats[p], powerdistance)
                if distance < distance0:
                    votes[p] += 1
    return votes.index(max(votes))

def approbationveaututile(x0, y0, candidats, veaututile):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
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
                distance = finddistance((x, y), candidats[p], powerdistance)
                if distance < distance0:
                    votes[p] += 1
    return votes.index(min(votes))

def untour(x0, y0, candidats):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
            for candidat in candidats:
                distance = finddistance((x, y), candidat, powerdistance)
                distances.append(distance)
            p = distances.index(min(distances))
            votes[p] += 1
    return votes.index(max(votes))

def untourveaututile(x0, y0, candidats, veaututile):
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
    return votes.index(max(votes))

def deuxtours(x0, y0, candidats):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            distance0 = numpy.random.normal(100, 30, 1)[0]
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

def deuxtoursveaututile(x0, y0, candidats, veaututile):
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

def bordouille(x0, y0, candidats):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            classement = []
            for candidat in candidats:
                distance = finddistance((x, y), candidat, powerdistance)
                distances.append(distance)
            while len(classement) < len(candidats):
                p = distances.index(min(distances))
                classement.append(p)
                distances[p] = 10000
            note = len(candidats)
            for rang in classement:
                votes[rang] += note
                note -= 1
    return votes.index(max(votes))

def bordouilleveaututile(x0, y0, candidats, veaututile):
    votes = [0 for candidat in candidats]
    for x1 in range(width):
        for y1 in range(width):
            x = x0 + x1 - width
            y = y0 + y1 - width
            distances = []
            p0 = 0
            classement = []
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x, y), candidats[0], powerdistance)
                distance2 = finddistance((x, y), candidats[1], powerdistance)
                if distance1 <= distance2:
                    distances.append(0)
                    distances.append(1000)
                else:
                    distances.append(1000)
                    distances.append(0)
                for candidat in candidats[p0:]:
                    distance = finddistance((x, y), candidat, powerdistance)
                    distances.append(distance)
                while len(classement) < len(candidats):
                    p = distances.index(min(distances))
                    classement.append(p)
                    distances[p] = 10000
            note = len(candidats)
            for rang in classement:
                votes[rang] += note
                note -= 1
    return votes.index(max(votes))

def display(candidats1, candidats2, fenetre, color):
    for i in range(len(candidats1)):
        candidat1 = candidats1[i]
        candidat2 = candidats2[i]
        #x = int(candidat[0])
        #y = int(candidat[1])
        pygame.draw.line(fenetre, pygame.Color(color[i]), candidat1, candidat2)
        #fenetre.set_at((2*x,2*(599-y)), pygame.Color(color[i]))
        #fenetre.set_at((2*x+1,2*(599-y)), pygame.Color(color[i]))
        #fenetre.set_at((2*x,2*(599-y)+1), pygame.Color(color[i]))
        #fenetre.set_at((2*x+1,2*(599-y)+1), pygame.Color(color[i]))

partis = []
for i in range(npartis):
    x = 600*random.random()
    y = 600*random.random()
    sigma1 = 100*random.random()
    sigma2 = 100*random.random()
    partis.append((x, y, sigma1, sigma2))

candidats = []
for parti in partis:
    x = numpy.random.normal(parti[0], parti[2], 1)[0]
    y = numpy.random.normal(parti[1], parti[3], 1)[0]
    candidats.append((x, y))

non_convergent = True
niter = 0
listes = []
pygame.init()
fenetre = pygame.display.set_mode((600,600), RESIZABLE)
continuer = 1
color=["White","Red","Blue","Green","Magenta","Cyan","Yellow","Gray","Brown","Orange"]
while non_convergent:
    veaututile = 1.0/math.log(len(candidats) - 1)
    electorats = [[] for candidat in candidats]
    for x in range(30):
        for y in range(30):
            partielu = deuxtoursveaututile(float(20 * x), float(20 * y), candidats, veaututile)
            electorats[partielu].append((float(20 * x), float(20 * y)))
    newpartis = []
    for p in range(len(candidats)):
        if len(electorats[p]) != 0:
            xcandidat = sum([float(x) for (x, y) in electorats[p]])/float(len(electorats[p]))
            ycandidat = sum([float(y) for (x, y) in electorats[p]])/float(len(electorats[p]))
            newpartis.append((xcandidat, ycandidat))
        elif len(electorats[p]) == 0 and p < len(newpartis):
            color = list([color[i] for i in range(len(color)) if i != p])
    niter += 1
    print niter, candidats, len(candidats)
    listes.append(candidats)
    if len(listes) >= 2:
        display(listes[-1], listes[-2], fenetre, color)
    pygame.display.flip()
    non_convergent = set(newpartis) not in [set(i) for i in listes]# and niter < 1000
    candidats = copy.deepcopy(newpartis)
display(candidats, listes[-2], fenetre, color)

pygame.display.flip()

print candidats, len(candidats), len(listes) - [set(i) for i in listes].index(set(candidats))

while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
