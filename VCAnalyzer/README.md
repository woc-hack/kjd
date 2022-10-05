<!--todo: define blob, define original project vs cloned project
phases allow replacing a phase, for example, to get a different (maybe better)
list of vulnerable projects or to get more accurate idea of when a vulnerability was introduced
do i need more implementation details (for replication)
-->

# VCAnalyzer (Vulnerable Clones Analyzer)

VCAnalyzer is a tool to analyze vulnerabilities that are propagated
through copy-based code reuse. The tool reads a list of information
about known vulnerabilities in open source projects, it finds 
other projects which have cloned the vulnerable file, and then it
produces statistics about those projects with the cloned vulnerable file.

Run VCAnalyzer from the command line with the following usage:
- usage: vca <output directory> <input data file>

  See the description below for full details of the input file format. 


## Input

The input to the tool is a .csv (common separated values) file containing 
information about a vulnerability as defined in the CVE list at cve.org. 
The input file contains one line per vulnerability with the following fields:
  - CVE ID (example: CVE-2007-6761)
  - Commit that fixed the vulnerability (sha1 hash of the commit)
  - Project (URL for the project listed in the CVE Record)
  - File (The full pathname of the affected file within the project) 
  - Date the vulnerability was fixed
  - Date the CVE Record was created

Here is an example input line:
  
CVE-2022-34299,7ef09e1fc9ba07653dd078edb2408631c7969162,http&#8203;s://github.com/davea42/libdwarf-code,src/lib/libdwarf/dwarf_form.c,2022-06-15 14:46:01-07:00,2022-06-23T17:15Z

## Output
The output of the tool is a .csv file with one line for each project that
had copied a vulnerable file for a particular CVE ID.

The output records contain the following fields:
  - CVE ID
  - Project URL
  - Project Name (in the format used by WoC)
  - status (fixed, notfixed, or unknown)
  - 1stBadBlob (sha1 hash of the first vulnerable blob committed to the project)
  - 1stBadTime (Time 1stBadBlob was committed in unix time format)
  - 1stGoodBlob (sha1 hash of the first fixed blob committed to the project)
  - 1stGoodTime (Time 1stGoodBlob was committed in unix time format)
  - TimeSinceFix (Time between fix in original project and fix in clone)
  - TimeSinceFixF (TimeSinceFix formatted to be human readable)
  - TimeSincePub (Time between CVE publication and fix in clone)
  - TimeSincePubF (TimeSincePub formatted to be human readable))
  - NumAuthors (Number of authors)
  - EarliestCommitDate (Date of earliest commit in unix time format)
  - LatestCommitDate (Date of latest commit in unix time format)
  - NumActiveMon ()
  - RootFork  ()
  - NumStars (The number of stars as reported by WoC. Github projects only)
  - NumCore ()
  - CommunitySize ()
  - NumCommits (Number of Commits as reported by WoC)
  - NumForks (Number of forks)
  - NumAuthors (Number of Authors)
  - FileInfo (The most used language in this project)

Here is an example line from the final output file:
  
CVE:CVE-2002-2443, ProjectUrl:github.com/eurolinux-enterprise-linux-sources/krb5, Project:eurolinux-enterprise-linux-sources_krb5, status:fixed, 1stBadBlob:f0b9a295b5eee43a73d103f81dabfaa8dfc8da36, 1stBadTime:1578606599, 1stGoodBlob:63c6ddb376f0d04c9bbb8b36413cda390d8b49a1, 1stGoodTime:1578634380, TimeSinceFix:2432, TimeSinceFixF:6 years and 66 days, TimeSincePub:2416, TimeSincePubF: 6 years and 61 days, NumAuthors:1, EarliestCommitDate:1578575615, LatestCommitDate:1578634769, NumActiveMon:1, RootFork:-, NumStars:-, NumCore:1, CommunitySize:1, NumCommits:11, NumForks:0, NumAuthors:1, EarliestCommitDate:1578575615, FileInfo:C/C++

## Architecture

VCAnalyzer is layered on top the of the World of Code infrastructure.
World of Code contains a nearly complete collection of open source software.
It includes software from many git repository hosting platforms such as
github, gitlab, and bitbucket. VCAnalyzer also utilizes the APIs from those
hosting platforms to get the most up-to-date versions of files.

The tool is divided into 4 phases:
  
### Phase 1
Phase 1 creates a list of vulnerable blobs and fixed blobs in the 
original project.

The input for phase 1, for each CVE, is:
    - The CVE ID
    - The project name
    - The file path of the vulnerable file 
    - The sha1 hash of the fixing commit

For each CVE ID from the input file, the tool:
    - Finds the blobs that were committed before the fixing commit. These are
      the potentially vulnerable blobs.
    - Finds the blob in the fixing commit and all later blobs. These are the
      presumably fixed blobs.
    - Finds blobs that are in both lists. These are likely cases where a fix
      was later reverted to an older version, possibly because the fix 
      introduced a worse problem. 
    - Finds cases where the fixing commit is not connected to the HEAD
      commit. In these cases, the tool does not know which blobs are
      vulnerable and which are fixed, so it skips these cases.

The output from phase 1, for each CVE, is:
    - A list of all of the potentially vulnerable blobs in files named
      bad_blobs.txt.
    - A list of all of the presumably fixed blobs in files named 
      good_blobs.txt.
    - A list of blobs common to the good and bad lists in files named 
      comm_blobs.txt)

### Phase 2
Phase 2 finds all projects in WoC that have at some time contained
the vulnerable file. These are the cloned project. It then discovers 
if each cloned project has been fixed and, if so, the time of the fix.

The input for phase 2 is the lists of good blobs and bad blobs generated in 
phase 1 for each CVE from the input file.

For each CVE from phase 1, the tool:
    - Finds all open source projects available in World of Code that have 
      cloned the vulnerable file.
    - For each cloned project, determines if the vulnerable file:
           1. Has been fixed.
           2. Has not been fixed it.
           3. Has changed, but we don't know the change fixed the vulnerability.
    - Find the date of the first commit of a known vulnerable file.
    - For each fixed project, find the date of the first commit of a known
      fixed file.

The output from phase 2, for each CVE, is:
    - Lists of cloned  projects that are fixed, still vulnerable, or unknown.
    - Time the first potentially vulnerable file was committed in the cloned
      projects.
    - For fixed projects, time the first known fixed file was committed.
    - Length of time elapsed between time the CVE was published and the
      first fixing commit for each cloned project.
    - Length of time elapsed between time the vulnerability was fixed
      in the original project and the time of the first fixing commit in

### Phase 3
Phase 3 finds statistics about each project. 

The input to phase 3 is the list of cloned projects and the data produced from
phase 2.

For each project, the tool retrieves statistics from either World of Code or
from the repository hosting platform. In most cases, the statistics
are available from World of Code. In a few cases, the tool uses the API of the
repository hosting platform to get the information directly fro the platform.

The output of phase 3 includes the output of phase 2 and the following 
additional information about each cloned project:
  - Number of authors
  - Date of earliest commit 
  - Date of latest commit
  - NumActiveMon
  - Root Fork
  - The number of stars as reported by WoC
  - NumCore
  - CommunitySize
  - Number of Commits as reported by WoC
  - Number of forks
  - Number of Authors
  - The most used language in this project

### Phase 4
Phase 4 Analyzes the results (not implemented yet)


