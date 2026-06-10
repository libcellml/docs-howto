from libcellml import Model, Parser, Variable, Units


def main():
    annotate_model_ex01 = """<?xml version="1.0" encoding="UTF-8"?>
    <!-- start - ANNOTATE_MODEL_XML 1 -->

<model name="annotateModelEx01" xmlns="http://www.cellml.org/cellml/2.0#">
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
"""

    annotate_model_ex02 = """
  <!-- start - ANNOTATE_MODEL_XML 2 -->
    <model name="annotateModelEx02" xmlns="http://www.cellml.org/cellml/2.0#">
      <component name="grandparent" id="grandparentComponentId" />
      <component name="parent" id="parentComponentId" />
      <component name="child" id="childComponentId" />

      <!-- The ids of the components in the encapsulation structure are distinct
           from the ids on the components themselves. -->
      <encapsulation id="encapsId">
        <component_ref component="grandparent" id="grandparentEncapsId">
          <component_ref component="parent" id="parentEncapsId">
            <component_ref component="child" id="childEncapsId" />
          </component_ref>
        </component_ref>
      </encapsulation>
    </model>
    <!-- end - ANNOTATE_MODEL_XML 2 -->
"""

    parser = Parser()
    model = parser.parseModel(annotate_model_ex01)

    for i in range(parser.errorCount()):
        print(parser.error(i).description())

    print("Section 1: Annotating a Model item with an ID attribute.")

    # start - ANNOTATE_MODEL 1

    # Set and get model ID
    model.setId("myModelId")
    my_model_id_string = model.id()

    # end - ANNOTATE_MODEL 1

    print("Section 1a: Annotating a Model item with an ID attribute.")
    print(f"{parser.errorCount()} errors found during parsing.")

    v1 = model.component("c1").variable("v1")
    v2 = model.component("c2").variable("v2")

    print("Section 2: Annotating a Model item with an ID attribute.")

    # start - ANNOTATE_MODEL 2

    # Set and get equivalence mapping ID
    Variable.setEquivalenceMappingId(v1, v2, "v1v2Id")
    v1v2_id_string = Variable.equivalenceMappingId(v1, v2)

    # Set and get equivalence connection ID
    Variable.setEquivalenceConnectionId(v1, v2, "c1c2id")
    c1c2_id_string = Variable.equivalenceConnectionId(v1, v2)

    # end - ANNOTATE_MODEL 2

    # Parse second model
    model = parser.parseModel(annotate_model_ex02)

    for i in range(parser.errorCount()):
        print(parser.error(i).description())

    grandparent_component = model.component("grandparent")

    print("Section 3: Annotating a Model item with an ID attribute.")

    # start - ANNOTATE_MODEL 3

    # Set encapsulation IDs
    model.setEncapsulationId("encapsId")
    grandparent_component.setEncapsulationId("grandparentEncapsId")

    # Get encapsulation IDs
    model_encapsulation_id = model.encapsulationId()
    grandparent_encapsulation_id = grandparent_component.encapsulationId()

    # end - ANNOTATE_MODEL 3

    print("Section 4: Annotating a Model item with an ID attribute.")

    # start - ANNOTATE_MODEL 4

    # Create units: mm^3 per second
    mm3_per_second = Units("mm3PerSecond")

    # Add per second part
    mm3_per_second.addUnit("second", 0, -1.0, 1.0, "perSecondUnitId")

    # Add mm^3 part
    mm3_per_second.addUnit("metre", "milli", 3.0, 1.0, "mmCubedUnitId")

    # Check IDs
    check_id1 = mm3_per_second.unitId(0)
    check_id2 = mm3_per_second.unitId(1)

    # Update ID
    mm3_per_second.setUnitId(1, "millimetreCubedUnitId")

    # Retrieve unit attributes
    unit_reference, unit_prefix, unit_exponent, unit_multiplier, unit_id = mm3_per_second.unitAttributes(0)

    # end - ANNOTATE_MODEL 4

    return 0


if __name__ == "__main__":
    exit(main())
