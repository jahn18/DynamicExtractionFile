 #!/bin/bash

# Should include both the JUnit tests and the main application tests within one jar file. The Path to the jar file.
PROJECT_JAR_FILE=$1
PROJECT_DEP_DIR=$2
PROJECT_NAME=$3
PROJECT_CLASS_NAMES=$4
PROJECT_TEST_CLASS_NAMES=$5

# Generate the static graph
java -cp "Slicer4J/Slicer4J/target/slicer4j-jar-with-dependencies.jar:Slicer4J/Slicer4J/libs/:Slicer4J/Slicer4J/target/lib/soot-infoflow-2.9.0-SNAPSHOT.jar:" ca.ubc.ece.resess.slicer.dynamic.slicer4j.getStaticGraph ${PROJECT_JAR_FILE} static.csv
python3 filterClasses.py ${PROJECT_CLASS_NAMES} static.csv ${PROJECT_NAME}StaticGraph.csv

rm -r static.csv

# Generate the dynamic graph
#python3 extractDynamicDependencies.py -j ${PROJECT_JAR_FILE} -d ${PROJECT_DEP_DIR} -tc ${PROJECT_TEST_CLASS_NAMES} -o dynamic.csv
#python3 filterClasses.py ${PROJECT_CLASS_NAMES} dynamic.csv ${PROJECT_NAME}DynamicGraph.csv
#rm -r traces
#rm -r dynamic.csv
