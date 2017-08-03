# FileSearcher
# Author: Maxence Weyrich
# Version: 8/3/2017
#
# PYTHON 3 REQUIRED
#
# Searches the contents of files for the given string.
# Can be used to search recursively by looking at all the files
# in all the subfolders.


from sys import *
import os


class FoundFiles:
    def __init__(self, fileName, lineNumber, filePath, isError):
        self.fileName = fileName
        self.filePath = filePath
        self.lineNumber = lineNumber
        self.isError = isError


def main():

    #Verifying that arguments are valid
    if not (len(argv) == 3 or len(argv) == 4):
        print("\nSeaches all files in the specified folder for the specified string.\n\npython FileSeacher.py SEARCH PATH [FLAGS]\n\n SEARCH        The string to search for.\n PATH          The directory to search.\n FLAGS         Search modifiers, see below.\n\n\nFlags\n -s        Searches folder and all subfolders for the string\n -e        Prints out all files that could not be read\n\nFlags can be combined together. (E.g.: -se)")
        exit()
    try:
        searchKey = argv[1]
        pathKey = argv[2]
        #reformatting the pathkey without ending "/" characters and changes "\" to "/"
        while len(pathKey) > 0 and ((pathKey[len(pathKey)-1] == "/") or (pathKey[len(pathKey)-1] == "\\")):
            pathKey = pathKey[:len(pathKey)-1]
        if pathKey.find("\\"):
            newPath = []
            for i in range(len(pathKey)):
                if pathKey[i] == "\\":
                    newPath.append("/")
                else:
                    newPath.append(pathKey[i])
            pathKey = "".join(newPath)

        if not os.path.isdir(pathKey):
            print("\nPath is either incorrect, or is not a folder")
            return
        searchSubfolders = (len(argv) == 4 and not argv[3].find("s") == -1)
        logErrors = (len(argv) == 4 and not argv[3].find("e") == -1)
    except:
        print("\nSeaches all files in the specified folder for the specified string.\n\npython FileSeacher.py SEARCH PATH [FLAGS]\n\n SEARCH        The string to search for.\n PATH          The directory to search.\n FLAGS         Search modifiers, see below.\n\n\nFlags\n -s        Searches folder and all subfolders for the string\n -e        Prints out all files that could not be read\n\nFlags can be combined together. (E.g.: -se)")
        print("Note: terminating the path with ' \\\" ' character will escape the ' \" ' character. Use ' \\\\ ' or use ' / '")
        exit()

    #reformatting the search string
    searchKey = searchKey.split("||")

    #announce the search
    foundFiles = []
    if searchSubfolders:
        print ("\nSearching " + pathKey + "/ and all subfolders for files containing the string(s)", end=" ")
        for key in searchKey:
            print (" '" + key + "'", end=" ")
        print ("")
    else:
        print ("\nSearching " + pathKey + "/ for files containing the string(s)", end=" ")
        for key in searchKey:
            print(" '" + key + "'", end=" ")
        print("")

    #do search using recursion
    searchFolder(pathKey, foundFiles, searchKey, searchSubfolders, logErrors)

    #print the matches (if applicable)
    if len(foundFiles) > 0:
        #print("\nFound "+str(len(foundFiles))+" results:\n")
        foundString = []
        errorString = []
        errorCount = 0
        for foundFile in foundFiles:
            if(foundFile.isError):
                errorCount += 1
                errorString.append("%-45s    %s\n" % (foundFile.fileName, foundFile.filePath))
            else:
                foundString.append("%-30s   %-5d    %s\n" % (foundFile.fileName, foundFile.lineNumber, foundFile.filePath))
        if(len(foundString) > 0):
            print("\nFound  "+str(len(foundFiles)-errorCount)+" results:\n\n"+"".join(foundString))
        else:
            print("\nNo matches found!\n")
        if(logErrors and len(errorString) > 0):
            print("\nErrors ecountered in "+str(errorCount)+" files:\n\n"+"".join(errorString))
        elif(logErrors):
            print("\nNo errors reading files.")
    else:
        print("\nNo matches found!")
    print("")

def searchFolder(path, foundFiles, searchKeys, searchSubfolders, logErrors):
    files = os.listdir(path)
    for file in files:
        try:
            if os.path.isfile(str(path)+"/"+str(file)):
                try:
                    thisFile = open(str(path)+"/"+str(file), "r")
                    lineCount = 0
                    if findInString(str(file), searchKeys):
                        foundFiles.append(FoundFiles(file, lineCount, str(path)+"/"+str(file), False))
                    for line in thisFile:
                        lineCount+=1
                        if findInString(line, searchKeys):
                            foundFiles.append(FoundFiles(file, lineCount, str(path)+"/"+str(file), False))
                except:
                    if(logErrors):
                        foundFiles.append(FoundFiles(">>> READ ERROR: " + file, -1, str(path)+"/"+str(file), True))
            elif searchSubfolders:
                searchFolder(path+"/"+file, foundFiles, searchKeys, searchSubfolders, logErrors)
        except:
            pass


def findInString(string, keyList):
    for strn in keyList:
        if string.find(strn) != -1:
            return True
    return False


if __name__ == "__main__":
   main()
