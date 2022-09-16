# This is a sample Python script.

import PyPDF2
import xlsxwriter
import re

# open the pdf file
object = PyPDF2.PdfFileReader("test.pdf")

# get number of pages
NumPages = object.getNumPages()

# define keyterms
String = "VE09"
String1 = "TE09"
String2 = "AS09"
ch = "AS09.01"
AllText=""
ch1="6.10 Self-tests"
# extract text and do the search
for i in range(0, NumPages):
    PageObj = object.getPage(i)

    Text = PageObj.extractText()

    AllText = AllText + Text

AllText = AllText.replace("© ISO/IEC 2014 – All rights reserved", "\n*****************************************************************************\n" )
AllText = AllText.replace("LICENSED TO MINISTRY OF IT-STQC DIRECTORATE - CORPORATE LICENSE FOR INTERNAL USE AT THIS LOCATION ONLY, SUPPLIED BY BOOK SUPPLY BUREAU.", "\n*****************************************************************************\n" )


# Remove all characters before the ch from string
before, sep, after = AllText.partition(ch)
if len(after) > 0:
    AllText = after
#print(AllText)

# Remove all characters after the ch1 from string
head, sep, tail = AllText.partition(ch1)
if len(head) > 0:
    AllText = head
AllText = AllText.replace(String2, "\n==========================\n(((((((((((((((\n\n\n\n"+String2)
AllText = AllText.replace(String, "\n==========================\n"+String)
AllText = AllText.replace(String1, "\n==========================\n~~~~~~~~~~~~~~~~~~~~~~~~~\n"+String1)
AllText = AllText.replace("Required Test Procedures", "\n===============================\n\n******Required Test Procedures******\n" )
print(AllText)