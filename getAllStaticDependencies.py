import os
import csv

working_dir = os.getcwd()
names = []
with open("file_names.txt", 'r') as f:
    csv_reader = csv.reader(f)
    for name in csv_reader:
        if name[0].find("#") == -1:
            names.append(name[0])


for n in names:
    os.system("cd {}".format(working_dir))
    cmd = "./generateStructualGraphs.sh hadoop/{} staticGraphs/{}".format(n, n.replace("jar", "csv"))
    print(cmd)
    os.system(cmd)
