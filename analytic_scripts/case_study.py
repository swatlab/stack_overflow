from __future__ import division
import csv, shutil
import pandas as pd
from numpy import median

def loadAppCodeDate(csv_path):
    app_date_dict = dict()
    with open(csv_path, 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader, None)
        for row in csvreader:
            file_path = row[0]
            clone_range = row[1]
            creation_date = row[2]
            app_date_dict[file_path + '+' + clone_range] = creation_date
    return app_date_dict

def firstAppDuplication(app_file_set, app_date_dict, app_dup_dict):
    earlist_date = None
    first_dup_file = None
    for app_file in app_file_set:
        if app_file in app_dup_dict:
            created_date = app_date_dict[app_file]
            if earlist_date:
                if created_date < earlist_date:
                    first_dup_file = app_file
            else:
                earlist_date = created_date
                first_dup_file = app_file
    return first_dup_file


def calculateLineNumber(clone_range):
    return int(clone_range.split('-')[1]) - int(clone_range.split('-')[0]) + 1

def RQ1(app_dup_dict):
    print 'Android apps clone snippet number:', len(app_dup_dict)
    app_cloned_lines = list()
    app_file_set = set()
    app_name_set = set()
    dup_in_app_dict = dict()
    clone_class_list = list()
    clone_file_set = set()
    for app_file_range in app_dup_dict:
        app_file = app_file_range.split('+')[0]
        clone_file_set.add(app_file)
        app_name_set.add('/'.join(app_file.split('/')[:2]))
        app_file_set.add(app_file)
        clone_range = app_file_range.split('+')[1]
        clone_line_num = calculateLineNumber(clone_range)
#        if clone_line_num > 50:
#            print app_file_range
        app_cloned_lines.append(clone_line_num)
        for stack_snippet in app_dup_dict[app_file_range]:
            stack_id = stack_snippet.split('+')[0]
            similarity = int(stack_snippet.split('+')[1])
            if stack_id in dup_in_app_dict:
                dup_in_app_dict[stack_id].add(app_file_range)
            else:
                dup_in_app_dict[stack_id] = set([app_file_range])
#            if similarity > 90:
#                print app_file_range, stack_id, similarity
    #print sorted(app_cloned_lines)
    print 'Android apps median cloned lines:', median(app_cloned_lines)
    print 'App file number:', len(app_file_set)
    print 'App name number:', len(app_name_set)
    multi_app_clone_count = 0
    for stack_id in dup_in_app_dict:
        app_list = dup_in_app_dict[stack_id]
        #print len(app_list)
        clone_class_list.append(app_list)
        if len(app_list) > 1:
#            print stack_id, app_list
            multi_app_clone_count += 1
#            if len(app_list) > 3:
#                print stack_id, app_list
    print 'Number of groups where more than one apps cloned from a post:', multi_app_clone_count
    return clone_file_set, clone_class_list

def RQ2(clone_file_set):
    for app_file_path in clone_file_set:
        file_old_path = '_home-students_mlouki_androidReleases_' + '_'.join(app_file_path.split('/'))
        input_dir = '../inconsistent_files/'
        output_dir = '../RQ2/'
        shutil.copyfile(input_dir+file_old_path, output_dir+file_old_path)
    return

def RQ3(stack_dup_dict):
    post_date_dict = dict()
    with open('../data/post_date.csv') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row[1] in post_date_dict:
                post_date_dict[row[1]].add(row[0])
            else:
                post_date_dict[row[1]] = set([row[0]])
    large_chunk_set = set()
    line_num_list = list()
    post_ids = set()
    for stack_file_range in stack_dup_dict:
        clone_range = stack_file_range.split('+')[1]
        line_num = calculateLineNumber(clone_range)
        line_num_list.append(line_num)
        stack_file = stack_file_range.split('+')[0]
        stack_date = stack_file.split('_')[0]
        posts = post_date_dict[stack_date]
        post_ids |= posts
        '''if line_num > 50:            
            for post_id in posts:
                #if post_id in large_chunk_set:
                #    print post_id
                large_chunk_set.add(post_id)'''
