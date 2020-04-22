import os
import argparse

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', default='', type=str, help='')
    parser.add_argument('--output-path', default='', type=str, help='')
    print('finished parsing args.')
    return parser.parse_args()

def readFile(input_path):
    tprfpr_file = open(input_path)
    tpr = []
    fpr = []
    all_rate = []
    for l in tprfpr_file:
        all_rate.append(float(l[1:15]))
        all_rate.append(float(l[16:30]))
        all_rate.append(float(l[31:45]))
        all_rate.append(float(l[46:60]))
    tpr = all_rate[0:400]
    fpr = all_rate[400:800]
    thresold = list(range(400))
    # print(thresold)
    for i in range(len(thresold)):
        thresold[i] /= 100
    # print(thresold)
    tprfpr_file.close()
    print(len(thresold), len(tpr), len(fpr))
    print("finished readFile() and close file.")
    return tpr, fpr, thresold

def writeIt(output_path, tpr, fpr, thresold):
    f = open(output_path, "w")
    for i in range(400):
        s = str(thresold[i]) + '\t' + str(tpr[i]) + '\t' + str(1 - fpr[i]) + '\n'
        f.write(s)
    f.close()
    print("finished writeIt() and close file.")

if __name__ == "__main__":
    args = getArgs()
    input_path = args.input_path
    output_path = args.output_path
    tpr, fpr, thresold = readFile(input_path)
    writeIt(output_path, tpr, fpr, thresold)
    print ("finished all.")