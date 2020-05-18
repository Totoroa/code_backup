'''
get (BM)files and patch files by git.
'''
import subprocess

gitDir = r"F:\project\git_repo\linux"  # where .git exist    

GitBinary = r"E:\Program Files\Git\bin\git.exe"
diffBinary = r"E:\Program Files\Git\usr\bin\diff.exe"
keyword = "CVE-20"

def callGitLog(gitDir):
    """
    Collect CVE commit log from repository
    :param gitDir: repository path
    :return:
    """
    # print "Calling git log...",
    commitsList = []
    gitLogOutput = ""
    command_log = "\"{0}\" --no-pager log --all --pretty=fuller --grep=\"{1}\"".format(GitBinary, keyword)
    print gitDir
    os.chdir(gitDir)
    try:
        try:
            gitLogOutput = subprocess.check_output(command_log, shell=True)
            commitsList = re.split('[\n](?=commit\s\w{40}\nAuthor:\s)|[\n](?=commit\s\w{40}\nMerge:\s)', gitLogOutput)
        except subprocess.CalledProcessError as e:
            print "[-] Git log error:", e
    except UnicodeDecodeError as err:
        print "[-] Unicode error:", err

    # print "Done."
    return commitsList

def process(commitsList, subRepoName):
    flag = 0
    if len(commitsList) > 0 and commitsList[0] == '':
        flag = 1
        print "No commit in", info.RepoName,
    else:
        print len(commitsList), "commits in", info.RepoName,
    if subRepoName is None:
        print "\n"
    else:
        print subRepoName
        os.chdir(os.path.join(info.GitStoragePath, info.RepoName, subRepoName))

    if flag:
        return

    if info.DebugMode or "Windows" in platform.platform():
        # Windows - do not use multiprocessing
        # Using multiprocessing will lower performance
        for commitMessage in commitsList:
            parallel_process(subRepoName, commitMessage)
    else:  # POSIX - use multiprocessing
        pool = mp.Pool()
        parallel_partial = partial(parallel_process, subRepoName)
        pool.map(parallel_partial, commitsList)
        pool.close()
        pool.join()

if "__name__" == "__main__":
    commitsList = callGitLog(gitDir)
    process(commitsList, None)