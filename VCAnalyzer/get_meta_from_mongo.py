#! /usr/bin/python

# Get meta data about a project from the WoC mongo database.
# on error, write error message to stderr

#mongos> db.P_metadata.U.find({"ProjectID":"openssl_openssl"}).pretty()

import sys
import pymongo
import bson
import time

cur_time = time.time()

# output the csv data. if data is null, each value will be blank.
def write_data(data):
    sys.stdout.write("NumAuthors:")
    if (data.has_key("NumAuthors")):
        sys.stdout.write(str(data["NumAuthors"]))
    sys.stdout.write(", ")

    sys.stdout.write("EarliestCommitDate:")
    if (data.has_key("EarliestCommitDate")):
        sys.stdout.write(str(data["EarliestCommitDate"]))
    sys.stdout.write(", ")

    sys.stdout.write("LatestCommitDate:")
    if (data.has_key("LatestCommitDate")):
        sys.stdout.write(str(data["LatestCommitDate"]))
    sys.stdout.write(", ")

    sys.stdout.write("ValidDates:")
    if ( (data.has_key("LatestCommitDate")) and (data.has_key("EarliestCommitDate")) ):
        last = data["LatestCommitDate"]
        first = data["EarliestCommitDate"]
        if (first == last):
            #sys.stdout.write("1st=Last")
            sys.stdout.write("OK")
        elif ((first == 0) or (last == 0)):
            sys.stdout.write("Zero")
        elif ((first > cur_time) or (last > cur_time)):
            sys.stdout.write("Future")
        else: 
            sys.stdout.write("OK")
    sys.stdout.write(", ")

    sys.stdout.write("NumActiveMon:")
    if (data.has_key("NumActiveMon")):
        sys.stdout.write(str(data["NumActiveMon"]))
    sys.stdout.write(", ")

    #sys.stdout.write("RootFork:")
    #if (data.has_key("RootFork")):
    #    sys.stdout.write(data["RootFork"].encode('utf-8').strip())
    #sys.stdout.write(", ")

    sys.stdout.write("NumStars:")
    if (data.has_key("NumStars")):
        sys.stdout.write(str(data["NumStars"]))
    sys.stdout.write(", ")

    sys.stdout.write("NumCore:")
    if (data.has_key("NumCore")):
        sys.stdout.write(str(data["NumCore"]))
    sys.stdout.write(", ")

    sys.stdout.write("CommunitySize:")
    if (data.has_key("CommunitySize")):
        sys.stdout.write(str(data["CommunitySize"]))
    sys.stdout.write(", ")

    sys.stdout.write("NumCommits:")
    if (data.has_key("NumCommits")):
        sys.stdout.write(str(data["NumCommits"]))
    sys.stdout.write(", ")

    sys.stdout.write("NumForks:")
    if (data.has_key("NumForks")):
        sys.stdout.write(str(data["NumForks"]))
    sys.stdout.write(", ")

    sys.stdout.write("FileInfo:")
    if (data.has_key("FileInfo")):
        FileInfo = data["FileInfo"]
        if (len(FileInfo) > 0):
            if (FileInfo.has_key("other")):
                FileInfo.pop("other")
        if (len(FileInfo) > 0):
            sorted_FileInfo = sorted(FileInfo.items(), key=lambda t: t[1], reverse=True)
            sys.stdout.write(sorted_FileInfo[0][0])

    sys.stdout.write("\n")

# creat an empty dict to use for error cases.
empty = {}

if (len(sys.argv) != 2):
    sys.stderr.write( "usage: %s project\n" % sys.argv[0])
    sys.stderr.write("    example %s openssl_openssl\n" % sys.argv[0])
    write_data(empty)
    exit(1)

project=sys.argv[1]

#client = pymongo.MongoClient("mongodb://da1.eecs.utk.edu/")
client = pymongo.MongoClient("mongodb://da5.eecs.utk.edu/")
db = client ['WoC']
coll = db['P_metadata.U']

dataset = coll.find({"ProjectID":project}, {"NumAuthors":1, "EarliestCommitDate":1, "LatestCommitDate":1, "NumActiveMon":1, "RootFork":1, "NumStars":1, "NumCore":1, "CommunitySize":1, "NumCommits":1, "NumForks":1, "FileInfo":1}) 

#numitems = len(list(dataset.clone()))
numitems = dataset.count()
if (numitems == 0):
    sys.stderr.write("Error: no records found for project %s\n" % project)
    write_data(empty)
    exit(1)

if (numitems > 1):
    sys.stderr.write("Error: more than 1 records found for project %s\n" % project)
    write_data(empty)
    exit(1)

for data in dataset:
    write_data(data)

dataset.close()
exit(0)
