# VCAnalyzer (Vulnerable Clones Analyzer)

VCAnalyzer is a tool to analyze vulnerabilies that are propogated 
through copy-based code reuse. The tool reads a file with information
about known vulnerabilities in open source projects and then it
produces statistics about projects that have copied the vulnerabily

The input to the tool is a .csv file containing information about a
vulnerability as defined in the CVE list at cve.org. The input
file contains one line per vulnerability with the following fields:
  - CVE ID (example CVE-2007-6761

CVE-2022-34299,7ef09e1fc9ba07653dd078edb2408631c7969162,https://github.com/davea42/libdwarf-code,src/lib/libdwarf/dwarf_form.c,2022-06-15 14:46:01-07:00,2022-06-23T17:15Z

