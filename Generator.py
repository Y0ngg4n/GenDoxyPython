import sys
import Bitbucket as bb
import requests

def getArguments():
    if(len(sys.argv) < 5):
        print("Please provide at least 4 Parameter!")
        return
    token = sys.argv[2]
    baseUrl = sys.argv[3]
    outputFolder = sys.argv[4]

    if(sys.argv[1]== "bitbucket"):
        print("Using BitBucket as RMS")
        bb.getProjects(baseUrl, token, outputFolder)



if __name__ == "__main__":
    getArguments();