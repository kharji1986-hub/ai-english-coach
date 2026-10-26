
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from openai import OpenAI, RateLimitError, AuthenticationError, APIConnectionError
app = FastAPI(
    title="AI English Coach",
    description="AI-powered English learning assistant",
    version="0.1.0"
)


class GrammarRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Welcome to AI English Coach"}



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
