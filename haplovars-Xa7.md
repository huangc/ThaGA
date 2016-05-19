## Agenda of ThaRegGA development:
1. prove of concept using target genes LRK and Sub1:
   * (a). TRegGA of target gene with rice indica 93-11 reads against reference japonica. 
   * (b). TRegGA of target gene with rice indica 93-11 reads against reference using denovo assembled superscaffolds from haplovars (manually selected) on the target gene.
   * Comparison of result (a) and (b) to 93-11 reference: result (b) should be closer to ref 93-11 than result (a) due to the use of ThaRegGA.
2. develop algorithm for identifying haplotypes of a target gene from 3kRGP
3. repeat of Aim1 with developed algorithm for ThaRegGA.

## Cultivars that are Xoo resistant
* CX134 IRBB7 Indica Note: [6] Xa7
* IRIS 313-10605 DV86 Aus/boro  Note: [2][4] Xa7;Xa5
* CX369 IRBB62 Indica Note: [5] Xa4;Xa7;Xa21
* CX126 IRBB60 Indica Note: [3][4] Xa4;xa5;xa13;Xa21
* CX44 IR58025B Indica Note: [3][4] Xa4;xa5;xa13;Xa21

## Agenda of haplovars application on finding Xa7 gene.
#### Xa7 Target region:
* 1. M5_M5-56K in rice japonica is chr6:27,965,437..28,022,337, Length=56,901 bp.
* 2. M5_M5-56K in rice japonica is redefined as chr6:27,965,001..28,023,000, Length=58,000 bp.
* 3. M5_M5-56K in rice indica is chr6:29,683,670..29,828,319, Length=144,650 bp.
* 4. M5_M5-56K in rice indica is redefined to chr6:29,683,001..29,829,000, Length=146,000 bp.
* 5. M5_M5-56K in rice indica, after removing the artifact insert, Length=66,477 bp.
  * Artifact insert region in indica is chr6:29,704,162..29,783,684, Length=79,523 bp.
  * Gene annotations are all re-coordinated to start from position 1.
* Seven protein-coding genes are included in this region. They will be used as anchors to clarify the shifting regions such as the 17kb region defined in LeftFlank and RightFlank.
* Seven genes are: OS06G0673700, OS06G0674000, OS06G0674100, OS06G0674400, OS06G0674800, OS06G0675200, OS06G0675300.
* Among them, there are two pairs of overlapping genes: "OS06G0673700, OS06G0674000", and "OS06G0675200, OS06G0675300".
* So we have total of five anchors in this 58Kb Xa7QTL.
* use 5 Kb and  more on left and right of M5..M5_56K for rfguided assembly; chr6:27960001..28023000, 63 Kb.

#### Xa7 study with haplovars

* 1. Xa7 Query Parameters and TRegGA run for prior (and presumably unsatified) preliminary results
```bash
source ./TRegGA.source
cd ${TRegGA_DIR}
# generate TRegGA.sample with a list of sample names
\rm -f TRegGA.sample
SAMPLE="IRBB7 DV86 IRBB62"
for k in ${SAMPLE}
do
grep "$k" ${TRegGA_DIR}/reads/rice_line_metadata_20140521.tsv > rec.rice_line
VARID=`cut -f1 rec.rice_line`
SNPseekID=`cut -f5 rec.rice_line`
VARNAME=`cut -f13 rec.rice_line`
VARGROUP=`cut -f18 rec.rice_line`
echo "$VARID|$SNPseekID|$VARNAME|$VARGROUP" >> TRegGA.sample
done

# The VARNAME/SYNONYME (third column, $3) CANNOT have any whitespace in it. Replace the whitespaces with "_" or remove it if there is any. 
awk 'BEGIN {OFS=FS="|"} {gsub(/\s/,"_",$3); print }' TRegGA.sample > tmp && \mv tmp TRegGA.sample
# awk 'BEGIN {OFS=FS="|"} {gsub(/\s/,"",$3); print }' TRegGA.sample > tmp && \mv tmp TRegGA.sample

# To assign the first/third column as the sample names for TRegGA run
# SAMPLE=`cut -d"|" -f1 TRegGA.sample | awk 1 ORS=" "`
SAMPLE=`cut -d"|" -f3 TRegGA.sample | awk 1 ORS=" "`

# Edit TRegGA-Example.run and save as TRegGA-Xa7.run as described in TRegGA-Example.md
TARGET=OsjXa7
REFERENCE=OsjCHR6
FROM=27965001
TO=28023000

sh TRegGA-Xa7.run
sh runTRegGA_IRBB7-on-OsjXa7 &
sh runTRegGA_DV86-on-OsjXa7 &
sh runTRegGA_IRBB62-on-OsjXa7 &

# Modify TORQUE specific commands for mason, if needed
\cp PREREQ.sh PREREQ-mason.sh
grep -v "#PBS" PREREQ.sh | grep -v "module" | grep -v "PBS_O_WORKDIR" > tmp && \mv tmp PREREQ.sh
sed -i 's/qsub/sh/g;' PREREQ.sh
\cp x4-WGblat x4-WGblat-mason
grep -v "#PBS" x4-WGblat | grep -v "module" | grep -v "PBS_O_WORKDIR" > tmp && \mv tmp x4-WGblat
\cp x5-WGindelT x5-WGindelT-mason
grep -v "#PBS" x5-WGindelT | grep -v "module" | grep -v "PBS_O_WORKDIR" > tmp && \mv tmp x5-WGindelT
\cp x6-DFPtree x6-DFPtree-mason
grep -v "#PBS" x6-DFPtree | grep -v "module" | grep -v "PBS_O_WORKDIR" > tmp && \mv tmp x6-DFPtree

```

