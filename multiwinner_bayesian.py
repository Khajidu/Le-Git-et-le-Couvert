#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, sys, random, copy, numpy, pygame
from pygame.locals import *

# eventuellement demander le nombre de deputes et de ministres et d'electeurs, et le nombre de partis qui presentent des deputes, et la distance
ndeputes = 577
nministres = 40
nelecteurs = 100
npartis = 10
powerdistance = 1
veaututile = 0.5

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

def votedevaleur(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = 20*x
            y0 = 20*y
            for p in range(len(candidats)):
                distance = finddistance((x0, y0), candidats[p], powerdistance)
                votes[p] += int(distance/distance0)
                totalvotes[p] += int(distance/distance0)
    return votes.index(min(votes)), totalvotes

def votedevaleurveaututile(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = 20*x
            y0 = 20*y
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[1] += int(280/distance0)
                    totalvotes[1] += int(280/distance0)
                else:
                    votes[0] += int(280/distance0)
                    totalvotes[0] += int(280/distance0)
            for p in range(p0, len(candidats)):
                distance = finddistance((x0, y0), candidats[p], powerdistance)
                votes[p] += int(distance/distance0)
                totalvotes[p] += int(distance/distance0)
    return votes.index(min(votes)), totalvotes

def jugementmajoritaire(candidats, totalvotes):
    jugements = []
    for p in range(len(candidats)):
        jugements.append([])
    for x in range(10):
        for y in range(10):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = 20*x
            y0 = 20*y
            for p in range(len(candidats)):
                distance = finddistance((x0, y0), candidats[p], powerdistance)
                jugements[p].append(int(distance/distance0))
                totalvotes[p] += int(distance/distance0)
    jugement = []
    for p in range(len(candidats)):
        notes = sorted(jugements[p])
        note = notes[len(notes)/2]
        jugement.append(note)
    return jugement.index(min(jugement)), totalvotes

def jugementmajoritaireveaututile(candidats, totalvotes):
    jugements = []
    for p in range(len(candidats)):
        jugements.append([])
    for x in range(10):
        for y in range(10):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = 20*x
            y0 = 20*y
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    jugements[1].append(int(280/distance0))
                    jugements[0].append(0)
                    totalvotes[1] += int(280/distance0)
                else:
                    jugements[0].append(int(280/distance0))
                    jugements[1].append(0)
                    totalvotes[0] += int(280/distance0)
            for p in range(p0, len(candidats)):
                distance = finddistance((x0, y0), candidats[p], powerdistance)
                jugements[p].append(int(distance/distance0))
                totalvotes[p] += int(distance/distance0)
    jugement = []
    for p in range(len(candidats)):
        notes = sorted(jugements[p])
        note = notes[len(notes)/2]
        jugement.append(note)
    return jugement.index(min(jugement)), totalvotes

def approbation(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = 20*x
            y0 = 20*y
            for p in range(len(candidats)):
                distance = finddistance((x0, y0), candidats[p], powerdistance)
                if distance < distance0:
                    votes[p] += 1
                    totalvotes[p] += 1
    return votes.index(max(votes)), totalvotes

def approbationveaututile(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            distance0 = numpy.random.normal(30, 10, 1)[0]
            x0 = 20*x
            y0 = 20*y
            p0 = 0
            if random.random() <= veaututile:
                p0 = 2
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                    totalvotes[0] += 1
                else:
                    votes[1] += 1
                    totalvotes[1] += 1
            for p in range(p0, len(candidats)):
                distance = finddistance((x0, y0), candidats[p], powerdistance)
                if distance < distance0:
                    votes[p] += 1
                    totalvotes[p] += 1
    return votes.index(min(votes)), totalvotes

def untour(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
            for candidat in candidats:
                distance = finddistance((x0, y0), candidat, powerdistance)
                distances.append(distance)
            p = distances.index(min(distances))
            votes[p] += 1
            totalvotes[p] += 1
    return votes.index(max(votes)), totalvotes

def untourveaututile(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
            if random.random() <= veaututile:
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                    totalvotes[0] += 1
                else:
                    votes[1] += 1
                    totalvotes[1] += 1
            else:
                for candidat in candidats:
                    distance = finddistance((x0, y0), candidat, powerdistance)
                    distances.append(distance)
                p = distances.index(min(distances))
                votes[p] += 1
                totalvotes[p] += 1
    return votes.index(max(votes)), totalvotes

def deuxtours(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
            for candidat in candidats:
                distance = finddistance((x0, y0), candidat, powerdistance)
                distances.append(distance)
            p = distances.index(min(distances))
            votes[p] += 1
            totalvotes[p] += 1
    p1 = votes.index(max(votes))
    votes[p1] = 0
    p2 = votes.index(max(votes))
    deuxiemetour = [candidats[p1], candidats[p2]]
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
            for candidat in deuxiemetour:
                distance = finddistance((x0, y0), candidat, powerdistance)
                distances.append(distance)
    if distances[0] < distances[1]:
        p = p1
    else:
        p = p2
    return p, totalvotes

def deuxtoursveaututile(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
            if random.random() <= veaututile:
                distance1 = finddistance((x0, y0), candidats[0], powerdistance)
                distance2 = finddistance((x0, y0), candidats[1], powerdistance)
                if distance1 <= distance2:
                    votes[0] += 1
                    totalvotes[0] += 1
                else:
                    votes[1] += 1
                    totalvotes[1] += 1
            else:
                for candidat in candidats:
                    distance = finddistance((x0, y0), candidat, powerdistance)
                    distances.append(distance)
                p = distances.index(min(distances))
                votes[p] += 1
                totalvotes[p] += 1
    p1 = votes.index(max(votes))
    votes[p1] = 0
    p2 = votes.index(max(votes))
    deuxiemetour = [candidats[p1], candidats[p2]]
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
            for candidat in deuxiemetour:
                distance = finddistance((x0, y0), candidat, powerdistance)
                distances.append(distance)
    if distances[0] < distances[1]:
        p = p1
    else:
        p = p2
    return p, totalvotes

def bordouille(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
            classement = []
            for candidat in candidats:
                distance = finddistance((x0, y0), candidat, powerdistance)
                distances.append(distance)
            while len(classement) < len(candidats):
                p = distances.index(min(distances))
                classement.append(p)
                distances[p] = 10000
            note = len(candidats)
            for rang in classement:
                votes[rang] += note
                totalvotes[rang] += note
                note -= 1
    return votes.index(max(votes)), totalvotes

def bordouilleveaututile(candidats, totalvotes):
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
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
                totalvotes[rang] += note
                note -= 1
    return votes.index(max(votes)), totalvotes

# les centres et ecarts types en x et y des partis sont tires au hasard, l'importance de chaque parti est le produit des ecarts types
partis = []
for i in range(npartis):
    x = 200*random.random()
    y = 200*random.random()
    sigma1 = 20*random.random() + 10
    sigma2 = 20*random.random() + 10
    partis.append((x, y, sigma1, sigma2))
# demander si le regime est parlementaire, semi presidentiel ou presidentiel, ca a son importance plus tard
regime = 0 # mettons que ce soit un regime parlementaire
# demander si le prez est elu directement, et comment, l'election sera faite en meme temps que le reste, et tirer au hasard les candidats a la prez selon les distributions statistiques des partis
prezelu = False
# demander le mode de scrutin pour elire les deputes
modedescrutin = 0 # on va dire que c la proportionnelle
# il y aura une partie (eventuellement de taille nulle) des deputes elus dans des circonscriptions
# et une partie (eventuellement nulle) elue par listes
# dans chaque circonscription :
    # tirer au hasard le ou les deputes de chaque parti au hasard selon la gaussienne
    # tirer 1d10 et si on fait 10 tirer un sans etiquette de facon equiprobable dans le plan
    # recommencer
    # pour chaque point du plan faire 100 (ou tout autre nombre de) fois :
        # tirer au hasard si besoin les criteres individuels de cet electeur genre a quelle distance il met telle note, etc.
        # le faire voter selon ses criteres et le mode de scrutin (si c un mode de scrutin crado par ex le faire voter pour le depute le plus pres, etc.)
        # le faire voter pour le prez si besoin, memes criteres et mode de scrutin choisi pour le prez
        # pooler tous les bulletins de vote, depouiller et elire le ou les deputes
# pour les listes : tirer au hasard selon la gaussienne autant de candidats que de deputes
regret = 0
totalvotes = []
for parti in partis:
    totalvotes.append(0)
ndeputesproportionnelle = 200
ndeputescirconscriptions = ndeputes - ndeputesproportionnelle
disprop = 0
dispropcarres = 0
votescarres = 0
votescarres2 = 0
eluscentristes = 0
ministrescentristes = 0
for election in range(100):
    partis = []
    for i in range(npartis):
        x = 200*random.random()
        y = 200*random.random()
        sigma1 = 20*random.random() + 10
        sigma2 = 20*random.random() + 10
        partis.append((x, y, sigma1, sigma2))
    candidats = []
    for parti in partis:
        candidats.append([])
        for i in range(ndeputesproportionnelle):
            x = numpy.random.normal(parti[0], parti[2], 1)[0]
            y = numpy.random.normal(parti[1], parti[3], 1)[0]
            candidats[-1].append((x, y))
    # classer dans la liste selon l'ordre de tirage ou de distance croissante du centre (demander avant)
    # demander si le parti fixe l'ordre (voir ci dessus) ou si c les electeurs
    # faire voter 1 electeur par point (ca suffit) en fonction des distances moyennes ou medianes (demander avant)
    votes = []
    for i in range(npartis):
        votes.append(0)
    for x in range(10):
        for y in range(10):
            distances = []
            x0 = 20*x
            y0 = 20*y
            for parti in candidats:
                distance = 0.0
                for candidat in parti:
                    distance += finddistance((x0, y0), candidat, powerdistance)
                distances.append(distance)
            p = distances.index(min(distances))
            votes[p] += 1
            totalvotes[p] += ndeputesproportionnelle
    # calculer le nombre total de sieges pour chaque parti a la proportionnelle (par ex)
    nbrestheoriques = []
    for vote in votes:
        nbrestheoriques.append(vote*ndeputesproportionnelle/100)
    nbres = []
    for nombre in nbrestheoriques:
        nbres.append(1.0*int(nombre))
    # ajouter ou enlever les deputes au besoin en regardant qui a plus besoin de les gagner/perdre (on teste combien d'electeurs sont representes par un depute de chaque liste en ajoutant/enlevant un depute)
    plusfortreste = True
    if plusfortreste:
        restes = []
        for nombre in nbrestheoriques:
            restes.append(nombre - int(nombre))
        while sum(nbres) < ndeputesproportionnelle:
            reste = restes.index(max(restes))
            nbres[reste] += 1
            restes[reste] = 0
    while sum(nbres) < ndeputesproportionnelle:
        electeurs = []
        for i in range(len(nbres)):
            electeurs.append(votes[i]/(nbres[i] + 1))
        p = electeurs.index(max(electeurs))
        nbres[p] += 1
    while sum(nbres) > ndeputesproportionnelle:
        electeurs = []
        for i in range(len(nbres)):
            electeurs.append(votes[i]/(nbres[i] - 1))
        p = electeurs.index(min(electeurs))
        nbres[p] -= 1
    elus = []
    for i in range(len(candidats)):
        elus.append([])
        elus[-1] = copy.deepcopy(candidats[i][:int(nbres[i])])
    # une fois l'assemblee elue, choisir aleatoirement parmi les deputes de chaque parti (selon la gaussienne) le prez de groupe
    for circonscription in range(ndeputescirconscriptions):
        candidats = []
        votes = []
        for parti in partis:
            x = numpy.random.normal(parti[0], parti[2], 1)[0]
            y = numpy.random.normal(parti[1], parti[3], 1)[0]
            candidats.append((x, y))
            votes.append(0)
        partielu, totalvotes = jugementmajoritaireveaututile(candidats, totalvotes)
        elus[partielu].append(candidats[partielu])
    prezdegroupes = []
    nbres = []
    for parti in elus:
        nbres.append(len(parti))
        if len(parti) != 0:
            prezdegroupes.append(parti[0]) # en fait on prend la tete de liste pour l'instant
        else:
            prezdegroupes.append((1000,1000))
    winner = nbres.index(max(nbres))
    # le plus gros parti essaye de former une coalition avec les autres, il le fera avec l'un d'entre eux avec des probas proportionnelles aux nbre de deputes respectifs
    # et inversement proportionnelles aux distances entre prez de groupe
    premierministre = prezdegroupes[winner] # ici on prend juste le plus gros groupe et il coalesce avec les groupes successivement plus proche jusqu'a la majorite absolue
    majorite = int(ndeputes/2) + 1
    coalition = int(nbres[winner])
    distancesgroupes = []
    distance = 0.0
    for i in range(len(nbres)):
        distance = 0.0
        if i != winner:
            distance = 0.0
            x = premierministre[0]
            y = premierministre[1]
            x0 = prezdegroupes[i][0]
            y0 = prezdegroupes[i][1]
            distance = finddistance((x, y), (x0, y0), powerdistance)
            distancesgroupes.append(distance)
        else:
            distancesgroupes.append(10000)
    while coalition < majorite:
        groupe = distancesgroupes.index(min(distancesgroupes))
        distancesgroupes[groupe] = 10000
        coalition += int(nbres[groupe])
    # on prend comme centre du nouveau blob le barycentre des centres de ses composantes et comme taille la somme des tailles
    # on fusionne le plus gros blob non nouvellement cree avec un autre blob non nouvellement cree, de meme
    # on arrete des qu'un blob fait plus de la moitie du total des deputes
    # le plus gros parti de cette coalition sort son prez de groupe, c le 1er ministre
    # il forme le gvt dans la coalition, les nbres de ministres sont proportionnels aux nbre de deputes
    # les ministres sont tires aleatoirement parmi les deputes selon les gaussiennes
    ministres = []
    for i in range(len(nbres)):
        if distancesgroupes[i]==10000:
            nbreministres = int(nbres[i]/10)
            ministres += copy.deepcopy(elus[i][:nbreministres])

    # on fait passer 1 electeur par point et il mesure sa distance totale (ou moyenne ou mediane) avec les ministres
    # le 1er ministre compte 5
    # le prez compte 1 dans un regime parlementaire, 5 dans un regime semi presidentiel et 10 dans un regime presidentiel

    distancetotale = 0
    for ministre in ministres:
        x0 = ministre[0]
        y0 = ministre[1]
        for x in range(20):
            for y in range(20):
                x1 = 10*x
                y1 = 10*y
                distancetotale += 1/finddistance((x0, y0), (x1, y1), powerdistance)
    regret += 1/distancetotale*(len(ministres)*400)
    distancetotale = 0
    for parti in elus:
        for elu in parti:
            x0 = elu[0]
            y0 = elu[1]
            for x in range(20):
                for y in range(20):
                    x1 = 10*x
                    y1 = 10*y
                    distancetotale += 1/finddistance((x0, y0), (x1, y1), powerdistance)
    regret += 1/distancetotale*(ndeputes*400)
    for p in range(len(partis)):
        disprop += abs(totalvotes[p]/10000.0 - len(elus[p]))/ndeputes
        dispropcarres += (abs(totalvotes[p]/10000.0 - len(elus[p]))/ndeputes)*(abs(totalvotes[p]/10000.0 - len(elus[p]))/ndeputes)
        votescarres += ((totalvotes[p]/10000.0)/ndeputes)*((totalvotes[p]/10000.0)/ndeputes)
        votescarres2 += (1.0*len(elus[p])/ndeputes)*(1.0*len(elus[p])/ndeputes)
        eluscentristes += 1.0 * len([elu for elu in elus[p] if 50 < elu[0] < 150 and 50 < elu[1] < 150]) / ndeputes
    ministrescentristes += 1.0 * len([ministre for ministre in ministres if 50 < ministre[0] < 150 and 50 < ministre[1] < 150]) / len(ministres)

#print sum([((totalvotes[p]/10000.0)/ndeputes)*((totalvotes[p]/10000.0)/ndeputes) for p in range(len(partis))])

print regret/100, disprop/100, math.sqrt(dispropcarres)/10
print 100/votescarres2/npartis, 10/votescarres/npartis
print eluscentristes / 100, ministrescentristes / 100

pygame.init()
fenetre = pygame.display.set_mode((600,600), RESIZABLE)
continuer = 1
color=["White","Red","Blue","Green","Magenta","Cyan","Yellow","Gray","Brown","Orange"]

for i in range(len(elus)):
    for elu in elus[i]:
        fenetre.set_at((int(3 * elu[0]), int(3 * elu[1])), pygame.Color(color[i]))
for ministre in ministres:
    i = [p for p in range(len(elus)) if ministre in elus[p]][0]
    fenetre.set_at((int(3 * ministre[0]), int(3 * ministre[1])), pygame.Color(color[i]))
    fenetre.set_at((int(3 * ministre[0]) + 1, int(3 * ministre[1])), pygame.Color(color[i]))
    fenetre.set_at((int(3 * ministre[0]), int(3 * ministre[1]) + 1), pygame.Color(color[i]))
    fenetre.set_at((int(3 * ministre[0]) + 1, int(3 * ministre[1]) + 1), pygame.Color(color[i]))

pygame.display.flip()

while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
