
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to AI English Coach"
    }

from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_grammar_check():
    mock_feedback = {
        "original_text": "He go to school.",
        "corrected": "He goes to school.",
        "explanation": "Use 'goes' with 'he'.",
        "natural": "He goes to school."
    }

    with patch("main.OpenAI") as mock_openai:
        import json

        mock_openai.return_value.responses.create.return_value.output_text = (
            json.dumps({
                "corrected": mock_feedback["corrected"],
                "explanation": mock_feedback["explanation"],
                "natural": mock_feedback["natural"]
            })
        )

        response = client.post(
            "/grammar/check",
            json={"text": "He go to school."}
        )

    assert response.status_code == 200
    assert response.json() == mock_feedback

