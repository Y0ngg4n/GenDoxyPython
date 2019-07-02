#!/usr/bin/env python
import sys
import Bitbucket as bb
import requests
import os

def getArguments():
    if len(sys.argv) < 6:
        print("Please provide at least 5 Parameter!")
        return
    username = sys.argv[2]
    password = sys.argv[3]
    baseUrl = sys.argv[4]
    outputFolder = sys.argv[5]
    genOutPutFolder = sys.argv[6]

    os.system("echo machine " + baseUrl.replace("http://", "").replace("https://", "") + " >> ~/.netrc")
    os.system("echo login " + username + " >> ~/.netrc")
    os.system("echo password " + password + " >> ~/.netrc")

    if sys.argv[1]== "bitbucket":
        print("Using BitBucket as RMS")
        bb.getProjects(baseUrl, username, password, outputFolder, genOutPutFolder)

if __name__ == "__main__":
    getArguments()