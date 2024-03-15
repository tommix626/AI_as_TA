import logging

class BaseComponent:
    component_schema = {
        # the schema defining the component's input and output.
    }
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
