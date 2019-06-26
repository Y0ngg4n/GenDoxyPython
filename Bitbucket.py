import requests
import json
import os

def getProjects(baseUrl, token, outputFolder):
    apiUrl = baseUrl + "/rest/api/1.0/"
    print(apiUrl)
    projects = requests.get(apiUrl + "projects", headers={'Authorization': 'Bearer ' + token}).text
    projects = json.loads(projects)["values"]
    projectKeys = {}
    for project in projects:
        projectKeys[project["key"]] = project["name"]
        os.makedirs(outputFolder + "/" + project["name"], exist_ok=True)

    for projectKey in projectKeys.keys():
        repos = requests.get(apiUrl + "projects/" + projectKey + "/repos", headers={'Authorization': 'Bearer ' + token}).text
        repos = json.loads(repos)["values"]
        for repo in repos:
            repoFolder = outputFolder + "/" + projectKeys[projectKey] + "/" + repo["name"]
            os.makedirs(repoFolder, exist_ok=True)
            httpUrl = ""

            for links in repo["links"]["clone"]:
                if(links["name"] == "http"):
                    httpUrl = links["href"]

            if(httpUrl.startswith("http://")):
                httpUrl = insert_string(httpUrl, token, 6)
            elif(httpUrl.startswith("https://")):
                httpUrl = insert_string(httpUrl, token, 7)
            print(httpUrl)
            os.system("git clone " + httpUrl + " " + repoFolder)


def insert_string(string, index, token):
    return string[:index] + "x-token-auth:" + token + string[index:]