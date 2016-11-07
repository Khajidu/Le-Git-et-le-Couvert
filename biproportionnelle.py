#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, sys, random, copy, numpy, pygame
from pygame.locals import *

ndeputes = 30
npartis = 10
powerdistance = 1
veaututile = 0.8
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
    return classementfinal

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
    return classementfinal

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
    return classementfinal

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
    return classementfinal

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
    return [sorted(votes, reverse = True).index(vote) + 1 for vote in votes]

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
    return [sorted(votes, reverse = True).index(vote) + 1 for vote in votes]

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
    classementfinal = [0 for i in range(npartis)]
    classementfinal[p] = 1
    classementfinal[p1 if p == p2 else p2] = 2
    votespremiertour = [votes[i] if i != p1 and i != p2 else 0 for i in range(npartis)]
    for i in [j for j in range(npartis) if j != p1 and j != p2]:
        classementfinal[i] = sorted(votespremiertour, reverse = True).index(votespremiertour[i]) + 3
    return classementfinal

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
    return [sorted(votes, reverse = True).index(vote) + 1 for vote in votes]

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
colles = [[] for i in range(ndeputes / 2)]
classes = [[] for i in range(ndeputes / 2)]
votestotaux = [[] for i in range(ndeputes / 2)]
votestotauxoriginels = [[] for i in range(ndeputes / 2)]
nvotes = 0
for circonscription in range(ndeputes / 2):
    candidats = []
    votes = []
    for parti in partis:
        x = numpy.random.normal(parti[0], parti[2], 1)[0]
        y = numpy.random.normal(parti[1], parti[3], 1)[0]
        xprime = numpy.random.normal(parti[0], parti[2], 1)[0]
        yprime = numpy.random.normal(parti[1], parti[3], 1)[0]
        candidats.append(((x, y), (xprime, yprime)))
        votes.append(0)
    partielus = jugementmajoritaireaffine([candidat[0] for candidat in candidats])
    partielu = partielus.index(1)
    voteparti = untourpartis([((candidat[0][0] + candidat[1][0]) / 2.0, (candidat[0][1] + candidat[1][1]) / 2.0) for candidat in candidats])
    votepartis = [votepartis[i] + voteparti[i] for i in range(npartis)]
    nvotes += sum(voteparti)
    colles[circonscription] = [candidats[i][0] if i != partielu else candidats[i][1] for i in range(npartis)]
    classes[circonscription] = [0 for p in partielus]
    for p in partielus:
        classes[circonscription][p - 1] = colles[circonscription][partielus.index(p)]
    votestotaux[circonscription] = [voteparti[i] if i != partielu else voteparti[i] / 2 for i in range(npartis)]
    votestotauxoriginels[circonscription] = copy.deepcopy(voteparti)
    elus[partielu].append(candidats[partielu][0])

pygame.init()
fenetre = pygame.display.set_mode((600,600), RESIZABLE)
continuer = 1
color=["White","Red","Blue","Green","Magenta","Cyan","Yellow","Gray","Brown","Orange"]

for i in range(len(elus)):
    for elu in elus[i]:
        fenetre.set_at((int(3 * elu[0]), int(3 * elu[1])), pygame.Color(color[i]))
        fenetre.set_at((int(3 * elu[0] + 1), int(3 * elu[1])), pygame.Color(color[i]))
        fenetre.set_at((int(3 * elu[0]), int(3 * elu[1]) + 1), pygame.Color(color[i]))
        fenetre.set_at((int(3 * elu[0] + 1), int(3 * elu[1]) + 1), pygame.Color(color[i]))

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
restes = [max(0, totaux[i] - attribues[i]) for i in range(npartis)]
print sum(restes)
restesreels = copy.deepcopy(restes)
#while sum(restes) != ndeputes / 2:
#    k = restes.index(max(restes))
#    restes[k] = max(0, restes[k] - (sum(restes) - ndeputes / 2))
while sum(restes) != ndeputes / 2:
    if sum(restes) > ndeputes / 2:
        electeurs = [1.0 * votepartis[i]/(restes[i] - 1) if restes[i] > 1 else numpy.inf for i in range(npartis)]
        p = electeurs.index(min(electeurs))
        restes[p] -= 1
    if sum(restes) < ndeputes / 2:
        electeurs = [1.0 * votepartis[i]/(restes[i] + 1) for i in range(npartis)]
        p = electeurs.index(max(electeurs))
        restes[p] += 1
