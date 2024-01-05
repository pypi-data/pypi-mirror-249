from logging import (
    Logger,
    getLogger,
)
from typing import (
    Any,
    Dict,
    List,
    Type,
)

from event_driven_app.entities import (
    Command,
    CommandHandler,
    Event,
    EventHandler,
)
from event_driven_app.services import (
    CommandManager,
    DependencyInjector,
    EventManager,
    ServiceManager,
)


class App:
    def __init__(self, logger: Logger = None):
        if not logger:
            logger = getLogger('default')
        self.service_manager = ServiceManager(logger)
        self.dependency_injector = DependencyInjector(self.service_manager)
        self.event_manager = EventManager(logger)
        self.command_manager = CommandManager(logger)
        logger.info('App inited')

    def process_event(self, event: Event):
        self.event_manager.trigger(
            event=event, dependency_injector=self.dependency_injector
        )

    def run_command(self, command: Command):
        return self.command_manager.execute(
            command=command,
            event_manager=self.event_manager,
            dependency_injector=self.dependency_injector,
        )

    def register_services(self, services_list: Dict[Type, Any]):
        for service_type, service in services_list.items():
            self.service_manager.set_service(service_type, service)

    def register_events(self, events: Dict[Type[Event], List[Type[EventHandler]]]):
        for event_type, event_handlers in events.items():
            for event_handler in event_handlers:
                self.event_manager.register_handler(event_type, event_handler)

    def register_commands(self, commands: Dict[Type[Command], Type[CommandHandler]]):
        for command_type, command_handler in commands.items():
            self.command_manager.register_handler(command_type, command_handler)
