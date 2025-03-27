from fastapi import FastAPI

app = FastAPI()

# app.include_router(users.router)
# app.include_router(todos.router)

@app.get("/")
def home():
    return {"message": "Welcome to my Todo App"}