import os, json, subprocess, time

# Execute a shell command
def shellCommand(command_str):
    cmd = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
    cmd_out, cmd_err = cmd.communicate()
    return cmd_out

if __name__ == '__main__':
    SNIPPET_DIR = 'code_snippets'
    file_list = os.listdir(SNIPPET_DIR)
    for a_file in sorted(file_list):
        if a_file.endswith('.json'):
            print a_file
            split_path = 'stack_code/' + a_file.split('.')[0]
            shellCommand('mkdir -p %s' %split_path)
            with open('%s/%s' %(SNIPPET_DIR, a_file), 'r') as json_file:
                code_dict = json.load(json_file)
                for a_date in code_dict:
                    snippet_list = code_dict[a_date]
                    i = 1
                    for a_snippet in snippet_list:
                        # write a code snippet into the analytic folder
                        with open('%s/%s_%d.java' %(split_path,a_date,i), 'w') as f_snippet:
                            f_snippet.write(a_snippet.encode('utf-8'))
                        i += 1
                        