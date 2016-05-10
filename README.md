# Targeted Haplotype-Assisted Reference-Guided Genome Assembly
Contributed by Chun-Yuan Huang, 3/10/2016

## Aims: 
Reference guided (rfguided) assembly of target sequence using tools such as TRegGA [1] often show different results on the target gene assembly when different reference genomes are used. It become critical to select the "correct" reference for optimal assembly when the sample sequence is distant in phylogeny from available references. This workflow Targeted Haplotype-Assisted Reference-Guided Genome Assembly (ThaRegGA) aims to build a reliable targeted reference sequence in order to improve the accuracy of targeted rfguided genome assembly. Taking advantage of the Rice 3,000 Genome Project (3kRGP) [2] and SNP-Seek database [3], the ThaRegGA takes a specific rice cultivar and the genomic coordinate of the target region of interest on rice reference IRGSP-1.0 as inputs, applies the haplotype search program [4] to identify cultivars in SNP-Seek database that have high similarity in haplotype with regard to the target region of interest (we call such cultivars as **Haplovars**), retrieves the haplovar reads from 3kRGP [5] for denovo assembly, then returns with a superscaffold sequence with annotation in embl format. The ThaRegGA superscaffold can serve to replace the original IRGSP reference sequence as a more reliable alternative reference in order to gain accurate rfguided assembly of the target gene. Combines with TRegGA, this workflow output more reliable and accurate targeted sequence assembly that should be valuable in applications such as disease gene identification and characterization. 

## Workflow setup: haplovars as a module inside TRegGA.
```
git clone https://github.com/huangc/TRegGA.git
cd TRegGA
git clone https://github.com/huangc/haplovars.git
```

## Workflow description:
1. Identfy haplovars to the sample with regards to the region of interest on the reference genome.
2. Retrieve and denovo assembly of haplovar contigs and scaffolds.
3. Finding Deletion Fingerprints (DFPs) of haplovar contigs for secondary validation (besides SNP fingerprinting in step1).
4. Mix and match of SNP/InDel fingerprint-validated haplovar reads and scaffolds for denovo assembly of haplovar superscaffolds.
5. (Optional) rfguided assembly of haplovar superscaffolds into haplovar pseudomolecule with [multiple] reference genomes.
6. rfguided assembly of sample reads/scaffolds using haplovar superscafffolds/pseudomolecule as reference.

## Workflow execution:
1. Edit and setup the parameters as described in 0SOURCE, then `source 0SOURCE`
2. Edit and prepare for the prerequisite files and softwares as described in PREREQ.sh, then `sh PREREQ.sh`
3. (Optional) If sample vcf is not available, run whole genome variant calling: `sh x1-WGvarSNP`
4. Run haplotype search program to identify haplovars: `qsub x2-HaplovarFinder`
5. Run denovo assembly of haplovar contigs and scaffolds: `qsub x3-TRegGA-denovo`
6. Run whole genome blat alignment on haplovar contigs: `sh x4-WGblat`
7. Run Deletion Fingerprinting (DFP) of haplovar contigs: `qsub x5-WGindelT`
8. Run DFP clustering to identify close-relatives of haplovar contigs: `qsub x6-DFPtree`
9. Run superscaffold assembly of haplovar scaffolds, then use that as reference for rfguided assembly: `qsub x7-TRegGA-rfguided`
10. Find main outputs in *data/*.
11. Cleanup files with `sh xcleanup`

## Sub-directories for workflow implementation:
1. *prereq/*: prerequisite inputs such as retrieval and storage of TRegGA assembled contigs; retrieval and storage of reference genomes, preparation of BLAST+ database for reference genome.
2. *doc/*: reference and tutorial documents.
3. *bin/*: ancillary codes and scripts.
4. *src/*: prerequisite softwares
5. *run/*: main scripts and execution results.
6. *data/*: final outputs and reports.

## Reference:
1. TRegGA: https://github.com/BrendelGroup/TRegGA
2. 3,000 rice genomes project. The 3,000 rice genomes project. Gigascience. 2014  May 28;3:7.
3. Alexandrov N, et al. SNP-Seek database of SNPs derived from 3000 rice genomes. Nucleic Acids Res. 2015 Jan;43(Database issue):D1023-7.
4. Murat Öztürk, https://github.com/muzcuk/rice3k
5. The Rice 3000 Genomes Project Data. http://gigadb.org/dataset/200001.
