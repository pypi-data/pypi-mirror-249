from abc import (
    ABC,
    abstractmethod,
)
from importlib import import_module
from inspect import isclass
from logging import Logger
from os import (
    listdir,
    sep,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Type,
)

from event_driven_app.entities import (
    Command,
    CommandHandler,
    Event,
    EventHandler,
)
from event_driven_app.services.dependeny_injection import DependencyInjector


class AbstractManager(ABC):
    @abstractmethod
    def register_handler(self, event_type: Type, handler: Type) -> None:
        pass

    @abstractmethod
    def get_entity(self) -> Tuple[Type, Type]:
        pass

    def discover(self, path):
        python_path = path.replace(sep, ".")
        expected_executor, expected_actor = self.get_entity()
        for module_name in listdir(path):
            if not module_name.endswith(".py") or module_name.startswith("__"):
                continue
            module = import_module(f"{python_path}.{module_name[:-3]}")

            for attr_name in dir(module):
                executor = getattr(module, attr_name)
                if not isinstance(executor, type) or not issubclass(
                    executor, expected_executor
                ):
                    continue
                for argument, actor in executor.__init__.__annotations__.items():
                    if not isclass(actor) or not issubclass(actor, expected_actor):
                        continue
                    self.register_handler(actor, executor)


class EventManager(AbstractManager):
    """
    Manages event handling by registering and triggering event handlers.
    """

    def get_entity(self) -> Tuple[Type, Type]:
        return EventHandler, Event

    def __init__(self, logger: Logger):
        self.logger = logger
        self._handlers: Dict[Type[Event], List[Type[EventHandler]]] = {}

    def register_handler(
        self, event_type: Type[Event], handler: Type[EventHandler]
    ) -> None:
        """
        Registers an event handler for a specific event type.

        :param event_type: The type of the event.
        :param handler: The handler class for the event.
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def trigger(self, event: Event, dependency_injector: DependencyInjector) -> None:
        """
        Triggers all handlers for a given event.

        :param event: The event instance to be handled.
        :param dependency_injector: The DependencyInjector to prepare dependencies.
        """
        self.logger.info('Event triggered', extra={event.__class__.__name__: event.model_dump_json()})
        for handler in self._handlers.get(type(event), []):
            dependency = dependency_injector.prepare_dependency(handler)
            self.logger.info(f'Event handler {handler.__name__} start')
            handler_instance: EventHandler = handler(event=event, **dependency)
            self.logger.info(f'Event handler {handler.__name__} finish')
            handler_instance.handle()
            for new_event in handler_instance.events:
                self.trigger(event=new_event, dependency_injector=dependency_injector)


class CommandManager(AbstractManager):
    """
    Manages command execution by handling command types with respective handlers.
    """

    def __init__(self, logger: Logger):
        self.logger = logger
        self._handlers: Dict[Type[Command], Type[CommandHandler]] = {}

    def get_entity(self) -> Tuple[Type, Type]:
        return CommandHandler, Command

    def register_handler(
        self, command_type: Type[Command], handler: Type[CommandHandler]
    ) -> None:
        """
        Registers a command handler for a specific command type.

        :param command_type: The type of the command.
        :param handler: The handler class for the command.
        """
        if command_type in self._handlers:
            raise ValueError(f"A lot of command handler for command {command_type}")
        self._handlers[command_type] = handler

    def execute(
        self,
        command: Command,
        event_manager: EventManager,
        dependency_injector: DependencyInjector,
    ) -> Any:
        """
        Executes a command by invoking its handler.

        :param command: The command instance to be executed.
        :param event_manager: The EventManager for event handling.
        :param dependency_injector: The DependencyInjector for dependency injection.
        :return: The result of the command execution.
        """
        self.logger.info('Command execute', extra={command.__class__.__name__: command.model_dump_json()})
        handler: Type[CommandHandler] = self._handlers.get(type(command))
        if not handler:
            raise ValueError(f"No handler registered for command type: {type(command)}")
        dependency = dependency_injector.prepare_dependency(handler)
        self.logger.info(f'Command handler {handler.__name__} start')
        handler_instance: CommandHandler = handler(command=command, **dependency)
        result = handler_instance.handle()
        self.logger.info(f'Command handler {handler.__name__} finish')
        for new_event in handler_instance.events:
            event_manager.trigger(
                event=new_event, dependency_injector=dependency_injector
            )
        return result
