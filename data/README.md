# Data Files

  - `cvefixes.csv` Data about vulnerability fixing commits extracted from the CVEfixes dataset at https://github.com/secureIT-project/CVEfixes
  - `test_data1.csv` Subset of WoC vulnerability data created by script TBD. The fields are:
    - Commit hash for commit that fixed vulnerability
    - Pathname of file in which vulnerability was fixed
    - Blob containing the fixed file
    - Old blob containing the vulnerability file before the fix
    - WoC project name
    - WoC project name
    - Tree identifier
    - Hash of parent of vulnerability fixing commit
    - Commit author with email
    - Commit author with email
    - Time (which?)
    - Time (which?)
    - TZ
    - TZ
    - Commit message for vulnerability fixing commit

# Data Files in kjd-tmp repository

Files in https://github.com/woc-hack/kjd-tmp/ are organized into directories with names of the form `outN` where `N` is an integer starting at 1. The data collection process is parallelized into `N` threads, each creating its own directory for its part of the work.

Each `outN` directory contains a set of directories named after the CVEs processed by that thread. In each CVE directory, there are three types of output files in two formats: csv and html. The files are

  - `results.fixed` contains commits where the vulnerability has been fixed.
  - `results.notfixed` contains commits where vulnerability is not fixed.
  - `results.unknown` contains commits where the file is changed since the vulnerability was introduced but the file does not match the fixed file from the original repository.
