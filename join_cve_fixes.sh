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

for i in {0..127}
   do join -1 2 -2 1 -t \; cvefixes-sorted.csv <(zcat /da5_data/basemaps/gz/c2fbbFullU$i.s) > results/join$i.csv
   awk -F\; '$3 == $6' results/join$i.csv > results/filtered$i.csv
done

