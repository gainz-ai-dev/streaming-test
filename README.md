
Recording of ChatBot

https://github.com/user-attachments/assets/8d9452de-01dd-4472-9375-d6e87b960ed8


# WebSocket Chatbot with Authentication

This project sets up a web application with user authentication and real-time chatbot interaction using WebSockets. The application integrates with the OpenAI API to provide real-time responses to users connected to the same chat thread.

## Project Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Pip (Python package installer)

### Dependencies

Install the required Python packages using pip:

```bash
pip install fastapi uvicorn pydantic python-jose openai
```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
ASSISTANT_ID=your_assistant_id
API_KEY=your_api_key_for_authentication
```

Replace `your_openai_api_key`, `your_assistant_id`, and `your_api_key_for_authentication` with your actual OpenAI API key, assistant ID, and authentication API key respectively.

## Running the Project

### 1. Start the Authentication Server

Run the `Auth.py` file to start the authentication server:

```bash
python Auth.py
```

This server will start on port 8001.

### 2. Authenticate and Access Chatbot

- Open your browser and navigate to `http://localhost:8001`.
- Enter the login credentials:
  - **Username:** `user@example.com`
  - **Password:** `secret`
- Once authenticated, you will be redirected to the chatbot interface running on port 8000.

### 3. Chatbot Interface

The chatbot will be accessible at `http://localhost:8000`. Here, you can interact with the chatbot in real-time using WebSockets.

#### Chatbot Features
**Document Retrieval Mechanism**
The chatbot includes a retrieval mechanism that allows it to pull information from documents that have been uploaded to the backend. This mechanism ensures that the chatbot can provide accurate and relevant responses based on the content of these documents.

#### Contextual Understanding
The chatbot leverages the OpenAI API to understand the context of the conversation. It uses contextual understanding to generate responses that are coherent and relevant to the ongoing conversation, improving the overall user experience.

## API Endpoints

### Authentication

- **POST /token**
  - **Description:** Authenticate a user and obtain a JWT token.
  - **Request:**
    ```json
    {
      "username": "user@example.com",
      "password": "Secret"
    }
    ```
  - **Response:**
    ```json
    {
      "access_token": "jwt_token_here",
      "token_type": "bearer"
    }
    ```
  - **Note:** The JWT token is set in a secure cookie.

- **GET /**
  - **Description:** Displays the login page.

### WebSocket

- **WebSocket /ws/{thread_id}**
  - **Description:** Establish a WebSocket connection for real-time interaction with the chatbot.
  - **Path Parameters:**
    - `thread_id`: Identifier for the chat thread.
  - **Behavior:** The WebSocketManager class manages connections per thread, allowing broadcasting of messages to all clients in the same thread. The OpenAI API is used to generate responses to client messages.

## Recommended File Structure

<img width="181" alt="project_struct" src="https://github.com/user-attachments/assets/98977238-8883-40a7-97af-f0503c05bb4f">



## Notes

- Ensure that the `Auth.py` file and the main server script (`App.py`) use the correct environment variables and API keys.
- The WebSocket server will handle real-time communication and should be properly secured and tested for performance, especially if handling multiple clients.

