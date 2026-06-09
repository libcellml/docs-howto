"""
    This program is intended to demonstrate a workflow typical of a simulation
    tool developer who would like to be able to interact with CellML model files.
    The general principles are:
    - parse a CellML model file;
    - resolve any import dependencies in the model;
    - validate the model (check for semantic/syntactic errors);
    - debug the model (check for modelling errors);
    - generate runnable code in C and/or Python; and
    - output in the desired format.
"""

import os
import sys
from libcellml import Importer, Parser, Validator, Analyser, Generator, GeneratorProfile
from utilities import print_issues, print_import_dependencies

if __name__ == '__main__':

    # STEP 1
    # Parse the model from a CellML file.
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "simulationExample.cellml"

    # Create a libCellML Parser, and use it to parse the fileContents
    # string and convert it into a CellML Model structure.
    read_file = open(file_name, "r")
    parser = Parser()
    model = parser.parseModel(read_file.read())
    print_issues(parser)

    # STEP 2
    # Resolve any import dependencies (if present) in the model.

    if(model.hasUnresolvedImports()):

        # Create an Importer instance.
        importer = Importer()

        import_path = os.path.dirname(file_name)
        # Submit the model to the importer and the absolute location 
        # against which the import reference paths will be resolved.
        importer.resolveImports(model, import_path)
        print_issues(importer)

        # Print a list of sources that this model requires. This list will 
        # be empty after the model has been flattened.
        print_import_dependencies(model)

        # Retrieve a "flattened" (ie: import-free) model from the importer,
        # and use it to over-write the current model.
        model = importer.flattenModel(model)

    # STEP 3
    # Validate the model: check for syntactic and semantic errors.

    # Create a Validator instance and pass the model for checking.
    validator = Validator()
    validator.validateModel(model)
    print_issues(validator)

    # STEP 4
    # Analyse a model: check for mathematical and modelling errors.
    analyser = Analyser()
    analyser.analyseModel(model)
    print_issues(analyser)

    # STEP 5
    # Generate runnable code in other language formats for this model.

    # Create a Generator instance.  Note that by default this is the C language.
    generator = Generator()

    # Get the analysed model for processing.
    analyserModel = analyser.analyserModel()

    # STEP 6
    # Retrieve and write the interface code (*.h) and implementation code (*.cpp) to files.
    with open("sineComparisonExample.h", "w") as write_file:
        write_file.write(generator.interfaceCode(analyserModel))

    with open("sineComparisonExample.cpp", "w") as write_file:
        write_file.write(generator.implementationCode(analyserModel))

    # If required, change the generator profile to Python and reprocess the model.
    profile = GeneratorProfile(GeneratorProfile.Profile.PYTHON)

    # Retrieve and write the implementation code (*.py) to a file.
    with open("sineComparisonExample.py", "w") as write_file:
        write_file.write(generator.implementationCode(analyserModel, profile))

    # END
