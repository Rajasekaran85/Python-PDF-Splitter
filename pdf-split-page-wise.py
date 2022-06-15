import os
import fitz
from pikepdf import Pdf
from datetime import datetime


print("\n PDF Splitter - Single Page wise PDF \n")
print("\n Application Split the PDF by each page wise \n")
print("\n Date: 15 June 2022 \n\n")

# using fitz library for creating the split pdf
# using pikepdf library for applying the file creation datetime & fast web view

filepath1 = input(" Enter the File path: ")

filepath = filepath1 + "\\"

filelist = os.path.isdir(filepath)

directory = "Output"

Out = filepath + directory + "\\"

# creating the output directory
if os.path.exists(Out):
    pass
else:
    os.mkdir(Out)

#delete if pdf file already present in the Output folder
for rem in os.listdir(Out):
	if rem.endswith('.pdf'):
		os.remove(Out + rem)


# Loop convert the combined pdf into page level pdf 
print("\n Extracting the Pages ... \n")
for fname in os.listdir(filepath):
	if not fname.endswith(".pdf"):
		continue
	path = os.path.join(filepath, fname)
	pdfname = os.path.splitext(fname)[0]
	input_file = fitz.open(path)
	for n, page in enumerate(input_file, start=0):  # n = for each page number
		new_pdf = fitz.open()
		new_pdf.insert_pdf(input_file, from_page=n, to_page=n)
		output_file = Out + "Extract-" + pdfname + "_" + f"{n+1:03}" + '.pdf'
		new_pdf.save(output_file)                   # saving the extracted pdf file (this is not final file)
		new_pdf.close()
		with Pdf.open(output_file) as pdf:           # assign the pdf creation datetime & fastweb view for the page level pdf
			rem = "Extract-"
			final =  output_file.replace(rem, "")
			with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:         # set_pikepdf_as_editor=False for applying the Producer value
				meta["pdf:Producer"] = "pikepdf"
				meta["xmp:CreateDate"] = datetime.now(datetime.utcnow().astimezone().tzinfo).isoformat()   # Current date of file saving date
				meta["xmp:ModifyDate"] = datetime.now(datetime.utcnow().astimezone().tzinfo).isoformat()
			pdf.save(final, linearize=True)
			pdf.close()
			print(final)
		os.remove(output_file)                                            # delete the intermediate extracted pdf file
