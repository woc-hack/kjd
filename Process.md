# Process

The process of data gathering consists of the following steps: 

  1. Get data on vulnerability fixes (CVE identifier, commit hash, path of file that fixed vulnerability, author commit date, vulnerability publication date).
  2. Join vulnerability data with WoC blobs: c2fbb (CVE identifier, commit hash, path of file that fixed vulnerability, author date, vulnerability publication date, path of file in WoC, fixed blob, previous vulnerable blob).
  3. Filter data on matching file path.
  4. For each vulnerable blob find all previous blobs.
  5. For each found blob match it to commits in other projects, get earliest date.
  6. For each fixing blob match it to commits in other projects, get earliest date.
  7. Match result file with vulnerable projects to result file with fixed projects.
  8. For each project with vulnerable blob and fixed blob calculate time delta.

# Process Step Details

## 1. Get data on vulnerability fixes (CVE, commit, file path, author date, vulnerability date)

Data is downloaded from https://github.com/secureIT-project/CVEfixes and read into an SQLlite3 database. The database contains information on vulnerabilities and their fixing commits. Data is extracted into a CSV file `data/cvefixes.csv` by the script `extract-cvefixes-data.py`.

## 2. Join vulnerability data with WoC blobs: c2fbb (CVE, commit, file path, author date, vulnerability date, path name in WoC, fixed blob, vulnerable blob)

Data from CVEfixes is merged with WoC data through the c2fbb relationships. The c2fbb relationships matches commits to the connected blobs, the corresponding files and the previous blog. The result is a file containing commits, file names, vulnerable blobs and fixed blobs for each vulnerability. 

CVEfixes is first sorted

     sort data/cvefixes.csv -t \; -k 2 > cvefixes-sorted.csv
     
Then it is joined with the c2fbb table: 

     join cvefixes-sorted.csv  -1 2 -2 1 -t \; <( zcat /da5_data/basemaps/gz/c2fbbFullU0.s ) >> results/join2.csv
     
__TODO:__ Post-hackathon, we should modify this to run over all (up to 128) c2fbb map files instead of just one to get all the matches. During the hackathon, we only have time to examine a few projects, so this does not matter.

## 3. Filter data on matching file path

Data is filtered by file path matching all rows where file path from CVEfixes matches the file path from WoC. This way all rows are filtered out where the commit was matched to a blob corresponding to some unrelated file change. 

     awk -F\; '$3 == $6' results/join2.csv > results/filtered.csv

## 4. For each vulnerable blob find all previous blobs

## 5. For each found blob match it to commits in other projects, get earliest date

## 6. For ech fixing blob match it to commits in other projects, get earliest date

## 7. Match result file with vulnerable projects to result file with fixed projects

## 8. For each project with vulnerable blob and fixed blob calculate time delta

First extract data from result files into a .csv file: 

    ./extract_results.sh out2 > cve_analysis_output.csv
    
The data is expected to be in the following folders

 * CVE-xx-yy
   * project_name1_bad_sorted.txt
   * project_name1_good_sorted.txt
   * project_name2_bad_sorted.txt
   * project_name2_good_sorted.txt
 * CVE-zz-aa
   * project_name2_bad_sorted.txt
   * project_name2_good_sorted.txt

The script extract_results.sh first extracts CVE numbers, then for each CVE number the project names that contain both the fix and the vulnerability. Then the script reads in the first good and the first bad commmit and outputs data on the CVE, project, fix commit, vulnerable commit and commit times. 

Output is in the format: 

    CVE-2010-5331;0Litost0_linux_kernel_2.6_ver_1;c83efad97b90134cb7db6fd76145b6151502d44f;c83efad97b90134cb7db6fd76145b6151502d44f;2016-10-12:23:03:17;2016-10-12:23:03:17
    CVE-2010-5331;0Litost0_test_1;4ce4402851dece658921ec92ba8b97a7b5843017;4ce4402851dece658921ec92ba8b97a7b5843017;2017-04-24:01:36:41;2017-04-24:01:36:41

Next the result file can be joined with the original vulnerability data file: 

    join -t \; data/cve_analysis_output.csv data/cvefixes.csv > data/cve_analysis_joined.csv
   
This join adds data on the original project, file name and on the vulnerability release date. 

Last it is necessary to
* calculate max (bad commit time, vulnerability release time) which will be the vulnerability introduction time
* calculate diff between the vulnerability introduction time and the vulnerability fix time 
