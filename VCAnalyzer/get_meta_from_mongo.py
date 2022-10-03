#! /usr/bin/python

#mongos> db.P_metadata.U.find({"ProjectID":"openssl_openssl"}).pretty()

import sys
import pymongo
import bson

if (len(sys.argv) != 2):
    print("usage: %s project" % sys.argv[0])
    print("    example %s openssl_openssl" % sys.argv[0])
    exit(1)

project=sys.argv[1]

client = pymongo.MongoClient("mongodb://da1.eecs.utk.edu/")
db = client ['WoC']
coll = db['P_metadata.U']

dataset = coll.find({"ProjectID":project}, {"NumAuthors":1, "EarliestCommitDate":1, "LatestCommitDate":1, "NumActiveMon":1, "RootFork":1, "NumStars":1, "NumCore":1, "CommunitySize":1, "NumCommits":1, "NumForks":1, "FileInfo":1}) 

#numitems = len(list(dataset.clone()))
numitems = dataset.count()
if (numitems == 0):
    print("Error: no records found for project %s" % project)
    exit(1)

if (numitems > 1):
    print("Error: more than 1 records found for project %s" % project)
    exit(1)


for data in dataset:
    sys.stdout.write(project)
    sys.stdout.write(", ")

    sys.stdout.write("NumAuthors:")
    if (data.has_key("NumAuthors")):
        sys.stdout.write(str(data["NumAuthors"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("EarliestCommitDate:")
    if (data.has_key("EarliestCommitDate")):
        sys.stdout.write(str(data["EarliestCommitDate"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("LatestCommitDate:")
    if (data.has_key("LatestCommitDate")):
        sys.stdout.write(str(data["LatestCommitDate"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("NumActiveMon:")
    if (data.has_key("NumActiveMon")):
        sys.stdout.write(str(data["NumActiveMon"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("RootFork:")
    if (data.has_key("RootFork")):
        sys.stdout.write(data["RootFork"].encode('utf-8').strip())
    else:
        sys.stdout.write ("-")
    sys.stdout.write(", ")

    sys.stdout.write("NumStars:")
    if (data.has_key("NumStars")):
        sys.stdout.write(str(data["NumStars"]))
    else:
        sys.stdout.write ("-")
    sys.stdout.write(", ")

    sys.stdout.write("NumCore:")
    if (data.has_key("NumCore")):
        sys.stdout.write(str(data["NumCore"]))
    else:
        sys.stdout.write ("-")
    sys.stdout.write(", ")

    sys.stdout.write("CommunitySize:")
    if (data.has_key("CommunitySize")):
        sys.stdout.write(str(data["CommunitySize"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("NumCommits:")
    if (data.has_key("NumCommits")):
        sys.stdout.write(str(data["NumCommits"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("NumForks:")
    if (data.has_key("NumForks")):
        sys.stdout.write(str(data["NumForks"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("NumAuthors:")
    if (data.has_key("NumAuthors")):
        sys.stdout.write(str(data["NumAuthors"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("EarliestCommitDate:")
    if (data.has_key("EarliestCommitDate")):
        sys.stdout.write(str(data["EarliestCommitDate"]))
    else:
        sys.stdout.write("-")
    sys.stdout.write(", ")

    sys.stdout.write("FileInfo:")
    if (data.has_key("FileInfo")):
        FileInfo = data["FileInfo"]
        FileInfo.pop("other")
        sorted_FileInfo = sorted(FileInfo.items(), key=lambda t: t[1], reverse=True)
        sys.stdout.write(sorted_FileInfo[0][0])
    else:
        sys.stdout.write("- ")

    sys.stdout.write("\n")

dataset.close()
exit(0)
