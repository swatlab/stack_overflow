import HTMLParser, re, json, gc, subprocess
import xml.dom.minidom
import xml.etree.ElementTree as ET

def extractCodeSnippet(line):
    # question tags
    matched_tags = re.findall(r'Tags\=\"(.*?)\"', line)
    if matched_tags:
        tags_str = html_parser.unescape(matched_tags[0])
        if '<java>' in tags_str or '<android>' in tags_str:
            # post ID
            matched_id = re.findall(r'row Id\=\"([0-9]+)\"', line)
            if matched_id:
                post_id = matched_id[0]
            else:
                return
            # question created date
            matched_date = re.findall(r'CreationDate\=\"(.*?)\"', line)
            if matched_date:
                created_date = int(re.sub(r'[^0-9]', '', matched_date[0])[:-3])
            else:
                return
            # question body
            matched_body = re.findall(r'Body\=\"(.*?)\"', line)
            if matched_body:
                body_str = html_parser.unescape(html_parser.unescape(matched_body[0].decode('utf-8')))
                code_snippets = re.findall(r'<pre><code>(.+?)</code></pre>', body_str, re.DOTALL)
            else:
                return
            if len(code_snippets):
                return (post_id, created_date, code_snippets)
    return

if __name__ == '__main__':
    ITEM_IN_FILE = 2000
    html_parser = HTMLParser.HTMLParser()
    subprocess.call(['rm', '-rf', 'code_snippets'])
    subprocess.call(['mkdir', 'code_snippets'])
    # data analysis and saving
    snippet_dict = dict()
    date_list = list()
    item_cnt = 0
    res_num = 1
    print 'Save the block #%d ...' %res_num
    with open('dump/Posts.xml', 'r') as f:
        for line in f:
            # extract info from each line of the dump
            if re.search(r'^\s*\<row', line):
                res = extractCodeSnippet(line)
                if res:
                    post_id, created_date, code_snippets = res
                    snippet_id = 1
                    for snippet in code_snippets:
                        line_num = len(snippet.split('\n'))
                        if line_num >= 10:
                            # eliminate XML snippets
                            try:
                                ET.fromstring(snippet)
                            except:
                                snippet_dict['%s_%d' %(post_id, snippet_id)] = snippet
                                snippet_id += 1
                                date_list.append([post_id, created_date]) 
                                item_cnt += 1
            # write a group of posts into a JSON file
            if item_cnt >= ITEM_IN_FILE:
                last_date = date_list[-1][-1]
                with open('code_snippets/%d.json' %last_date, 'w') as json_file:
                    json.dump(snippet_dict, json_file)
                print '\t #%d until the date: %d' %(res_num,last_date)
                res_num += 1
                print 'Save the block #%d ...' %res_num
                item_cnt = 0
                # release memory
                del snippet_dict
                gc.collect()
                # create a new dict object
                snippet_dict = dict()
        # Save the last JSON file
        last_date = date_list[-1][-1]
        with open('code_snippets/%d.json' %last_date, 'w') as json_file:
            json.dump(snippet_dict, json_file)
        print '\t #%d until the date: %d' %(res_num,last_date)
