#!/bin/bash

# output should be: cve, project-identifier (project that copies), fix commit, first commit, fix time, first commit time, vulnerability publish time, file name
# this script outputs: cve, project-identifier (project that copies), fix commit, first commit, fix time, first commit time

# input: folder name that contains subfolders with CVE numbers
 
folder="$1"

for cve in $( ls -1 out2 | grep CVE)
 do
    #echo "cve: $cve"
    
    file_ending="_bad_sorted.txt"
    
    for project_string in $( ls -1 "$folder/$cve" | grep $file_ending )
    do
        project=$( echo "$project_string" |  sed "s/$file_ending//g" )
        
        #echo "project: $project"
        
        bad_blobs="out2/$cve/${project}_bad_sorted.txt"
        good_blobs="out2/$cve/${project}_good_sorted.txt"
        
        first_bad=$(head -n 1 $bad_blobs )
        last_bad=$(tail -n 1 $bad_blobs )
        
        first_good=$(head -n 1 $good_blobs )
        
        #echo "first bad $first_bad"
        #echo "first bad $first_good"
        
        first_bad_commit=$( echo $first_bad | cut -d\; -f3 )
        last_bad_commit=$( echo $last_bad | cut -d\; -f3 )
        
        first_good_commit=$( echo $first_good | cut -d\; -f3 )
        
        first_bad_commit_time=$( echo $first_bad | cut -d\; -f2 )
        last_bad_commit_time=$( echo $last_bad | cut -d\; -f2 )
        
        good_commit_time=$( echo $first_good | cut -d\; -f2 )
        
        echo "$cve;$project;$first_good_commit;$first_bad_commit;$last_bad_commit;$good_commit_time;$first_bad_commit_time;$last_bad_commit_time"
    done
done
