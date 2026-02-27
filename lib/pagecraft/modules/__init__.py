"""Module system for Pagecraft.

To create a custom module, subclass Module and implement render():

    from pagecraft.modules import Module

    class MyModule(Module):
        def render(self, data, styles, pagesize, **kwargs):
            # Return a list of reportlab Flowable objects
            ...

Then register it on a document:

    doc.register_module('my_thing', MyModule())
    doc.add('my_thing', some_data)
"""

from abc import ABC, abstractmethod


class Module(ABC):
    """Base class for PDF content modules."""

    @abstractmethod
    def render(self, data, styles, pagesize, **kwargs):
        """Render data into a list of reportlab flowables.

        Args:
            data: Module-specific input data.
            styles: reportlab StyleSheet1 with available paragraph styles.
            pagesize: Tuple of (width, height) in points.
            **kwargs: Additional module-specific options.

        Returns:
            List of reportlab Flowable objects.
        """


class ModuleRegistry:
    """Registry for content modules."""

    def __init__(self):
        self._modules = {}

    def register(self, name, module):
        if not isinstance(module, Module):
            raise TypeError(
                f"Module must be an instance of Module, got {type(module)}"
            )
        self._modules[name] = module

    def get(self, name):
        if name not in self._modules:
            available = ', '.join(sorted(self._modules.keys()))
            raise KeyError(f"Unknown module '{name}'. Available: {available}")
        return self._modules[name]

    def list_modules(self):
        return list(self._modules.keys())
