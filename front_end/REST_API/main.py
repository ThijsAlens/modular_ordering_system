from fastapi import FastAPI

front_end = FastAPI()

@front_end.get("/")
def root():
    return {"message": "Welcome to the front_end REST API. Visit \"/docs\" for the API documentation."}