* 2. Setup haplovars for TRegGA improvement
```bash
cd ${TRegGA_DIR}/haplovars 
source ./0SOURCE
# include the TRegGA.source
# TRegGA_DIR=`dirname $PWD`
source ${TRegGA_DIR}/TRegGA.source
# copy the TRegGA.sample and rename for haplovars operation
\cp ${TRegGA_DIR}/TRegGA.sample sample.TRegGA
# Select/edit sample.TRegGA and save as sample.tofindbySNP for the cultivars to be subject to haplovars study
\cp sample.TRegGA sample.tofindbySNP
```

* 3. Prepare for haplovars identification of $SAMPLE in sample.tofindbySNP using SNP profiling with x1-WGvarSNP
```bash
cd ${run_DIR}
mkdir -p SNPs
cd SNPs
\cp ${WORK_DIR}/sample.tofindbySNP .
CULTIVAR=`cut -d"|" -f1 sample.tofindbySNP | awk 1 ORS=" "`
SYNONYM=`cut -d"|" -f3 sample.tofindbySNP | awk 1 ORS=" "`
SAMPLE=`cut -d"|" -f3 sample.tofindbySNP | awk 1 ORS=" "`

# (Optional) Retrieve SNP vcf files from SNP-Seek. Note that SNP-Seek uses $CULTIVAR naming format.
# wget ${VCF_DIR}/${CULTIVAR}.snp.vcf.gz

# (Optional) SNPs calling for cultivars using x1-WGvarSNP with reads processed by TRegGA
sh ${WORK_DIR}/x1-WGvarSNP
for i in $SAMPLE
    do qsub gatk_${i}-on-${REFSEQNAME}.qsub
    sed -i 's/^OsjChr//' ${i}_env_snp.vcf
done

# Modify REFERENCE in vcf file so that it is consistent with the SNP-Seek convention for chromosome name.
echo $REFERENCE > tmp
REFERENCE=`sed 's/OsjCHR//' tmp`

# (Optional) Restrict SNPs to the target region defined by TARGET, REFERENCE(chromosome), FROM, and TO in 0SOURCE of TRegGA
for file in ${SAMPLE}
do
grep -w "^$REFERENCE" ${file}_env_snp.vcf |\
awk -v from=${FROM} -v to=${TO} '{ if ( $2 >= from && $2 <= to ) print $0 }' > ${file}_env_snp_${TARGET}.vcf
done
```

* 4. Identify haplovars of $SAMPLE in sample.tofindbySNP based on SNP profiling with x2-findbySNP. This generates sample.foundbySNP.
```bash
cd ${WORK_DIR}
sh x2-findbySNP
```
### sample.foundbySNP
```
CX134|CX134|IRBB7|Indica
CX369|CX369|IRBB62|Indica
IRIS_313-10177|IRIS 313-10177|DA_GANG_ZHAN|Indica
IRIS_313-10605|IRIS 313-10605|DV86|Aus/boro
IRIS_313-10861|IRIS 313-10861|ARC_11276|Aus/boro
IRIS_313-10892|IRIS 313-10892|ARC_12920|Aus/boro
IRIS_313-10976|IRIS 313-10976|LAKHSMI_DIGHA|Aus/boro
IRIS_313-11051|IRIS 313-11051|AUS_242|Aus/boro
IRIS_313-11054|IRIS 313-11054|AUS_295|Aus/boro
IRIS_313-11057|IRIS 313-11057|AUS_308|Aus/boro
IRIS_313-11062|IRIS 313-11062|BEGUNBICHI_33|Basmati/sadri
IRIS_313-11064|IRIS 313-11064|BORO_275|Aus/boro
IRIS_313-11163|IRIS 313-11163|NATEL_BORO|Aus/boro
IRIS_313-11636|IRIS 313-11636|NCS271_A|Indica
```

