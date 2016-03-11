#!/usr/bin/env python2
# coding: utf-8

from numpy import *
import gzip 

def multidim_intersect(arr1, arr2):
    arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
    arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
    intersected = intersect1d(arr1_view, arr2_view)
    return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])


def find_indices(small, big) :
    index=[]
    j=0
    i=0

    while i <len(small)  :
        while (big[j] < small[i]).any() and j< len(big)-1 :
            j+=1
    
        if (small[i] == big[j]).all():
            index.append(j)
        i += 1
    return index


def ped_iterator(pedfname, index) :#, refindex, ref) :
    f = gzip.open(pedfname, 'r')
    for line in f :
        snpseq=''
        tmp = line.strip().split(' ')
        for i in index :
            alelle1 = tmp[6+2*i]
            alelle2 = tmp[7+2*i]
            if alelle1 == alelle2 :
                snpseq += alelle1 
            else :
                snpseq += ' '
        yield tmp[0], snpseq


# In[13]:

def hamdist(str1, str2):       
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs


# In[28]:

from itertools import imap
from operator import ne
def hamming2(str1, str2):
    assert len(str1) == len(str2)
    #ne = str.__ne__  ## this is surprisingly slow
    #ne = operator.ne
    return sum(imap(ne, str1, str2))


# In[21]:

from sys import argv
#fname = 'CX133.lean.homo.dat'
fname = argv[1]
unknown = loadtxt(fname, usecols=[0,1], dtype = int)
unknownBase = loadtxt(fname, usecols=[3], dtype = str)
#reference = loadtxt(fname, usecols=[2], dtype = str)
mapfile = loadtxt ('../NB-core_v4/NB-core_v4.map', dtype=int, usecols=(0,3))


# In[22]:

intersect = multidim_intersect(unknown,mapfile)
mapindex = find_indices(intersect, mapfile)
unknownindex = find_indices(intersect, unknown)
print len(unknown), len(mapfile), len(intersect),  len(unknownindex), len(mapindex)


# In[23]:

unknownseq=''
for i in unknownindex :
    unknownseq+=unknownBase[i]


# In[31]:

name=[]
dist=[]
for cultivar in ped_iterator('../NB-core_v4/NB-core_v4.ped.gz', mapindex) :
    name.append(cultivar[0])
    dist.append(hamming2(unknownseq, cultivar[1]))

print min(dist), max(dist)
print min(dist), 1.0-min(dist)/len(intersect), argmin(dist), name[argmin(dist)]

