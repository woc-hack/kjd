#! /bin/bash
#
# This script is just a wrapper around the other scripts
#
# go1 finds bad (vulnerable) and good (fixed) blobs.
# go2 find projects containing both good and bad blobs and timestamps
#
#------------------------------------------------------------------------

#data_file=data/filtered.csv
data_file=data/short.csv

echo Reading $data_file

# Check the command line args
if [[ $# -ne 1 ]]; then
   echo "usage: go <output directory> "  >&2
   echo "example: ./go out"
   exit 1
fi
if [ ! -f $data_file ]; then
   echo "file $data_file does not exist"
   exit 1
fi
outdir="$1"

#
# Run the go scripts
#

echo "go ---- 1 "
cat $data_file | ./go1 $outdir
if [ $? -ne 0 ]; then
    echo "Running \"./go1 $outdir\" failed with error code $?"
    exit 1
fi


echo "go ---- 2 "
for dir in $(ls -d $outdir/*); do
    echo working on $dir
    ./go2 $dir
    if [ $? -ne 0 ]; then
        echo "Running \"./go2 $dir\" failed with error code $?"
        exit 2
    fi
    echo ""
done
