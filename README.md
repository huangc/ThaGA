# Targeted Haplotype-Assisted Reference-Guided Genome Assembly
Contributed by Chun-Yuan Huang, 3/10/2016

## Aims: 
Reference guided (rfguided) assembly of target sequence using tools such as TRegGA (https://github.com/BrendelGroup/TRegGA) often show different results on the target gene assembly when different reference genomes are used. It become critical to select the "correct" reference for optimal assembly when the sample sequence is distant from available references. This project Targeted Haplotype-Assisted Reference-Guided Genome Assembly (ThaRegGA) aims to improve reference guided genome assembly by building a reference from denovo assembled supercontigs derived from closely-related haplotype blocks of the target gene. Using the Rice 3,000 Genome Project (3kRGP) as our precious resource, ThaRegGA takes a specific rice cultivar and the genome coordinate of target gene of interest on reference Japponica genome as inputs, apply the haplotype search algorithm for its **close-related cultivars by targeted haplotype (Haplovar)** of the target gene in 3kRGP, retrieve and subject the Haplovar reads for denovo assembly using TRegGA, then returns with a supercontig sequence with annotation in Embl format. The ThaRegGA supercontig can be served as the new reference sequence in order to gain reliable reference-guided assembly of the target gene. Combined with TRegGA, this workflow can streamline and improve current targeted reference genome assembly by taking advantage of large-size genome projects such as 3kRGP.  

## Agenda of ThaRegGA development and application:
1. prove of concept using a target gene (TBD) and:
   * TRegGA of target gene with rice indica 93-11 reads against reference japonica
   * TRegGA of target gene with rice indica 93-11 reads against reference using denovo assembled supercontigs from close haplotypes (manually selected) on the target gene.
   * Comparison of result a and result b to 93-11 reference: result b should be closer to ref 93-11 than result a due to the use of ThaRegGA.
2. develop algorithm for identifying haplotypes of a target gene from 3kRGP
3. repeat of Aim1 with developed algorithm for ThaRegGA.
4. Application of ThaRegGA on finding Xa7 gene.

## Workflow description:
1. Identfy rice cultivars with closely-related haplotype (haplovars) to the sample with regards to the region of interest on the reference genome.
2. Retrieve and denovo assembly of haplovar contigs.
3. InDel fingerprinting of haplovar contigs for secondary validation (besides SNP fingerprinting in step1).
4. Mix and match of SNP/InDel fingerprinted haplovar reads and contigs for de novo assembly of haplovar supercontigs.
5. (Optional) rfguided assembly of haplovar supercontigs into haplovar pseudomolecule with [multiple] reference genomes.
6. rfguided assembly of sample reads/contigs using haplovar supercontig/pseudomolecule as reference.

## Workflow execution:
1. Edit and setup the parameters as described in 0SOURCE, then `source 0SOURCE`
2. Edit and prepare for the prerequisite files and softwares as described in PREREQ.sh, then `sh PREREQ.sh`
3. (Optional) If sample vcf not available, run whole genome variant calling: `sh x1-WGvarSNP`
4. Run haplovar finder: `qsub x2-HaplovarFinder`
5. Run denovo assembly of Haplovar contigs: `qsub x3-TRegGA-denovo`
6. Run indel fingerprinting of Haplovar contigs: `qsub x4-WGvarINDEL`
7. Run supercontig assembly of Haplovar contigs: `qsub x5-TRegGA-denovo`
8. Run rfguided assembly of sample contigs using haplovar supercontig as reference: `qsub x6-TRegGA-rfguided`
5. Find main outputs in *data/*.
6. Cleanup files with `sh xcleanup`

## Sub-directories for workflow implementation:
1. *prereq/*: prerequisite inputs such as retrieval and storage of TRegGA assembled contigs; retrieval and storage of reference genomes, preparation of BLAST+ database for reference genome.
2. *doc/*: reference and tutorial documents.
3. *bin/*: ancillary codes and scripts.
4. *src/*: prerequisite softwares
5. *run/*: main scripts and execution results.
6. *data/*: final outputs and reports.
