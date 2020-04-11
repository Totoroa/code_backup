"""对程序进行抽象"""
import os
import subprocess

class function:
    parentFile = None  # Absolute file which has the function
    parentNumLoc = None  # Number of LoC of the parent file
    name = None  # Name of the function
    lines = None  # Tuple (lineFrom, lineTo) that indicates the LoC of function
    funcId = None  # n, indicating n-th function in the file
    parameterList = []  # list of parameter variables
    variableList = []  # list of local variables
    dataTypeList = []  # list of data types, including user-defined types
    funcCalleeList = []  # list of called functions' names
    funcBody = None

    def __init__(self, fileName):
        self.parentFile = fileName
        self.parameterList = []
        self.variableList = []
        self.dataTypeList = []
        self.funcCalleeList = []

    def removeListDup(self):
        # for best performance, must execute this method
        # for every instance before applying the abstraction.
        self.parameterList = list(set(self.parameterList))
        self.variableList = list(set(self.variableList))
        self.dataTypeList = list(set(self.dataTypeList))
        self.funcCalleeList = list(set(self.funcCalleeList))

        # def getOriginalFunction(self):
        #   # returns the original function back from the instance.
        #   fp = open(self.parentFile, 'r')
        #   srcFileRaw = fp.readlines()
        #   fp.close()
        #   return ''.join(srcFileRaw[self.lines[0]-1:self.lines[1]])


javaCallCommand = os.path.join(os.getcwd(), r"FuncParser-opt.exe ")
delimiter = "\r\0?\r?\0\r"

def parseFile_deep(srcFileName):
    global javaCallCommand
    global delimiter
    #setEnvironment(caller)  
    # this parses function definition plus body.
    javaCallCommand += "\"" + srcFileName + "\" 1"
    functionInstanceList = []

    try:
        astString = subprocess.check_output(javaCallCommand, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print "Parser Error:", e
        astString = ""

    funcList = astString.split(delimiter)
    for func in funcList[1:]:
        functionInstance = function(srcFileName)

        elemsList = func.split('\n')[1:-1]
        # print elemsList
        if len(elemsList) > 9:
            functionInstance.parentNumLoc = int(elemsList[1])
            functionInstance.name = elemsList[2]
            functionInstance.lines = (int(elemsList[3].split('\t')[0]), int(elemsList[3].split('\t')[1]))
            functionInstance.funcId = int(elemsList[4])
            functionInstance.parameterList = elemsList[5].rstrip().split('\t')
            functionInstance.variableList = elemsList[6].rstrip().split('\t')
            functionInstance.dataTypeList = elemsList[7].rstrip().split('\t')
            functionInstance.funcCalleeList = elemsList[8].rstrip().split('\t')
            functionInstance.funcBody = '\n'.join(elemsList[9:])
            # print '\n'.join(elemsList[9:])
            functionInstanceList.append(functionInstance)

    return functionInstanceList

f_list = parseFile_deep("net#~sctp#~ulpqueue.c")
for index, ff in enumerate(f_list):
    print "##",index+1
    print "name = ", ff.name
    print "lines = ", ff.lines
    print "parameterList = ", ff.parameterList
    print "variableList = ", ff.variableList
    print "dataTypeList = ", ff.dataTypeList
    print "funcCalleeList = ", ff.funcCalleeList
    print "\n"
    