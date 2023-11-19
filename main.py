from fastapi import FastAPI
from pydantic import BaseModel
from handlers.telegram import Telegram

app = FastAPI()


class EventMeta(BaseModel):
    kind: str
    name: str
    namespace: str
    reason: str


class WebhookMessage(BaseModel):
    eventmeta: EventMeta
    text: str
    time: str


@app.get("/healthz", status_code=200)
def health_check():
    return {"status": "healthy"}


@app.post("/webhook-telegram", status_code=200)
async def webhook_telegram(message: WebhookMessage):
    t = Telegram()
    t.send_message(message)
    return {"message": "Message sent succesfully."}
