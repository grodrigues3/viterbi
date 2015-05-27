import string, pdb

def read_file(fn, delimiter=" "):
    toRet = []
    with open(fn) as f:
        for line in f:
            words = line.strip().split(delimiter)
            toRet += [float(word) for word in words if word != "\n"]
    return toRet

fns = ['transitionMatrix', 'observations', 'initialStateDistribution',
        'emissionMatrix']

for i in range(len(fns)):
    fns[i] = fns[i] + ".txt"

trans = read_file(fns[0])
obs = read_file(fns[1])
init = read_file(fns[2])
emit = read_file(fns[3], "\t")
states = string.uppercase 
pdb.set_trace()
