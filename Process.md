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
