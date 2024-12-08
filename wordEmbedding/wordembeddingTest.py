from scipy import spatial
import gensim.downloader as api
import numpy as np

model = api.load("glove-wiki-gigaword-50") #choose from multiple models https://github.com/RaRe-Technologies/gensim-data

s0 = 'game piece'
s1 = 'poker chip'
s2 = 'pencil'
s3 = 'player'
s4 = 'human'

def preprocess(s):
    return [i.lower() for i in s.split()]

def get_vector(s):
    return np.sum(np.array([model[i] for i in preprocess(s)]), axis=0)


print('s0 vs s1 ->',1 - spatial.distance.cosine(get_vector(s0), get_vector(s1)))
print('s0 vs s2 ->', 1 - spatial.distance.cosine(get_vector(s0), get_vector(s2)))
print('s0 vs s3 ->', 1 - spatial.distance.cosine(get_vector(s0), get_vector(s3)))
print('s0 vs s4 ->', 1 - spatial.distance.cosine(get_vector(s0), get_vector(s4)))