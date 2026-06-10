from libcellml import Model, Component, Variable, Reset


def main():
    # Create a model and populate it with components, variables, resets, etc.
    my_model = Model("Grandfather")

    my_uncle_component = Component("Uncle")
    my_model.addComponent(my_uncle_component)

    my_component = Component("Mother")
    my_model.addComponent(my_component)

    my_daughter_component = Component("Daughter")
    my_component.addComponent(my_daughter_component)

    my_son_component = Component("Son")
    my_component.addComponent(my_son_component)

    my_grandchild_component = Component("Grandchild")
    my_son_component.addComponent(my_grandchild_component)

    # Creating a Variable instance:
    my_variable = Variable("testVariable")
    my_variable.setInitialValue("3.14")
    my_component.addVariable(my_variable)

    my_reset = Reset()
    my_reset.setTestVariable(my_component.variable("testVariable"))
    my_component.addReset(my_reset)

    # start - VIEW_MODEL 1

    # Retrieve the model name.
    my_model_name = my_model.name()

    # Retrieve the initial value of the variable.
    my_initial_value = my_variable.initialValue()

    # end - VIEW_MODEL 1

    # start - VIEW_MODEL 2

    # Retrieve the test variable from the reset.
    my_test_variable = my_reset.testVariable()

    # end - VIEW_MODEL 2

    # start - VIEW_MODEL 3

    # Loop through variables in the component and retrieve names
    for v in range(my_component.variableCount()):
        my_variable = my_component.variable(v)
        my_variable_name = my_variable.name()

    # Retrieve a variable by name.
    my_hello_there_variable = my_component.variable("helloThere")

    # This will return None if not found.
    my_missing_variable = my_component.variable("nameThatDoesntExist")

    # This will cause an error.
    # my_missing_name = my_missing_variable.name()

    # Safe alternative:
    if my_missing_variable is not None:
        my_missing_name = my_missing_variable.name()

    # end - VIEW_MODEL 3

    grandfather = my_model

    # start - VIEW_MODEL 4

    # Direct children count only.
    grandfather_has_two_kids = grandfather.componentCount()  # 2

    # Check children of components.
    uncle_has_no_kids = grandfather.component(0).componentCount()  # 0
    mother_has_two_kids = grandfather.component("Mother").componentCount()  # 2

    # end - VIEW_MODEL 4

    return 0


if __name__ == "__main__":
    exit(main())
