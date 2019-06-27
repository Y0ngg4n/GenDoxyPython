import sys
import Bitbucket as bb
import requests

def getArguments():
    if(len(sys.argv) < 6):
        print("Please provide at least 5 Parameter!")
        return
    username = sys.argv[2]
    password = sys.argv[3]
    baseUrl = sys.argv[4]
    outputFolder = sys.argv[5]

    if(sys.argv[1]== "bitbucket"):
        print("Using BitBucket as RMS")
        bb.getProjects(baseUrl, username, password, outputFolder)

if __name__ == "__main__":
    getArguments();