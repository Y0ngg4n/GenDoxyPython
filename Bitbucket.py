import requests
import json
import os
import subprocess
import urllib


def getProjects(baseUrl, username, password, outputFolder):
    apiUrl = baseUrl + "/rest/api/1.0/"
    print(apiUrl)
    projects = requests.get(apiUrl + "projects", auth=(username, password)).text
    projects = json.loads(projects)["values"]
    projectKeys = {}
    for project in projects:
        projectKeys[project["key"]] = project["name"]
        os.makedirs(outputFolder + "/git/" + project["name"], exist_ok=True)

    for projectKey in projectKeys.keys():
        repos = requests.get(apiUrl + "projects/" + projectKey + "/repos", auth=(username, password)).text
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
            outputRepoDir = "/data/doxygen/output/" + projectKeys[projectKey] + "/" + repo["name"]
            os.makedirs(outputRepoDir, exist_ok=True)

            # Branches
            proc = subprocess.Popen("cd " + repoFolder + " && git branch", stdout=subprocess.PIPE, shell=True)
            lines = proc.stdout.readlines();
            for branch in lines:
                branch = branch.decode("utf-8")
                print(branch)
                outputBranchDir = outputRepoDir + "/" + branch.replace("*", "").replace("\r", "").strip()

                os.system("echo \"OUTPUT_DIRECTORY = " + outputBranchDir + "\" >> Doxyfile.conf")
                os.system("cp /data/doxygen/Doxyfile Doxyfile.conf")
                os.system("echo \"INPUT = " + repoFolder + "\" >> Doxyfile.conf")
                os.system("echo \"PROJECT_NAME = \"" + repo["name"] + "\"")
                os.system("cd " + repoFolder + " && git checkout " + branch)
                os.makedirs(outputBranchDir, exist_ok=True)
                os.system("doxygen Doxyfile.conf")
