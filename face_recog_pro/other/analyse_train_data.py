import os
import sys
import argparse


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=str, help='Enter the croppedFace directory.')
    parser.add_argument('--output-path', type=str, help='Enter the output directory.')
    args = parser.parse_args()
    print ("parse args complete")
    return args

def analyseIt(input_dir, output_path):
    result = []
    all_folders = os.listdir(input_dir)
    for folder in all_folders:
        rrr = []
        rrr.append(folder)
        rrr.append(len(os.listdir(os.path.join(input_dir, folder))))
        result.append(rrr)
    print("There is %d folders in %s" %(len(all_folders), input_dir))
    return result

def writeIt(result):
    lines = []
    for r in result:
        line = str(r[0]) + "\t" + str(r[1]) + "\n"
        lines.append(line)
    with open("test.txt", 'w') as f:
        f.writelines(lines)
    print("finished writing the result.")

if __name__ == "__main__":
    args = parseArgs()
    input_dir = args.input_dir
    output_path = args.output_path
    result = analyseIt(input_dir, output_path)
    writeIt(result)
    print("finished all.")