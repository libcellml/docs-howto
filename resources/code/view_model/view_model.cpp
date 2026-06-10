#include <libcellml>

int main(int argc, char *argv[])
{
    // Create a model and populate it with components, variables, resets, etc. 
    libcellml::ModelPtr myModel = libcellml::Model::create("Grandfather");
    libcellml::ComponentPtr myUncleComponent = libcellml::Component::create("Uncle");
    myModel->addComponent(myUncleComponent);
    libcellml::ComponentPtr myComponent = libcellml::Component::create("Mother");
    myModel->addComponent(myComponent);
    libcellml::ComponentPtr myDaughterComponent = libcellml::Component::create("Daughter");
    myComponent->addComponent(myDaughterComponent);
    libcellml::ComponentPtr mySonComponent = libcellml::Component::create("Son");
    myComponent->addComponent(mySonComponent);
    libcellml::ComponentPtr myGrandchildComponent = libcellml::Component::create("Grandchild");
    mySonComponent->addComponent(myGrandchildComponent);

    // Creating a Variable instance:
    libcellml::VariablePtr myVariable = libcellml::Variable::create("testVariable");
    myVariable->setInitialValue("3.14");
    myComponent->addVariable(myVariable);

    libcellml::ResetPtr myReset = libcellml::Reset::create();
    myReset->setTestVariable(myComponent->variable("testVariable"));
    myComponent->addReset(myReset);

    // start - VIEW_MODEL 1

    // Retrieving the name attribute from the myModel item:
    const std::string myModelName = myModel->name();

    // Retrieving the initial value of the myVariable item:
    const std::string myInitialValue = myVariable->initialValue();

    // end - VIEW_MODEL 1

    // start - VIEW_MODEL 2

    // Retrieve the test variable from the myReset item:
    libcellml::VariablePtr myTestVariable = myReset->testVariable();

    // end - VIEW_MODEL 2

    // start - VIEW_MODEL 3

    // Loop through variables in the component myComponent and retrieve their names.
    //    NOTE that indexing starts from zero.
    for(size_t v = 0; v < myComponent->variableCount(); ++v) {

        // Retrieve the Variable item at index v:
        auto myVariable = myComponent->variable(v);

        // Retrieve the name of the myVariable item:
        auto myVariableName = myVariable->name();
    }

    // Retrieve a variable called "helloThere" by name.
    //    NOTE that a nullptr will be returned if no variable of that name is found.
    auto myHelloThereVariable = myComponent->variable("helloThere");

    // In this case, the myMissingVariable will be a nullptr:
    auto myMissingVariable = myComponent->variable("nameThatDoesntExist");

    // This will cause a segfault as myMissingVariable is null:
    //auto myMissingName = myMissingVariable->name();

    // Safe alternative:
    if (myMissingVariable != nullptr) {
        auto myMissingName = myMissingVariable->name();
    }

    // end - VIEW_MODEL 3

    auto grandfather = myModel;

    // start - VIEW_MODEL 4

    // The number of components owned by the grandfather model refers *only* to its direct children:
    auto grandfatherHasTwoKids = grandfather->componentCount(); // returns 2

    // Each component must be interrogated individually to determine its children.
    //    Note that the uncle component is the 0th child of the grandfather model.
    auto uncleHasNoKids = grandfather->component(0)->componentCount();          // returns 0
    auto motherHasTwoKids = grandfather->component("Mother")->componentCount(); // returns 2

    // end - VIEW_MODEL 4
    return 0;
  }
