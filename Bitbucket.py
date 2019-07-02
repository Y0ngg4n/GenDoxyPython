#!/usr/bin/env python
import requests
import json
import os
import subprocess
import Doxygen
import shutil


def getProjects(baseUrl, username, password, outputFolder, genOutPutFolder):
    apiUrl = baseUrl + "/rest/api/1.0/"
    print(apiUrl)
    projects = requests.get(apiUrl + "projects?limit=1000", auth=(username, password)).text.encode("ascii", "ignore")
    projects = json.loads(projects)["values"]
    projectKeys = {}
    for project in projects:
        projectKeys[project["key"]] = project["name"]
        os.makedirs(outputFolder + "/git/" + project["name"], exist_ok=True)

    for projectKey in projectKeys.keys():
        repos = requests.get(apiUrl + "projects/" + projectKey + "/repos?limit=1000", auth=(username, password)).text.encode("ascii", "ignore")
        repos = json.loads(repos)["values"]
        for repo in repos:
            repoFolder = outputFolder + "/git/" + projectKeys[projectKey] + "/" + repo["name"]
            os.makedirs(repoFolder, exist_ok=True)
            httpUrl = ""

            for links in repo["links"]["clone"]:
                if (links["name"] == "http"):
                    httpUrl = links["href"]

            print(httpUrl)

            os.system("git clone " + httpUrl + " " + repoFolder)
            outputRepoDir = genOutPutFolder + "/" + projectKeys[projectKey] + "/" + repo["name"]
            os.makedirs(outputRepoDir, exist_ok=True)

            # Branches
            proc = subprocess.Popen("cd " + repoFolder + " && git branch", stdout=subprocess.PIPE, shell=True)
            lines = proc.stdout.readlines();
            for branch in lines:
                branch = branch.decode("ascii").replace("*", "").replace("\r", "").strip()
                outputBranchDir = outputRepoDir + "/" + branch
                Doxygen.generateDocumentation(repoFolder, repo["name"], outputBranchDir, branch)

    shutil.rmtree(outputFolder)
