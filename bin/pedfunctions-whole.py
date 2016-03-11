from numpy import *
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord 
from Bio.Seq import Seq

def heteroProcess( index, ped, genome) :
    nsample, ncols = ped.shape 
    amplified = empty([nsample, (ncols-6)/2], dtype=str )
    supressed = empty([nsample, (ncols-6)/2], dtype=str )

    homocount = zeros(nsample, dtype=int)
    heterocount = zeros(nsample, dtype=int)
    identitycount=zeros(nsample, dtype=int)

    for i in range(nsample) :
        for j in range (6, ncols, 2) :
            # number of snp after collapsing alelles
            nsnp=(j-6)/2
            # location in the genome
            reference=genome[index[nsnp][0]] [index[nsnp][1]-1 ]

            # homozygous case
            if ped[i][j] == ped[i][j+1] :
                amplified[i][nsnp] = ped[i][j]
                supressed[i][nsnp] = ped[i][j]

                if ped[i][j] == reference:
                    identitycount[i]+=1
                homocount[i] +=1;
            
            #heterozygous case
            else : 
#                print ped[i][0] ,index[numsnp][0], index[numsnp][1], reference, ped[i][j], ped[i][j+1]

                if ped[i][j] == reference :
                    amplified[i][nsnp] = ped[i][j+1]
                elif ped[i][j+1] == reference : 
                    amplified[i][nsnp] = ped[i][j]
                else :
                    print 'Hetero but no allele is identical to reference. Wow, thats rare!'
                    amplified[i][nsnp] = '0'

                supressed[i][nsnp] = reference;
                    
                heterocount[i] +=1

    return amplified, supressed,homocount,heterocount,identitycount

# takes a pedline and processes it wrt a reference genome
# removes the first 6 columns
# collapses hetero snps and makes 2 versions of half size
# supressed has all hetero snps reverted to reference
# amplified has all hetero snps biased to variant
# also counts identities, homo, hetero snps and no-recalls 

def pedline(genome, index, pedline) :
    ncols = len(pedline)
    amplified = empty((ncols-6)/2, dtype=str )
    supressed = empty((ncols-6)/2, dtype=str )

    for i in range(6,ncols,2) :
        # number of snp after collapsing alelles
        nsnp=(i-6)/2

        # reference for this snp
        reference = genome[index[nsnp][0]] [index[nsnp][1]-1]

        # homozygous case
        if pedline[i] == pedline[i+1] :
            homo += 1
            amplified[nsnp] = pedline[i]
            supressed[nsnp] = pedline[i]

            if pedline[i] == reference:
                identity += 1
            elif pedline[i] == '0' :
                norecall += 1
              
        #heterozygous case
        else : 
            hetero =+ 1
            #print ped[i][0] ,index[numsnp][0], index[numsnp][1], reference, ped[i][j], ped[i][j+1]

            if ped[i] == reference :
                amplified[nsnp] = pedline[i+1]
            elif ped[i+1] == reference : 
                amplified[nsnp] = pedline[i]
            else :
                print 'Hetero but no allele is identical to reference. Wow, thats rare!'
                amplified[nsnp] = '0'

            supressed[nsnp] = reference;
            
            return supressed, amplified, (identity,homo,hetero,norecall)



# takes a line from a ped file and mutates a genome accordingly 
def mutate (genome, name, index, pedline) :
    nsnps = len(pedline)
    newgenome=[0]

    ## ADD EXCEPTION/ERROR HERE!
     
    # make mutable copy of the genome 
    for i in range(1,13) :
        newgenome.append(SeqRecord (genome[i].tomutable(), id='chr'+str(i), description=''))

    # mutate the genome for each snp
    for i in range(nsnps) :
        chromosome = index[i][0]
        position   = index[i][1]
        mutateto   = pedline[i]
        
        if mutateto!='0' :
            newgenome[chromosome].seq[position] = mutateto 

    return newgenome




        


if __name__ == "__main__":

    mapfilename='NB-core_v4.map'
    pedfilename='iris.ped'

    
    #load mapfile
    mapfile = loadtxt (mapfilename, dtype=int)
    mapfile = mapfile[:,[0,3]]
    nsnps = mapfile.shape[0]

    #load pedfile
    pedfile = loadtxt(pedfilename, dtype=str)
    nsamples = pedfile.shape[0]

    #load genome
    genome=[0] ## have first element 0 to shift index
    nchromosomes = 0
    for chrom in SeqIO.parse('../all.chrs.con', 'fasta') :
        genome.append(chrom.seq)
        nchromosomes +=1

    amplified,supressed,homocount,heterocount,identitycount = heteroProcess(mapfile,pedfile,genome)

    for i in range(nsamples) :
        cultivar = pedfile[i,0]
        newgenome = mutate(genome, cultivar, mapfile, amplified[i]) 
        newfasta = open(cultivar+'.fasta', 'w')
        SeqIO.write(newgenome[1:], newfasta, 'fasta')



