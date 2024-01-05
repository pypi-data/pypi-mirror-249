from logging import Logger
from typing import (
    Any,
    Dict,
    Type,
)


class ServiceManager:
    """
    Manages service instances for dependency injection.
    """

    def __init__(self, logger: Logger):
        self._services: Dict[Type, Any] = {Logger: logger}

    def get_service(self, service_type: Type) -> Any:
        """
        Retrieves a service instance of the specified type.

        :param service_type: The type of the service to retrieve.
        :return: The service instance or None if not found.
        """
        return self._services.get(service_type)

    def set_service(self, service_type: Type, instance: Any) -> None:
        """
        Sets a service instance for a specified type.

        :param service_type: The type of the service.
        :param instance: The instance of the service to be registered.
        """
        self._services[service_type] = instance
