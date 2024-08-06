from abc import ABC, abstractmethod
import asyncio
from typing import Dict, Callable, Optional
import time

from dataclasses import dataclass


@dataclass
class AgentMessage:
    message_type: str
    message_content: str


class MessageHandler(ABC):
    @abstractmethod
    async def handle(self, message: AgentMessage):
        pass


class Behavior(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass

# TODO: make even better: different types for outbox and inbox (by specifying the type of the message).


class MessageQueue(ABC):
    @abstractmethod
    async def put(self, item):
        pass

    @abstractmethod
    async def get(self):
        pass

    @abstractmethod
    def empty(self) -> bool:
        pass


class AsyncioQueue(MessageQueue):
    def __init__(self):
        self.queue = asyncio.Queue()

    async def put(self, item):
        await self.queue.put(item)

    async def get(self):
        return await self.queue.get()

    def empty(self) -> bool:
        return self.queue.empty()


class AutonomousAgentABC(ABC):
    @abstractmethod
    async def run(self):
        pass

    @abstractmethod
    def register_message_handler(self, message_type: str, handler: MessageHandler):
        pass

    @abstractmethod
    def register_behavior(
            self, behavior_name: str, behavior: Behavior, delta: float, condition: Optional[Callable] = None):
        pass

    @abstractmethod
    async def send_message(self, message: AgentMessage, to: 'AutonomousAgentABC'):
        pass

    @abstractmethod
    async def receive_message(self, message: AgentMessage):
        pass


class AutonomousAgentAsyncio(AutonomousAgentABC):
    def __init__(self, inbox: MessageQueue, outbox: MessageQueue):
        self.inbox = inbox
        self.outbox = outbox
        self.message_handlers: Dict[str, MessageHandler] = {}
        self.behaviors: Dict[str, tuple[Behavior, float, Optional[Callable]]] = {}
        self.last_execution_time = 0

    async def run(self):
        while True:
            await asyncio.gather(
                self.execute_behaviors(),
                self.process_inbox(),
                self.process_outbox(),
            )

    def register_message_handler(self, message_type: str, handler: MessageHandler):
        self.message_handlers[message_type] = handler

    def register_behavior(
            self, behavior_name: str, behavior: Behavior, delta: float, condition: Optional[Callable] = None):
        self.behaviors[behavior_name] = (behavior, delta, condition)

    async def send_message(self, message: AgentMessage, to: 'AutonomousAgentABC'):
        await self.outbox.put({'to': to, 'message': message})

    async def receive_message(self, message: AgentMessage):
        await self.inbox.put(message)

    async def process_inbox(self):
        while not self.inbox.empty():
            message = await self.inbox.get()
            handler = self.message_handlers.get(message.message_type)
            if handler:
                await handler.handle(message)

    async def process_outbox(self):
        while not self.outbox.empty():
            message = await self.outbox.get()
            await message['to'].receive_message(message['message'])

    async def execute_behaviors(self):
        current_time = time.time()
        if current_time - self.last_execution_time >= min(delta for _, delta, _ in self.behaviors.values()):
            for behavior_name, (behavior, delta, condition) in self.behaviors.items():
                if current_time - self.last_execution_time >= delta:
                    if condition is None or condition():
                        await behavior.execute()
            self.last_execution_time = current_time
