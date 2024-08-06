import asyncio
import random

from agents import AutonomousAgentAsyncio, MessageHandler, AgentMessage, AsyncioQueue, Behavior


async def run_connected_agents():
    agent1 = AutonomousAgentAsyncio(AsyncioQueue(), AsyncioQueue())
    agent2 = AutonomousAgentAsyncio(AsyncioQueue(), AsyncioQueue())

    # Set up message handlers and behaviors for both agents
    words = ['hello', 'sun', 'world', 'space', 'moon', 'crypto', 'sky', 'ocean', 'universe', 'human']

    # Create handler from the task.
    class HelloMessageHandler(MessageHandler):
        async def handle(self, message: AgentMessage):
            if 'hello' in message.message_content.lower():
                print(f"{id(self)} received message containing 'hello': {message}")

    class RandomMessagePublisherBehavior(Behavior):
        def __init__(self, send_from: AutonomousAgentAsyncio, send_to: AutonomousAgentAsyncio):
            self.send_from = send_from
            self.send_to = send_to

        async def execute(self):
            message = ' '.join(random.choices(words, k=2))
            print(f"{id(self.send_from)} publish message {message} for {id(self.send_to)}")
            await self.send_from.send_message(
                message=AgentMessage(message_type='all', message_content=message), to=self.send_to)

    # Register handlers.
    agent1.register_message_handler('all', HelloMessageHandler())
    agent2.register_message_handler('all', HelloMessageHandler())

    # Register behaviors.
    agent1.register_behavior('random_message_publish', RandomMessagePublisherBehavior(agent1, agent2), 2.0)
    agent2.register_behavior('random_message_publish', RandomMessagePublisherBehavior(agent2, agent1), 2.0)

    # Run both agents.
    await asyncio.gather(
        agent1.run(),
        agent2.run(),
    )


if __name__ == '__main__':
    print('Starting...')
    print('To cancel press Ctrl+C.')
    try:
        asyncio.run(run_connected_agents())
    except KeyboardInterrupt:
        print('Stopped.')
