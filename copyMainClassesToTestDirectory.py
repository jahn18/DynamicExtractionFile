import sys
import glob
import os, shutil

def copyMainClassesToTestDirectory(path_to_main_directory, path_to_test_directory):
    files = glob.glob(path_to_main_directory + '/**/*.java', recursive=True)
    main_class_files = []
    for fileName in files:
        getPackage = fileName.split("/")
        getPackage.pop()
        packageDir = ""
        for folder in getPackage:
            packageDir += folder + "/"
        testPackageDir = packageDir.replace(path_to_main_directory, path_to_test_directory)
        try:
            shutil.copy(fileName, testPackageDir)
        except IOError as io_err:
            os.makedirs(os.path.dirname(testPackageDir))
            shutil.copy(fileName, testPackageDir)

# python3 pro.py main_dir_path test_dir_path
# e.g python3 pro.py ..src/main/java ..src/test/java
if __name__ == "__main__":
    main_dir = sys.argv[1]
    test_dir = sys.argv[2]
    copyMainClassesToTestDirectory(main_dir, test_dir)
