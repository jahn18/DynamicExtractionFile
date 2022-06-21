import csv
import sys

def filterClasses(class_names_txt, dependency_graph, new_name):
    all_class_names = []
    with open(class_names_txt, 'r') as class_name_file:
        txt_csv_reader = csv.reader(class_name_file)
        for className in txt_csv_reader:
            all_class_names.append(className[0])

    previous_graph_deps = []
    with open(dependency_graph, 'r') as graph_file:
        graph_csv_reader = csv.reader(graph_file)
        for row in graph_csv_reader:
            if row[0] not in all_class_names or row[1] not in all_class_names:
                continue
            elif row[0] == row[1]:
                continue
            else:
                previous_graph_deps.append([row[0], row[1], row[2]])

    with open(new_name, 'w') as f:
        writer = csv.writer(f)
        for dep in previous_graph_deps:
            writer.writerow(dep)

# python3 pro.py class_names_in_application.txt dependency_graph.csv new_dependency_graph.csv
if __name__ == '__main__':
    class_txt_file = sys.argv[1]
    dep_graph = sys.argv[2]
    new_name = sys.argv[3]
    filterClasses(class_txt_file, dep_graph, new_name)
