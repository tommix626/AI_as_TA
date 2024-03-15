"""
I think we currently don't need to use registry for specifc component.
It is only used by the factory.
"""
import logging


class ComponentRegistry:
    def __init__(self):
        self.components = {}

    def register(self, component):
        """Register a component instance in the registry."""
        if component.component_id in self.components:
            raise ValueError(f"Component ID {component.component_id} is already registered.")
        self.components[component.component_id] = component

    def get(self, component_id):
        """Retrieve a component instance by its ID."""
        component = self.components.get(component_id)
        if not component:
            logging.error(f"Component with ID {component_id} not found.")
            return None
        return component

    def execute(self, component_id):
        """Execute a component by its ID, ensuring output freshness."""
        component = self.get(component_id)
        if component:
            if not component.is_output_fresh:
                component.run()
            return component.get_output()
        return None
