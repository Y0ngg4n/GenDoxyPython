import os

def generateDocumentation(repoFolder, repoName, outputBranchDir, branch):
    os.system("cp /data/doxygen/Doxyfile Doxyfile.conf")
    os.system("echo \"OUTPUT_DIRECTORY = " + outputBranchDir + "\" >> Doxyfile.conf")
    os.system("echo \"INPUT = " + repoFolder + "\" >> Doxyfile.conf")
    os.system("echo \"PROJECT_NAME = \"" + repoName + "\" >> Doxyfile.conf")
    print("Switching to " + branch)
    os.system("cd " + repoFolder + " && git checkout " + branch)
    os.makedirs(outputBranchDir, exist_ok=True)
    os.system("doxygen Doxyfile.conf")