#!/bin/bash
#
# Create data file with following fields:
#   Commit hash of commit that fixed the vulnerability
#   CVE identifier for vulnerability
#   Pathname of file in which the vulnerability was fixed
#   Date on which author made commit
#   Date on which CVE was published
#   Pathname of fixed file from World of Code commit
#   Blob hash with contents of fixed file
#   Old blob hash with contents of file before fix
#
# Unique key is CVE and pathname. Fixes may affect multiple
# files, so there are lines with the same CVE identifier.
#
#------------------------------------------------------------------------

sort data/cvefixes.csv -t \; -k 2 > cvefixes-sorted.csv
join cvefixes-sorted.csv  -1 2 -2 1 -t \; <( zcat /da5_data/basemaps/gz/c2fbbFullU0.s ) >> results/join2.csv
awk -F\; '$3 == $6' results/join2.csv > results/filtered.csv
