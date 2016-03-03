# Targeted Haplotype-Assisted Genome Assembly
Contributed by Chun-Yuan Huang, 3/3/2016

## Aims: 
Reference guided assembly of target sequence using tools such as TRegGA often show different results on the target gene when different reference genomes are used. It become critical to select the "correct" reference for optimal result. Targeted Haplotype-Assisted Genome Assembly (ThaGA) aims to improve reference guided genome assembly by building a reference from denovo assembled supercontigs derived from closely-related haplotypes of the target gene. ThaGA takes a specific rice cultivar and the target gene of interest's coordinate on reference Japponica genome as inputs, apply the haplotype search algorithm to serach for the close-related haplotypes of the target gene in 3kRGP, retrieve and subject the haplotype reads for denovo assembly and RATT annotation using TRegGA, then returns with a supercontig sequence with annotation in Embl format. The ThaGA supercontig can be served as the new reference sequence in order to gain reliable reference-guided assembly of the target gene.

## Agenda of ThaGA development and application:
1. prove of concept using a target gene (TBD) and:
    * TRegGA of target gene with rice indica 93-11 reads against reference japonica
    * TRegGA of target gene with rice indica 93-11 reads against reference using denovo assembled supercontigs from close haplotypes (manually selected) on the target gene.
    * Comparison of result a and result b to 93-11 reference: result b should be closer to ref 93-11 than result a due to the use of ThaGA.
2. develop algorithm for identifying haplotypes of a target gene from 3kRGP
3. repeat of Aim1 with developed algorithm for ThaGA.
4. Application of ThaGA on finding Xa7 gene.

## Sub-directories for workflow implementation:
1. *prereq/*: prerequisite inputs such as retrieval and storage of TRegGA assembled contigs; retrieval and storage of reference genomes, preparation of BLAST+ database for reference genome.
2. *doc/*: reference and tutorial documents.
3. *bin/*: ancillary codes and scripts.
4. *src/*: prerequisite softwares
5. *run/*: main scripts and execution results.
6. *data/*: final outputs and reports.
