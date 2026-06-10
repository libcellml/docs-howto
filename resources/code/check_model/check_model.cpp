

#include <iostream>
#include <libcellml>

int main(int argc, char *argv[])
{
    // Create a Validator, and use it to validate a model.
    auto validator = libcellml::Validator::create();
    auto model = libcellml::Model::create();

    validator->validateModel(model);

    auto printer = libcellml::Printer::create();
    auto parser = libcellml::Parser::create();
    auto generator = libcellml::Generator::create();

    // start CHECK_MODEL 1
    
    // Iterate through all the issues in a Validator, regardless of level, and print to the terminal.
    for (size_t i = 0; i < validator->issueCount(); ++i) {
        // Retrieve the i-th issue and store it in the variable "myIssue".
        libcellml::IssuePtr myIssue = validator->issue(i);

        // Print the issue's description:
        std::cout << myIssue->description() << std::endl;

        // Print the issue's URL.  This is a URL at which more 
        // information could be found about the cause and corrections
        // are needed to avoid it.
        std::cout << myIssue->url() << std::endl;

        // Validator only: Print the issue's reference. This is 
        // the heading reference in the normative specification which 
        // relates to this issue.
        std::cout << myIssue->referenceHeading() << std::endl;
    }

    // Retrieve the second ERROR level issue from a Printer. Note indexing from 0.
    auto secondError = printer->error(1);

    // Retrieve the last WARNING level issue from a Parser.
    auto lastWarning = parser->warning(parser->warningCount()-1);

    // Iterate through all MESSAGE level issues in a Generator.
    for (size_t m = 0; m < generator->messageCount(); ++m) {
        // Retrieve the m-th message and store it in the variable "myMessage".
        auto myMessage = generator->message(m);
    }

    // end CHECK_MODEL 1

    auto issue = validator->issue(0);

    // start CHECK_MODEL 2

    // Retrieve and print the description of the issue.
    std::cout << issue->description() << std::endl;

    // Retrieve and print the reference heading number, if related to CellML2.0 specification and format.
    std::cout << issue->referenceHeading() << std::endl;

    // Retrieve and print the URL for more help and information about the issue. 
    std::cout << issue->url() << std::endl;

    // Retrieve the item type - a libcellml::CellmlElementType enum - for the issue.
    auto myType = issue->item()->type();

    // Retrieve the level - a libcellml::Issue::LEVEL enum - for the issue.
    auto myLevel = issue->level();

    // end CHECK_MODEL 2

    return 0;
}