* 5. Denovo assemble contigs of $SAMPLE in sample.foundbySNP for haplovars identification with x3-TRegGA-denovo
```bash
# run TRegGA with modified Makefile_denovo-orig to run only contig, skip QUAST, and skip GapFiller.
# asm_flags  =      1#  1(only contig assembly), 2 (only scaffold assembly), 3(both contig and scaffold assembly), 4 (only gap closure).
# QTO-t =     0#  Maximum number of threads; set to 0 to not run QUAST
# GFO-i     =       0#  maximum number of iterations; set to 0 to not run GapFiller
\cp ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig-orig
sed -i 's/asm_flags  =      3#/asm_flags  =      1#/;' ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig
sed -i 's/QTO-t =     NUMPROC#/QTO-t =     0#/;' ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig
sed -i 's/GFO-i     =       3#/GFO-i     =       0#/;' ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig

# Replace TRegGA.sample with sample.foundbySNP, then run x3-TRegGA-denovo with modified Makefile_denovo-orig
cd ${WORK_DIR}
\cp ${run_DIR}/findbySNP/sample.foundbySNP TRegGA.sample
sh x3-TRegGA-denovo
\cp runTRegGA_${SYNONYM}-denovo ${TRegGA_DIR}
cd ${TRegGA_DIR}
SYNONYM=`cut -d"|" -f3 ${WORK_DIR}/sample.foundbySNP | awk 1 ORS=" "`
for i in $SYNONYM
do sh runTRegGA_${SYNONYM}-denovo
done

# Revert the modified Makefile_denovo-orig back to original
\mv ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig-orig ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig
```
	   
* 6. Finding Deletion Fingerprints (DFPs) of $SAMPLE in sample.foundbySNP with x4-WGblat and x5-WGindelT.
```bash
# Assign $VARNAME (the third column) in sample.foundbySNP as the sample names
cd ${WORK_DIR}
sh ${WORK_DIR}/x4-WGblat &&\
sh ${WORK_DIR}/x5-WGindelT &&\
```

* 7. Identify haplovars of $SAMPLE in sample.foundbySNP based on DFPs with x6-DFPtree. This generates distance matrix Seq.t_sum_Lg${GAP_MINSIZE_FP}.dmx.
```bash
sh ${WORK_DIR}/x6-DFPtree
```
#### DMX
```
        NATEL_BORO      BORO_275        NCS271_A        IRBB62  LAKHSMI_DIGHA   AUS_295 AUS_242 ARC_11276       DA_GANG_ZHAN    DV86    BEGUNBICHI_33   AUS_308 IRBB7   ARC_12920
NATEL_BORO      0.00    0.33    0.44    0.44    0.44    0.56    0.56    0.56    0.56    0.56    0.56    0.67    0.67    0.67
BORO_275        0.33    0.00    0.11    0.11    0.11    0.22    0.22    0.22    0.22    0.22    0.22    0.33    0.33    0.33
NCS271_A        0.44    0.11    0.00    0.22    0.22    0.33    0.33    0.33    0.33    0.33    0.33    0.44    0.44    0.44
IRBB62  0.44    0.11    0.22    0.00    0.00    0.11    0.11    0.11    0.11    0.11    0.33    0.22    0.22    0.22
LAKHSMI_DIGHA   0.44    0.11    0.22    0.00    0.00    0.11    0.11    0.11    0.11    0.11    0.33    0.22    0.22    0.22
AUS_295 0.56    0.22    0.33    0.11    0.11    0.00    0.00    0.00    0.00    0.00    0.22    0.11    0.11    0.11
AUS_242 0.56    0.22    0.33    0.11    0.11    0.00    0.00    0.00    0.00    0.00    0.22    0.11    0.11    0.11
ARC_11276       0.56    0.22    0.33    0.11    0.11    0.00    0.00    0.00    0.00    0.00    0.22    0.11    0.11    0.11
DA_GANG_ZHAN    0.56    0.22    0.33    0.11    0.11    0.00    0.00    0.00    0.00    0.00    0.22    0.11    0.11    0.11
DV86    0.56    0.22    0.33    0.11    0.11    0.00    0.00    0.00    0.00    0.00    0.22    0.11    0.11    0.11
BEGUNBICHI_33   0.56    0.22    0.33    0.33    0.33    0.22    0.22    0.22    0.22    0.22    0.00    0.11    0.11    0.11
AUS_308 0.67    0.33    0.44    0.22    0.22    0.11    0.11    0.11    0.11    0.11    0.11    0.00    0.00    0.00
IRBB7   0.67    0.33    0.44    0.22    0.22    0.11    0.11    0.11    0.11    0.11    0.11    0.00    0.00    0.00
ARC_12920       0.67    0.33    0.44    0.22    0.22    0.11    0.11    0.11    0.11    0.11    0.11    0.00    0.00    0.00
```

