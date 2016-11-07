#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, sys, random, copy, numpy, pygame
from pygame.locals import *

ndeputes = 577
ndeputesproportionnelle = 300
npartis = 10
powerdistance = 1
veaututile = 0.5
veaututileprop = 0.3

def finddistance(point1, point2, powerdistance):
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    if powerdistance == 1:
        return abs(x2 - x1) + abs(y2 - y1)
    elif powerdistance == 2:
        return math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
    elif powerdistance == 0:
        return max(abs(x2 - x1), abs(y2 - y1))
    else:
        return math.pow(math.pow(abs(x2 - x1), powerdistance) + math.pow(abs(y2 - y1), powerdistance), 1.0/powerdistance)

def votedevaleur(candidats):
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            p0 = 0
            distances = [finddistance((x0, y0), candidats[p], powerdistance) for p in range(npartis)]
            notes = [int(max(0, 6 - distance / (500* random.random()))) for distance in distances]
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[1] += int(6)
                else:
                    votes[0] += int(6)
            for p in range(p0, len(candidats)):
                votes[p] += notes[p]
    sortedvotes = sorted(votes, reverse=True)
    classementfinal = [sortedvotes.index(vote) + 1 for vote in votes]
    elu = classementfinal.index(1)
    return elu

def chiasma(candidats):
    jugements = [[] for candidat in candidats]
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            p0 = 0
            distances = [finddistance((x0, y0), candidats[p], powerdistance) for p in range(npartis)]
            notes = [max(0, 6 - distance / (500* random.random())) for distance in distances]
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    jugements[1].append(0)
                    jugements[0].append(6)
                else:
                    jugements[0].append(0)
                    jugements[1].append(6)
            for p in range(p0, len(candidats)):
                jugements[p].append(notes[p])
    jugement = []
    for p in range(len(candidats)):
        grades = sorted(jugements[p], reverse=True)
        cumulative = [1.0 * grade * 201 ** 2 / 6 for grade in grades]
        diff = [abs(cumulative[i] - i) for i in range(201 ** 2)]
        jugement.append(((201 ** 2 - list(reversed(diff)).index(min(diff))) * 6.0 / 201 ** 2, grades[len(grades) / 2], sum(grades)))
    sortedvotes = sorted(jugement, key = lambda l: (-l[0], -l[1], -l[2]))
    classementfinal = [sortedvotes.index(j) + 1 for j in jugement]
    elu = classementfinal.index(1)
    return elu

def jugementmajoritaire(candidats):
    jugements = [[] for candidat in candidats]
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            p0 = 0
            distances = [finddistance((x0, y0), candidats[p], powerdistance) for p in range(npartis)]
            notes = [int(max(0, 6 - distance / (500* random.random()))) for distance in distances]
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    jugements[1].append(0)
                    jugements[0].append(6)
                else:
                    jugements[0].append(0)
                    jugements[1].append(6)
            for p in range(p0, len(candidats)):
                jugements[p].append(notes[p])
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
    return elu

def jugementmajoritaireaffine(candidats):
    jugements = [[] for candidat in candidats]
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            p0 = 0
            distances = [finddistance((x0, y0), candidats[p], powerdistance) for p in range(npartis)]
            notes = [int(max(0, 6 - distance / (500* random.random()))) for distance in distances]
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    jugements[1].append(0)
                    jugements[0].append(6)
                else:
                    jugements[0].append(0)
                    jugements[1].append(6)
            for p in range(p0, len(candidats)):
                jugements[p].append(notes[p])
    jugement = []
    for p in range(len(candidats)):
        grades = sorted(jugements[p], reverse=True)
        reversedgrades = sorted(jugements[p])
        if len(grades) != 0:
            note = grades[len(grades)/2]
            jugement.append((note, grades.index(note), reversedgrades.index(note)))
        else:
            jugement.append(0, grades.index(0), reversedgrades.index(0))
    nvotes = len(grades)
    sortedvotes = sorted(jugement, key = lambda l: (-l[0], -(nvotes / 2 - l[2]) / (nvotes - l[1] - l[2])))
    classementfinal = [sortedvotes.index(j) + 1 for j in jugement]
    elu = classementfinal.index(1)
    return elu

def approbation(candidats):
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                else:
                    votes[1] += 1
            for p in range(p0, len(candidats)):
                distance = finddistance((x0, y0), candidats[p], powerdistance)
                if distance < distance0:
                    votes[p] += 1
    return votes.index(min(votes))

def untour(candidats):
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            if random.random() <= veaututile:
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                else:
                    votes[1] += 1
            else:
                for candidat in candidats:
                    distance = finddistance((x0, y0), candidat, powerdistance)
                    distances.append(distance)
                p = distances.index(min(distances))
                votes[p] += 1
    return votes.index(max(votes))

def deuxtours(candidats):
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            if random.random() <= veaututile:
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                else:
                    votes[1] += 1
            else:
                for candidat in candidats:
                    distance = finddistance((x0, y0), candidat, powerdistance)
                    distances.append(distance)
                p = distances.index(min(distances))
                votes[p] += 1
    p1 = votes.index(max(votes))
    votes[p1] = 0
    p2 = votes.index(max(votes))
    deuxiemetour = [candidats[p1], candidats[p2]]
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            for candidat in deuxiemetour:
                distance = finddistance((x0, y0), candidat, powerdistance)
                distances.append(distance)
    if distances[0] < distances[1]:
        p = p1
    else:
        p = p2
    return p

