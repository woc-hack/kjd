# Annotated Bibliography

## Vulnerability Data

  - [CVEfixes](https://github.com/secureIT-project/CVEfixes)
  - [Snyk](https://security.snyk.io/)
  - [SZZUnleashed](https://github.com/wogscpar/SZZUnleashed)
  - [V0Finder](https://github.com/WOOSEUNGHOON/V0Finder-public)

## Papers

  - Mahmoud Alfadel; Empirical Analysis of Security Vulnerabilities in Python Packages.

    A study of 550 vulnerability reports affecting 252 Python packages in the Python ecosystem (PyPi). Vulnerabilities in Python packages are increasing over time, and they take more than 3 years to be discovered. The majority of these vulnerabilities (50.55%) are only fixed after being publicly announced.

  - Guru Bhandari et al; CVEfixes: automated collection of vulnerabilities and their fixes from open-source software. Proceedings of the 17th International Conference on Predictive Models and Data Analytics in Software Engineering. 2021.

  - Johannes Daijsing. Analyzing the Direct and Transitive Impact of Vulnerabilities onto Different Artifact Repositories

  - Alexandre Decan; On the impact of security vulnerabilities in the npm package dependency network. MSR 2018.

    A study of 399 vulnerability reports affecting 269 npm packages and 6,752 releases of those packages. Following dependencies, 72,470 other packages are affected by those vulnerable releases. 1/3 of vulnerabilities fixed by discovery date, 1/2 fixed after discovery but before publication date, and 15% fixed after discovery date or not at all. More than 40% of packages cannot be fixed by upgrading the vulnerable package due to dependency constraints that don't allow the fixed package to be installed. NPM has a total of 610K packages when the paper was written.

  - Antonios Gkortzis, Daniel Feitosa, and Diomidis Spinellis. Software reuse cuts both ways: An empirical analysis of its relationship with security vulnerabilities. Journal of Systems and Software 172 (2021).

  Empirical investigation of 1244 open-source projects, 65% of analyzed projects suffer from at least one disclosed vulnerability. Classified projects as enterprise vs volunteer and well-known vs less-known using lists (enterprise from Spinellis 2020 paper, well-known=Apache,Google,MySQL, etc.) Potential vulnerability information was obtained from the static analyzer SpotBugs, while disclosed vulnerabilities were found using the OWASP dependency checker. Found that the number of disclosed and potential vulnerabilities increases with number of dependencies. Reuse ratio (total code/new code) not correlated with security.

  - Mohammad Gharehyazie et al; Some From Here, Some From There: Cross-Project Code Reuse in GitHub

   This study analyses code reuse in GitHub projects. They found that cross-project code reuse is prevalent on GitHub. In total 5753 projects contained clones with token size 20, 5533 with tokensize 30 and 628 projcts contained clones with tokensize 50. They found that cross-project clones are generally restricted to projects in the same domain and follow certain patterns. 
   
  - Malin Källén et al; Jupyter Notebooks on GitHub: Characteristics and Code Clones

   This study analysed Jupyter notebooks found on GitHub. They found that more than 70% of all code snippets are exact copies of other snippets. Note: this might not be completely relevant to us, as jupyter notebooks are not really programs with vulnerabilities?

  - Ruala Kula. Do developers update their library dependencies?; ESE 2018.

    A study of >4600 GitHub projects and 2700 library dependencies. Survey of developers found that 69% were unaware of vulnerable dependencies and that updating dependencies was regarded as a low priority task. Related work cites other studies with similar results on priority of updating dependencies. Found that 81.5% of projects had outdated dependencies.

  - Viet Hung Nguyen and Fabio Massacci. The (un)reliability of NVD vulnerable versions data: an empirical experiment on Google Chrome vulnerabilities. ASIA CCS '13: Proceedings of the 8th ACM SIGSAC symposium on Information, computer and communications security. May 2013 Pages 493-498 https://doi.org/10.1145/2484313.2484377

  TBD

  - Joel Ossher et al; File Cloning in Open Source Java Projects: The Good, The Bad, and The Ugly

   This study analysed 13,000 Java project from the Sourcerer Repository (aggregation of multiple open source repositories). They found that over 10% of file are clones and that over 15% of projects contain at least one cloned file. They found that most commonly cloned fles were Java extension classes and popular third-party libraries. 

  - Iavn Pashchenko; A qualitative study of dependency management and its security implications.

    Study included 25 semi-structured interviews with developers. Found that developers perceive that popular libraries with community support are more secure. Developers focus on functionality over security when choosing dependencies. 14 out of 25 used GitHub as primary source of information about dependencies, looking at stars, number of contributors and users, number of issues, and how quickly issues are fixed. While developers perceive security fixes as easy to adopt, they avoided updated dependencies if possible to avoid breaking changes and preferred security fixes that did not include improvements in functionality. If no fix is available, developers preferred to disable affected functionality or to do nothing, though 5 of 25 had created their own fixes.

  - Niko Schwarz et al; On How Often Code Is Cloned across Repositories

   This study analysed projects in the Squeaksource ecosystem. This ecosystem contains thousands of projects with more than 40 million versions of methods. They found that 15 to 18 percent of methods were cloned (depending on the clone type considered). 
   
  - Seunghoon Woo et al; V0Finder: Discovering the Correct Origin of Publicly Reported Software Vulnerabilities; USENIX Security 2021. 
    https://www.usenix.org/conference/usenixsecurity21/presentation/woo

    TBD

  - Markus Zimmerman at al; Small world with high risks: A study of security threats in the npm ecosystem; USENIX Security 2019.

    This study analyzes dependencies between package maintainers as well as the packages themselves. Study examined 609 vulnerabilities in 5,386,237 package versions with 199,327 maintainers. Found mean number of dependencies for an npm package to be 79 packages and 39 maintainers. Packages in the npm ecosystem has a higher number of dependencies than Java packages, and include micropackages with only a few lines of source code. Up to 40% of packages have dependencies with at least one known vulnerability. The paper provides a set of threat models for attacking software via dependencies.
