

from fastapi import FastAPI
from User import User

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.post("/{prompt}")
def process_prompt(prompt):
    response = User(prompt)
    return {"response": response}
