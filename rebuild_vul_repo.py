import os
import sys
import subprocess
import re
import pickle
# r'https://github.com/openssl/openssl.git',r'https://github.com/Microsoft/ChakraCore.git', 
repos = [r'https://github.com/freebsd/freebsd.git', 
        r'https://github.com/mozilla/gecko-dev.git', r'git://sourceware.org/git/glibc.git',
        r'https://github.com/apache/httpd.git', r'https://github.com/krb5/krb5.git', 
        r'git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git',
        r'https://github.com/postgres/postgres.git', r'git://kernel.ubuntu.com/ubuntu/ubuntu-trusty.git',
        r'https://git.qemu.org/git/qemu.git']
repo_name = ['freebsd', 'gecko-dev', 'glibc', 'httpd', 'krb5', 'linux', 'postgres', 'ubuntu-trusty', 'qemu']
gitRepo_path = r"F:\project\git_repo"  #storage git repositories
git_vul_path = r"F:\project\vul_repo"
gitBinary = r"E:\Program Files\Git\bin\git.exe"

def filterCommitMessage(commitMessage):
    """
    Filter false positive commits 
    Will remove 'Merge', 'Revert', 'Upgrade' commit log
    :param commitMessage: commit message
    :return: 
    """
    filterKeywordList = ["merge", "revert", "upgrade"]
    matchCnt = 0
    for kwd in filterKeywordList:
        keywordPattern = r"\W" + kwd + r"\W|\W" + kwd + r"s\W"
        compiledKeyworddPattern = re.compile(keywordPattern)
        match = compiledKeyworddPattern.search(commitMessage.lower())

        # bug fixed.. now revert and upgrade commits will be filtered out.
        if match:
            matchCnt += 1

    if matchCnt > 0:
        return 1
    else:
        return 0 

def callGitLog(gitDir):
    """
    Collect CVE commit log from repository
    :param gitDir: repository path
    :return:
    """
    # print "Calling git log...",
    commitsList = []
    gitLogOutput = ""
    command_log = "\"{0}\" --no-pager log --all --pretty=fuller --grep=\"{1}\"".format(gitBinary, "CVE-20")
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

def updateCveInfo(cveDict, cveId):
    """
    Get CVSS score and CWE id from CVE id
    :param cveId: 
    :return: 
    """
    # print "Updating CVE metadata...",
    try:
        cvss = str(cveDict[cveId][0])
    except:
        cvss = "0.0"
    if len(str(cvss)) == 0:
        cvss = "0.0"

    try:
        cwe = cveDict[cveId][1]
    except:
        cwe = "CWE-000"
    if len(cwe) == 0:
        cwe = "CWE-000"
    else:
        cweNum = cwe.split('-')[1].zfill(3)
        cwe = "CWE-" + str(cweNum)

    # print "Done."
    return cveId + '_' + cvss + '_' + cwe + '_'

def process(commitsList, repoName):
    '''
    get patch files and original files about repoName
    '''
    os.chdir(os.path.join(gitRepo_path, repoName))
    if len(commitsList) > 0 and commitsList[0] == '':
        print "No commit in", repoName
        return
    else:
        print len(commitsList), "commits in", repoName
    for index, commitMessage in enumerate(commitsList):
        print "processing ",index+1, '/' , len(commitlist)
        parallel_process(repoName, commitMessage)
        print "Ok.."

def parallel_process(repoName, commitMessage):
    if filterCommitMessage(commitMessage):
        return
    else:
        commitHashValue = commitMessage[7:47]
        cvePattern = re.compile('CVE-20\d{2}-\d{4,7}')  # note: CVE id can now be 7 digit numbers
        cveIdList = list(set(cvePattern.findall(commitMessage)))  
        """    
        Note: Aug 5, 2016
        If multiple CVE ids are assigned to one commit,
        store the dependency in a file which is named after
        the repo, (e.g., ~/diff/dependency_ubuntu)    and use
        one representative CVE that has the smallest ID number
        for filename. 
        A sample:
        CVE-2014-6416_2e9466c84e5beee964e1898dd1f37c3509fa8853    CVE-2014-6418_CVE-2014-6417_CVE-2014-6416_
        """
        if len(cveIdList) > 1:  # do this only if muliple CVEs are assigned to a commit
            dependency = os.path.join(git_vul_path, repoName,"dependency_" + repoName)
            with open(dependency, "a") as fp:
                cveIdFull = ""
                minCve = ""
                minimum = 9999999
                for cveId in cveIdList:
                    idDigits = int(cveId.split('-')[2])
                    cveIdFull += cveId + '_'
                    if minimum > idDigits:
                        minimum = idDigits
                        minCve = cveId
                fp.write(str(minCve + '_' + commitHashValue + '\t' + cveIdFull + '\n'))        
        elif len(cveIdList) == 0:
            print "The number of cve is 0 in", repoName, commitHashValue
            return
        else:
            minCve = cveIdList[0]
        #get commitHashValue content
        command_show = "\"{0}\" show --pretty=fuller {1}".format(gitBinary, commitHashValue)
        gitShowOutput = ''
        try:
            gitShowOutput = subprocess.check_output(command_show, shell=True)
        except subprocess.CalledProcessError as e:
            print "error:", e
        CveDict = {}
        with open(r"F:\project\vuddy-master\vulnDBGen\data\cvedata.pkl", "rb") as f:
            CveDict = pickle.load(f)        
        finalFileName = updateCveInfo(CveDict, minCve)
        diffFileName = "{0}{1}.diff".format(finalFileName, commitHashValue)
        try:
            with open(os.path.join(git_vul_path, repoName, diffFileName), "w") as fp:
                fp.write(gitShowOutput)
        except IOError as e:
            with printLock:
                print "[+] Writing {0} Error:".format(diffFileName), e        
   
if __name__ == '__main__':
    os.chdir(gitRepo_path)
    for i in range(len(repos)):
        if os.path.exists(os.path.join(gitRepo_path, repo_name[i])) and len(os.listdir(os.path.join(gitRepo_path, repo_name[i])))>2:
            print "[+]repository %s has already exists."%repo_name[i]
        else:
            os.system("git clone %s"%repos[i])
            if os.path.exists(os.path.join(gitRepo_path, repo_name[i])) and len(os.listdir(os.path.join(gitRepo_path, repo_name[i])))>2:
                print "[+]repository %s successfully cloned !"%repo_name[i]
            else:
                print "[-]repository %s clone failed !"%repo_name[i]
                continue
        if not os.path.exists(os.path.join(git_vul_path, repo_name[i])):
            os.mkdir(os.path.join(git_vul_path, repo_name[i]))
        os.chdir(os.path.join(gitRepo_path, repo_name[i]))
        commitlist = callGitLog(os.path.join(gitRepo_path, repo_name[i]))#(r'F:\project\vuddy-master\gitrepos\openssl')
        process(commitlist, repo_name[i])
        print "[+++++]", repo_name[i], "has been proccessed..."
