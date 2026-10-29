
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
from openai import OpenAI, RateLimitError, AuthenticationError, APIConnectionError
app = FastAPI(
    title="AI English Coach",
    description="AI-powered English learning assistant",
    version="0.1.0"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

class GrammarRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return FileResponse("static/index.html")



@app.post("/grammar/check")
def check_grammar(request: GrammarRequest):
    try:
        client = OpenAI()

        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are a professional English teacher. "
                "Correct the student's sentence and explain mistakes. "
                "Suggest a more natural English sentence."
            ),
            input=request.text,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "grammar_feedback",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "corrected": {"type": "string"},
                            "explanation": {"type": "string"},
                            "natural": {"type": "string"}
                        },
                        "required": [
                            "corrected",
                            "explanation",
                            "natural"
                        ],
                        "additionalProperties": False
                    }
                }
            }
        )

        feedback = json.loads(response.output_text)

        return {
            "original_text": request.text,
            "corrected": feedback["corrected"],
            "explanation": feedback["explanation"],
            "natural": feedback["natural"]
        }

    except RateLimitError:
        raise HTTPException(
            status_code=503,
            detail="AI service quota exceeded. Please try again later."
        )

    except AuthenticationError:
        raise HTTPException(
            status_code=503,
            detail="AI service authentication is unavailable."
        )

    except APIConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Unable to connect to the AI service."
        )
from pydantic import BaseModel
from fastapi import HTTPException
from openai import OpenAI

class ChatRequest(BaseModel):
    level: str = "A1"
    message: str
    history: list[dict[str, str]] = []

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        client = OpenAI()

        response = client.responses.create(
            model="gpt-4.1-mini",
       instructions=(
    "You are a friendly and professional English speaking coach. "
    "Have a natural conversation with the student in English. "
    f"The student's English level is {request.level}. "
"Adapt your vocabulary, grammar, and sentence complexity to this CEFR level. "
    "If the student makes a grammar mistake, briefly correct it. "
    "Show the corrected sentence and explain the mistake simply. "
    "Then respond naturally and ask one follow-up question. "
    "If the sentence is correct, do not invent mistakes. "
    "Keep your response under 80 words. "
),
            input=[
    *request.history,
    {"role": "user", "content": request.message}
]
        )

        return {"reply": response.output_text}

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate a reply."
        )