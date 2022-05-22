
sort data/cvefixes.csv -t \; -k 2 > cvefixes-sorted.csv
join cvefixes-sorted.csv  -1 2 -2 1 -t \; <( zcat /da5_data/basemaps/gz/c2fbbFullU0.s ) >> results/join2.csv
