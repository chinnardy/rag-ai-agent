from fastapi import FastAPI
from pydantic import BaseModel

from agents.router_agent import RouterAgent
from agents.retrieval_agent import RetrievalAgent
from agents.response_agent import ResponseAgent

app = FastAPI()

docs = [
    "You can reset your password from the settings page.",
    "We support AWS, Azure, and GCP deployments.",
    "APIs are available via REST endpoints.",
]

router = RouterAgent()
retrieval_agent = RetrievalAgent(docs)
response_agent = ResponseAgent()


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(req: ChatRequest):
    route = router.route(req.question)

    if route == "rag":
        answer = retrieval_agent.execute(req.question)
    else:
        answer = response_agent.generate(req.question)

    return {"route": route, "answer": answer}


@app.get("/")
def root():
    return {"status": "ok"}
