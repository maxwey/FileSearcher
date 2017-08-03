# FileSearcher
Searches files, and subdirectories for the specified search key

**PYTHON 3 REQUIRED**

Searches the contents of files for the given string. Will match with either text contained within the file or the filename itself. Can be used to search recursively by looking at all the files in all the subfolders. The output contains the title of the file, the line number the match was found on, and the absolute path of the file. A match with the filename itself will have a line number of 0.

The search string can be multiple parts: using the `||` delimiter in the search string will cause the program to search for any one of the search keys to appear in the file(s).

By default, it will only search in the current directory for search matches. Using the `-s` flag will indicate to search recursively. In addition, by default, the program will skip files that it cannot open for reading (such as binary files, or files it does not have permission to read). Using the `-e` flag will cause the program to print out all of these skipped files. 
