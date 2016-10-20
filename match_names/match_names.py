import csv

def loadFile(filename):
    mapping_dict = dict()
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[0].lower()
            values = row[1].decode('utf8')
            if len(values):
                mapping_dict[key] = [v.lower() for v in values.split('^')]
    return mapping_dict

question = 'RQ2'  
poster_name_dict = loadFile('posters.csv')
contributor_dict = loadFile('real_names.csv')
post2app = loadFile('%s_mapping.csv' %question)
for post in post2app:
    if post in poster_name_dict:
        poster_names = poster_name_dict[post]
        app = post2app[post][0]
        app_contributors = contributor_dict[app]
        for a_poster in poster_names:
            if a_poster in app_contributors:
                print post, app, a_poster