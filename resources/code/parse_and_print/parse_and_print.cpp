#include <cassert>
#include <fstream>
#include <libcellml>

int main(int argc, char *argv[])
{
  // Create a Printer instance.
  auto printer = libcellml::Printer::create();

  // Create a Model instance.
  auto model = libcellml::Model::create("my_model");

  // The output of the printModel function is a string representing the serialised input model.
  const std::string serialisedModelString = printer->printModel(model);

  // Check the printer for issues.
  assert(printer->issueCount() == 0);

  // Write the serialised string to a file.
  const std::string outFileName = "my_printed_file.cellml";
  std::ofstream outFile(outFileName);
  outFile << serialisedModelString;
  outFile.close();

  return 0;
}
