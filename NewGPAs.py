#!/usr/bin/env python3

# This script uses the IE data to create GPA and unit rows in the STS so exam numbers can be created later on

import csv
import pandas as pd
from datetime import datetime
import os
import re

with open('extract_14640404-4222.txt', 'r') as newgpa:
# may not need this term code regex at all (also, see line 23)
	filetxt = str(newgpa)
	termc = re.findall(r'[0-9]{4}', filetxt)
	termcode = (termc[2])
	gpareader = csv.reader(newgpa, delimiter='\t')
	with open('gpaextract.csv', 'w') as gpaextract:
		gpawriter = csv.writer(gpaextract, delimiter=',')
		for line in gpareader:
			gpawriter.writerow(line)
# the csv getting the new column 'Term Code':
missingen = pd.read_csv('gpaextract.csv', dtype = str)
#missingen['Term Code'] = termcode
missingen['ExamNumber'] = ""
missingen.to_csv('gpaextract.csv', index=False)
# the section in which pandas selects the necessary columns from the csv
#newextractpd = pd.read_csv('newextract.csv', dtype = str) 
#OR -- if we apply the dtype=str ONLY to specific columns and not ao ALL the columns as the line does above:
gpaextractpd = pd.read_csv('gpaextract.csv', converters={'University ID': lambda x: str(x)}) [['University ID', 'Term Code', 'Total Term Units', 'ExamNumber',
	'Cumulative Units In Progress For GPA', 'Cumulative GPA']]
# 'University I' needs to be 'IUID' and 'Term Code' should be ''Term' in the final document
gpaextractpd.rename(columns={"University ID":"IUID"}, inplace=True)
gpaextractpd.rename(columns={"Term Code":"Term"}, inplace=True)
gpaextractpd.rename(columns={"Total Term Units":"TermUnits"}, inplace=True)
gpaextractpd.rename(columns={"Cumulative GPA":"CumulativeGPA"}, inplace=True)
gpaextractpd.rename(columns={"Cumulative Units In Progress For GPA":"CumulativeUnits"}, inplace=True)

# writing all tha data to the XLSX according to the template
filedate = datetime.now().strftime("%Y%m%d")
gpaextractpd.to_excel('NewGPAs' + '-' + filedate + '-' + termcode + '.xlsx', index=0)
# removing the temporary csv document
os.remove('gpaextract.csv')
# final check is a print if all has run as expected
print('newGPAs populated')



# Columns for the NewGPSs.xlsx template
# 'IUID'
# 'Term'
# 'TermUnits'
# 'ExamNumber'
# 'CumulativeGPA'
# 'CumulativeUnits'