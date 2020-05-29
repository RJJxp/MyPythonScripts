import os
import argparse
import matplotlib.pyplot as plt

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-path', default='', type=str, help='Enter the log path')
    print('finished parsing args.')
    return parser.parse_args()

def getData(log_path):
    # get the acc lines
    acc_lines = []
    with open(log_path, 'r') as log_file:
        log_lines = log_file.readlines()
        log_line_num = len(log_lines)
        for i in list(range(log_line_num)):
            log_line = log_lines[i].strip()
            if (log_line == "call reset()"):
                acc_lines.append(log_lines[i-2])
    print("Read %d acc line" %len(acc_lines))
    # get the acc value
    acc_value = []
    for acc_line in acc_lines:
        equal_idx = acc_line.find("=")
        if (equal_idx != -1):
            acc = acc_line[equal_idx+1:].strip()
            acc_value.append(float(acc))
    print("Get %d acc data" %len(acc_value))

    print("finished get data func.")
    return acc_value

def drawAcc(acc_value):
    x_cor = list(range(len(acc_value)))
    y_cor = acc_value
    plt.plot(x_cor, y_cor)
    plt.show()
    print("finished drawAcc value.")


if __name__ == "__main__":
    args = getArgs()
    log_path = args.log_path
    acc = getData(log_path)
    drawAcc(acc)
    print("finished all.")

    