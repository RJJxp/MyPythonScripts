import os
import random
import sys
import argparse
import itertools

# input the aligned face directory and output the pairs.txt in the same folder
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', default='', type=str, help='Enter the aligned face directory')
    parser.add_argument('--same-pair-nums', default=10000, type=int, help='Enter the same pair number')
    parser.add_argument('--diff-pair-nums', default=10000, type=int, help='Enter the diff pair number')
    print('finished parsing args.')
    return parser.parse_args()

def getImageId(file_name):
    id_str = file_name[-8:-4]
    return id_str.lstrip('0') 

def generatePairs(input_dir, same_pair_num, diff_pair_num):
    person_names = os.listdir(input_dir)
    person_num = len(person_names)
    per_same_person_num = int(same_pair_num / person_num)
    if (per_same_person_num < 1):
        per_same_person_num = 1
    # print('len(person_names) is %d, per_same_person_num is %d' %(len(person_names), per_same_person_num))
    # lines to be written into the file
    lines = []
    # same persons' pairs
    print('start generating same person pairs.')
    for person_name in person_names:
        image_names = os.listdir(os.path.join(input_dir, person_name))
        image_num = len(image_names)
        combs = list(itertools.combinations(range(image_num), 2))
        if (len(combs) > per_same_person_num):
            combs = random.sample(combs, per_same_person_num)
        for comb in combs:
            pair_string = person_name + "\t" + getImageId(image_names[comb[0]]) + "\t" + getImageId(image_names[comb[1]]) + "\n"
            lines.append(pair_string)
            # print('same person pair +1s')
    # diff persons' pairs
    diff_lines = []
    diff_combs = list(itertools.combinations(range(person_num), 2))
    print("diff combs is %d" %len(diff_combs))
    print("diff_pair_num is %d" %diff_pair_num)
    # random pick diff_pair_num combs
    if (len(diff_combs) > diff_pair_num):
        diff_combs = random.sample(diff_combs, diff_pair_num)
    print("Now diff combs is %d" %len(diff_combs))
    print('start generating different person pairs.')
    gen_diff_count_n = 0
    for diff_comb in diff_combs:
        person_01_name = person_names[diff_comb[0]]
        person_02_name = person_names[diff_comb[1]]
        person_01_images = os.listdir(os.path.join(input_dir, person_01_name))
        # person_02_images = os.listdir(os.path.join(input_dir, person_02_name))
        person_01_id = getImageId(random.sample(person_01_images, 1)[0])
        # person_02_id = getImageId(random.sample(person_02_images, 1)[0])
        # make sure person1-01, person2-02 or person1-02, person2-01
        if (person_01_id == '1'):
            pair_string = person_01_name + "\t" + person_01_id + "\t" + person_02_name + "\t" + "2" + "\n"
            diff_lines.append(pair_string)
            gen_diff_count_n += 1
        elif (person_01_id == '2'):
            pair_string = person_01_name + "\t" + person_01_id + "\t" + person_02_name + "\t" + "1" + "\n"
            diff_lines.append(pair_string)
            gen_diff_count_n += 1
        else:
            continue

        if (gen_diff_count_n % 1000 == 0):
            print("diff pair +1000")

        # if ((person_01_id == '1' and person_02_id != '1') or (person_01_id != '1' and person_02_id == '1')):
        #     pair_string = person_01_name + "\t" + person_01_id + "\t" + person_02_name + "\t" + person_02_id + "\n"
        #     diff_lines.append(pair_string)
        #     print('diff person pair +1s')
        # else:
        #     continue

    # get the finallines and disorder it
    lines += diff_lines
    random_lines = random.sample(lines, len(lines))
    # write lines into the pairs.txt
    output_file = open(os.path.join(input_dir, 'pairs.txt'), 'w')
    print('start writing lines into the file')
    for l in random_lines:
        output_file.write(l)
    print('finished writing lens into the file')

if __name__ == '__main__':
    args = getArgs()
    input_dir = args.input_dir
    same_pair_num = args.same_pair_nums
    diff_pair_num = args.diff_pair_nums
    generatePairs(input_dir, same_pair_num, diff_pair_num)
