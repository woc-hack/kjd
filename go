#! /bin/bash
#
# This script is just a wrapper around the other scripts
#
# go1 finds bad (vulnerable) and good (fixed) blobs.
# go2 find projects containing both good and bad blobs and timestamps
#
#------------------------------------------------------------------------

#data_file=data/filtered.csv
data_file=data/short.cvefixes.csv
if [ ! -f $data_file ]; then
    echo Error: file not found: $data_file
    exit 1
fi

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


for line in $(cat "$data_file"); do
#while read line; do
    echo $line
#done < /dev/stdin
done
echo "#####"

#
# Run the go scripts
#


echo "go1 ------------------------------------------------- "
cat $data_file | ./go1 $outdir
if [ $? -ne 0 ]; then
    echo "\"./go1 $outdir\" failed with error code $?"
    exit 1
fi



echo ""
echo "go2 ------------------------------------------------- "
for dir in $(ls -d $outdir/* | grep CVE); do
    echo "./go2 $dir"
    ./go2 $dir
    err="$?"
    if [ $err -ne 0 ]; then
        echo "\"./go2 $dir\" failed with error code $err"
        echo ""
        continue
    fi
    echo ""
done


echo "go3 ------------------------------------------------- "
for dir in $(ls -d $outdir/* | grep CVE); do
    file="$dir/results.csv"
    echo "./go3 $file"
    ./go3 $file
    err="$?"
    if [ $err -ne 0 ]; then
        echo "\"./go3 $file\" failed with error code $err"
        echo ""
        continue
    fi
    echo ""
done
