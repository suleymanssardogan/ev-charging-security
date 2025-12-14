import os
import json
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from shared.utils.logger import get_logger

app = FastAPI()
logger = get_logger("Proxy")

TARGET_CSMS = os.getenv("TARGET_CSMS", "ws://csms:9000")
MODE = os.getenv("MODE", "PASS_THROUGH")

@app.websocket("/ocpp/{charge_point_id}")
async def proxy_endpoint(client_ws: WebSocket, charge_point_id: str):
    await client_ws.accept()
    logger.info(f"CP {charge_point_id} connected to Proxy.")
    
    # Connect to upstream CSMS
    csms_url = f"{TARGET_CSMS}/ocpp/{charge_point_id}"
    try:
        async with websockets.connect(csms_url) as csms_ws:
            logger.info(f"Proxy connected to CSMS for {charge_point_id}")
            
            async def forward_to_csms():
                try:
                    while True:
                        data = await client_ws.receive_text()
                        logger.info(f"CP -> CSMS: {data}")
                        # Manipulation hook could go here
                        await csms_ws.send(data)
                except Exception as e:
                    logger.error(f"Error forwarding to CSMS: {e}")

            async def forward_to_cp():
                try:
                    while True:
                        data = await csms_ws.recv()
                        logger.info(f"CSMS -> CP: {data}")
                        await client_ws.send_text(data)
                except Exception as e:
                    logger.error(f"Error forwarding to CP: {e}")

            await asyncio.gather(forward_to_csms(), forward_to_cp())

    except Exception as e:
        logger.error(f"Failed to connect to CSMS: {e}")
        await client_ws.close()
