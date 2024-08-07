from openai import OpenAI
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key and assistant ID here
openai_key         = os.getenv("OPENAI_API_KEY")
assistant_id    = os.getenv("assistant_id")


# Initialize OpenAI client and assistant
def initialize_openai(api_key, assistant_id):
    client = OpenAI(api_key=api_key)
    assistant = client.beta.assistants.retrieve(assistant_id)
    thread = client.beta.threads.create()
    return client, assistant, thread

client, my_assistant, assistant_thread = initialize_openai(openai_key, assistant_id)

# Wait for the assistant to complete the response
async def wait_for_response(run, thread):
    while run.status in ["queued", "in_progress"]:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        await asyncio.sleep(1)
    return run

# Get response from the assistant
async def get_assistant_response(client, thread, assistant_id, user_input):
    message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_input)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
    run = await wait_for_response(run, thread)
    
    # Retrieve all messages after the user's last message
    messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc", after=message.id)
    return messages.data[0].content[0].text.value

async def get_response(user_input):
    return await (get_assistant_response(client, assistant_thread, assistant_id, user_input))