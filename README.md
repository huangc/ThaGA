# Targeted Haplotype-Assisted Reference-Guided Genome Assembly
Contributed by Chun-Yuan Huang, 3/10/2016

## Aims: 
Reference guided assembly of target sequence using tools such as TRegGA (https://github.com/BrendelGroup/TRegGA) often show different results on the target gene assembly when different reference genomes are used. It become critical to select the "correct" reference for optimal assembly when the sample sequence is distant from available references. This project Targeted Haplotype-Assisted Reference-Guided Genome Assembly (ThaRegGA) aims to improve reference guided genome assembly by building a reference from denovo assembled supercontigs derived from closely-related haplotype blocks of the target gene. Using the Rice 3,000 Genome Project (3kRGP) as our resource, ThaRegGA takes a specific rice cultivar and the genome coordinate of target gene of interest on reference Japponica genome as inputs, apply the haplotype search algorithm for its **close-related cultivars by targeted haplotype (Haplovar)** of the target gene in 3kRGP, retrieve and subject the Haplovar reads for denovo assembly and RATT annotation using TRegGA, then returns with a supercontig sequence with annotation in Embl format. The ThaRegGA supercontig can be served as the new reference sequence in order to gain reliable reference-guided assembly of the target gene. Combined with TRegGA, this workflow can streamline and improve current targeted reference genome assembly by taking advantage of large-size genome projects such as 3kRGP.  

## Agenda of ThaRegGA development and application:
1. prove of concept using a target gene (TBD) and:
    * TRegGA of target gene with rice indica 93-11 reads against reference japonica
    * TRegGA of target gene with rice indica 93-11 reads against reference using denovo assembled supercontigs from close haplotypes (manually selected) on the target gene.
    * Comparison of result a and result b to 93-11 reference: result b should be closer to ref 93-11 than result a due to the use of ThaRegGA.
2. develop algorithm for identifying haplotypes of a target gene from 3kRGP
3. repeat of Aim1 with developed algorithm for ThaRegGA.
4. Application of ThaRegGA on finding Xa7 gene.

## Workflow description:
1. Blat of sample contigs (by SOAP-denovo assembly) against WG reference.

## Workflow execution:
1. Edit and setup the parameters as described in 0SOURCE, then `source 0SOURCE`
2. Edit and prepare for the prerequisite files and softwares as described in PREREQ.sh, then `sh PREREQ.sh`
3. (Optional) If sample vcf not available, submit qsub script for whole genome variant calling on Mason: `sh x1-WGvarSNP`
4. Submit qsub script for Haplovar finder on Mason: `qsub x2-HaploVarFinder`
5. Submit qsub script for denovo assembly of Haplovar contigs on Mason: `qsub x3-TRegGA-denovo`
5. Find main outputs in *data/*.
6. Cleanup files with `sh xcleanup`

## Sub-directories for workflow implementation:
1. *prereq/*: prerequisite inputs such as retrieval and storage of TRegGA assembled contigs; retrieval and storage of reference genomes, preparation of BLAST+ database for reference genome.
2. *doc/*: reference and tutorial documents.
3. *bin/*: ancillary codes and scripts.
4. *src/*: prerequisite softwares
5. *run/*: main scripts and execution results.
6. *data/*: final outputs and reports.
