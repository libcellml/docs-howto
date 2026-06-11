import os
import libcellml


def generate_solvable_model(cellml_file, output_dir=os.path.curdir, profile=libcellml.GeneratorProfile.Profile.PYTHON):
    # This function is a placeholder for the code which generates the model
    # to be solved.  In this example, the model is generated using the
    # Python profile of libCellML, and the generated code is in the file
    # "exact_sine.py".  The module_from_file() function can be used to import
    # this generated code as a module, and then the functions within it can
    # be used to solve the model.
    with open(cellml_file, 'r') as f:
        model_code = f.read()
    
    parser = libcellml.Parser()
    model = parser.parseModel(model_code)
    if parser.errorCount() > 0:
        print("Errors encountered during parsing:")
        for i in range(parser.errorCount()):
            print(parser.error(i).description())
        return None
    
    analyser = libcellml.Analyser()
    analyser.analyseModel(model)
    if analyser.errorCount() > 0:
        print("Errors encountered during analysis:")
        for i in range(analyser.errorCount()):
            print(analyser.error(i).description())
        return None
    
    analyser_model = analyser.analyserModel()
    generator = libcellml.Generator()

    file_base_name = os.path.basename(cellml_file).split(".")[0]
    if profile == libcellml.GeneratorProfile.Profile.PYTHON:
        implementation_file = file_base_name + "_generated.py"
    else:
        modified_profile = libcellml.GeneratorProfile()
        implementation_file = file_base_name + "_generated.c"
        interface_file = file_base_name + "_generated.h"
        modified_profile.setInterfaceFileNameString(interface_file)
        profile = modified_profile
        with open(os.path.join(output_dir, interface_file), 'w') as f:
            f.write(generator.interfaceCode(analyser_model, profile))
    
    generated_code = generator.implementationCode(analyser_model, profile)
    generated_file = os.path.join(os.path.realpath(output_dir), implementation_file)
    with open(generated_file, 'w') as f:
        f.write(generated_code)

    return generated_file


if __name__ == '__main__':
    # This is a placeholder for the code which calls the function to generate
    # the model to be solved.  In this example, the model is generated using
    # the Python profile of libCellML, and the generated code is in the file
    # "exact_sine.py".  The module_from_file() function can be used to import
    # this generated code as a module, and then the functions within it can
    # be used to solve the model.
    import argparse

    parser = argparse.ArgumentParser(description='Generate a solvable model from a CellML file.')
    parser.add_argument('-m', '--model', dest='m', type=str, required=True,
                        help='the CellML file containing the model to generate')
    parser.add_argument('-o', '--output', dest='o', type=str, default=os.curdir,
                        help='the directory to write the generated code to (default: current directory)')
    parser.add_argument('-p', '--profile', dest='p', type=str, default='python',
                        help='the generator profile to use (default: python)')
    args = parser.parse_args()
    generated_file = generate_solvable_model(args.m, output_dir=args.o, profile=getattr(libcellml.GeneratorProfile.Profile, args.p.upper()))
    print(f"Generated file: {generated_file}")