def bordouille(candidats):
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            p0 = 0
            classement = []
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    distances.append(0)
                    distances.append(1000)
                else:
                    distances.append(1000)
                    distances.append(0)
                for candidat in candidats[p0:]:
                    distance = finddistance((x0, y0), candidat, powerdistance)
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

def untourpartis(candidats):
    for x in range(201):
        for y in range(201):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = x
            y0 = y
            if random.random() <= veaututileprop:
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                else:
                    votes[1] += 1
            else:
                for candidat in candidats:
                    distance = finddistance((x0, y0), candidat, powerdistance)
                    distances.append(distance)
                p = distances.index(min(distances))
                votes[p] += 1
    return votes

partis = []
xcandidats=[143, 5, 124, 25, 160, 111, 168, 159, 165, 115]
ycandidats=[167, 175, 150, 178, 101, 83, 112, 170, 127, 194]
for i in range(npartis):
    x = xcandidats[i]#200*random.random()
    y = ycandidats[i]#200*random.random()
    sigma1 = 10*random.random() + 10
    sigma2 = 10*random.random() + 10
    partis.append((x, y, sigma1, sigma2))

elus = [[] for parti in partis]
votepartis = [random.random() for parti in partis]
#colles = [[] for i in range(ndeputes / 2)]
#votestotaux = [[] for i in range(ndeputes / 2)]
#votestotauxoriginels = [[] for i in range(ndeputes / 2)]
nvotes = 0
for circonscription in range(ndeputes - ndeputesproportionnelle):
    candidats = []
    votes = []
    for parti in partis:
        x = numpy.random.normal(parti[0], parti[2], 1)[0]
        y = numpy.random.normal(parti[1], parti[3], 1)[0]
        candidats.append((x, y))
        votes.append(0)
    partielu = votedevaleur(candidats)
    voteparti = untourpartis([(parti[0], parti[1]) for parti in partis])
    votepartis = [votepartis[i] + voteparti[i] for i in range(npartis)]
    nvotes += sum(voteparti)
    #votestotaux[circonscription] = [voteparti[i] if i != partielu else voteparti[i] / 2 for i in range(npartis)]
    #votestotauxoriginels[circonscription] = copy.deepcopy(voteparti)
    elus[partielu].append(candidats[partielu])

pygame.init()
fenetre = pygame.display.set_mode((600,600), RESIZABLE)
continuer = 1
color=["White","Red","Blue","Green","Magenta","Cyan","Yellow","Gray","Brown","Orange"]

for i in range(len(elus)):
    for elu in elus[i]:
        fenetre.set_at((int(3 * (elu[0] % 200)), int(3 * (elu[1] % 200))), pygame.Color(color[i]))
        fenetre.set_at((int(3 * (elu[0] % 200) + 1), int(3 * (elu[1] % 200))), pygame.Color(color[i]))
        fenetre.set_at((int(3 * (elu[0] % 200)), int(3 * (elu[1] % 200)+ 1)), pygame.Color(color[i]))
        fenetre.set_at((int(3 * (elu[0] % 200) + 1), int(3 * (elu[1] % 200) + 1)), pygame.Color(color[i]))

pygame.display.flip()

totauxreels = [random.random() * v * ndeputes / nvotes for v in votepartis]
attribues = [len(elu) for elu in elus]
totaux = [int(total + 0.5) for total in totauxreels]
while sum(totaux) < ndeputes:
    electeurs = [1.0 * votepartis[i]/(totaux[i] + 1) for i in range(npartis)]
    p = electeurs.index(max(electeurs))
    totaux[p] += 1
while sum(totaux) > ndeputes:
    electeurs = [1.0 * votepartis[i]/(totaux[i] - 1) if totaux[i] > 1 else numpy.inf for i in range(npartis)]
    p = electeurs.index(min(electeurs))
    totaux[p] -= 1
current = copy.deepcopy(attribues)
for j in range(ndeputes - sum(attribues)):
    votescorriges = [1.0 * votepartis[k] / (current[k] + 1) for k in range(npartis)]
    i = votescorriges.index(max(votescorriges))
    current[i] += 1
    parti = partis[i]
    elus[i] = elus[i] + [(numpy.random.normal(parti[0], parti[2], 1)[0], numpy.random.normal(parti[1], parti[3], 1)[0])]

disprop = sum([abs(1.0 * len(elus[i]) / votepartis[i] / ndeputes * sum(votepartis) - 1.0) for i in range(npartis)])
dispropcarres = math.sqrt(sum([(1.0 * len(elus[i]) / votepartis[i] / ndeputes * sum(votepartis) - 1.0) ** 2 for i in range(npartis)]))
print disprop, dispropcarres
enopv = sum([(1.0 * votepartis[i] / sum(votepartis)) ** 2 for i in range(npartis)])
enopd = sum([(1.0 * len(elu) / ndeputes) ** 2 for elu in elus])
print enopv, enopd

for i in range(len(elus)):
    for elu in elus[i]:
        fenetre.set_at((int(3 * (elu[0] % 200)), int(3 * (elu[1] % 200))), pygame.Color(color[i]))

pygame.display.flip()

while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
