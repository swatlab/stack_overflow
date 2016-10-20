import os, subprocess, shutil, gc

# Execute a shell command
def shellCommand(command_str):
    cmd = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE)
    cmd_out, cmd_err = cmd.communicate()
    return cmd_out

def cloneDetection(json_num):
    # initialisation
    SRC_DIR = 'inconsistent_files'
    DES_DIR = '%s/analytic_files' %INPUT_DIR
    NICAD_RES = '%s/analytic_files_functions-crossclones/analytic_files_functions-crossclones-0.30-classes.xml' %INPUT_DIR
    
    # clean and create the result folder (which might be previously created)
    shellCommand('rm -rf clone_results/%s' %json_num)
    shellCommand('mkdir -p clone_results/%s' %json_num)
    
    inconsistent_files = os.listdir(SRC_DIR)
    if DEBUG:
        PART = 1
    else:
        PART = SPLIT 
    
    print ' - copying files ...'
    for i in range(0,PART):
        print ' Dealing with Part:', i+1
        # clean and prepare directories
        shellCommand('rm -rf %s' %DES_DIR)
        shellCommand('mkdir -p %s' %DES_DIR)
        result_path = 'clone_results/%s/result_%d.xml' %(json_num,i+1)
        # Copy inconsistent files
        begin_index = len(inconsistent_files)/SPLIT*i
        end_index = len(inconsistent_files)/SPLIT*(i+1)
        if i == SPLIT - 1:
            end_index = len(inconsistent_files)
        analytic_files = inconsistent_files[begin_index:end_index]
        for file_name in analytic_files:
            if file_name.endswith('.java'):
                src_path = '%s/%s' %(SRC_DIR,file_name)
                des_path = '%s/%s' %(DES_DIR,file_name)
                shutil.copy(src_path, des_path)
        # Perform clone detection
        print '  - performing clone detection ...'
        
        # Run the NiCad cross tool
        shellCommand('nicad4cross functions java %s/analytic_files %s/%s' %(INPUT_DIR,INPUT_DIR,json_num))
        # COPY THE RESULT TO THE RESULT PATH
        shutil.copy(NICAD_RES, result_path)
        
        # Clean memory and disk
        print '  - releasing memory and disk ...'
        shellCommand('rm -rf %s' %DES_DIR)
        shellCommand('rm -rf %s/*functions*' %INPUT_DIR)
        gc.collect()
        shellCommand('sudo sysctl -w vm.drop_caches=3')
    return

if __name__ == '__main__':
    DEBUG = False
    SPLIT = 200
    
    # initialisation
    INPUT_DIR = 'nicad_input'
    
    for json_num in sorted(os.listdir('stack_code'))[1:2]:
        print 'Analysing the slice until the date %s ...' %json_num
        print ' Moving the analytic file directory ...'
        # clean and create the input folder
        shellCommand('rm -rf %s' %INPUT_DIR)
        shellCommand('mkdir -p %s' %INPUT_DIR)
        # clone detection process
        src_dir = 'stack_code/' + json_num
        des_dir = '%s/%s' %(INPUT_DIR,json_num)
        shutil.copytree(src_dir, des_dir)
        cloneDetection(json_num)
        print ' Moving back the analytic file directory ...'
        shutil.move(des_dir, src_dir)
        # clean the input folder
        shellCommand('rm -rf %s' %INPUT_DIR)
        print ''
