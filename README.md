# Autonomous Agent Implementation | Test Task

This project implements an autonomous agent system with asynchronous message handling and customizable behaviors.

The task goal is to test python developer

<details>
  <summary>The task</summary>
  
  ```markdown
  Python Software Engineer - Project A
  Instructions
  Your task, should you choose to accept it, is to implement an autonomous agent.
  Autonomous agents have a number of defining characteristics:
  - Communicate with the environment via asynchronous messages
  - Display reactiveness (handling messages) and proactiveness (generating new
  messages based on internal state or local time)
  - Can be thought of as representing a human, organisation, or thing in a specific
  domain and tasks
  Your autonomous agent should support these operations and characteristics:
  - Continuously consume messages (of different types) from an InBox
  - Emit messages to an OutBox
  - Allow for registration of message handlers to handle a given message type with its
  specific handler (reactive: if this message then that is done)
  - Allow for registration of behaviours (proactive: if this internal state or local time is
  reached then this message is created)
  Once the generic autonomous agent exists, create a concrete instance which:
  - Has one handler that filters messages for the keyword “hello” and prints the whole
  message to stdout
  - Has one behaviour that generates random 2-word messages from an alphabet of
  10 words (“hello”, “sun”, “world”, “space”, “moon”, “crypto”, “sky”, “ocean”, “universe”,
  “human”) every 2 seconds
  Run two instances of your concrete agents where the InBox of agent 1 is the OutBox of
  agent 2 and vice versa.
  Write one unit and one integration (both agents) test.

  Notes
  - Imagine you’re submitting a PR to a production project you’re working on
  
  - The design is light on details intentionally – we encourage you to make
  clarifications and request changes
  - Actual designs in the course of normal work at Valory would be much more fleshed
  out
  - We recommend using only pure Python3 and its standard libraries
  - Include some notes in the PR to walk us through any choices you needed to make
  or any feedback you have on the design
  - Ideally you would spend no more than 3 hours implementing
  ```
</details>

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
