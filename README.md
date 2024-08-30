Here's the setup guide for your FastAPI Chat Application broken down into a step-by-step format:

### FastAPI Chat Application Setup Guide

#### Prerequisites:
1. **Python 3.8 or higher**
2. **MySQL Server**
3. **pip** (Python package installer)

#### Database Setup:
1. **Start MySQL Server:**
   - Ensure that your MySQL server is running.
2. **Create a Database:**
   - Log into your MySQL shell.
   - Execute the following SQL command to create a new database:
     ```sql
     CREATE DATABASE gainzai;
     ```

#### Environment Setup:
1. **Clone the Repository:**
   - Download the code to your local machine using:
     ```bash
     git clone <repository-url>
     cd fastapi-chatbot
     ```
2. **Create and Activate a Virtual Environment:**
   - For Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - For MacOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Install Dependencies:**
   - Install all required Python packages using:
     ```bash
     pip install -r requirements.txt
     ```

#### Configuration:
1. **Environment Variables:**
   - Copy the provided `.env.txt` file to a new `.env` file using:
     ```bash
     cp .env.txt .env
     ```
   - Open the `.env` file and update it with your MySQL credentials and any other required settings.

#### Running the Application:
1. **Run your Application (`main.py`):**
   - Start the FastAPI server with:
     ```bash
     uvicorn main:app --reload
     ```
   - This command starts the server with live reloading enabled, which is suitable for development.

2. **Access the Application:**
   - Open a web browser and go to `http://127.0.0.1:8000/` to view the application.

These detailed instructions should guide you smoothly through setting up and running your FastAPI Chat Application.
