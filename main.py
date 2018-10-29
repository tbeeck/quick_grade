#!/usr/bin/env python

import os
import sys
import shutil
import re
import subprocess

# Evaluate parameters before starting
argSet = set()
for arg in sys.argv[1:]:
    argSet.add(arg)

# Set of student names:
students = set()
# Messages to output at the end of everything:
outputMessages = []

# Add students to set and make folders for each of them.
for file in os.listdir("./"):
    student = file.split("_")[0]
    students.add(student)

    # Make directory for the student...
    studentdir = "./" + student
    if not os.path.isdir(studentdir):
        os.mkdir(studentdir)
        print("Folder created for: " + student)

    # Move student file to their directory that should exist by now.
    if os.path.isfile(file):
        shutil.move(file, studentdir + "/" + file)

# Keep a list of everything to compile after this walk.
filesToCompile = set()

# Now we step through the whole file tree, renaming files appropriately.
for folderName, subFolders, fileNames in os.walk("./"):
    # print("Processing folder: " + folderName)

    # Reference filename: lastfirst_late_4145_839726_Exercise11_01-1.java
    for filename in fileNames:
        # Piece together file names
        fileSplit = filename.split("_")

        # name starts at index 3 if not late, if late then index 4
        startIndex = 3 if not "_late_" in filename else 4
        className = fileSplit[startIndex] 
        # If there are additional underscores, append them to the class name.
        for piece in fileSplit[(startIndex + 1):]:
            className += "_" + piece

        # Get rid of any additional submission marks, like -1.java or -2.java
        className = re.sub("-[0-9]*.java", ".java", className)

        # Rename the files to their "real" names that should compile...
        # print("Renaming " + folderName + "/" + filename + " to " +folderName + "/" + className)
        oldLocation = folderName + "/" + filename
        newLocation = folderName + "/" + className
        shutil.move(oldLocation, newLocation)

        if newLocation.endswith(".java"):
            filesToCompile.add(newLocation)

# After the walk, do some operations:
# java: attempt to compile java files.
if "java" in argSet:
    for sourceFile in filesToCompile:
        # Source file looks like: ./lastfirst/Exercise12_21.java
        workingDir =  "./" + sourceFile.split("/")[1]
        filename = sourceFile.split("/")[2]

        exitCode = subprocess.call(["javac", filename],
                                cwd=workingDir)
        if exitCode != 0:
            outputMessages.append("[javac] Failed to compile: " + sourceFile)

# Sort and display output messages.
outputMessages.sort()
for message in outputMessages:
    print(message)