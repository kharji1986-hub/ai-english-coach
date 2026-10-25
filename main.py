from fastapi import FastAPI

app = FastAPI(
    title="AI English Coach",
    description="AI-powered English learning assistant",
    version="0.1.0"
)

@app.get("/")
def home():
    return {"message": "Welcome to AI English Coach"}
