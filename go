#! /bin/bash
#
# This script is mainly a wrapper around the other scripts
#
# The fields in the input file are: CVE identifier, commit hash, project, 
#     path of file that fixed vulnerability, author commit date, 
#     vulnerability publication date
#
# go1 finds bad (vulnerable) and good (fixed) blobs.
# go2 find projects containing both good and bad blobs and timestamps
# go3 formats the results 
#
#------------------------------------------------------------------------

#default_data_file=data/short.cvefixes2.csv
#default_data_file=data/cvefixes_with_repo.csv
default_data_file=data/cvefixes_new.csv
#default_data_file=veryshort

#
# Call when user hits control-c. Kill all child processes before exitting.
#
trap 'pkill -P $$; echo killed; exit' SIGINT SIGTERM

# Check the command line args
if [[ $# -eq 1 ]]; then
    data_file="$default_data_file"
elif [[ $# -eq 2 ]]; then
    data_file="$2"
else
   echo "usage: go <output directory> [<input data file>]"  >&2
   echo "example: ./go out"
   exit 1
fi
outdir="$1"

# Make sure the input data file exists
if [ ! -f $data_file ]; then
    echo Error: file not found: $data_file
    exit 1
fi

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
touch $outdir/log.error

# Initialize some variables that are just used for informational purposes
count=0
num_entries=`grep -v "^#" "$data_file" | grep -v "^$" | wc -l`

# Read and process the input data file
while read line; do
    if [[ "$line" == "#"* ]] || [[ "$line" == "" ]]; then
        # skip comments and blank lines
        continue
    fi

    # count lines (just to provide user feedback)
    count=$((count+1))

    # extract the fields from the input data file.
    cve=`echo $line | cut -d\; -f 1`
    working_dir="$outdir/$cve"
    echo ""
    echo "------------ $cve ($count of $num_entries, `date +"%D %T"`)"
    if [ "$cve" == "" ]; then
        echo "Failure: Invalid input line: CVE missing: $line" | tee -a $outdir/log.error
        continue
    fi
    commit=`echo $line | cut -d\; -f 2`
    project_url=`echo $line | cut -d\; -f 3`
    platform=`echo $project_url | sed -e "s@https?*://@@" -e "s/\.com.*$//"`
    project_name=`echo $project_url | sed -e "s@http.*\.com/@@" -e "s@/@_@"`
    filepath=`echo $line | cut -d\; -f 4`
    #commit_date=`echo $line | cut -d\; -f 5`
    vdate=`echo $line | cut -d\; -f 6`  # date vulnerability was published

    # Error check the input line
    if [[ "$commit" == "" ]] || [[ "$project_url" == "" ]] || [[ "$filepath" == "" ]] || [[ "$vdate" == "" ]] ; then
        echo "$cve Failure: Invalid input line: $line" | tee -a $outdir/log.error
        continue
    fi

    filename=`basename $filepath`
    v_unixtime=$(date -d "${vdate}" +"%s")

    echo -n "Stage 1" 
    echo " (echo $cve;$commit;$platform;$project_name;$filepath | ./go1 $working_dir)"
    echo "$cve;$commit;$platform;$project_name;$filepath" | ./go1 $working_dir
    if [ $? -ne 0 ]; then
        echo "Failure (go1): \"./go1 $working_dir\""
        mv $working_dir $outdir/fail/$cve.stage1
        continue
    fi
#echo SKIPPING stage 2/3
#continue

    echo -n "Stage 2"
    echo " (./go2 $working_dir $v_unixtime)"
    ./go2 $working_dir $v_unixtime
    if [ $? -ne 0 ]; then
        echo "Failure (go2): \"./go2 $working_dir\" failed"
        mv $working_dir $outdir/fail/$cve.stage2
        continue
    fi

    echo -n "Stage 3"
    file="$working_dir/results.fixed.csv"
    echo " (./go3 $cve: $project_name, $filepath $file)"
    ./go3 "$cve: $project_name, $filepath" $file
    if [ $? -ne 0 ]; then
        echo "Failure (go3): \"./go3 $cve ...\" failed"
        mv $working_dir $outdir/fail/$cve.stage3
        continue
    fi
    ./go3 "$cve: $project_name, $filepath" $working_dir/results.notfixed.csv
    ./go3 "$cve: $project_name, $filepath" $working_dir/results.unknown.csv

    # Create a top level html file to link all the results.html files together
    #echo "<a href='$cve/results.html'>$cve</a><br>" >> $outdir/allresults.html
    echo "<a href='$cve'>$cve</a><br>" >> $outdir/allresults.html

    echo ""
done < $data_file
echo "============"

# Create the error log by copying error messages from each directory to one
# top level file named log.error
if [ -z "$(ls -A $outdir/fail)" ]; then
    # if there are no failures, just remove the fail directory
    rmdir $outdir/fail
else
    for dir in $( ls -1d $outdir/fail/CVE-*); do
        echo -n "`basename "$dir"`: " >> $outdir/log.error
        if [ -f $dir/error_log ]; then
            cat $dir/error_log >> $outdir/log.error
        else
            echo "Error (no error_log)" >> $outdir/log.error
        fi
    done
fi

# Output some summary information
echo "`cat $outdir/log.error | wc -l` failed (see $outdir/log.error)"
echo "`ls -1d $outdir/CVE-* | wc -l` succeeded (see $outdir/CVE-*)"
echo ""

exit 0
