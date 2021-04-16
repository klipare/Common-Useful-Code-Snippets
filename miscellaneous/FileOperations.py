import os
from os import getcwd
from os import listdir
from os.path import isfile, join
import numpy as np

# set the number of files to be created
n = 20
print('number of files to create', n)

# create files with the file number in name based on sequence 1,2,3,....,n having content as the file number
i = 1
while i <= n:
    print('create file', i)
    try:
        # Needed to search on google for a way to pass varibales as a file name
        # pass counter value as file number to the file name
        r = open('%s_file.txt' % i, 'w', encoding='utf-8')
        # since a text file requires only string values as input, converting the file number i into string
        r.write(str(i))
    finally:
        # when no error found close the file
        r.close()
    # iterate the counter
    i = i+1

# Needed to search on google how to list only files in a directory and store them in a list
# get list of files in current working directory
cwd = os.getcwd()
print("current working directory", cwd)
# Assign only files from the listed objects in a directory to a varibale
filenames = [f for f in listdir(cwd) if isfile(join(cwd, f))]
#sort files based on the numerical value
sorted(filenames[:])
print("list of files in current working directory", filenames[:])

# read files created previously based on sequence 1,2,3,....,n show first line contents of the file
print('read first line contents of all files created previously')
j = 0
while j < n:
    print('read file', j)
    try:
        file = filenames[j]
        print(file)
        a = open(file, 'r', encoding='utf-8')
        print(a.readline())
        a.close()
    finally:
        # when no error found iterate the counter
        j = j+1

# merge all n file contents based on sequence 1,2,3,....,n
print('merge files sequentially')
k = 0
while k < n:
    print('reading file', k)
    try:
        # assign a variable to get the file name from the list
        file = filenames[k]
        print(file)
        with open('merge_file.txt', 'a', encoding='utf-8') as p:
            # open the file using the filename stored as an element of the list
            r = open(file, 'r', encoding='utf-8')
            p.writelines(r)
            p.write('\n')
    finally:
        # when no error found iterate the counter
        k = k+1
