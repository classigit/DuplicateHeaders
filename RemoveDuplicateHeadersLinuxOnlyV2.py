################################################################################
#
#   Duplicate header finder:
#   This script goes over all the .cc/.h files and looks for duplicate headers
#
################################################################################
import os
import collections
import sys

DIR_PATH = r''

ext = [".cpp", ".cc", ".c", ".h"]
ext_without_h = [".cpp", ".cc", ".c"]


def ParseFile(file, filepath):
    headers_list = []
    for line in file:
        if '#include' in line:
            if '//' in line:
                line = line.split('//')[0].strip()
            if '/*' in line:
                line = line.split('/*')[0].strip()
            try:
                _, header = line.rsplit(' ', 1)
                headers_list.append(header.strip())
            except ValueError:
                pass
    return headers_list


def getLineNumber(filepath, lookup):
    with open(filepath) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                return num

def fix(file,n):
    with open(file, "r") as infile:
        lines = infile.readlines()

    with open(file, "w") as outfile:
        for pos, line in enumerate(lines):
            if pos != n:
                outfile.write(line)

def fix2(file,n):
    os.system("sed -i '" + str(n) + "d' " + file)


for root, dirs, files in os.walk(DIR_PATH):
    for filename in files:
        if filename.endswith(tuple(ext)):
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            with open(filepath, "r") as f:
                headers_list = ParseFile(f, filepath)
                dupes_list = [item for item, count in collections.Counter(headers_list).items() if count > 1]
                if dupes_list:
                    print filepath, "DUPES:", dupes_list
                if filepath.endswith(tuple(ext_without_h)):
                    _, file_extension = os.path.splitext(filepath)
                    h_filepath = filepath.replace(file_extension, '.h')
                    if os.path.isfile(h_filepath):
                        with open(h_filepath, "r") as f_h:
                            h_headers_list = ParseFile(f_h, h_filepath)
                            new_set =  set(h_headers_list) & set (headers_list)
                            if(new_set):
                                print h_filepath + ' & ' + filename +' HAVE '+ ', '.join(new_set)
                                for element in new_set:
                                    cpp_file = h_filepath.replace(os.path.splitext(h_filepath)[1], os.path.splitext(filename)[1])
                                    line = getLineNumber(cpp_file , element)
                                    print("FIX: " + cpp_file , ": " + str(line))
                                    fix2(cpp_file,line)
