from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from shared.utils.logger import get_logger
from rules import check_rules

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = get_logger("Detection")

alerts = []
# State to track previous meter values for monotonicity check
session_state = {} 

@app.post("/event")
async def receive_event(request: Request):
    event = await request.json()
    logger.info(f"Received event: {event}")
    
    new_alerts = check_rules(event, session_state)
    if new_alerts:
        alerts.extend(new_alerts)
        logger.warning(f"Generated Alerts: {new_alerts}")
        
    return {"status": "ok"}

@app.get("/alerts")
def get_alerts():
    return alerts
