from __future__ import division
import csv

def rangePercentage(incomp_range, dup_list, file_path, overlap_dict):
    incomp_start = int(incomp_range.split('-')[0])
    incomp_end = int(incomp_range.split('-')[1])
    incomp_lines = range(incomp_start, incomp_end+1)
    for elems in dup_list:
        raw_path = elems[0]
        if file_path == raw_path:
            dup_range = elems[1]
            dup_start = int(dup_range.split('-')[0])
            dup_end = int(dup_range.split('-')[1])
            dup_lines = range(dup_start, dup_end+1)
            common_lines = set(incomp_lines) & set(dup_lines)
            new_rate = round(len(common_lines) / len(incomp_lines) * 100, 1)
            if new_rate > 0:
                file_range = file_path + '+' + dup_range
                if file_range in overlap_dict:
                    old_rate = overlap_dict[file_range]
                    if new_rate > old_rate:
                        overlap_dict[file_range] = new_rate
                else:
                    overlap_dict[file_range] = new_rate
    return overlap_dict

def overlap(dup_list, dup_files):
    overlap_dict = dict()
    with open('../raw_data/inconsistant_couples.csv') as f:
        csvreader = csv.reader(f)
        next(csvreader, None)
        for row in csvreader:
            path1 = row[0]
            range1 = row[1]
            path2 = row[2]
            range2 = row[3]
            if path1 == '_home-students_mlouki_androidReleases_systemApps_AcDisplay_3.0.5_AcDisplay-3.0.5_project_app_src_main_java_com_achep_acdisplay_utils_BitmapUtils.java' or path2 == '_home-students_mlouki_androidReleases_systemApps_AcDisplay_3.0.5_AcDisplay-3.0.5_project_app_src_main_java_com_achep_acdisplay_utils_BitmapUtils.java':
                print row
            if path1 in dup_files:
                overlap_dict = rangePercentage(range1, dup_list, path1, overlap_dict)
            if path2 in dup_files:
                overlap_dict = rangePercentage(range2, dup_list, path2, overlap_dict)
    '''for k in overlap_dict:
        v = overlap_dict[k]
        if v > 50:
            print v, k'''
    for v in overlap_dict.values():
        print v
    return

if __name__ == '__main__':
    dup_list = list()
    dup_files = set()
    with open('../data/cloned_app_code.csv', 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            dup_list.append([row[0], row[1]])
            dup_files.add(row[0])
    overlap(dup_list, dup_files)