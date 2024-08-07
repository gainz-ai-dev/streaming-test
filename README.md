# Gainz Streaming Test

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Endpoints](#endpoints)

## Getting Started

Follow these instructions to set up and run the Gainz Streaming Test project on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following software installed:

- Docker
- Docker Compose
- Node.js
- npm

### Installation

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd gainz
```

## Running the Application

1. Start the Backend:

   - Navigate to the gainz directory
   - Rename the .env.example file to .env
   - Add your OpenAI API key to the `GAINZ_OPENAI_KEY` variable in the .env file
   - Start the backend services using Docker Compose:

   ```
   cd gainz
   mv .env.example .env
   docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
   ```

2. Run Database Migrations:
   Open a new terminal tab, navigate to the gainz directory, and run the database migrations:

   ```
   cd gainz
   docker-compose run --rm api alembic upgrade "head"
   ```

3. Start the Frontend:

   - Open another new terminal tab, navigate to the frontend directory
   - Rename the .env.example file to .env
   - Start the frontend development server:

   ```
   cd frontend
   mv .env.example .env
   npm install
   npm run start
   ```

## Usage

Once the application is running, you can access the various services as follows:

### Backend

The backend API documentation can be accessed at:

```
http://localhost:8000/api/docs#/
```

### Frontend

1. Register:
   Go to the registration page to create a new user account:

   ```
   http://localhost:3000/auth/register
   ```

2. Login:
   After successful registration, go to the login page:

   ```
   http://localhost:3000/auth/login
   ```

3. Chat Page:
   Access the chat page:

   ```
   http://localhost:3000/
   ```

### Endpoints

Here are some of the primary endpoints available in the application:

- Register: `/auth/register`
- Login: `/auth/login`
- Chat: `/`
- Create New Thread: `POST /api/openai/threads/`
- Send Message to Thread: `POST /api/openai/threads/{thread_id}/messages/`
