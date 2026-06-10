#include <iostream>
#include <libcellml>

int main(int argc, char *argv[])
{
  const std::string annotateModelEx01 = R"(<?xml version="1.0" encoding="UTF-8"?>
    <!-- start - ANNOTATE_MODEL_XML 1 -->

<model name="annotateModelEx01" xmlns="http://www.cellml.org/cellml/2.0#" >
  <component name="c1" id="c1id">
    <variable name="v1" id="v1id" />
  </component>
  <component name="c2" id="c2id">
    <variable name="v2" id="v2id" />
  </component>

  <!-- The variable equivalence is stored separately to the variables themselves. -->
  <connection component1="c1" component2="c2" id="c1c2id">
    <map_variables variable1="v1" variable2="v2" id="v1v2id" />
  </connection>
</model>
<!-- end - ANNOTATE_MODEL_XML 1 -->
)";

  const std::string annotateModelEx02 = R"(
  <!-- start - ANNOTATE_MODEL_XML 2 -->
    <model name="annotateModelEx02" xmlns="http://www.cellml.org/cellml/2.0#" >
      <component name="grandparent" id="grandparentComponentId" />
      <component name="parent" id="parentComponentId" />
      <component name="child" id="childComponentId" />

      <!-- The ids of the components in the encapsulation structure are distinct
           from the ids on the components themselves. -->
      <encapsulation id="encapsId">
        <component_ref component="grandparent" id="grandparentEncapsId" >
          <component_ref component="parent" id="parentEncapsId" >
            <component_ref component="child" id="childEncapsId" />
          </component_ref>
        </component_ref>
      </encapsulation>
    </model>
    <!-- end - ANNOTATE_MODEL_XML 2 -->
)";

    auto parser = libcellml::Parser::create();
    auto model = parser->parseModel(annotateModelEx01);
    for (size_t i = 0; i < parser->errorCount(); ++i) {
        std::cout << parser->error(i)->description() << std::endl;
    }

    std::cout << "Section 1: Annotating a Model item with an ID attribute." << std::endl;
    // start - ANNOTATE_MODEL 1

    // Set the ID attribute for a Model item.
    model->setId("myModelId");

    // Retrieve the ID attribute from a Model item.
    std::string myModelIdString = model->id();

    // end - ANNOTATE_MODEL 1
    std::cout << "Section 1a: Annotating a Model item with an ID attribute." << std::endl;
    std::cout << parser->errorCount() << " errors found during parsing." << std::endl;
    auto v1 = model->component("c1")->variable("v1");
    auto v2 = model->component("c2")->variable("v2");

    std::cout << "Section 2: Annotating a Model item with an ID attribute." << std::endl;
    // start - ANNOTATE_MODEL 2

    // Set the ID of the mapping between variables v1 and v2.
    libcellml::Variable::setEquivalenceMappingId(v1, v2, "v1v2Id");

    // Get the ID of the mapping between variables v1 and v2. Note that
    // equivalences and connections go both ways, so the ID is the same
    // whichever order the variables are specified.
    std::string v1v2IdString = libcellml::Variable::equivalenceMappingId(v1, v2);

    // Since a connection item between two components will only exist
    // when there is a variable equivalence between at least one each
    // of their children.  The connection is accessed through those
    // child variable pairs, just as the equivalence mapping itself is.
    libcellml::Variable::setEquivalenceConnectionId(v1, v2, "c1c2id");

    // Get the ID of the connection between the parent components of
    // equivalent variable pair. Note that equivalences and connections
    // go both ways, so the ID is the same whichever order the variables
    // are specified.
    std::string c1c2IdString = libcellml::Variable::equivalenceConnectionId(v1, v2);

    // end - ANNOTATE_MODEL 2

    model = parser->parseModel(annotateModelEx02);
        for (size_t i = 0; i < parser->errorCount(); ++i) {
        std::cout << parser->error(i)->description() << std::endl;
    }

    auto grandparentComponent = model->component("grandparent");
    std::cout << "Section 3: Annotating a Model item with an ID attribute." << std::endl;

    // start - ANNOTATE_MODEL 3

    // Set the encapsulation ID.
    model->setEncapsulationId("encapsId");
    grandparentComponent->setEncapsulationId("grandparentEncapsId");

    // Get the encapsulation ID.
    std::string modelEncapsulationId = model->encapsulationId();
    std::string grandparentEncapsulationId = grandparentComponent->encapsulationId(); 

    // end - ANNOTATE_MODEL 3
    std::cout << "Section 4: Annotating a Model item with an ID attribute." << std::endl;

    // start - ANNOTATE_MODEL 4

    // Create a Units item representing millimetre^3 per second.
    auto mm3PerSecond = libcellml::Units::create("mm3PerSecond");

    // Add the per second part with the ID "perSecondUnitId".
    mm3PerSecond->addUnit("second", 0, -1.0, 1.0, "perSecondUnitId");

    // Add the mm^3 part with with the ID "mmCubedUnitId".
    mm3PerSecond->addUnit("metre", "milli", 3.0, 1.0, "mmCubedUnitId");

    // Check that the ID has been assigned to the Unit children.
    auto checkId1 = mm3PerSecond->unitId(0); // returns "perSecondUnitId".
    auto checkId2 = mm3PerSecond->unitId(1); // returns "mmCubedUnitId".

    // Change the ID of the second (ie: index = 1) child to be "millimetreCubedUnitId":
    mm3PerSecond->setUnitId(1, "millimetreCubedUnitId");

    // Retrieve the unit attributes for the first (index = 0) unit item, including the ID attribute:
    std::string unitReference;
    std::string unitPrefix;
    double unitExponent;
    double unitMultiplier;
    std::string unitId;
    mm3PerSecond->unitAttributes(0, unitReference, unitPrefix, unitExponent, unitMultiplier, unitId);

    // end - ANNOTATE_MODEL 4

    return 0;
}
