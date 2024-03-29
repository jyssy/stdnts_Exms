#!/usr/bin/env python3

# This script uses the IE data to create GPA and unit rows in the STS so exam numbers can be created later on

import csv
import pandas as pd
import numpy as np
from datetime import datetime
import os
import re
import glob

# Globbing the file extension 
file_type = ".txt"
iuieExtract = glob.glob("*" + file_type)

# opening the 'globbed' text file and adding the comma separations
for file in iuieExtract:	
	with open(file, 'r') as gpas1:
		gpas2 = csv.reader(gpas1, delimiter='\t')
		with open('gpahours.csv', 'w') as gpas:
			gpaswriter = csv.writer(gpas, delimiter=',')
			for line in gpas2:
				gpaswriter.writerow(line)

# the csv getting the new column 'ExamNumber' + 'CumulativeGPA' as well as doing the SUMS and stringigying 'University ID'
# missingen = pd.read_csv('gpaextract.csv', dtype = 'str')
missingen = pd.read_csv('gpahours.csv', converters={'University ID': lambda x: str(x), 'Term Code': lambda x: str(x)})

missingen['TermUnits'] = missingen['Total Term Units'] + missingen['Units In Progress For GPA']
missingen['CumulativeUnits'] = missingen['Total Cumulative Units'] + missingen['Units In Progress For GPA']
missingen['ExamNumber'] = ""
missingen['CumulativeGPA'] = ""

# writing this new organization to a CSV
missingen.to_csv('gpahours2.csv', index=False)

# opening the CSV and reading all the needed columns
gpahourspd = pd.read_csv('gpahours2.csv', converters={'University ID': lambda x: str(x)}) [['University ID', 'Term Code', 'ExamNumber', 'CumulativeGPA', 'TermUnits', 'CumulativeUnits']]

# 'University ID' needs to be 'IUID' and 'Term Code' should be ''Term' in the final document
gpahourspd.rename(columns={"University ID":"IUID"}, inplace=True)
gpahourspd.rename(columns={"Term Code":"Term"}, inplace=True)

# writing all tha data to the XLSX according to the template
filedate = datetime.now().strftime("%Y%m%d%H%M")

# termcode = gpahourspd.values['Term']
termcode = str(gpahourspd.loc[1].Term)

# termcode = '4232'
gpahourspd.to_excel('NewGPAsno' + '-' + filedate + '-' + termcode + '.xlsx', index=0)

# removing the temporary csv document
os.remove('gpahours.csv')
os.remove('gpahours2.csv')

# final check is a print if all has run as expected
print('newGPAsno populated')
            

