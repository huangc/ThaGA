#!/bin/bash
source ./0SOURCE

## Prerequisite data:
# The soapdenovo2-assembled contigs of genomic samples.
# The reference sequence.
# The paired-TALEN (pTALEN) repeat variable diresidue (RVD).

## Prerequisite software:
# NCBI BLAST+
# blat/35 (The BLAST-Like Alignment Tool)
# TALE-NT2 Target Finder 

##--------------------------------------------
# Setup sub-directory for workflow
cd ${WORK_DIR}
mkdir -p ${WORK_DIR}/prereq
mkdir -p ${WORK_DIR}/doc
mkdir -p ${WORK_DIR}/bin
mkdir -p ${WORK_DIR}/src
mkdir -p ${WORK_DIR}/data
mkdir -p ${WORK_DIR}/run
mkdir -p ${WORK_DIR}/scratch

## Prepare for the SOAPdenovo2-assembled sample contigs.
# Note: the contigs have been assembled previously, and we are just retrieving those contig files.
cd ${prereq_DIR}
for i in ${SAMPLE}
do
ln -s ${denovo_DIR}/${i}/${i}-SOAP/${i}-soap.contig .
makeblastdb -in ${i}-soap.contig -dbtype nucl -out DB_${i}_contig -parse_seqids
done

## Prepare the pTALEN RVD sequences for use in the TALE-NT2 target finder
# Generate pTALEN RVD as follows:
# echo '"rvdseq1" "rvdseq2"' > pTALEN_Name

echo '"HD NG NG HD HD NG NG HD HD NG NI NN HD NI HD NG NI NG NI NG NI NI" "NN HD NG NG NN NI NI NN NN HD NG NG NN NI NG NN NI NN HD NG NG NI"' > pTALEN_Os11N3

echo '"NG NI NN NI NG NI NG NN HD NI NG HD NG HD HD HD NG" "NI NG NI NG NI NN NG NG NN NN NI NN NI HD HD HD NG HD HD NI HD NG NG"' > pTALEN_Os8N3

## Retrieve and index the reference genome
echo "
#!/bin/bash
#PBS -m abe
#PBS -l nodes=1:ppn=8,vmem=20gb,walltime=00:30:00
#PBS -N prereq-on-${REFSEQNAME}
#PBS -j oe

cd ${prereq_DIR}

# Retrieve and index the reference sequence for Blast
sh ${bin_DIR}/xgetseq
" > prereq-on-${REFSEQNAME}.qsub
qsub prereq-on-${REFSEQNAME}.qsub

