import os
import openai


# OpenAI Key is in .env. However, it would not save in gitHub. Please send request to henry930@gmail.com, or you create your own. 
# This file has not been used. Just for reference. 

openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = OPENAI_API_KEY

completion = openai.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

print(completion.choices[0].message)