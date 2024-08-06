import pytest
import asyncio
from agents import AutonomousAgentAsyncio, AsyncioQueue, AgentMessage, MessageHandler


@pytest.mark.asyncio
async def test_register_and_handle_message():
    inbox = AsyncioQueue()
    outbox = AsyncioQueue()
    agent = AutonomousAgentAsyncio(inbox, outbox)

    class TestHandler(MessageHandler):
        def __init__(self):
            self.handled_message = None

        async def handle(self, message):
            self.handled_message = message

    test_handler = TestHandler()
    agent.register_message_handler('test', test_handler)

    test_message = AgentMessage(message_type='test', message_content='Hello, world!')
    await agent.receive_message(test_message)
    await agent.process_inbox()

    assert test_handler.handled_message == test_message
    assert test_handler.handled_message.message_type == 'test'
    assert test_handler.handled_message.message_content == 'Hello, world!'


@pytest.mark.asyncio
async def test_two_agents_communication():
    agent1 = AutonomousAgentAsyncio(AsyncioQueue(), AsyncioQueue())
    agent2 = AutonomousAgentAsyncio(AsyncioQueue(), AsyncioQueue())

    messages_received = []

    class TestHandler:
        async def handle(self, message):
            messages_received.append(message.message_content)

    agent1.register_message_handler('all', TestHandler())
    agent2.register_message_handler('all', TestHandler())

    await agent1.send_message(AgentMessage(message_type='all', message_content='Hello from agent1'), agent2)
    await agent2.send_message(AgentMessage(message_type='all', message_content='Hello from agent2'), agent1)

    await asyncio.gather(
        agent1.process_outbox(),
        agent2.process_outbox(),
        agent2.process_inbox(),
        agent1.process_inbox(),
    )

    assert messages_received == ['Hello from agent1', 'Hello from agent2']
