# Autonomous Agent Implementation

This project implements an autonomous agent system with asynchronous message handling and customizable behaviors.

The task goal is to test python developer [task definition: TODO].

## Features

- Asynchronous message processing using inbox and outbox queues. Quess are customizable and e.g. external Redis queues could be added
- Customizable message handlers for different message types
- Configurable behaviors that can be executed periodically
- Abstract base class (AutonomousAgentABC) defining the agent interface
- Concrete implementation (AutonomousAgentAsync) using asyncio

## Dependencies

- python3.7+

## Core Components

### AutonomousAgentABC

Abstract base class defining the interface for autonomous agents, including:

- Message handler registration
- Behavior registration
- Asynchronous message sending and receiving
- Main run loop

### AutonomousAgentAsync

Concrete implementation of AutonomousAgentABC providing:

- Asynchronous processing of inbox and outbox messages
- Execution of registered behaviors based on time intervals and conditions
- Fully async, single-threaded operation

## Usage

To create and run autonomous agents:

1. Instantiate AutonomousAgentAsync objects
2. Register message handlers for specific message types
3. Register behaviors with execution intervals and optional conditions
4. Set up message relaying between agents
5. Run the agents' main loops

## Example

The provided example demonstrates two interconnected agents:

- Agent 1 generates random 2-word messages every 2 seconds
- Both agents handle messages containing "hello"
- Messages are relayed between the agents' outboxes and inboxes

To run the example:

```python
python example.py
```

## Testing

This project includes unit and integration tests to ensure the correct functionality of the autonomous agents. The tests are implemented using pytest and can be found in the `test_agents.py` file.

### Running Tests

To run the tests, make sure you have pytest installed:

```bash
pytest
```