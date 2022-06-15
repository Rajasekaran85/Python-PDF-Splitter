import os
from pikepdf import Pdf
from datetime import datetime

print("\n PDF Splitter - Single Page wise PDF \n")
print("\n Application Split the PDF by each page wise \n")
print("\n Date: 15 June 2022 \n\n")

# using pikepdf library for creating the page wise pdf

filepath1 = input(" Enter the File path: ")

filepath = filepath1 + "\\"

filelist = os.path.isdir(filepath)

directory = "Output"

Out = filepath + directory + "\\"

if os.path.exists(Out):
    pass
else:
    os.mkdir(Out)

for fname in os.listdir(filepath):
	if not fname.endswith(".pdf"):
		continue
	path = os.path.join(filepath, fname)
	print(fname)
	pdfname = os.path.splitext(fname)[0]
	input_file = Pdf.open(path)
	output_file = Out + pdfname
	for n, page in enumerate(input_file.pages):  # n = for each page number
		new_pdf = Pdf.new()                      # creating new pdf file
		new_pdf.pages.append(page)               # assigning current page to the new created pdf
		with new_pdf.open_metadata(set_pikepdf_as_editor=False) as meta:         # set_pikepdf_as_editor=False for applying the Producer value
			meta["pdf:Producer"] = "pikepdf"
			meta["xmp:CreateDate"] = datetime.now(datetime.utcnow().astimezone().tzinfo).isoformat()   # Current date of file saving date
			meta["xmp:ModifyDate"] = datetime.now(datetime.utcnow().astimezone().tzinfo).isoformat()
		new_pdf.save(output_file + "_"+ f"{n+1:03}" + '.pdf', linearize=True, force_version="1.4")
		new_pdf.close()

