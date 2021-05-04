import io
import os
import sys
import argparse
from PyPDF2 import PdfFileWriter, PdfFileReader

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str, help='Enter the input pdf file.')
    parser.add_argument('--split-list', nargs='+', type=int, help='Enter the split list.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def checkSplitList(split_list, page_max_num) -> bool:
    # reorder of split_list
    split_list.sort()
    # judge the page_max_num 
    if (split_list[len(split_list)-1] > page_max_num or split_list[0] <= 1):
        print("split_list element is bigger than page_max_num or smaller than 1.")
        return False
    # convenience for PyPDF2 split
    for i in range(len(split_list)):
        split_list[i] = split_list[i] - 1
    print("split_list is Good to go.")
    return True

def splitPDF(split_list, pdf_file, output_dir): 
    split_list.insert(0, 0)
    split_list.append(pdf_file.getNumPages())
    print("processed split_list: ")
    print(split_list)
    for i in range(len(split_list) - 1):
        pdf_writer = PdfFileWriter()
        start_p = split_list[i]
        end_p = split_list[i+1]
        for ii in range(start_p, end_p):
            pdf_writer.addPage(pdf_file.getPage(ii))
        output_path = output_dir + "split" + ("_%s" % (start_p+1)) + ("_%s" % end_p) + ".pdf"
        print(output_path)
        output_stream = open(output_path, 'wb')
        pdf_writer.write(output_stream)
        print("write to %s" %output_path)   
    print("finished func splitPDF.")

if __name__ == "__main__":
    # get args
    args = getArgs()
    input_path = args.input_path
    output_dir = os.path.dirname(input_path)
    split_list = args.split_list
    # check split_list
    pdf_file = PdfFileReader(open(input_path, "rb"))
    pdf_pages_num = pdf_file.getNumPages()
    print ("Pages: %d" %pdf_pages_num)
    if (not checkSplitList(split_list, pdf_pages_num)):
        print("split_list is not right.")
        print("Program exit.")
        sys.exit()
    # split and output the pdf
    splitPDF(split_list, pdf_file, output_dir)
    print("Finshed spliting the pdf.")