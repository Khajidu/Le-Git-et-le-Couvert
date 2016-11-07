#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, sys, random, copy, numpy, pygame, svvamp
from pygame.locals import *

pop = svvamp.PopulationEuclideanBox(V=4000000, C=8, box_dimensions=[1, 1, 1, 1])
print "Population generated"
election = svvamp.TwoRound(pop)#svvamp.MajorityJudgment(pop, min_grade=0, max_grade=6, step_grade=1, rescale_grades=False)
print "Election done"

election.CM_option = 'exact'
print(election.CM_with_candidates())
print(election.ICM_with_candidates())
print(election.TM_with_candidates())
election.UM_option = 'exact'
print(election.UM_with_candidates())
election.IM_option = 'exact'
print(election.candidates_IM())
election.IIA_subset_maximum_size = numpy.inf
print(election.not_IIA_full())
