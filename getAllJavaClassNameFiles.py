import sys
import glob
import os

def getJavaClassNames(path_to_src_code):
    """
    The path to the src code should be before the packages.
    Ex. if the directory structure is main/java/package1/... then you should set main/java as the path.
    """
    files = glob.glob(path_to_src_code + '/**/*.java', recursive=True)
    java_files = []
    for fileName in files:
        # Get only the class name.
        reformatted_file_name = fileName.replace(path_to_src_code, "").replace("/", ".").replace(".java", "")

        # # exclude classes in a test directory
        # if ("test" in reformatted_file_name.lower()):
        #     continue

        java_files.append(reformatted_file_name)
    return java_files

def writeJavaClassNamesToFile(java_files, application_txt_file_name):
    with open(application_txt_file_name, "w") as text_file:
        for className in java_files:
            text_file.write(className + "\n")

# python3 getAllJavaClassNameFiles.py ./ classNames.txt
if __name__ == '__main__':
    path = sys.argv[1]
    txt_file_name = sys.argv[2] # name of file for output
    java_files = getJavaClassNames(path)
    writeJavaClassNamesToFile(java_files, txt_file_name)
