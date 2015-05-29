"""
author: Garrett Rodrigues
Notes:
    Uses only built-in modules
    Runs in about a minute with 152k obs on 4GB, i5 machine
"""

##################################################################################
#Load the files
##################################################################################

import string, pdb
from time import time 
from math import log 
from random import random

DEFAULT_OBSERVATION_FILE = "observations.txt"
NEW_OBSERVATION_FILE = 'new_obs.txt' #used if generating new observations
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

##################################################################################
#VITERBI ALGORITHM
##################################################################################
pdb.set_trace()
def Viterbi(obs, trans, emit, init, states, debug = False):
    V = [[0] * len(states)] #contain all the probs
    path = [[] for i in range(len(states))] #contain all the paths
    state_lookup = {state:i for i, state in enumerate(states)}
    #initialization
    start = time()
    print "Beginning the viterbi algorithm ..."
    for i, state in enumerate(states):
        V[0][i] = log(init[i]) + log( emit[i][int(obs[0])])
        path[i] = [state]

    n = len(obs)
    for t in range(1, len(obs)):
        V.append([0]*len(states))
        current_obs = int(obs[t])

        for i, curState in enumerate(states):
            (prob, state) = max( 
                    (V[0][j] + log(trans[j][i]) + log(emit[i][current_obs]), prevState) 
                    for j, prevState in enumerate(states))
            V[1][i] = prob #highest probability ending in in curState
            stateInd = state_lookup[state]
            
            # in general, you would append a new state at each iteration
            # but in this case, since most of the time a state transitions to itself
            # (see transitionmatrix), only append to the path list if we go to a new 
            # state
            if state != curState:
                path[i] = path[stateInd] + [curState]
        
        # for the next iteration, we only need the previous one iteratin
        # NOT the previous two
        del V[0]

        if t % 2000 == 0:
            print "Observation Count:{0} \t Precent Complete {1:.2f} \tTime Elapsed {2:.2f}".format(
                    t, t*1./n, time() - start)

    if debug:
        print "The probability values: "
        print V[0]
        print "The most probable paths ending in each letter: "
        print path
    prob, finalState = max ( (V[0][i], lastState) for i, lastState in enumerate(states))
    stateInd = state_lookup[finalState]
    return (prob, path[stateInd])


##################################################################################
# GENERATING A NEW SEQUENCE OF OBSERVATIONS
##################################################################################

def generate_new_obs(input_str, emit, states):
    total_str_length = 10**5
    num_obs_per_letter = total_str_length/len(input_str)
    obs = [0 for jj  in range(len(input_str) * num_obs_per_letter)]
    c = 0
    with open(NEW_OBSERVATION_FILE, 'w') as g:
        for letter in input_str:
            zero_thresh = emit[states.index(letter)][0]
            for kk in range(num_obs_per_letter):
                cur_obs = 0 if random() <= zero_thresh else 1
                obs[c] = cur_obs
                g.write(str(cur_obs) +" ")
                c+=1
    return obs
    
if __name__ == "__main__":
    
    fns = ['transitionMatrix.txt', 'new_obs.txt', 'initialStateDistribution.txt',
            'emissionMatrix.txt']
    #0. Load the parameter data
    trans = read_file(fns[0], dim = 2)
    init = read_file(fns[2])
    emit = read_file(fns[3], "\t", dim =2)
    states = string.uppercase 

    # 1. If desired, generate a new text sequence (comment this out to skip it)
    test_str = 'IntellisisIsACoolPlaceToWork' 
    new_obs = generate_new_obs(test_str.upper(), emit, states)
    
    # 2. Load the obs
    obs = read_file(DEFAULT_OBSERVATION_FILE) #read_file(NEW_OBSERVATION_FILE)
    print "All the parameters have been loaded ..."

    # 3. Process the observations to try and recover the original string based only
    # on the observations
    prob, bestPath = Viterbi(obs, trans, emit, init, states)
    print "The following is the log of the probability is the most likely state sequence."
    print "Note that the true probability can be calculated by e^(log_prob)" 
    print prob
    print bestPath
    print "".join(bestPath)
