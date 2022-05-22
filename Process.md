#Process

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

## 2. Join vulnerability data with WoC blobs: c2fbb (cve, commit, file path, author date, vulnerabilty date, path name in WoC, fixed blob, vulnerable blob)

## 3. Filter data on matching file path

## 4. For each vulnerable blob find all previous blobs

## 5. For each found blob match it to commits in other projects, get earliest date

## 6. For ech fixing blob match it to commits in other projects, get earliest date

## 7. Match result file with vulnerable projects to result file with fixed projects

## 8. For each project with vulnerable blob and fixed blob calculate time delta
