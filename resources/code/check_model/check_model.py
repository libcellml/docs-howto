from libcellml import Model, Validator, Printer, Generator, Parser


def main():
    # Create a Validator, and use it to validate a model.
    validator = Validator()
    model = Model()

    validator.validateModel(model)

    printer = Printer()
    parser = Parser()
    generator = Generator()

    # start CHECK_MODEL 1

    # Iterate through all issues in the Validator and print them
    for i in range(validator.issueCount()):
        my_issue = validator.issue(i)

        # Print the issue's description:
        print(my_issue.description())

        # Print the issue's URL.  This is a URL at which more 
        # information could be found about the cause and corrections
        # are needed to avoid it.
        print(my_issue.url())

        # Validator only: Print the issue's reference. This is 
        # the heading reference in the normative specification which 
        # relates to this issue.
        print(my_issue.referenceHeading())

    # Retrieve the second ERROR-level issue from a Printer
    second_error = printer.error(1)

    # Retrieve the last WARNING-level issue from a Parser
    if parser.warningCount() > 0:
        last_warning = parser.warning(parser.warningCount() - 1)
    else:
        last_warning = None

    # Iterate through all MESSAGE-level issues in a Generator
    for m in range(generator.messageCount()):
        my_message = generator.message(m)

    # end CHECK_MODEL 1

    issue = validator.issue(0) if validator.issueCount() > 0 else None

    # start CHECK_MODEL 2

    # Retrieve and print the description of the issue.
    print(issue.description())

    # Retrieve and print the reference heading number, if related to CellML2.0 specification and format.
    print(issue.referenceHeading())

    # Retrieve and print the URL for more help and information about the issue. 
    print(issue.url())

    # Retrieve item type (CellmlElementType enum)
    my_type = issue.item().type()

    # Retrieve issue level (Issue.Level enum)
    my_level = issue.level()

    # end CHECK_MODEL 2

    return 0


if __name__ == "__main__":
    exit(main())
