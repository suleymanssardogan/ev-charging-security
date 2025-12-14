import os
import json
import asyncio
import requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from shared.utils.logger import get_logger
from shared.schemas.ocpp_messages import OCPPMessage

app = FastAPI()
logger = get_logger("CSMS")

DETECT_URL = os.getenv("DETECT_URL", "http://detect:9300")
BILLING_URL = os.getenv("BILLING_URL", "http://billing:9200")

@app.websocket("/ocpp/{charge_point_id}")
async def websocket_endpoint(websocket: WebSocket, charge_point_id: str):
    await websocket.accept()
    logger.info(f"Charge Point {charge_point_id} connected.")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received from {charge_point_id}: {data}")
            
            # Simple OCPP 1.6J parsing (Array format: [MessageTypeId, UniqueId, Action, Payload])
            try:
                msg_list = json.loads(data)
                if len(msg_list) != 4:
                    logger.error("Invalid message format")
                    continue
                
                msg_type, unique_id, action, payload = msg_list
                
                # Forward to Detection and Billing Engines
                event_data = {
                    "charge_point_id": charge_point_id,
                    "action": action,
                    "payload": payload,
                    "timestamp": payload.get("timestamp") # Might be None or in different field
                }
                
                # Fire and forget (or async call) to other services
                # In a real app, use a queue. Here, we'll try a simple post in background or just log it.
                # For this simulation, let's just print we would send it.
                # But to make it functional, we should actually send it.
                
                asyncio.create_task(forward_event(event_data))

                # Send response
                response = [3, unique_id, {}]
                await websocket.send_text(json.dumps(response))
                
            except json.JSONDecodeError:
                logger.error("Failed to decode JSON")
            
    except WebSocketDisconnect:
        logger.info(f"Charge Point {charge_point_id} disconnected.")

async def forward_event(event_data):
    try:
        # Forward to Detect
        requests.post(f"{DETECT_URL}/event", json=event_data, timeout=1)
        # Forward to Billing if it's a transaction event
        if event_data["action"] in ["StartTransaction", "StopTransaction", "MeterValues"]:
             requests.post(f"{BILLING_URL}/event", json=event_data, timeout=1)
    except Exception as e:
        logger.error(f"Failed to forward event: {e}")

