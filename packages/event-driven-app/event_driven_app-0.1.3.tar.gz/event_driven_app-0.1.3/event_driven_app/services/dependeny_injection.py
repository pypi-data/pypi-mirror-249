from typing import (
    Any,
    Dict,
    Type,
)

from event_driven_app.services.service_manager import ServiceManager


class DependencyInjector:
    """
    Injects dependencies into classes automatically based on type annotations.
    """

    def __init__(self, service_manager: ServiceManager):
        self.service_manager = service_manager

    def prepare_dependency(self, class_type: Type) -> Dict[str, Any]:
        """
        Prepares dependencies for the given class type based on constructor annotations.

        :param class_type: The class for which dependencies are to be prepared.
        :return: A dictionary of parameter names and their corresponding instances.
        """
        constructor = class_type.__init__
        param_annotations = constructor.__annotations__
        params = {
            name: self.service_manager.get_service(param_type)
            for name, param_type in param_annotations.items()
            if name != "return"
            and self.service_manager.get_service(param_type) is not None
        }
        return params
