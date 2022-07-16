#! /bin/bash
#
# This script is mainly a wrapper around the other scripts
#
# go1 finds bad (vulnerable) and good (fixed) blobs.
# go2 find projects containing both good and bad blobs and timestamps
# go3 formats the results 
#
#------------------------------------------------------------------------

#data_file=data/short.cvefixes.csv
data_file=data/cvefixes.csv

# Make sure the input data file exists
if [ ! -f $data_file ]; then
    echo Error: file not found: $data_file
    exit 1
fi

# Check the command line args
if [[ $# -ne 1 ]]; then
   echo "usage: go <output directory> "  >&2
   echo "example: ./go out"
   exit 1
fi
outdir="$1"

# Initialize the output directory
if [ "$outdir" == "out" ]; then
    # If the output directory has the special name "out", remove it if it
    # already exists. 
    rm -rf out
elif [ -d $outdir ]; then
   # In all other cases, do not remove or overwrite the directory, just exit.
   echo Error: directory $outdir already exits >&2
   exit 1
fi
mkdir $outdir
if [ $? -ne 0 ]; then
    exit 1
fi
mkdir $outdir/fail
if [ $? -ne 0 ]; then
    exit 1
fi


# Initialize some variables that are just used for informational purposes
count=0
num_entries=`grep -v "^#" "$data_file" | wc -l`

# Read and process the input data file
while read line; do
    if [[ "$line" == "#"* ]]; then
        # skip comments
        continue
    fi

    count=$((count+1))
    cve=`echo $line | cut -d\; -f 1`
    working_dir="$outdir/$cve"
    echo ""
    echo "------------ $cve ($count of $num_entries)"

    echo "Stage 1"
    echo "echo $line | ./go1 $working_dir"
    echo $line | ./go1 $working_dir
    if [ $? -ne 0 ]; then
        echo "Failure (go1): \"./go1 $working_dir\" failed"
        mv $working_dir $outdir/fail/$cve.stage1
        continue
    fi

    echo "Stage 2"
    echo "./go2 $working_dir"
    ./go2 $working_dir
    if [ $? -ne 0 ]; then
        echo "Failure (go2): \"./go2 $working_dir\" failed"
        mv $working_dir $outdir/fail/$cve.stage2
        continue
    fi

    echo "Stage 3"
    file="$working_dir/results.csv"
    echo "./go3 $cve $file"
    ./go3 $cve $file
    if [ $? -ne 0 ]; then
        echo "Failure (go3): \"./go3 $cve $file\" failed"
        mv $working_dir $outdir/fail/$cve.stage3
        continue
    fi
    echo ""

    # Create a top level html file to link all the results.html files together
    echo "<a href='$cve/results.html'>$cve</a><br>" >> $outdir/allresults.html
done < $data_file

echo ""
exit 0