print restes

#la somme des votetotaux[i] / ndeputes doit faire 1, la somme des [votetotal[i] for votetotal in votetotaux] / ndeputes doit faire restes[i]

nombresreels = [[1.0 * v / (nvotes / (ndeputes / 2)) for v in voteparti] for voteparti in votestotaux]
nombres = copy.deepcopy([copy.deepcopy(nombre) for nombre in nombresreels])#[[int(n + 0.5) for n in nombre] for nombre in nombresreels]
nn = 2
diffdeputes = [1.0 for i in range(ndeputes / 2)]
diffpartis = [1.0 * reste for reste in restes]
while sum(diffdeputes) > 10 ** -6 or sum(diffpartis) > 10 ** -6:
    for i in range(ndeputes / 2):
        nombresreels[i] = [1.0 * nombresreels[i][j] / sum(nombresreels[i]) for j in range(npartis)]
        nombres[i] = copy.deepcopy(nombresreels[i])#[int(n + 0.5) for n in nombresreels[i]]
    for i in range(npartis):
        for j in range(ndeputes / 2):
            nombresreels[j] = [nombresreels[j][k] * 1.0 * restes[i] if k == i else nombresreels[j][k] for k in range(npartis)]
            nombresreels[j] = [nombresreels[j][k] / sum([1.0 * nombre[i] for nombre in nombres]) if k == i and 1.0 * restes[i] != 0.0 else nombresreels[j][k] for k in range(npartis)]
            nombres[j] = copy.deepcopy(nombresreels[j])#[int(n + 0.5) for n in nombresreels[j]]
    nn += 1
    diffdeputes = [abs(1.0 * sum(nombre) - 1.0) for i in range(ndeputes / 2)]
    diffpartis = [abs(sum([1.0 * nombre[i] for nombre in nombres]) - 1.0 * restes[i]) for i in range(npartis)]
nombresreels = copy.deepcopy([copy.deepcopy(nombre) for nombre in nombres])
nombres = [[int(n + 0.5) for n in nombre] for nombre in nombresreels]
while [sum(nombre) for nombre in nombres] != [1 for i in range(ndeputes / 2)] or [sum([nombre[i] for nombre in nombres]) for i in range(npartis)] != restes:
    for i in range(ndeputes / 2):
        while sum(nombres[i]) != 1:
            while sum(nombres[i]) > 1:
                nombresreels[i] = [nombresreels[i][j] * (1 - 0.1) for j in range(npartis)]
                nombres[i] = [int(n + 0.5) for n in nombresreels[i]]
            while sum(nombres[i]) < 1:
                nombresreels[i] = [nombresreels[i][j] * (1 + 0.1) for j in range(npartis)]
                nombres[i] = [int(n + 0.5) for n in nombresreels[i]]
    for i in range(npartis):
        while sum([nombre[i] for nombre in nombres]) != restes[i]:
            while sum([nombre[i] for nombre in nombres]) > restes[i]:
                for j in range(ndeputes / 2):
                    nombresreels[j] = [nombresreels[j][k] * (1 - 0.1) if k == i else nombresreels[j][k] for k in range(npartis)]
                    nombres[j] = [int(n + 0.5) for n in nombresreels[j]]
            while sum([nombre[i] for nombre in nombres]) < restes[i]:
                for j in range(ndeputes / 2):
                    nombresreels[j] = [nombresreels[j][k] * (1 + 0.1) if k == i else nombresreels[j][k] for k in range(npartis)]
                    nombres[j] = [int(n + 0.5) for n in nombresreels[j]]
    nn += 1
print nombres
classements = []
for i in range(ndeputes / 2):
    partielu = nombres[i].index(1)
    elus[partielu].append(colles[i][partielu])
    collesavecvotes = [(colles[i][j], votestotauxoriginels[i][j]) for j in range(npartis)]
    classements.append(classes[i].index(colles[i][partielu]) + 1)
print classements

for i in range(len(elus)):
    for elu in elus[i]:
        fenetre.set_at((int(3 * elu[0]), int(3 * elu[1])), pygame.Color(color[i]))

pygame.display.flip()

while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
