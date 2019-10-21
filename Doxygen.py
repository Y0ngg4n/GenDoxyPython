import os
import subprocess


def generateDocumentation(repoFolder, repoName, outputBranchDir, branch):
    os.system("cp /data/doxygen/Doxyfile Doxyfile.conf")
    os.system("echo \"OUTPUT_DIRECTORY = " + outputBranchDir + "\" >> Doxyfile.conf")
    os.system("echo \"INPUT = " + repoFolder + "\" >> Doxyfile.conf")
    os.system("echo \"PROJECT_NAME = " + repoName + "\" >> Doxyfile.conf")
    os.system("echo \"PROJECT_BRIEF = " + branch + "\" >> Doxyfile.conf")
    print("Switching to " + branch)
    os.system("cd " + repoFolder + " && git checkout " + branch)
    proc = subprocess.Popen("git describe", stdout=subprocess.PIPE, shell=True)
    lines = proc.stdout.readlines()
    if len(lines) > 0:
        os.system("echo \"PROJECT_NUMBER = " + lines[0] + "\" >> Doxyfile.conf")
    os.makedirs(outputBranchDir, exist_ok=True)
    os.system("doxygen Doxyfile.conf")
