import argparse
import io
from PyPDF2 import PdfFileWriter, PdfFileReader

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, help='Enter the idcard directory.')
    parser.add_argument('--start-page', type=int, default=0, help='Enter the idcard directory.')
    parser.add_argument('--end-page', type=int, default=1000, help='Enter the idcard directory.')
    parser.add_argument('--output-file', type=str, help='Enter the idcard directory.')
    parser.add_argument('--from-start', type=bool, default=False, help='from page 0 to the end page desinated')
    parser.add_argument('--to-end', type=bool, default=False, help='from page desinated to the last page')
    args = parser.parse_args()
    print ("parse args complete")
    return args

if __name__ == '__main__':
    # get the args
    args = getArgs()
    input_path = args.input_file
    start_page = args.start_page
    end_page = args.end_page
    output_path = args.output_file
    from_start = args.from_start
    to_end = args.to_end
    # setup the args
    pdf_file = PdfFileReader(open(input_path, "rb"))
    pdf_pages_len = pdf_file.getNumPages()
    if (from_start == True and to_end == True):
        start_page = 0
        end_page = pdf_pages_len
    elif (from_start == True and to_end == False):
        start_page = 0
    elif (from_start == False and to_end == True):
        end_page = pdf_pages_len
    else:
        print('...')
    # trim the file
    output = PdfFileWriter()
    for i in range(start_page - 1, end_page):
        output.addPage(pdf_file.getPage(i))
    outputStream = open(output_path, 'wb')
    output.write(outputStream)
    print('finished the trim of the pdf')
    print('write to %s' %output_path)

