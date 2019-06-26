import requests
import json
import os

def getProjects(baseUrl, token, outputFolder):
    apiUrl = baseUrl + "/rest/api/1.0/"
    print(apiUrl)
    projects = requests.get(apiUrl + "projects", headers={'Authorization': 'TOK:' + token}).text
    projects = json.loads(projects)["values"]
    projectKeys = {}
    for project in projects:
        projectKeys[project["key"]] = project["name"]
        os.makedirs(outputFolder  + "/" + project["name"], exist_ok=True)

    for projectKey in projectKeys.keys():
        repos = requests.get(apiUrl + "projects/" + projectKey + "/repos", headers={'Authorization': 'TOK:' + token}).text
        repos = json.loads(repos)["values"]
        for repo in repos:
            repoFolder = outputFolder + "/" + projectKeys[projectKey] + "/" + repo["name"]
            os.makedirs(repoFolder, exist_ok=True)
            httpUrl = ""

            for links in repo["links"]["clone"]:
                if(links["name"] == "http"):
                    httpUrl = links["href"]

            os.system("git clone " + httpUrl + " " + repoFolder)