#    print line_num_list
    print 'Number of Stack posts containing code cloned from an app:', len(post_ids)
    print 'Median line number of Stack cloned code:', median(line_num_list)
        #stack_date = stack_file.split('_')[0]
        #post_id = post_date_dict[stack_date]
        #print post_id
    return

def laundering(app_dup_dict, stack_dup_dict):
    second_dup_list = list()
    for app_file_range in app_dup_dict:
        for stack_file in app_dup_dict[app_file_range]:
            #print stack_file
            for stack_file_range in stack_dup_dict:
                if stack_file == stack_file_range.split('+')[0]:
                    original_app_name = app_file_range.split('/')[1]
                    original_app_code = app_file_range
                    first_dup_post = stack_file
                    for second_dup_app in stack_dup_dict[stack_file_range]:
                        dup_app_name = second_dup_app.split('/')[1]
                        if original_app_name != dup_app_name:
                            second_dup_list.append([original_app_code, first_dup_post, second_dup_app])
    df_sec_dup = pd.DataFrame(second_dup_list, columns=['2nd_dup_app', '1st_dup_stack', 'original_app']).drop_duplicates()
#    print df_sec_dup
    #df_sec_dup.to_csv('../data/sec_dup.csv', index=False, header=False)
    return

def RQ4(clone_class_list):
    evolution_snippets = list()
    for clone_class in clone_class_list:
        projects_in_clone_class = set()
        for path_range in sorted(clone_class):
            project = path_range.split('/')[1]
            if project not in projects_in_clone_class:
                path = path_range.split('+')[0]#.split('/',1)[-1]
                clone_range = path_range.split('+')[1]
                start_line = clone_range.split('-')[0]
                end_line = clone_range.split('-')[1]
                evolution_snippets.append([path,start_line,end_line])
                projects_in_clone_class.add(project)
    df = pd.DataFrame(evolution_snippets, columns=['path', 'start', 'end'])
    df.to_csv('../raw_data/RQ4_input.csv', index=False)
    return
    
if __name__ == '__main__':
    # app files copied from stack overflow
    app_dup_dict = dict()
    # stack files copied from Android apps
    stack_dup_dict = dict()
    # load app snippets' creation date
    app_date_dict = loadAppCodeDate('../raw_data/creation_date.csv')
    # identify code copied from Stack overflow or from Android apps
    df = pd.read_csv('../data/clone_results.csv')    
    for index,row in df.iterrows():
        stack_file = row['stack_file'].split('/')[-1]
        stack_file_date = stack_file.split('_')[0]
        app_file = row['app_file']
        app_range = row['app_clone_range']
        stack_range = row['stack_clone_range']
        similarity = str(row['similarity'])
        app_file_range = '/'.join(app_file.split('_')[4:]) + '+' + app_range
        stack_file_range = stack_file + '+' + stack_range
        if app_file_range in app_date_dict:
            app_file_date = app_date_dict[app_file_range]
#            print stack_file_date, app_file_date
            if stack_file_date < app_file_date:
                if app_file in app_dup_dict:
                    app_dup_dict[app_file_range].add(stack_file + '+' + similarity)
                else:
                    app_dup_dict[app_file_range] = set([stack_file + '+' + similarity])
            elif stack_file_date > app_file_date:
                if stack_file in stack_dup_dict:
                    stack_dup_dict[stack_file_range].add(app_file_range)
                else:
                    stack_dup_dict[stack_file_range] = set([app_file_range])
    
    # statistics for code cloned from Stack to Android (RQ1)
    clone_file_set, clone_class_list = RQ1(app_dup_dict)
    # RQ2
#    RQ2(clone_file_set)
    # statistics for code cloned from Android to Stack (RQ3)
    RQ3(stack_dup_dict)
    # code laundering couting
    laundering(app_dup_dict, stack_dup_dict)
    # output RQ4's input
#    RQ4(clone_class_list)

