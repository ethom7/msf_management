# -*- coding: utf-8 -*-

import os
import csv
import sys
import json
import time
from PIL import Image
import pytesseract
import random
import fileinput
import zipfile

""" 
	Initially created August 23, 2016; Updated April 26, 2017; June 22, 2018
	@author: Evan Thompson [ethom7/nave2cool]
	
	Accepts an input file as listed in INPUT_RESOURCE.
	Outputs data to OUTPUT_RESOURCE. 
"""

##--Vars---##
INPUT_RESOURCE = "resources/MSFAllianceData.csv"  # "data/20k.txt"
INPUT_DELIMITER = ','
OUTPUT_RESOURCE = "data/data.json"
SCREENSHOT_ZIP = "resources/msf.zip"
DATA_RESOURCE_DIRECTORY = "data/msf_screenshots"

current_time = time.strftime("%m/%d/%Y-%H:%M:%S")
current_date = time.strftime("%m/%d/%Y")

##--Functions--##


"""
	Function will import a csv or textfile as a list.
	@param	file1: a string with the location of a delimited file.
			delim: a string containing a delimiter, typically a comma ',', space ' ', 
					or other specified entry
"""


def get_csv(file1, delim):
    returnlist = []
    with open(file1, 'U') as csvfile:
        freader = csv.reader(csvfile, delimiter=delim, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in freader:
            returnlist.append(row)

    return returnlist

def unpack_to_target(input_directory, output_directory):
    with zipfile.ZipFile(input_directory, "r") as zip_ref:
        if not os._exists(output_directory):
            os.mkdir(output_directory)
        zip_ref.extractall(output_directory)

def process_data(resource_directory):
    file_list = os.listdir(resource_directory)
    ## update location of the tesseract install
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

    with open('data/tempout.txt', 'w') as out:
        for f in file_list:
            out.write("image name: " + f + "\n\n" +
                      pytesseract.image_to_string(Image.open(resource_directory + "/" + f), lang="eng").encode('utf-8').strip() + "\n\n")

##--Helper-Functions--##

def assembledictionary(header, data):
    returndictionary = {}

    columnlist = []

    ## create a list of values for each column
    for col in range(len(data[0])):
        templist = []
        for row in range(len(data)):
            templist.append(data[row][col])

        columnlist.append(templist)

    # accept input of a row, index is across columns
    for x in range(len(header)):
        returndictionary[header[x]] = columnlist[x]

    return returndictionary

def assembleplayerdictionary(header, data):
    returnlist = []
    returndictionary = {}

    columnlist = []

    ## create a list of values for each column
    for row in range(len(data)):
        tempdict = {}
        for col in range(len(data[0])):
            tempdict[header[col]] = data[row][col]  #need to change this to list of dicts

        columnlist.append(tempdict)

    return columnlist

def output_data_to_json(player_data_list, timestamp):
    output_dict = {}
    output_dict[timestamp] = player_data_list

    with open(OUTPUT_RESOURCE, 'w') as out:
        out.write(json.dumps(output_dict))


##--Main--##

def main():
    ## Run timers
    start_time = time.time()
    print "Starting at %s..." % current_time

    ## Function call with timer
    print "Doing functions..."
    function_start = time.time()

    datalist = get_csv(INPUT_RESOURCE, INPUT_DELIMITER)

    ## datalist contains each row of the data sheet.
    ## Top row is the header, which will be the keys for the output dict,
    ## value is a list of values for each row.
    playerdatalist = assembleplayerdictionary(datalist[0], datalist[1:])

    output_data_to_json(playerdatalist, current_time)

    #unpack_to_target(SCREENSHOT_ZIP, DATA_RESOURCE_DIRECTORY)

    process_data(DATA_RESOURCE_DIRECTORY)

    function_end = time.time() - function_start
    print "Function processing time %.4f seconds" % (function_end,)

    end_time = time.time() - start_time
    print "%.4f seconds" % (end_time,)


if __name__ == '__main__':
    status = main()
    sys.exit(status)