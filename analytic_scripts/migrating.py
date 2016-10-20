from __future__ import division
import csv
from datetime import datetime

def loadAppCreationDate():
    app_date_dict = dict()
    with open('../raw_data/creation_date.csv', 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            app_file_range = row[0] + '+' + row[1]
            app_date_dict[app_file_range] = row[2]
    return app_date_dict

def dateDiff(d1_str, d2_str):
    d1 = datetime.strptime(d1_str, '%Y%m%d%H%M%S')
    d2 = datetime.strptime(d2_str, '%Y%m%d%H%M%S')
    return int((d2 - d1).total_seconds()/3600/24)

def loadLaundering(app_date_dict):
    migrating_list = list()
    duration_list = list()
    with open('../data/sec_dup.csv', 'r') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            file1 = row[0].split('+')[0]
            file2 = row[2].split('+')[0]
            orginal_path = '_home-students_mlouki_androidReleases_' + '_'.join(file1.split('/'))
            dup_path = '_home-students_mlouki_androidReleases_' + '_'.join(file2.split('/'))
            migrating_list.append([orginal_path, dup_path])
            original_date = app_date_dict[row[2]]
            sec_dup_date = app_date_dict[row[0]]
            duration_list.append(dateDiff(original_date, sec_dup_date))
    print duration_list
    return migrating_list

def incompatible(dup_list, dup_files, migrating_list):
    incompatible_counter = 0
    with open('../raw_data/inconsistant_couples.csv') as f:
        csvreader = csv.reader(f)
        next(csvreader, None)
        for row in csvreader:
            path1 = row[0]
            range1 = row[1]
            path2 = row[2]
            range2 = row[3]
            for dup_path, original_path in migrating_list:
                if original_path == path1:
                    if dup_path == path2:
                        incompatible_counter += 1
                        print 'incompatibility'
                elif original_path == path2:
                    if dup_path == path1:
                        incompatible_counter += 1
                        print 'incompatibility'
    print incompatible_counter      
    return

if __name__ == '__main__':
    dup_list = list()
    dup_files = set()
    app_date_dict = loadAppCreationDate()
    migrating_list = loadLaundering(app_date_dict)
    incompatible(dup_list, dup_files, migrating_list)