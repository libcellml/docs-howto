from libcellml import Model, Printer

# Create a Printer instance.
printer = Printer()

# Create a model to print.
model = Model("my_model")

# The output of the printModel function is a string representing the serialised input model.
serialised_model = printer.printModel(model)

# Check the printer for issues.
assert(printer.issueCount() == 0)

# Write the string to a file.
with open("my_printed_file.cellml", "w") as write_file:
    write_file.write(serialised_model)
