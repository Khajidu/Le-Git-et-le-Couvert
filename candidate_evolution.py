#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, sys, random, copy, numpy, pygame
from pygame.locals import *

npartis = 3
veaututile = True

def finddistance(point1, point2):
    return abs(point2 - point1)

positions = range(100)

candidates = [int(100 * random.random()) for i in range(npartis)]

candidatenames = ["A", "B", "C"]
electoratenames = ["a", "b", "c"]

iteration = ""
iterations = []
for p in positions:
    if p in candidates:
        iteration += candidatenames[candidates.index(p)]
    else:
        iteration += "-"
print iteration
iterations.append(iteration)

def untour(candidates, distances, veaututile):
    counts = []
    if veaututile:
        return untour(candidates[:2], [distance[:2] for distance in distances], False) + [0 for i in range(2, len(candidates))]
    for i in range(len(candidates)):
        counts.append(len([distance for distance in distances if min(distance) == distance[i] and distance.count(distance[i]) == 1]))
    return counts

def deuxtours(candidates, distances, veaututile):
    if veaututile:
        for p in positions:
            distance = distances[p]
            if distance[0] < distance[1]:
                distance[0] = 0
                distance[1] = 100
            else:
                distance[1] = 0
                distance[0] = 100
    counts = untour(candidates, distances, veaututile)
    i = counts.index(max(counts))
    j = counts.index(max([counts[k] for k in range(len(candidates)) if k != i]))
    distances = [[distance[k] if k == i or k == j else 100 for k in range(len(candidates))] for distance in distances]
    counts = untour(candidates, distances, veaututile)
    return counts

def bordouille(candidates, distances, veaututile):
    counts = [0 for i in range(npartis)]
    for i in range(len(candidates)):
        for p in positions:
            if p != candidates[i]:
                distance = distances[p]
                ds = sorted(distance)
                if veaututile:
                    if (i == 0 and distance[i] < distance[1]) or (i == 1 and distance[i] < distance[0]):
                        counts[i] += npartis
                    elif (i == 0 and distance[i] > distance[1]) or (i == 1 and distance[i] > distance[0]):
                        counts[i] += 1
                    else:
                        counts[i] += npartis - 1
                else:
                    counts[i] += npartis - ds.index(distance[i])
    return counts

def votedevaleur(candidates, distances, veaututile):
    if veaututile:
        for p in positions:
            distance = distances[p]
            if distance[0] < distance[1]:
                distance[0] = 0
                distance[1] = 100
            else:
                distance[1] = 0
                distance[0] = 100
    counts = [sum([100 - distance[i] for distance in distances]) for i in range(len(candidates))]
    return counts

def jugementmajoritaire(candidates, distances, veaututile):
    if veaututile:
        for p in positions:
            distance = distances[p]
            if distance[0] < distance[1]:
                distance[0] = 0
                distance[1] = 100
            else:
                distance[1] = 0
                distance[0] = 100
    counts = [sorted([100 - distance[i] for distance in distances])[49] for i in range(len(candidates))]
    return counts

def approbation(candidates, distances, veaututile):
    if veaututile:
        for p in positions:
            distance = distances[p]
            if distance[0] < distance[1]:
                distance[0] = 0
                distance[1] = 100
            else:
                distance[1] = 0
                distance[0] = 100
    counts = [len([distance[i] for distance in distances if distance[i] < 25]) for i in range(len(candidates))]
    return counts

def irv(candidates, distances, veaututile):
    if veaututile:
        for p in positions:
            distance = distances[p]
            if distance[0] < distance[1]:
                distance[0] = 0
                distance[1] = 100
            else:
                distance[1] = 0
                distance[0] = 100
    counts = untour(candidates, distances, veaututile)
    eliminated = []
    while max(counts) <= 50 and not (max(counts) == 50 and counts.count(50) > 1):
        eliminate = counts.index(min([counts[i] for i in range(len(candidates)) if i not in eliminated]))
        eliminated.append(eliminate)
        counts[eliminate] = 0
        distances = [[distance[i] if i not in eliminated else 100 for i in range(len(candidates))] for distance in distances]
        counts = untour(candidates, distances, veaututile)
    return counts

def printout(candidates):
    iteration = ""
    votes = []
    for p in positions:
        distances = [finddistance(p, candidate) for candidate in candidates]
        votes.append(distances)
        if p in candidates:
            iteration += candidatenames[candidates.index(p)]
        else:
            d = min(distances)
            if distances.count(d) > 1:
                iteration += "-"
            else:
                i = distances.index(d)
                iteration += electoratenames[i]
        if p == 49:
            iteration += "*"
    return iteration, votes

def improved (i, p, candidates):
    candidate = candidates[i]
    iter1, ds1 = printout(candidates)
    iter2, ds2 = printout(candidates[:i] + [p] + candidates[i + 1:])
    electorate1 = irv(candidates, ds1, veaututile)[i]
    electorate2 = irv(candidates[:i] + [p] + candidates[i + 1:], ds2, veaututile)[i]
    return electorate2 > electorate1

nonconvergent = True
while nonconvergent:
    iter1, votes = printout(candidates)
    for i in range(len(candidates)):
        candidate = candidates[i]
        for p in positions:
            if p not in candidates and improved(i, p, candidates):
                candidates = copy.deepcopy(candidates[:i]) + [p] + copy.deepcopy(candidates[i + 1:])
        iteration, votes = printout(candidates)
        print iteration
    nonconvergent = iter1 != iteration
    iterations.append(iteration)
