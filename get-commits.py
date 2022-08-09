#!/usr/bin/env python3

from github import Github
from gitlab import Gitlab
from pathlib import Path
import sys
import urllib.parse

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
        if i == 10:
            break
        print(commit.sha)

#------------------------------------------------------------------------
# Get commits for filename from project on Gitlab 
#------------------------------------------------------------------------
def gitlab_commits(token, project, filepath):
    g = Gitlab(private_token=token)
    p = g.projects.get(project)
    commits = p.commits.list(get_all=True, path=filepath)
    # FIXME: Use HTTP access instead of gitlab module
    # This returns 404 API Version Not Found, apparently a known issue @
    # https://app.bountysource.com/issues/95835557-commits-list-does-not-filter-by-path
    for commit in commits:
        print(commit.sha)

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
        if i == 10:
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
    pass
else:
    print("Invalid host type \"{}\" specified.".format(host))
    printusage()
    sys.exit(2)

