
Recording of ChatBot

https://github.com/user-attachments/assets/8d9452de-01dd-4472-9375-d6e87b960ed8



Recommended Project structure :
  
<img width="181" alt="project_struct" src="https://github.com/user-attachments/assets/ff8b34bf-98ba-4c74-beba-1a0f27830d7d">

•	To Start the project Run Auth.py  File.


•	It will open on Port 8001 


•	Enter the Login Details :  Username: user@example.com    Password: Secret


•	Once Authenticated it redirect to chatbot on Port 8000


Note:  .env file should have openai_apikey , assistant_id  and Api_key (For Authentication)

API Endpoints


•	POST /token: Authenticate a user and obtain a JWT token. Set the token in a cookie for secure access.


•	GET /: Displays the login page.


•	WebSocket /ws/{thread_id}: Establish a WebSocket connection for real-time interaction.

