import csv, os, re

def extractSnippet(project, index, raw_path, start, end):
    with open(raw_path, 'r') as fr:
        #reader = fr.read().split('\n')
        #content = '\n'.join(reader[start-1:end])
        content = fr.read()
        codename = '%d@%s.java'%(index,project)
        print codename
        print content
        print '-'*30
        with open('../raw_data/RQ4/'+codename, 'w') as fw:
            fw.write(content)
    return content

with open('../raw_data/RQ4_input.csv', 'r') as f:
    csvreader = csv.reader(f)
    next(csvreader, None)
    index = 1
    for row in csvreader:
        path = row[0]
        project = path.split('/')[1]
        raw_path = '../inconsistent_files/_home-students_mlouki_androidReleases_' + re.sub('\/', '_', path)
        start = int(row[1])
        end = int(row[2])
        extractSnippet(project, index, raw_path, start, end)
        index += 1
