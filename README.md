# Targeted Haplotype-Assisted Reference-Guided Genome Assembly
Contributed by Chun-Yuan Huang, 3/10/2016

## Aims: 
Reference guided (rfguided) assembly of target sequence using tools such as TRegGA [1] often show different results on the target gene assembly when different reference genomes are used. It become critical to select the "correct" reference for optimal assembly when the sample sequence is distant in phylogeny from available references. This project Targeted Haplotype-Assisted Reference-Guided Genome Assembly (ThaRegGA) aims to improve reference guided genome assembly by building a reference sequence from denovo assembled superscaffold, which is derived from close-related cultivars by targeted haplotype **(Haplovar)** of the target gene. Using the Rice 3,000 Genome Project (3kRGP) as our resource, ThaRegGA takes a specific rice cultivar and the genomic coordinate of the target gene of interest on reference Japponica genome as inputs, apply the haplotype search algorithm for its haplovar finding in 3kRGP, retrieve and subject the haplovar reads for denovo assembly, then returns with a superscaffold sequence with annotation in embl format. The ThaRegGA superscaffold can be served as the new reference sequence in order to gain reliable rfguided assembly of the target gene. Combines with TRegGA, this workflow take advantage of mega-size genome projects such as 3kRGP to improve on current targeted rfguided genome assembly, and output reliabily assembled target sequence that should be valuable in applications such as disease gene identification and characterization.    

## Workflow description:
1. Identfy haplovars to the sample with regards to the region of interest on the reference genome.
2. Retrieve and denovo assembly of haplovar contigs and scaffolds.
3. InDel fingerprinting of haplovar contigs for secondary validation (besides SNP fingerprinting in step1).
4. Mix and match of SNP/InDel fingerprint-validated haplovar reads and scaffolds for de novo assembly of haplovar superscaffolds.
5. (Optional) rfguided assembly of haplovar superscaffolds into haplovar pseudomolecule with [multiple] reference genomes.
6. rfguided assembly of sample reads/scaffolds using haplovar superscafffolds/pseudomolecule as reference.

## Workflow execution:
1. Edit and setup the parameters as described in 0SOURCE, then `source 0SOURCE`
2. Edit and prepare for the prerequisite files and softwares as described in PREREQ.sh, then `sh PREREQ.sh`
3. (Optional) If sample vcf not available, run whole genome variant calling: `sh x1-WGvarSNP`
4. Run haplovar finder: `qsub x2-HaplovarFinder`
5. Run denovo assembly of Haplovar contigs and scaffolds: `qsub x3-TRegGA-denovo`
6. Run indel fingerprinting of Haplovar contigs: `qsub x4-WGvarINDEL`
7. Run superscaffold assembly of Haplovar scaffolds: `qsub x5-TRegGA-denovo`
8. Run rfguided assembly of sample scaffolds using haplovar superscaffolds as reference: `qsub x6-TRegGA-rfguided`
5. Find main outputs in *data/*.
6. Cleanup files with `sh xcleanup`

## Agenda of ThaRegGA development and application:
1. prove of concept using a target gene (TBD) and:
   a. TRegGA of target gene with rice indica 93-11 reads against reference japonica
   b. TRegGA of target gene with rice indica 93-11 reads against reference using denovo assembled superscaffolds from haplovars (manually selected) on the target gene.
   * Comparison of result (a) and (b) to 93-11 reference: result (b) should be closer to ref 93-11 than result (a) due to the use of ThaRegGA.
2. develop algorithm for identifying haplotypes of a target gene from 3kRGP
3. repeat of Aim1 with developed algorithm for ThaRegGA.
4. Application of ThaRegGA on finding Xa7 gene.

## Sub-directories for workflow implementation:
1. *prereq/*: prerequisite inputs such as retrieval and storage of TRegGA assembled contigs; retrieval and storage of reference genomes, preparation of BLAST+ database for reference genome.
2. *doc/*: reference and tutorial documents.
3. *bin/*: ancillary codes and scripts.
4. *src/*: prerequisite softwares
5. *run/*: main scripts and execution results.
6. *data/*: final outputs and reports.

## Reference:
1. TRegGA: https://github.com/BrendelGroup/TRegGA
