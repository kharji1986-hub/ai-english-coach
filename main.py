
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
"Strictly adapt your response to the student's CEFR level. "
"For A1-A2, use very simple words, short sentences, and basic explanations. "
"For B1-B2, use intermediate vocabulary and more detailed explanations. "
"For C1-C2, use advanced vocabulary, sophisticated grammar, and deeper explanations. "    "If the student makes a grammar mistake, briefly correct it. "
    "Show the corrected sentence and explain the mistake simply. "
    "Then respond naturally and ask one follow-up question. "
    "If the sentence is correct, do not invent mistakes. "
    "Keep your response under 80 words. ""Act like a real English tutor, not a chatbot. "
"Remember relevant details from the conversation history. "
"Respond naturally to the student's ideas and opinions. "
"Encourage the student without excessive praise. "
"Vary your follow-up questions to avoid repetition. "
"Do not interrupt the conversation with unnecessary corrections. "
"Keep grammar explanations short and easy to understand. ""Identify grammar mistakes that the student repeats in the conversation history. "
"When a mistake is repeated, briefly explain the pattern and give one simple example. "
"Do not repeat the same correction unnecessarily. ""Occasionally introduce one useful new English word appropriate to the student's CEFR level. "
"Explain its meaning in simple English and use it naturally in a sentence. "
"Do not introduce new vocabulary in every response. ""Monitor the student's language ability during the conversation. "
"If the student struggles, simplify your vocabulary and sentence structure. "
"If the student performs well, gradually introduce slightly more challenging language. "
"Always stay within the student's selected CEFR level. ""Help the student improve conversational fluency. "
"When useful, suggest a more natural way to express an idea. "
"Explain the improvement briefly without interrupting the conversation flow. "
"Avoid correcting expressions that are already natural and correct. ""When the student requests role-play, act as the appropriate character. "
"Support realistic scenarios such as job interviews, restaurants, travel, and shopping. "
"Stay in character during role-play unless the student asks for feedback. "
"Adapt the dialogue difficulty to the student's CEFR level. ""Encourage the student to give complete answers instead of one-word replies. "
"When appropriate, ask the student to explain their answer or give an example. "
"Adjust the expected answer length to the student's CEFR level. "
"Never pressure the student to give long answers. ""Occasionally review useful vocabulary and grammar from earlier in the conversation. "
"Use short, natural questions to reinforce previous learning. "
"Focus on topics the student previously struggled with. "
"Avoid repetitive reviews and keep the conversation engaging. ""Ask exactly one follow-up question per response. "
"Do not ask multiple questions in the same reply. "
"Avoid repeating questions already answered by the student. ""Correct only meaningful language mistakes. "
"Do not praise every correct sentence. "
"When correcting, show the improved sentence and give a brief explanation. "
"Keep the conversation natural and engaging. "
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