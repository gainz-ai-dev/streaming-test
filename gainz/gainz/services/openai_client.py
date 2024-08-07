from openai import OpenAI
from typing import Dict, Any, List

from loguru import logger
from gainz.settings import settings


class OpenAIClient:
    def __init__(self):
        """
        Initialize the OpenAIClient with the given API key and assistant settings.
        """
        self.client = OpenAI(api_key=settings.openai_key)
        self.assistant_name = "Gainz Test"
        self.assistant_instructions = "You are a personal assistant to answer questions."
        self.assistant_model = "gpt-4o-mini"

    def list_assistants(
            self, order: str = "desc", limit: int = 20
    ) -> Any:
        """
        List all available assistants.
        """
        try:
            return self.client.beta.assistants.list(order=order, limit=limit).data
        except Exception as e:
            logger.error(f"Failed to list assistants: {e}")
            raise

    def create_assistant(
            self, instructions: str, name: str, model: str
    ) -> Dict[str, Any]:
        """
        Create a new assistant.
        """
        try:
            return self.client.beta.assistants.create(
                instructions=instructions,
                name=name,
                model=model,
            )
        except Exception as e:
            logger.error(f"Failed to create assistant '{name}': {e}")
            raise

    def get_or_create_assistant(self) -> Dict[str, Any]:
        """
        Retrieve an existing assistant matching the specified name, instructions,
        and model, or create a new one if none exists.
        """
        try:
            assistants = self.list_assistants()
            for assistant in assistants:
                if (
                    assistant.name == self.assistant_name and
                    assistant.instructions == self.assistant_instructions and
                    assistant.model == self.assistant_model
                ):
                    return assistant
            return self.create_assistant(
                self.assistant_instructions,
                self.assistant_name,
                self.assistant_model
            )
        except Exception as e:
            logger.error(f"Failed to get or create assistant: {e}")
            raise

    def create_thread(self) -> Dict[str, Any]:
        """
        Create a new thread.
        """
        try:
            return self.client.beta.threads.create()
        except Exception as e:
            logger.error(f"Failed to create thread: {e}")
            raise

    def retrieve_thread(self, thread_id: str) -> Dict[str, Any]:
        """
        Retrieve a thread by its ID.
        """
        try:
            return self.client.beta.threads.retrieve(thread_id)
        except Exception as e:
            logger.error(f"Failed to retrieve thread {thread_id}: {e}")
            raise

    def update_thread(
            self, thread_id: str, metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a thread's metadata.
        """
        try:
            return self.client.beta.threads.update(thread_id, metadata=metadata)
        except Exception as e:
            logger.error(f"Failed to update thread {thread_id}: {e}")
            raise

    def create_and_run_thread(
            self,
            assistant_id: str,
            messages: List[Dict[str, str]],
            stream: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new thread and run the assistant on it.
        """
        try:
            return self.client.beta.threads.create_and_run(
                assistant_id=assistant_id,
                thread={"messages": messages},
                stream=stream
            )
        except Exception as e:
            logger.error(
                f"Failed to create and run thread with assistant "
                f"{assistant_id}: {e}"
            )
            raise

    def add_message_to_thread(
            self, thread_id: str, role: str, content: str
    ) -> Any:
        """
        Add a message to a thread.
        """

        try:
            return self.client.beta.threads.messages.create(
                thread_id, role=role, content=content
            )
        except Exception as e:
            logger.error(f"Failed to add message to thread {thread_id}: {e}")
            raise

    def run_assistant_on_thread(
            self, thread_id: str, assistant_id: str, stream: bool = False
    ) -> Any:
        """
        Run an assistant on a thread.
        """

        try:
            return self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                stream=stream,
            )
        except Exception as e:
            logger.error(f"Failed to run assistant on thread {thread_id}: {e}")
            raise

    def list_thread_messages(
            self, thread_id: str, limit: int = 20, order: str = 'desc'
    ) -> Dict[str, Any]:
        """
        List messages from a thread.
        """
        try:
            return self.client.beta.threads.messages.list(
                thread_id=thread_id, limit=limit, order=order
            )
        except Exception as e:
            logger.error(
                f"Failed to list messages for thread {thread_id}: {e}")
            raise

    def retrieve_assistant_response(self, thread_id: str, run_id: str) -> Any:
        """
        Retrieve the response from an assistant run on a thread.
        """

        try:
            return self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id
            )
        except Exception as e:
            logger.error(
                f"Failed to retrieve assistant response for thread"
                f"{thread_id}: {e}"
            )
            raise


openai_client = OpenAIClient()
