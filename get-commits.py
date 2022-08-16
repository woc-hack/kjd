#!/usr/bin/env python3

from github import Github
from pathlib import Path
import requests
import sys
from urllib.parse import quote, urljoin, urlencode

debug = False

#------------------------------------------------------------------------
# Get API token for host
#------------------------------------------------------------------------
def load_token(tokenfile):
    token_path = Path.home() / tokenfile
    if token_path.is_file():
        access_token = token_path.read_text().replace('\n','')
        return(access_token)
    else:
        print("Token file does not exist at {}.".format(token_path))
        sys.exit(3)

#------------------------------------------------------------------------
# Get commits for filename from project on Github 
#------------------------------------------------------------------------
def github_commits(token, project, filepath):
    g = Github(login_or_token=token)
    repo = g.get_repo(project)
    commits = repo.get_commits(path=filepath)
    # Print no more than 10 items for testing
    i = 0
    for commit in commits:
        i = i + 1
        if i == 10 and debug:
            break
        print(commit.sha)

#------------------------------------------------------------------------
# Get commits for filename from project on Gitlab 
#------------------------------------------------------------------------
def gitlab_commits(token, project, filepath):
    project = 'tortoisegit/tortoisegit'
    project = quote(project, safe='')
    filepath = 'LICENSE'
    gl_base = 'https://gitlab.com/'
    gl_path = 'api/v4/projects/' + project + "/repository/commits"
    gl_params = { 'file': filepath, 'per_page': 20 }
    gl_query = '?' + urlencode(gl_params)
    gl_url = urljoin(gl_base, gl_path + gl_query)

    while True:
        r = requests.get(gl_url)
        if r.status_code == 200:
            r_data = r.json()
        else:
            print("Error: HTTP response \"{} {}\" from URL {}.".format(r.status_code, r.reason, gl_url))
            sys.exit(3)

        for commit in r_data:
            print(commit['id'])

        break
        # FIXME: Handle pagination according to https://docs.gitlab.com/ee/api/

#------------------------------------------------------------------------
# Get commits for filename from project on BitBucket 
#------------------------------------------------------------------------
def bitbucket_commits(project, filepath):
    bb_base ='https://api.bitbucket.org/'
    bb_path = '2.0/repositories/' + project + "/commits/"
    bb_params = { 'path': filepath, 'pagelen': 20 }
    bb_query = '?' + urlencode(bb_params)
    bb_url = urljoin(bb_base, bb_path + bb_query)

    while True:
        r = requests.get(bb_url)
        if r.status_code == 200:
            r_data = r.json()
        else:
            print("Error: HTTP response \"{} {}\" from URL {}.".format(r.status_code, r.reason, bb_url))
            sys.exit(3)

        for commit in r_data['values']:
            print(commit['hash'])

        if 'next' in r_data.keys():
            bb_url = r_data['next']
        else:
            break

#------------------------------------------------------------------------
# Get commits for filename from project on Github 
#------------------------------------------------------------------------
def github_commits(token, project, filepath):
    g = Github(login_or_token=token)
    repo = g.get_repo(project)
    commits = repo.get_commits(path=filepath)
    # Print no more than 10 items for testing
    i = 0
    for commit in commits:
        i = i + 1
        if i == 10 and debug:
            break
        print(commit.sha)

#------------------------------------------------------------------------
# Print usage message
#------------------------------------------------------------------------
def printusage():
    prg = sys.argv[0]
    print("Usage: {} <host> <project> <file path>".format(prg))
    print("       supported hosts: github, gitlab, bitbucket")
    print("           shortcuts: gh, gl, bb")
    print("       example: {} github openssl/openssl apps/info.c".format(prg))
    print("       example: {} gitlab tortoisegit/tortoisegit LICENSE".format(prg))
    print("       example: {} bitbucket swsc/lookup showCnt".format(prg))

#------------------------------------------------------------------------
# Parse command line arguments
#------------------------------------------------------------------------
if len(sys.argv) != 4:
    printusage()
    sys.exit(1)
else:
    host = sys.argv[1]
    project = sys.argv[2]
    filepath = sys.argv[3]

#------------------------------------------------------------------------
# Check for valid host then load access tokens for specified host
#------------------------------------------------------------------------
if host == "github" or host == "gh":
    access_token = load_token('github-auth')
    github_commits(access_token, project, filepath)
elif host == "gitlab" or host == "gl":
    access_token = load_token('gitlab-auth')
    gitlab_commits(access_token, project, filepath)
elif host == "bitbucket" or host == "bb":
    bitbucket_commits(project, filepath)
else:
    print("Invalid host type \"{}\" specified.".format(host))
    printusage()
    sys.exit(2)
