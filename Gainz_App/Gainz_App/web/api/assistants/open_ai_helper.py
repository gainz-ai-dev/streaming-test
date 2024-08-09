import asyncio
import threading
from typing import Any, Optional

from loguru import logger
from openai import AssistantEventHandler, OpenAI
from typing_extensions import override

from Gainz_App.settings import settings

client = OpenAI(api_key=settings.openai_api_key)


class EventHandler(AssistantEventHandler):
    def __init__(self, connection_manager: Any, thread_id: str) -> None:
        """
        Initialize an EventHandler instance.

        Args:
            connection_manager (Any): The connection manager responsible for broadcasting messages.
            thread_id (str): The unique identifier for the thread associated with this handler.
        """

        super().__init__()
        self.connection_manager = connection_manager
        self.thread_id = thread_id
        self.lock = threading.Lock()

    def send_message(self, message: str) -> None:
        """
        Start a new thread to send a message.

        This method creates and starts a new thread to handle sending the message asynchronously.

        Args:
            message (str): The message to be sent.

        Returns:
            None: This method does not return a value.
        """

        threading.Thread(target=self._send_message, args=(message,)).start()

    def _send_message(self, message: str) -> None:
        """
        Send a message asynchronously by broadcasting it.

        This private method runs asynchronously and sends the provided message to the connection manager
        to broadcast to all relevant clients.

        Args:
            message (str): The message to be broadcasted.

        Returns:
            None: This method does not return a value.
        """

        async def broadcast_message() -> None:
            await self.connection_manager.broadcast(self.thread_id, message)

        asyncio.run(broadcast_message())

    @override
    def on_text_created(self, text: str) -> None:
        """
        Handle the creation of new text.

        This method is called when new text is created. It logs the event but does not process the text.

        Args:
            text (str): The newly created text.

        Returns:
            None: This method does not return a value.
        """

        logger.info("\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta: Any, snapshot: Optional[Any]) -> None:
        """
        Handle updates to text content.

        This method is called when there is a delta update to the text. It sends the updated text message.

        Args:
            delta (Any): The delta object containing the updated text.
            snapshot (Optional[Any]): Optional snapshot of the text state before the update.

        Returns:
            None: This method does not return a value.
        """

        self.send_message(delta.value)

    def on_tool_call_created(self, tool_call: Any) -> None:
        """
        Handle the creation of a new tool call.

        This method is called when a new tool call is created. It sends a message about the tool call creation.

        Args:
            tool_call (Any): The tool call object.

        Returns:
            None: This method does not return a value.
        """

        self.send_message(f"Tool call created: {tool_call.type}")
        logger.info(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta: Any, snapshot: Optional[Any]) -> None:
        """
        Handle updates to a tool call.

        This method is called when there is a delta update to a tool call. It sends messages based on the type
        of the delta update, including code input and outputs.

        Args:
            delta (Any): The delta object containing updates to the tool call.
            snapshot (Optional[Any]): Optional snapshot of the tool call state before the update.

        Returns:
            None: This method does not return a value.
        """

        if delta.type == "code_interpreter":
            if delta.code_interpreter.input:
                self.send_message(delta.code_interpreter.input)
                logger.info(delta.code_interpreter.input, end="", flush=True)

            if delta.code_interpreter.outputs:
                self.send_message("Code output:")
                logger.info("\n\noutput >", flush=True)

                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        self.send_message(output.logs)


def create_assistant() -> str:
    """
    Create a new AI assistant.

    This function initializes an AI assistant with specific instructions and tools,
    and returns the unique identifier of the created assistant.

    Returns:
        str: The unique identifier of the created assistant.
    """

    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. "
        "Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo",
    )

    logger.info(assistant)

    return assistant.id


def create_thread() -> str:
    """
    Create a new conversation thread.

    This function creates a new thread and returns the unique identifier for the thread.

    Returns:
        str: The unique identifier of the created thread.
    """

    thread = client.beta.threads.create()
    logger.info(thread)

    return thread.id


def add_msg_to_thread(thread_id: str, message_content: str) -> str:
    """
    Add a message to a specific conversation thread.

    This function sends a message to the specified thread and returns the unique identifier
    of the created message.

    Args:
        thread_id (str): The identifier of the thread to which the message will be added.
        message_content (str): The content of the message to be added.

    Returns:
        str: The unique identifier of the created message.
    """

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_content,
    )

    logger.info(message)

    return message.id


def run_assistant_on_thread_sync(
    assistant_id: str, thread_id: str, event_handler: EventHandler,
) -> None:
    """
    Run an assistant on a specific thread synchronously.

    This function starts a synchronous run of the assistant on the specified thread and
    uses an event handler to process events. It blocks until the stream is done.

    Args:
        assistant_id (str): The unique identifier of the assistant to be run.
        thread_id (str): The unique identifier of the thread on which the assistant is run.
        event_handler (EventHandler): The handler for processing events generated during the run.

    Returns:
        None: This function does not return a value.
    """

    with client.beta.threads.runs.stream(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please address the user as Jane Doe. "
        "The user has a premium account.",
        event_handler=event_handler,
    ) as stream:
        stream.until_done()


async def run_assistant_on_thread(
    assistant_id: str, thread_id: str, event_handler: EventHandler,
) -> None:
    """
    Run an assistant on a specific thread asynchronously.

    This function starts an asynchronous run of the assistant on the specified thread.
    It uses an event handler to process events and runs the synchronous function
    in a separate thread to avoid blocking the event loop.

    Args:
        assistant_id (str): The unique identifier of the assistant to be run.
        thread_id (str): The unique identifier of the thread on which the assistant is run.
        event_handler (EventHandler): The handler for processing events generated during the run.

    Returns:
        None: This function does not return a value.
    """

    await asyncio.to_thread(
        run_assistant_on_thread_sync,
        assistant_id,
        thread_id,
        event_handler,
    )
