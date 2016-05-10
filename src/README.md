## *src/* directory contains prerequisite softwares:
- TRegGA
- plink
- Anaconda2
- Python package Pyvcf
- Python package Biopython
- Blat
- Blast+

ThaRegGA is implemented as a collection of shell scripts and ancillary Python codes, so no compilation is required. However, the workflow depends on several third-party programs, and many of which do require compiling and/or additional configuration for your particular system. Please see the cited URLs below for details on the software installation. *src/* is assumed for the installation path, but should be replaced with the actual path.

For IU Mason cluster users, the prerequisite softwares can be loaded from the system:
- module add blat/35

### bin/
* add bin/ to PYTHONPATH
echo '# PYTHONPATH added by haplovar/bin
export PYTHONPATH="$PYTHONPATH:/projects/huangcy/MYGIT/TRegGA/haplovars/bin"
' | cat ~/.bashrc - > tmp && mv tmp ~/.bashrc
source ~/.bashrc

### TRegGA
* See https://github.com/huangc/TRegGA
* Last update: April 2016
* Step-by-step setup at: ${GIT_DIR}/TRegGA/TRegGA-Example.md
```bash
cd ${GIT_DIR}
git clone https://github.com/huangc/TRegGA.git

```

### Plink
* See http://pngu.mgh.harvard.edu/~purcell/plink
* Last update: May 2014
```bash
cd ${src_DIR}
mkdir plink
cd plink
wget https://www.cog-genomics.org/static/bin/plink160416/plink_linux_x86_64.zip
unzip plink_linux_x86_64.zip
export PATH=$PATH:${src_DIR}/plink

```

### Anaconda2
* See https://docs.continuum.io/anaconda
* Last update: Apr. 2016
* numpy, scipy, matplotlib and pandas are required python packages for /bin/DFPtree.py.
* Choose PYTHON 2 instead of PYTHON 3 version to be compatible with the python codes in rice3k.
```bash
cd ${src_DIR}
mkdir anaconda2
cd anaconda2
# download the installer from https://www.continuum.io/downloads
bash Anaconda2-4.0.0-Linux-x86_64.sh
# Add anaconda2 to PATH
echo '# PATH added by anaconda2
export PATH="/home/huangcy/src/anaconda2/bin:$PATH"
' | cat ~/.bashrc - > tmp && mv tmp ~/.bashrc
# Add anaconda2 to PYTHONPATH
echo '# PYTHONPATH added by anaconda2
export PYTHONPATH="$PYTHONPATH:/home/huangcy/src/anaconda2/lib/python2.7/site-packages"
' | cat ~/.bashrc - > tmp && mv tmp ~/.bashrc
source ~/.bashrc

```

### Python package Pyvcf
* See http://pyvcf.readthedocs.io/en/latest/
```bash
pip install pyvcf

```

### Python package Biopython
* See http://biopython.org/wiki/Biopython
```bash
pip install biopython

```

### Blat
* See https://genome.ucsc.edu/FAQ/FAQblat.html.
* Last update: Dec. 2014
```bash
cd ${src_DIR}
mkdir blatSuite
cd blatSuite
wget http://hgwdev.cse.ucsc.edu/~kent/exe/linux/blatSuite.zip
unzip blatSuite.zip
export PATH=$PATH:${src_DIR}/blatSuite

```

### Blast+
* See https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download.
* Last update: Dec. 2015
```bash
cd ${src_DIR}
mkdir blast
cd blast
wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.3.0/ncbi-blast-2.3.0+-x64-linux.tar.gz
tar -xzf ncbi-blast-2.3.0+-x64-linux.tar.gz
export PATH=$PATH:${src_DIR}/blast//ncbi-blast-2.3.0+/bin

```
