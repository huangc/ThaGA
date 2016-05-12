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
* 1. TRegGA run on Xa7 related cultivars
```bash
cd ${TRegGA_DIR}
# edit TRegGA.sample
# CX134|IRBB7
# IRIS 313-10605|DV86
# CX369|IRBB62

# edit TRegGA-Example.run and save as TRegGA-Xa7.run
# TARGET=OsjXa7
# REFERENCE=OsjCHR6
# FROM=27965001
# TO=28023000

sh TRegGA-Xa7.run
# edit to be run in shell as described in TRegGA-Example.md and then, 
sh runTRegGA_IRBB7-on-OsjXa7 &
sh runTRegGA_DV86-on-OsjXa7 &
sh runTRegGA_IRBB62-on-OsjXa7 &
```

* 2. prepare for haplovars run
```bash
cd haplovars
# edit 0SOURCE
source 0SOURCE
# include the TRegGA.source
TRegGA_DIR=`dirname $PWD`
source ${TRegGA_DIR}/TRegGA.source
\cp ${TRegGA_DIR}/TRegGA.sample .

# retrieve SNPs for IRBB7
cd ${run_DIR}
mkdir -p SNPs
cd SNPs
\cp ../TRegGA.sample .
len=`awk 'END { print NR }' TRegGA.sample`
for ((k=1; k<=$len; k++))
do
head -$k TRegGA.sample | tail -1 > rec
CULTIVAR=`cut -d "|" -f1 rec`
SYNONYM=`cut -d "|" -f2 rec`
# retrieve SNP vcf files from SNP-Seek
wget ${VCF_DIR}/${CULTIVAR}.snp.vcf.gz

# Alternatively, run x1-WGvarSNP with reads for SNPs
    do ln -s ${SNP_DIR}/gatk_${file}_env_snp.vcf .
	sed -i 's/^OsjChr//' gatk_${file}_env_snp.vcf
done

# Restrict SNPs to the target region defined by TARGET, REFERENCE, FROM, and TO in 0SOURCE of TRegGA, such as:
# TARGET=OsjSWEET13
# REFERENCE=OsjCHR12
# FROM=17292001
# TO=17315000
# Modify REFERENCE so that it is consistent with the SNP-Seek convention for chromosome name.
echo $REFERENCE > tmp
REFERENCE=`sed 's/OsjCHR//' tmp`
for file in ${SAMPLE}
do
grep -w "^$REFERENCE" gatk_${file}_env_snp.vcf |\
awk -v from=${FROM} -v to=${TO} '{ if ( $2 >= from && $2 <= to ) print $0 }' > gatk_${file}_env_snp_${TARGET}.vcf
done











```







## REFERENCE:
* [2] Xia Chun, Chen H, Zhu X. Identification, Mapping, Isolation of the Genes Resisting to Bacterial Blight and Breeding Application in Rice. Molecular Plant Breeding. 2012;3(12)121-131.
* [3] Khan, MueenAlam. Molecular breeding of rice for improved disease resistance, a review. Australasian Plant Pathology. 2015 May 1;44(3):273-282.
* [4] Iyer AS, McCouch SR. The rice bacterial blight resistance gene xa5 encodes a novel form of disease resistance. Mol Plant Microbe Interact. 2004 Dec;17(12):1348-54.
* [5] Le Cam Loan, Vo Thi Thu Ngan, and Pham Van Du. Preliminary Evaluation on Resistance Genes Against Rice Bacterial Leaf Blight In Can Tho Province - Vietnam. Omonrice 14 44-47 (2006).
* [6] Yuchen Zhang et al. Identification and molecular mapping of the rice bacterial blight resistance gene allelic to Xa7 from an elite restorer line Zhenhui 084. Eur J Plant Pathol (2009) 125:235–244

