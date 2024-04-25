import json
import logging

import deprecated


class BaseComponent:
    component_schema = ""  # the schema defining the component's input and output.
    thinker_description = ""  # TODO add the description field used for thinker.
    builder_description = ""  # TODO add the description field used for builder.

    def __init__(self, component_id):
        self.component_id = component_id
        self.output = None
        self.is_output_fresh = False
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{self.component_id}")
        self.upstream_dependency = []

    def add_dependency(self, dependency):
        """Add a single upstream dependency for this component."""
        if dependency not in self.upstream_dependency:
            self.upstream_dependency.append(dependency)
            dependency.register_downstream(self)

    def register_downstream(self, downstream_component):
        """Optionally used by upstream components to track downstream components. Placeholder for now."""
        pass

    def run(self):
        """Execute the component.
            NOTE: it has no return value, the result is set to self.output.
        """

        # Stage 1: Prepare input
        # This stage is specific to each component and will be implemented in subclasses.
        inputs = self.prepare_inputs()

        # Stage 2: Execute main logic
        self.execute(inputs)
        self.is_output_fresh = True

    def prepare_inputs(self):
        """Prepare inputs for the component. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method to prepare inputs.")

    def execute(self, inputs):
        """Execute the component's main logic with the prepared inputs. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method for execution.")

    def get_output(self):
        """Retrieve the component's output if it is fresh, or invoke the main run if the output is not fresh"""
        if not self.is_output_fresh:
            self.run()
            # self.logger.warning("Attempted to access stale output.")
        return self.output

    def perish(self):
        for upstream_component in self.upstream_dependency:
            upstream_component.perish()
        self.is_output_fresh = False

    @classmethod
    def get_component_schema(cls):
        """Return the parsed JSON schema for the component."""
        return json.loads(cls.component_schema)

    @property
    def modifiable_params(self):
        """Dynamically retrieve modifiable parameters based on the component schema."""
        schema = self.get_component_schema()
        params = {}
        for input_param in schema.get("inputs", []):
            param_name = input_param["parameter"]
            param_value = getattr(self, param_name, None)  # Default to None if not set
            params[param_name] = param_value
        # print("$$$$$$$$$$$$$")
        # print(params)
        return params

    @deprecated.deprecated #should not use, can directly use the registry to wrap around.
    def get_modifiable_params(self):
        """Extract and return modifiable parameters from the component schema."""
        return {self.component_id: self.modifiable_params}

    def update_modifiable_params(self, params):
        """Update the modifiable parameters of the component."""
        for param, value in params.items():
            if hasattr(self, param):
                setattr(self, param, value)
            else:
                self.logger.warning(f"No such parameter '{param}' to update in {self.__class__.__name__}.")
