import csv, os, xmltodict

def loadRange():
    range_dict = dict()
    index = 1
    with open('RQ4_input.csv', 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader, None)
        for row in csvreader:
            project = row[0].split('/')[1]
            start = int(row[1])
            end = int(row[2])
            if project in range_dict:
                range_dict[project][index] = [start, end]
            else:
                range_dict[project] = {index: [start, end]}
            index += 1
    return range_dict

def cloneInfo(clone_snippet):
    file_path = clone_snippet['@file']
    if '@' in file_path:
        file_name = int(file_path.split('/')[-1].split('@')[0])
    else:
        file_name = file_path.split('/',1)[-1]
    start = int(clone_snippet['@startline'])
    end = int(clone_snippet['@endline'])
    return file_name, start, end

def isInSide(range1, range2):
    if range1[0] >= range2[0] and range1[1] <= range2[1]:
        return True
    return False

if(__name__ == '__main__'):
    range_dict = loadRange()
    for project in range_dict:
        print project
        if os.path.exists('RQ4_output/%s/clone_in_releases.xml' %project):
            release_clone_dict = dict()
            with open('RQ4_output/%s/clone_in_releases.xml' %project) as f:
                reader = f.read()
                clone_res = xmltodict.parse(reader)
                for a_pair in clone_res['clones']['clone']:
                    snippet1 = a_pair['source'][0]
                    snippet2 = a_pair['source'][1]
                    file1, start1, end1 = cloneInfo(snippet1)
                    file2, start2, end2 = cloneInfo(snippet2)
                    reuse_range_dict = range_dict[project]
                    if file1 in reuse_range_dict:
                        reuse_range = reuse_range_dict[file1]
                        if isInSide(reuse_range, [start1, end1]):
                            if file1 in release_clone_dict:
                                release_clone_dict[file1].add(file2)
                            else:
                                release_clone_dict[file1] = set([file2])            
            for snippet_num in release_clone_dict:
                print ' ', snippet_num
#                for file_name in sorted(release_clone_dict[snippet_num]):
#                    print '\t', file_name
                rel_set = set()
                for file_name in release_clone_dict[snippet_num]:
                    rel_set.add(file_name.split('/')[0])
                print '     (%d)' %len(rel_set)
                for a_rel in rel_set:
                    print '\t', a_rel
                
                