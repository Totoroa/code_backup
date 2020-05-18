#!/bin/sh
start=$(date +%s)

./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.380.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.380,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 0---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.381.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.381,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 1---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.382.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.382,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 2---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.383.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.383,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 3---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.384.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.384,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 4---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.385.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.385,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 5---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.386.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.386,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 6---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.387.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.387,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 7---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.388.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.388,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 8---------------------------"
./joern --script E:/joern/joern-cli/graph/total-pdg.sc --params cpgFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.389.bin,inFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.389,outFile=C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38-lines,flag=src
echo "-----------------------compelete 9---------------------------"

end=$(date +%s)
take=$(( end - start ))
echo Time taken to execute commands is ${take} seconds.