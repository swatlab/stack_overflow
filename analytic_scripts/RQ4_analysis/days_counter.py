from datetime import datetime

# Compute date interval between two date strings
def dateDiff(d1_str, d2_str):
    d1 = datetime.strptime(d1_str, '%b %d, %Y')
    d2 = datetime.strptime(d2_str, '%b %d, %Y')
    return round((d2 - d1).total_seconds()/3600/24, 2)

date1 = 'Jun 7, 2012'
date2 = 'Aug 12, 2014'

print dateDiff(date1, date2)