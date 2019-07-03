import json
import os
import re
import subprocess

import requests

import Doxygen


def getProjects(baseUrl, username, password, outputFolder, genOutPutFolder):
    apiUrl = baseUrl + "/api/v1/"

    repos = requests.get(apiUrl + "user/subscriptions", auth=(username, password)).text.encode("ascii",
                                                                                               "ignore").decode("ascii")
    repos = json.loads(repos)
    print(repos)
    for repo in repos:
        print(repo)
        repoFolder = outputFolder + "/git/" + repo["owner"]["login"] + "/" + repo["name"]
        os.makedirs(repoFolder, exist_ok=True)
        httpUrl = repo["clone_url"]
        os.system("git clone " + httpUrl + " " + repoFolder)
        outputRepoDir = genOutPutFolder + "/" + repo["owner"]["login"] + "/" + repo["name"]
        os.makedirs(outputRepoDir, exist_ok=True)

        # Branches
        proc = subprocess.Popen("cd " + repoFolder + " && git branch -a", stdout=subprocess.PIPE, shell=True)
        lines = proc.stdout.readlines();
        for branch in lines:
            branch = re.sub(".*\/", "", branch.decode("ascii").replace("*", "").replace("\r", "").strip())
            outputBranchDir = outputRepoDir + "/" + branch
            Doxygen.generateDocumentation(repoFolder, repo["name"], outputBranchDir, branch)
