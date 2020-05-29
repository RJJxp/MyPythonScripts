import os
import random
import sys
import argparse
import itertools
import shutil

def getSamePairAndDist(pairs_txt_filename, dist_txt_filename):
    same_pair_id = []
    dist = []
    with open(pairs_txt_filename, 'r') as f1, open(dist_txt_filename, 'r') as f2:
        for line1, line2 in zip(f1.readlines()[1:], f2.readlines()):
            pair = line1.strip().split()
            if (len(pair) == 3):
                same_pair_id.append(pair[0])
                dist.append(line2.strip())    
    print("There is %d same pairs." %len(same_pair_id))
    print("There is %d dist." %len(dist))
    return same_pair_id, dist

def compareJhDist(self_score_filename, same_pair_id, dist, output_filename):
    
    assert len(same_pair_id) == len(dist)

    result_lines = []
    results = []
    with open(self_score_filename, 'r') as f:
        for line in f.readlines():
            jh_id = line.strip().split()[0]
            jh_dist = line.strip().split()[2]
            for pair_id, pair_dist in zip(same_pair_id, dist):
                if (jh_id == pair_id):
                    results.append([jh_id, jh_dist, pair_dist])
                    result_line = "%s" %jh_id + "\t" + "%s" %jh_dist + "\t\t" + "%s" %pair_dist + "\t\t" + "%s" %(float(pair_dist) - float(jh_dist)) + "\n"
                    result_lines.append(result_line)
    print("finished selecting lines. There is %d" %len(result_lines))
    with open(output_filename, 'w') as out_f:
        out_f.writelines(result_lines)
    print("finished output.")
    return results

def checkResults(final_results, thresold, bad_txt_filename):
    bad_results = []
    for result in final_results:
        mybool = (float(result[1]) - thresold) * (float(result[2]) - thresold)
        if mybool <= 0:
            bad_results.append(result)
    # generate bad_results to lines
    lines = []
    for bad_result in bad_results:
        line = "%s" %bad_result[0] + "\t" + "%s" %bad_result[1] + "\t\t" + "%s" %bad_result[2] + "\n"
        lines.append(line)
    # write to file
    with open(bad_txt_filename, 'w') as f:
        f.writelines(lines)
    print("finished checked.")
    return bad_results

def copyBadResults(bad_results, data_dir, output_dir):
    if os.path.exists(output_dir):
        # os.removedirs(output_dir)
        shutil.rmtree(output_dir)
        print('the dir already exists, deleted')
    os.mkdir(output_dir)

    for bad_result in bad_results:
        person_folder = os.path.join(data_dir, bad_result[0])
        for pic in os.listdir(person_folder):
            cpFromPath = os.path.join(person_folder, pic)
            cpToPath = os.path.join(output_dir, pic)
            shutil.copy(cpFromPath, cpToPath)
    print("finished cp bad results")


if __name__ == "__main__":
    same_pair_id, dist = getSamePairAndDist("pairs.txt", "dist.txt")
    final_results = compareJhDist("score_self_5000.txt", same_pair_id, dist, "output.txt")
    bad_results = checkResults(final_results, 1.40, "badresult.txt")
    copyBadResults(bad_results, r"G:\tenghui_data_backup\0414data\test_aligned", "bad_cases_align" )
    print("finished all.")