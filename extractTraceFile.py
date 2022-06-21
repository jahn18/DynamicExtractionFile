import csv
import argparse


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
                # if head == " smpl.ordering.controllers.ShipmentController" and class_name == " smpl.ordering.controllers.OrderController":
                #     print("here")
                if class_name == " smpl.ordering.controllers.ShipmentController":
                    print("here")
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
                if head == " smpl.ordering.controllers.ShipmentController" and class_name == " smpl.ordering.controllers.OrderController":
                    print("here")
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
    parser.add_argument("-f", "--file", dest="trace_file",
                        help="The trace file you want to parse", metavar="/path/to/trace_file", required=True)
    args = parser.parse_args()
    all_dynamic_dependencies = {}
    class_trace = extract_test_execution_trace(args.trace_file)
    get_dynamic_dependencies(class_trace, all_dynamic_dependencies)
    write_dependency_file(all_dynamic_dependencies, args.trace_file + ".csv")

