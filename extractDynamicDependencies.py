import csv
import sys
import os, glob
import argparse

current_directory = os.getcwd()
slicer4J_directory = current_directory + "/" + "Slicer4J" + "/" + "scripts/"


def get_all_test_class_names(name_file):
    test_file_names = []
    with open(name_file, "r") as f:
        csv_reader = csv.reader(f)
        for name in csv_reader:
            test_file_names.append(name[0])

    return test_file_names


def extract_trace_logs_from_tests(test_names, path_to_application_test_jar, path_to_application_build_dir, project_name):
    os.makedirs(current_directory + "/traces")

    print("Extracting log traces...")
    all_dynamic_dependencies = {}
    for count, testName in enumerate(test_names):
        print("Running test: ", testName)
        cmd = "python3 " + slicer4J_directory + "slicer4j.py -j " + current_directory + "/" + path_to_application_test_jar + " -dep " + current_directory + "/" + path_to_application_build_dir + " -tc " + testName + " -tm . -b .:. -o " + current_directory + "/traces"
        os.system(cmd)
        os.rename(current_directory + "/traces/trace.log_icdg.log", current_directory + "/traces/trace_{0}.log".format(count))
        class_trace = extract_test_execution_trace(current_directory + "/traces/trace_{0}.log".format(count))
        get_dynamic_dependencies(class_trace, all_dynamic_dependencies)
        cat = "cat " + current_directory + "/traces/trace_full.log"
        os.system(cat)

    write_dependency_file(all_dynamic_dependencies, project_name)
    print("Done")


def extract_test_execution_trace(execution_trace_file_name):
    execution_trace_file = open(execution_trace_file_name)
    csv_reader = csv.reader(execution_trace_file)
    # Class name is on the third column
    class_trace = []
    for row in csv_reader:
        info = {
            'lineNumber': row[0],
            'className': row[2],
            # A little messy, but if we have for example "if false then return:LINENUMBER0:...",
            # we first parse the first component "if false then return", and then check if it starts with "return".
            # If not, then this is not a returnCall statement.
            # This returnCall should equal true under 3 conditions: https://docs.oracle.com/javase/tutorial/java/javaOO/returnvalue.html
            # 1. Completes all statements in a method
            # 2. Reaches a return statement
            # 3. Throws an exception.
            'returnCall': should_return(row[3])
        }
        class_trace.append(info)

    return class_trace


def should_return(jimple_code_statement):
    parsed_jimple_code_statement = (jimple_code_statement.split(":")[0]).strip().split(" ")[0]
    if "return" in parsed_jimple_code_statement or "throw" in parsed_jimple_code_statement:
        return True
    else:
        return False


def get_dynamic_dependencies(class_trace, dynamic_deps: dict):
    stack = []
    head = None
    for class_info in class_trace:
        class_name = class_info['className']
        if class_info['returnCall'] is False and class_name not in stack:
            stack.append(class_name)
            if len(stack) > 1:
                if head in dynamic_deps:
                    if class_name in dynamic_deps[head]:
                        dynamic_deps[head][class_name] += 1
                    else:
                        dynamic_deps[head][class_name] = 1
                else:
                    dynamic_deps[head] = {class_name: 1}
            head = class_name
        elif class_info['returnCall'] is True and class_name not in stack:
            if len(stack) > 1:
                if head in dynamic_deps:
                    if class_name in dynamic_deps[head]:
                        dynamic_deps[head][class_name] += 1
                    else:
                        dynamic_deps[head][class_name] = 1
                else:
                    dynamic_deps[head] = {class_name: 1}
        elif class_info['returnCall'] is True and class_name in stack:
            stack.pop()
            if len(stack) > 0:
                head = stack[-1]


# Formats the dependency file in rsf format.
def write_dependency_file(dynamic_deps, dynamic_dep_file_name):
    # If method calle and caller are the same then do not add the dependency (no self loops)
    with open(dynamic_dep_file_name, mode='w') as dep_file:
        dynamic_writer = csv.writer(dep_file, delimiter=',')
        for caller_class in dynamic_deps:
            for calle_class in dynamic_deps[caller_class]:
                if caller_class != calle_class:
                    dynamic_writer.writerow([caller_class.strip(), calle_class.strip(), dynamic_deps[caller_class][calle_class]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jar_file", dest="jar_file",
                         help="the jar file of the application", metavar="/path/to/jar_file", required=True)
    parser.add_argument("-tc", "--test_classes", dest="test_classes",
                         help="A file containing all the names of the test classes in the application", metavar="/path/to/test_class_file", required=True)
    parser.add_argument("-d", "--dependencies", dest="build_dir",
                         help="Additional dependencies and packages required to run the application", metavar="/path/to/dependencies", required=True)
    parser.add_argument("-o", "--output_name", dest="output_name",
                         help="The name of the output file for the dynamic dependencies graph", metavar="output_name", required=True)

    args = parser.parse_args()
    testFileNames = get_all_test_class_names(args.test_classes)
    extract_trace_logs_from_tests(testFileNames, args.jar_file, args.build_dir, args.output_name)
