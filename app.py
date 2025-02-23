from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import app as agent_app  # Import the LangGraph agent
import re

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend URL if deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define request model
class QueryRequest(BaseModel):
    input: str


# Define response endpoint
@app.post("/query")
async def get_response(query: QueryRequest):
    response = agent_app.invoke({"input": query.input})
    response["output"] = re.sub(r"<think>.*?</think>", "", response["output"], flags=re.DOTALL).strip()
    return {"output": response["output"]}

# Run the FastAPI app (only if executed directly)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
