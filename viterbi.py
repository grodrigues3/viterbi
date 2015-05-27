"""
author: Garrett Rodrigues
"""

##################################################################################
#Load the files
##################################################################################

import string, pdb
from time import time 
from math import log #need this to keep probabilities from being too small


def read_file(fn, delimiter=" ", dim = 1):
    toRet = []
    with open(fn) as f:
        for line in f:
            words = line.strip().split(delimiter)
            if dim == 2:
                toRet += [[float(word) for word in words if word != "\n"]]
            else:
                toRet += [float(word) for word in words if word != "\n"]
    return toRet

fns = ['transitionMatrix', 'observations', 'initialStateDistribution',
        'emissionMatrix']

for i in range(len(fns)):
    fns[i] = fns[i] + ".txt"

trans = read_file(fns[0], dim = 2)
obs = read_file(fns[1])
init = read_file(fns[2])
emit = read_file(fns[3], "\t", dim =2)
states = string.uppercase 

##################################################################################
#VITERBI ALGORITHM
##################################################################################
pdb.set_trace()
def Viterbi(obs, trans, emit, init, states):
    V = [[0] * len(states)] #contain all the probs
    path = [[] for i in range(len(states))] #contain all the paths
    
    #initialization
    start = time()
    for i, state in enumerate(states):
        V[0][i] = log(init[i]) + log( emit[i][int(obs[0])])

    pdb.set_trace()
    n = len(obs)
    for t in range(1, len(obs)):
        V.append([0]*len(states))
        
        current_obs = int(obs[t])
        for i, curState in enumerate(states):
            (prob, state) = max( (V[0][j] + log(trans[j][i]) + log(emit[i][current_obs]), prevState) 
                    for j, prevState in enumerate(states))
            V[1][i] = prob #highest probability ending in in curState
            stateInd = states.index(state)
            if state != curState:
                path[i] = path[stateInd] + [curState]
        
        del V[0]

        if t % 2000 == 0:
            print t, t*1./n, time() - start
    try:
        prob, state = max ( (V[0][i], lastState) for i, lastState in enumerate(states))
        pdb.set_trace()
        stateInd = states.index(state)
        return (prob, path[stateInd])
    except:
        pdb.set_trace()


prob, bestPath = Viterbi(obs, trans, emit, init, states)
pdb.set_trace()
