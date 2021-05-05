import io
import os
import sys
import argparse
from PyPDF2 import PdfFileWriter, PdfFileReader

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the input pdf file.')
    parser.add_argument('--add-blank', action="store_true", help='To add blank page to separate pdf when merge.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def mergePDF(input_dir, add_blank):
    all_pdfs = os.listdir(input_dir)
    # order the filenames
    all_pdfs.sort(key=lambda x:int(x[-8:-4]))
    print("All PDF read: ")
    print(all_pdfs)
    output_pdf_path = os.path.join(input_dir, "merge.pdf")
    pdf_writer = PdfFileWriter()
    for each_pdf in all_pdfs:
        pdf_path = os.path.join(input_dir, each_pdf)
        pdf_file = PdfFileReader(open(pdf_path, "rb"))
        pdf_pages_num = pdf_file.getNumPages()
        print("************ NEW PDF ************")
        print("Pages: %d" %pdf_pages_num)
        for i in range(pdf_pages_num):
            pdf_writer.addPage(pdf_file.getPage(i))
        if (add_blank == True):
            pdf_writer.addBlankPage()
            print("Add blank page to this pdf.")
        else:
            pass
        output_stream = open(output_pdf_path, 'wb')
        pdf_writer.write(output_stream)
        print("************ PDF DONE ************")
    print("finished func mergePDF.")

if __name__ == "__main__":
    args = getArgs()
    input_dir = args.input_dir
    add_blank = args.add_blank
    mergePDF(input_dir, add_blank)
    print ("finished merge pdf.")
