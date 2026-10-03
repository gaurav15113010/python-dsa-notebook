"""
Validated endpoint: Accept a question and max_results between 1 and 20; reject invalid input before processing.
{
  "question": "Find packaging suppliers in India",
  "max_results": 5
}

Requirements:
- question is required and must contain at least one non-whitespace character.
- max_results must be an integer between 1 and 20, defaulting to 5 when omitted.
- Invalid input must be rejected before search processing runs.
- For valid input, return the cleaned question and max_results. No actual search or LLM call is needed.
"""


from fastapi import FastAPI
from pydantic import BaseModel,Field,StringConstraints
from typing import Annotated
import uvicorn

app = FastAPI()

class ValidData(BaseModel):
    question:Annotated[str,StringConstraints(strip_whitespace=True,min_length=1)]
    max_results:int = Field(5,ge=1,le=20)

@app.post("/")
def fun1(request:ValidData):
    return{
        "question":request.question,
        "max_results":request.max_results
    }

if __name__== "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)