# [Video Demo]
Path: "Gainz_App/demo/FastAPI Demo Video.mp4"

# [backend]
gainz/ is the backend source code. Building by fastAPI and python
For test and code review, please follow below instruction. 

1. Install MongoDB, Python, Docker, and related dependencies. 
2. Install Python modules. Please view gainz/pyproject.toml. 
3. As this is using poetry for virtual environment development, please make sure the modules/dependencies are installed under poetry. 
    `poetry show` can show a list. 
    `poetry install` will update the modules 
    `poetry add` [individual modules] 
4. Copy .env-example in gainz/ to .env. And fill up JWT_SECRET and OPENAI_API_KEY. Either inform henry930@gmail.com to get the key, or you create your own. 
5. Make sure MongoDB, Docker, Python are up and running. For mongoDB, please stay admin with no password. Then:
    `cd /gainz/gainz`
    `poetry run python -m gainz`

6. Make sure your API url is http://127.0.0.1:8000/api/ As the frontend API Url is hard-code. Otherwise, please change in react manually. (See frontend section)

7. Most of the code are under gainz/gainz/web/api/monitoring/

# [frontend]
react_websocket/my-websocket-app is the frontend source code. Building by React and Typescript
I havn't test for dist/ built. So, please test both fronend and backend LOCALLY.

1. Node and NPM install in machine (I have just tested in Mac, my Node is 20.x, Apple M1 chipset)
`cd react_websocket/my-websocket-app`
`npm install`

2. Make sure your backend is work properly in LOCAL. 
 `npm start`
3. Your testing URL generally, is http://localhost:3000/ But may vary in different machine. 

4. In frontend, at the first time, you have to register a user for testing. 
5. Click "Register", and type your email and password, you account should generally be created instantly. Then use your email and password, you can login and chat with AI.
6. Please use Desktop with chrome browser. The width is no less than 800px, suggested using fullscreen for testing.   

###### For an instant online video demo, you can send henry930@gmail.com or linkedin: http://www.linkedin.com/in/henry930 I can arrange a time for showing my works. ######
