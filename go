#! /bin/bash

#
# This script is just a wrapper around the other scripts
#
# go1 finds bad (vulnerable) and good (fixed) blobs.
# go2 find projects containing both good and bad blobs and timestamps
#

data_file=test-data0.1000

# Check the command line args
if [[ $# -ne 1 ]]; then
   echo "usage: go <output directory>"  >&2
   echo "example: ./go out"
   exit 1
fi
outdir="$1"

#
# Run the go scripts
#

echo " ---- 1 "
cat $data_file | ./go1 $outdir
if [ $? -ne 0 ]; then
    exit 1
fi


echo " ---- 2 "
for dir in $(ls -d $outdir/*); do
    echo working on $dir
    ./go2 $dir
    echo ""
done

