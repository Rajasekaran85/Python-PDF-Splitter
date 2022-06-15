import os
import pandas as pd
from csv import DictReader
import fitz
from pikepdf import Pdf
from datetime import datetime

print("\n PDF Splitter - certain range of pages from a PDF\n")
print("\n CSV input: Input PDF file name, Start Page number , End Page number, Output PDF file name \n")
print("\n Date: 15 June 2022 \n\n")


# using DictReader csv library for reading the CSV file
# using fitz library for creating the split pdf
# using pikepdf library for applying the file creation datetime & fast web view

filepath1 = input(" Enter the PDF File path: ")

inputfile = filepath1 + "\\"

filelist = os.path.isdir(inputfile)

directory = "Output"

Out = inputfile + directory + "\\"

csv_input = "page_range.csv"  # page range details should update in the csv file.

if os.path.exists(csv_input): # check the csv file present in the tool path
    pass
else:
    print("\n page_range.csv file is missing")

if os.path.exists(Out):
    pass
else:
    os.mkdir(Out)

# opening & reading the csv file
csv_file = open("page_range.csv", "r")
field = pd.read_csv(csv_file, delimiter=',') 


for row in field.iloc():
	Input_file = row[0]         # getting the Input pdf file name
	Filename = row[3]           # getting the Output pdf file name
	Start_Page = int(row[1]-1)  # getting the extract pages start & end number and convert into integer for using insert function 
	End_Page = int(row[2]-1)
	inputpdf = inputfile + "\\" + Input_file
	doc1 = fitz.open(inputpdf)                  # opening the Input PDF file
	output_file = Out + "Extract-" + Filename
	new_pdf = fitz.open()                       # opening the empty output PDF file
	new_pdf.insert_pdf(doc1, from_page=Start_Page, to_page=End_Page)  # extract the mentioned pages from the input pdf and insert into the output pdf file
	new_pdf.save(output_file)                   # saving the extracted pdf file (this is not final file)

	with Pdf.open(output_file) as pdf:          # opening each extracted pdf file and apply the date & time and fast web view
		final = Out + Filename
		with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:         # set_pikepdf_as_editor=False for applying the Producer value
			meta["pdf:Producer"] = "pikepdf"
			meta["xmp:CreateDate"] = datetime.now(datetime.utcnow().astimezone().tzinfo).isoformat()   # Current date of file saving date
			meta["xmp:ModifyDate"] = datetime.now(datetime.utcnow().astimezone().tzinfo).isoformat()
		pdf.save(final, linearize=True)	                             # linearize for assigning the Fastweb view & save final version of extracted pdf
		pdf.close()
	os.remove(output_file)                                            # delete the intermediate extracted pdf file
	print(Filename)
