#!/bin/sh
start=$(date +%s)
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.380 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.380.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.381 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.381.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.382 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.382.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.383 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.383.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.384 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.384.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.385 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.385.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.386 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.386.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.387 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.387.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.388 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.388.bin
./joern-parse C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.389 --out C:/Users/admin/Desktop/workspace-python/My_project/project_data/linux-2.6.27.38/linux-2.6.27.389.bin
end=$(date +%s)
take=$(( end - start ))
echo Time taken to execute commands is ${take} seconds.