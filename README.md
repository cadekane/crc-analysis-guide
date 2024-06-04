# crc-analysis-guide
A documentation of my process of taking whole genome/exome colorectal cancer (CRC) data in the form of fastq files, processing them into mutation annotation format (.maf) files, and analyzing the mutation data.

# DNAseq Pipeline
The GATK pipeline variant (I'll call it the pipeline) is run on the Arashi Linux server. However, to streamline the execution of the pipeline, a Jupyter Notebook was used to maintain the various necessary commands. A more detailed description can be found elsewhere, but the basic outline entails:

0. Preparing input files: this step can be taxing and overwhelming. 
1. SCMA: this step is short.
2. Pre-Processing: this is the longest step.
3. Panel of Normals (PoN): this step may also take a long time.
4. Mutect2: this step is longer than SCMA but shorter than PoN.
5. Aggregating MAFs: this step is short.

The pipeline is run using Oliver-Cromwell, which requires installation via conda environment. In fact, the entire pipeline must be run using a conda environment. There is an example Jupyter Notebook in this GitHub repository that contains Python/bash code to accomplish steps 0 through 5 of the pipeline. It speeds up the process, but be vigilant in checking that the path and name variables being passed to various commands are appropriate/correct.

## Preparing Your Pipeline Repository
The pipeline requires many folders/repositories for input and output. CRC data is more complicated than other cancer data because several fastqs are generated for a single sample/patient. Due to limited resources, this necessitates us to do the Pre-Processing in batches of 3 samples. PoN requires ALL pre-processed outputs (Normal .bam files). And Mutect2 should also be run in batches.

### Repository Substructure
Here is a depiction of the repository substructure I use, which can be trivially generated using the following bash code.


## 0. Preparing input files
This is extremely important to get right. Preparing the input files incorrectly will lead to immense trouble/grief/confusion later down the pipeline. 

### CSV containing sample metadata
I created a python script to generate this CSV.

#### Input:
- path to a directory containing directories that each represent one sample (SAMPLENAME_TA or SAMPLENAME_NA). Within these inner directories should be the corresponding fastq files.

An example of the parent directory whose path you would use as input:
```
/path/to/parent_directory
    ├── DCR0003_NA
    │   ├── V350083339_L01_B5GHUMxlydRAABA-525_1.fq.gz
    │   ├── V350083339_L01_B5GHUMxlydRAABA-525_2.fq.gz
    │   └── ...
    ├── DCR0004_TA
    │   ├── V350083340_L01_B5GHUMxlydRAABA-526_1.fq.gz
    │   ├── V350083340_L01_B5GHUMxlydRAABA-526_2.fq.gz
    │   └── ...
    └── ...

```

#### Output:
- a csv containing the necessary metadata and pathing for each sample.
- this script is specific for CRC data because there are multiple fastqs generated for a single sample, which requires a row for each pair of fastqs.

The script and an example output is included in the `preparing-input-files` directory. 

### Python Script and Config.ini
The input files for each step are generated all at once by a Python script. You must manually create a Config.ini file with the specified information:
- Group name

- Interval file: whole genome or whole exome sequencing? This is very important to specify, and it will affect the size of your ultimate MAF file. 

An example is included in this GitHub repository.

After running the script, it is necessary to move files to their correct places. This is trivially done with the following code: 
- I want to fix the script so I do not have to do this, but it might be non-trivial. We will see…

Here is a depiction of how the repository substructure will look after preparing the input files for the pipeline:

## 1. SCMA
This step is simple and short. The input file includes…

## 2. Pre-Processing
Pre-processing is the most tedious step because each batch must be run one at a time, and therefore you must return each time to pre-process each 3-batch of samples. 

The input file…

Given `n` paired samples (`n` Normal samples and `n` Tumor samples), you should ultimately generate `n` Normal .bam files and `n` Tumor .bam files.

### Error Handling for Pre-Processing
Common sources of failure include:
- High resource usage: 
- Not enough memory allocation (?)
- Incorrect path specification: this could indicate a deeper issue with how you set up the Congig.ini file and generated the input files.

## 3. PoN
Panel of Normals only requires the Normal .bam files. There should be only **ONE** input file, called `pon.json`. In my experience, the most relevant parts of the file to check are:
- "Mutect2_Panel.normal_bams": this should contain the paths to EVERY Normal .bam file.
- "Mutect2_Panel.scatter_count": 
- "Mutect2_Panel.intervals"
- "Mutect2_Panel.Mutect2.filter_mem"

An example is included in this GitHub repository. 


### Error Handling for PoN
- Not enough memory allocation: This has happened to me while running PoN for 10 samples.

## 4. Mutect2
At this point, the hardest work is over. Mutect2 should be run in batches of 3, similar to Pre-Processing. Each sample will have its own MAF file.

### Error Handling for Mutect2
- Not enough memory allocation:

## 5. Aggregating MAFs
This step is very simple.

# Analyzing MAF Files
There are many ways we analyze MAF files. Below are the methods I have worked on thus far. 

## Tumor Mutational Burden (TMB)
Tumor mutational burden is…

## Identifying Driver Genes with MutSig2CV
Driver genes are 

## Maftools (an R package) for in-depth MAF file analysis
maftools has a plethora of methods for quickly analyzing MAF files. 