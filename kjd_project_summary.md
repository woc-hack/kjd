# KJD: Vulnerability Lifespan Across Projects

**Kristiina Rahkema**, *Estonia*
**James Walden**, *Northern Kentucky University, USA*
**David Reid**, *University of Tennessee, USA*

**Abstract:** Please provide a short summary of your project here.

**Link:** N/A

### 1. Introduction

The goal of the project is to study vulnerability duration across projects. Since files are often copied across projects, vulnerable code can migrate from one project to another. However, vulnerability fixes may not propagate to all projects where the vulnerable code was copied. We are studying how long it takes for the same vulnerable code to be fixed across multiple projects. 


### 2. Methodology

The process of data gathering consists of the following steps: 

  1. Get data on vulnerability fixes (CVE identifier, commit hash, path of file that fixed vulnerability, author commit date, vulnerability publication date).
  2. Join vulnerability data with WoC blobs: c2fbb (CVE identifier, commit hash, path of file that fixed vulnerability, author date, vulnerability publication date, path of file in WoC, fixed blob, previous vulnerable blob).
  3. Filter data on matching file path.
  4. For each vulnerable blob find all previous blobs.
  5. For each found blob match it to commits in other projects, get earliest date.
  6. For each fixing blob match it to commits in other projects, get earliest date.
  7. Match result file with vulnerable projects to result file with fixed projects.
  8. For each project with vulnerable blob and fixed blob calculate time delta to find the vulnerability lifespan in that project.
  9. Overall vulnerability lifespan is the maximum lifespan across projects.

### 3. Preliminary Findings
Please describe your preliminary findings here.

### 4. Challenges
Please describe difficulties you encountered during the project related to World of Code. If possible, please also make suggestions on how you think they could be solved.

### 5. Future Work

  1. Include projects which have vulnerabilities but no fixes. Use survival analysis to model.

  2. Examine causes for different vulnerability durations. We expect that project resources, programming language, and vulnerability type will affect vulnerability duration. While project resources are difficult to measure directly, we can use related metrics, such as popularity as measured by GitHub stars, popularity as measured by how widely the project is imported by other projects, and the number of contributing authors.

### References

  - [CVEFixes](https://github.com/secureIT-project/CVEfixes)