* 8. Construct of supercontigs of $SAMPLE in sample.foundbyDFP with x7-TRegGA-rfguided
```bash
# Combine IRBB7, AUS_308, ARC_12920 to assemble supercontigs
cd ${WORK_DIR}
\rm -f sample.foundbyDFP
SAMPLE_foundbyDFP="IRBB7 AUS_308 ARC_12920"
for i in $SAMPLE_foundbyDFP
do grep "$i" sample.foundbySNP >> sample.foundbyDFP
done

# sample.foundbyDFP
# CX134|CX134|IRBB7|Indica
# IRIS_313-11057|IRIS 313-11057|AUS_308|Aus/boro
# IRIS_313-10892|IRIS 313-10892|ARC_12920|Aus/boro

# Replace TRegGA.sample with sample.foundbyDFP, abd create virtual reads for supercontig process
\cp sample.foundbyDFP TRegGA.sample
SYNONYM=`cut -d"|" -f3 ${WORK_DIR}/TRegGA.sample | awk 1 ORS=" "`
cd ${TRegGA_DIR}/reads
mkdir -p ${SAMPLENAME}
cd ${SAMPLENAME}
\rm -r ${SAMPLENAME}*.fq
for i in ${SYNONYM}
do
ln -s ${TRegGA_DIR}/reads/${i}/${i}_1.fq
ln -s ${TRegGA_DIR}/reads/${i}/${i}_2.fq
cat ${i}_1.fq >> ${SAMPLENAME}_1.fq
cat ${i}_2.fq >> ${SAMPLENAME}_2.fq
done

# run TRegGA with modified Makefile_denovo-orig to run using rice_japonica as REFERENCE
\cp ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig-orig
sed -i 's/REFERENCE            = rice_indica/#REFERENCE            = rice_indica/;' ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig
sed -i 's/#REFERENCE            = rice_japonica/REFERENCE            = rice_japonica/;' ${TRegGA_DIR}/assembly/denovo/Makefile_denovo-orig
# edit on Makefile_denovo-orig
else ifeq ($(REFERENCE), rice_japonica)
        REF_DIR            =  ${TRegGA_DIR}/reference/${REFERENCE}
        TARGET_SEQ         =  ${REF_DIR}/OsjCHR.fa
        TARGET_GFF         =  ${REF_DIR}/OsjCHR.gff3

# Run x7-TRegGA-rfguided
CULTIVAR="${SAMPLENAME}"
SYNONYM="${SAMPLENAME}"
sh x7-TRegGA-rfguided
# Modify TORQUE specific commands for mason, if needed
grep -v "#PBS" runTRegGA_${SYNONYM}-on-${TARGET} | grep -v "module" | grep -v "PBS_O_WORKDIR" > tmp && \mv tmp runTRegGA_${SYNONYM}-on-${TARGET}

\cp runTRegGA_${SYNONYM}-on-${TARGET} ${TRegGA_DIR}
cd ${TRegGA_DIR}

sh runTRegGA_${SYNONYM}-on-${TARGET}

```


* 10. Report back to haplovars
```bash
\cp *.haplovar ${data_DIR)
```


## REFERENCE:
* [2] Xia Chun, Chen H, Zhu X. Identification, Mapping, Isolation of the Genes Resisting to Bacterial Blight and Breeding Application in Rice. Molecular Plant Breeding. 2012;3(12)121-131.
* [3] Khan, MueenAlam. Molecular breeding of rice for improved disease resistance, a review. Australasian Plant Pathology. 2015 May 1;44(3):273-282.
* [4] Iyer AS, McCouch SR. The rice bacterial blight resistance gene xa5 encodes a novel form of disease resistance. Mol Plant Microbe Interact. 2004 Dec;17(12):1348-54.
* [5] Le Cam Loan, Vo Thi Thu Ngan, and Pham Van Du. Preliminary Evaluation on Resistance Genes Against Rice Bacterial Leaf Blight In Can Tho Province - Vietnam. Omonrice 14 44-47 (2006).
* [6] Yuchen Zhang et al. Identification and molecular mapping of the rice bacterial blight resistance gene allelic to Xa7 from an elite restorer line Zhenhui 084. Eur J Plant Pathol (2009) 125:235–244

