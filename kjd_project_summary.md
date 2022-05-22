# KJD: Vulnerability Lifespan Across Projects

**Team**
  - **Kristiina Rahkema**, *University of Tartu, Estonia*
  - **James Walden**, *Northern Kentucky University, USA*
  - **David Reid**, *University of Tennessee, USA*

**Abstract:** While vulnerabilities may be discovered and fixed in a single project, copies of the vulnerable code may persist in other projects for a considerable amount of time. We use the World of Code to find copies of vulnerable files that exist in multiple projects and measure the lifespan of vulnerabilities in those projects.

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

  1. We don't know when each vulnerability was introduced, so we consider all commits made before the vulnerability fixing commit to be vulnerable.
  2. Some projects may copy a fixed version of a file, then later revert to an older vulnerable version of a file because the fixed version introduced problems for the project, which means that the time between the introduction of a vulnerable file and a fixed file may be negative. 
  3. Related to the previous challenge, vulnerabilities and their fixes may be introduced multiple times during the history of a project. A fix could be introduced twice because the situation in #2 happened, followed by a modification of project code that allowed a later introduction of the fixed file without the problems caused by its first introduction to the project.
  4. We only look at vulnerabilities that are fixed with changes to a single file to make our data collection scripts faster to write and run.

### 5. Future Work

  1. Include projects which have vulnerabilities but no fixes. Use survival analysis to model.

  2. Examine causes for different vulnerability durations. We expect that project resources, programming language, and vulnerability type will affect vulnerability duration. While project resources are difficult to measure directly, we can use related metrics, such as popularity as measured by GitHub stars, popularity as measured by how widely the project is imported by other projects, and the number of contributing authors.

### References

  - [CVEFixes](https://github.com/secureIT-project/CVEfixes)
