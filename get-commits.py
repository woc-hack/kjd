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
def load_tokens(tokenfile):
    token_path = Path.home() / tokenfile
    if token_path.is_file():
        with open(token_path) as tf:
            lines = tf.readlines()
            tokens = [line.rstrip() for line in lines]
        return tokens
    else:
        print("Token file does not exist at {}.".format(token_path))
        sys.exit(3)

#------------------------------------------------------------------------
# Get commits for filename from project on Gitlab 
#------------------------------------------------------------------------
def gitlab_commits(tokens, project, filepath):
    project = 'tortoisegit/tortoisegit'
    project = quote(project, safe='')
    filepath = 'LICENSE'
    gl_base = 'https://gitlab.com/'
    gl_path = 'api/v4/projects/' + project + "/repository/commits"
    gl_params = { 'file': filepath, 'per_page': 20 }
    gl_query = '?' + urlencode(gl_params)
    gl_url = urljoin(gl_base, gl_path + gl_query)

    # Loop through pages while a next URL exists in HTTP link header
    while True:
        r = requests.get(gl_url)
        if r.status_code == 200:
            r_data = r.json()
        else:
            print("Error: HTTP response \"{} {}\" from URL {}.".format(r.status_code, r.reason, gl_url))
            sys.exit(3)

        for commit in r_data:
            print(commit['id'])

        if 'next' in r.links:
            gl_url = r.links['next']['url']
        else:
            break

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
# We use the first token that has enough queries left on its rate limit
# to complete listing the desired commits.
#------------------------------------------------------------------------
def github_commits(tokens, project, filepath):
    for token in tokens:
        try:
            g = Github(login_or_token=tokens.pop())
            repo = g.get_repo(project)
            commits = repo.get_commits(path=filepath)
            for commit in commits:
                print(commit.sha)
        except github.GithubException.RateLimitExceededException:
            pass
        else:
            break
    else:
        print("No GitHub access token had enough queries to complete.")
        sys.exit(5)

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
    access_tokens = load_tokens('github-auth')
    github_commits(access_tokens, project, filepath)
elif host == "gitlab" or host == "gl":
    access_token = load_token('gitlab-auth')
    gitlab_commits(access_token, project, filepath)
elif host == "bitbucket" or host == "bb":
    bitbucket_commits(project, filepath)
else:
    print("Invalid host type \"{}\" specified.".format(host))
    printusage()
    sys.exit(2)
