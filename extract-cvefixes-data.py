#!/bin/env python3
#
# Collect data from CVEfixes SQLite database, which can be built from
# code @ https://github.com/secureIT-project/CVEfixes and
# data @ https://zenodo.org/record/4476564
#
#------------------------------------------------------------------------
import pandas as pd
import sqlite3 as lite
from sqlite3 import Error
from pathlib import Path
from datetime import date
from collections import defaultdict
import re

import pprint
pp = pprint.PrettyPrinter(indent=4)

#------------------------------------------------------------------------
# User settable parameters
#------------------------------------------------------------------------
DATA_PATH = Path("../repos/CVEfixes/Data")   # Directory containing CVEfixes.db

#------------------------------------------------------------------------
# Database connection code for CVEfixes SQLite database
#------------------------------------------------------------------------
def create_connection(db_file):
    conn = None
    try:
        conn = lite.connect(db_file, timeout=10)  # connection via sqlite3
    except Error as e:
        print(e)
    return conn


conn = create_connection(DATA_PATH / "CVEfixes.db")

#------------------------------------------------------------------------
# Filter out files that don't contain source code
#------------------------------------------------------------------------
def filter_files(in_files):
    filtered_files = []
    for file in in_files:
        if re.match(r'(readme|changelog|install|makefile|makefile.pl)$', file, re.IGNORECASE):
            pass
        elif file.endswith('.html') or file.endswith('.md') or file.endswith('.txt'):
            pass
        else:
            filtered_files.append(file)
    # pp.pprint(filtered_files)
    return(filtered_files)

#------------------------------------------------------------------------
# Build cves dictionary from CVEfixes database
#------------------------------------------------------------------------
def file_has_method(file_change_id):
    file_exists = pd.read_sql_query("SELECT name FROM method_change WHERE file_change_id = '{}'".format(file_change_id), conn)
    if file_exists is None:
        return False
    else:
        return True

#------------------------------------------------------------------------
# Build cves dictionary from CVEfixes database
#------------------------------------------------------------------------
cves = defaultdict(list)

fixes_df = pd.read_sql_query("SELECT cve_id, hash FROM fixes", conn)
for row in fixes_df.itertuples():
    cves[row.cve_id] = [ row.hash ]

    commit_dates = pd.read_sql_query("SELECT committer_date FROM commits WHERE hash = '{}'".format(row.hash), conn)
    for daterow in commit_dates.itertuples():
        cves[row.cve_id].append(daterow.committer_date)

    files = []
    files_df = pd.read_sql_query("SELECT file_change_id,new_path FROM file_change WHERE hash = '{}'".format(row.hash), conn)
    for filerow in files_df.itertuples():
        files.append(filerow.new_path)
    out_files = filter_files(files)
    if out_files:
        file_string = ",".join(out_files)
    else:
        file_string = ""
    cves[row.cve_id].append(file_string)

cve_df = pd.read_sql_query("SELECT cve_id, published_date FROM cve", conn)
for row in cve_df.itertuples():
    cves[row.cve_id].append(row.published_date)

#------------------------------------------------------------------------
# Build cves dictionary from CVEfixes database
#------------------------------------------------------------------------
for cve in cves:
    data = cves[cve]
    files = data[2].split(",")
    # Print only CVEs with one file
    if len(files) == 1:
        print("{};{};{};{};{}".format(cve, data[0], files[0], data[1], data[3]))
    # FIXME: print all CVEs regardless of how many files
    # for file in files:
    #     print("{};{};{};{};{}".format(cve, data[0], file, data[1], data[3]))
