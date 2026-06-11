"""
    SIMPLE SOLVER for CellML models generated using the Python profile.

    This script uses Euler updates to solve a set of differential equations.

    Usage:
        python3 solveGeneratedModel.py:
            -m generated file to run
            -n number of steps to take
            -dt step size to use.

    The solution will be written to a tab-delimited text file in the same directory
    as the running file, with the extension _solution.txt added to the run file name.

"""

import sys
import importlib
import importlib.util

from generateModel import generate_solvable_model

# COMMAND LINE FUNCTION
import argparse


def process_arguments():
    parser = argparse.ArgumentParser(
        description="Run generated file with simulation parameters"
    )

    # Define arguments
    parser.add_argument(
        "-m",
        required=True,
        help="Generated file to run (.py)"
    )

    parser.add_argument(
        "-n",
        type=int,
        required=True,
        help="Number of steps to take before stopping"
    )

    parser.add_argument(
        "-dt",
        type=float,
        required=True,
        help="Step size to use"
    )

    # Return as dict like your original function
    return parser.parse_args()
# END COMMAND LINE FUNCTION

# MODULE FROM FILE
def module_from_file(input):

    # Check the extension is stripped during input.
    if input[-3:] != '.py':
        module_file = input + ".py"
        module_name = input.split("/")[-1]
    else:
        module_file = input
        module_name = ".".join(input.split("/")[-1].split(".")[:-1])

    # Import the generated code as a module, and return it.
    spec = importlib.util.spec_from_file_location(module_name, module_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
# END MODULE FROM FILE


# STEP 0
if __name__ == "__main__":

    args = process_arguments()

    print('-------------------------------------------------------------')
    print('   SIMPLE SOLVER')
    print('-------------------------------------------------------------')
    print('       model = {}'.format(args.m))
    print('       timestep = {}'.format(args.dt))
    print('       number of steps = {}'.format(args.n))
    print()

    # STEP 1
    # Retrieve model module from the generated code file.
    generated_file = generate_solvable_model(args.m)
    model = module_from_file(generated_file)

    # Inside the 'model' module are structures with information about the 
    # model and its dimensions.  These are:
    #   - VOI_INFO: a dict with the name, units, and component of the variable of integration,
    #   - STATE_INFO: a list of similar dicts for the state variables,
    #   - VARIABLE_INFO: a list of similar dicts for the non-state variables. 

    print('   VARIABLE OF INTEGRATION (units)')
    print('--------------------------------------------------------------------')
    print('      {} ({}, {})'.format(model.VOI_INFO['name'],
                                     model.VOI_INFO['units'],
                                     args.dt))
    print('      {} steps'.format(args.n))
    print()

    # STEP 2
    # Call module functions to construct the variable arrays.
    # Note that both the rates and the states arrays have the same dimensions,
    # so it's possible to call the create_states_array() function for both.
    voi = 0.0
    my_constants = model.create_constants_array()
    my_computed_constants = model.create_computed_constants_array()
    my_algebraic_variables = model.create_algebraic_variables_array()
    my_state_variables = model.create_states_array()
    my_rates = model.create_states_array()
    
    # STEP 3
    # Compute the parameters which require it, including the rates and variable values.
    model.initialise_arrays(my_state_variables, my_rates, my_constants, my_computed_constants, my_algebraic_variables)
    model.compute_computed_constants(voi, my_state_variables, my_rates, my_constants, my_computed_constants, my_algebraic_variables)
    model.compute_rates(voi, my_state_variables, my_rates, my_constants, my_computed_constants, my_algebraic_variables)
    model.compute_variables(voi, my_state_variables, my_rates, my_constants, my_computed_constants, my_algebraic_variables)

    print('   STATE VARIABLES (units, initial value)')
    print('--------------------------------------------------------------------')
    for i in range(0, model.STATE_COUNT):
        print('      {} ({}, {})'.format(model.STATE_INFO[i]['name'],
                                         model.STATE_INFO[i]['units'],
                                         my_state_variables[i]))
    print()
    print('   CONSTANTS (units, initial value)')
    print('--------------------------------------------------------------------')

    for v in range(0, model.CONSTANT_COUNT):
        print('      {} ({}, {})'.format(model.CONSTANT_INFO[v]['name'],
                                         model.CONSTANT_INFO[v]['units'],
                                         my_constants[v]))
    print()
    print('   COMPUTED CONSTANTS (units, initial value)')
    print('--------------------------------------------------------------------')

    for v in range(0, model.COMPUTED_CONSTANT_COUNT):
        print('      {} ({}, {})'.format(model.COMPUTED_CONSTANT_INFO[v]['name'],
                                         model.COMPUTED_CONSTANT_INFO[v]['units'],
                                         my_computed_constants[v]))
    print()
    print('   ALGEBRAIC VARIABLES (units, initial value)')
    print('--------------------------------------------------------------------')

    for v in range(0, model.ALGEBRAIC_VARIABLE_COUNT):
        print('      {} ({}, {})'.format(model.ALGEBRAIC_VARIABLE_INFO[v]['name'],
                                         model.ALGEBRAIC_VARIABLE_INFO[v]['units'],
                                         my_algebraic_variables[v]))
    print()

    # STEP 4
    # Prepare to write output to a file during the solution process.
    row = 'iteration\t{}({})'.format(
        model.VOI_INFO['name'], model.VOI_INFO['units'])
    for s in range(0, model.STATE_COUNT):
        row += '\t{}({})'.format(model.STATE_INFO[s]
                                 ['name'], model.STATE_INFO[s]['units'])
    for s in range(0, model.ALGEBRAIC_VARIABLE_COUNT):
        row += '\t{}({})'.format(model.ALGEBRAIC_VARIABLE_INFO[s]
                                 ['name'], model.ALGEBRAIC_VARIABLE_INFO[s]['units'])
    row += '\n'

    write_file_name = generated_file
    if write_file_name[-3:] == '.py':
        write_file_name = write_file_name[:-3]
    write_file_name = f'{write_file_name}_solution.txt'
    write_file = open(write_file_name, 'w')
    write_file.write(row)

    # STEP 5
    # Numerically integrate using Euler steps to solve the model.
    for step in range(0, args.n):
        voi = step * args.dt

        model.compute_rates(voi, my_state_variables, my_rates, my_constants, my_computed_constants, my_algebraic_variables)

        # Formatting for output.
        row = '{}\t{}'.format(step, voi)
        for s in range(0, model.STATE_COUNT):
            my_state_variables[s] = my_state_variables[s] + \
                my_rates[s] * args.dt
            row += '\t{}'.format(my_state_variables[s])

        # Note that the variables in the my_algebraic_variables array are those which 
        # are independent of the integration: thus, they only need to be
        # computed at timesteps where the solution is to be written to the
        # output.  For large simulations, this may not be every integration 
        # timestep.
        model.compute_variables(
            voi, my_state_variables, my_rates, my_constants, my_computed_constants, my_algebraic_variables)

        # Output the solution.
        for s in range(0, model.ALGEBRAIC_VARIABLE_COUNT):
            row += '\t{}'.format(my_algebraic_variables[s])

        row += '\n'
        write_file.write(row)

    write_file.close()

    # END

    print()
    print('   SOLUTION written to {}'.format(write_file_name))
    print('====================================================================')
    print()
    print()
