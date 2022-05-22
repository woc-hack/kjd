# Process

The process of data gathering constist of the following steps: 
1. Get data on vulnerability fixes (cve, commit, file path, author date, vulnerabilty date)
2. Join vulnerability data with WoC blobs: c2fbb (cve, commit, file path, author date, vulnerabilty date, path name in WoC, fixed blob, vulnerable blob)
3. Filter data on matching file path
4. For each vulnerable blob find all previous blobs
5. For each found blob match it to commits in other projects, get earliest date
6. For ech fixing blob match it to commits in other projects, get earliest date
7. Match result file with vulnerable projects to result file with fixed projects
8. For each project with vulnerable blob and fixed blob calculate time delta

## 1. Get data on vulnerability fixes (cve, commit, file path, author date, vulnerabilty date)

Data is downloaded from https://github.com/secureIT-project/CVEfixes and read into an sqllite database. The database contains information on vulnerabilities and their fixing commits. Additionally fixing commits are connected to file changes.

Data is queried with the following query: 
_TODO: add query_

## 2. Join vulnerability data with WoC blobs: c2fbb (cve, commit, file path, author date, vulnerabilty date, path name in WoC, fixed blob, vulnerable blob)

Data from CVEfixes is merged with WoC data throufh the c2fbb relationships. The c2fbb relationships matches commits to the connected blobs, the corresponding files and the previous blog. The result is a file containing commits, file names, vulnerable blobs and fixed blobs for each vulnerability. 

CVEfixes is first sorted

     sort data/cvefixes.csv -t \; -k 2 > cvefixes-sorted.csv
     
Then it is joinded with the c2fbb table: 

     join cvefixes-sorted.csv  -1 2 -2 1 -t \; <( zcat /da5_data/basemaps/gz/c2fbbFullU0.s ) >> results/join2.csv
     
_TODO: this should run over all 128 c2fbb files_

## 3. Filter data on matching file path



## 4. For each vulnerable blob find all previous blobs

## 5. For each found blob match it to commits in other projects, get earliest date

## 6. For ech fixing blob match it to commits in other projects, get earliest date

## 7. Match result file with vulnerable projects to result file with fixed projects

## 8. For each project with vulnerable blob and fixed blob calculate time delta
