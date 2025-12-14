import json
import asyncio
import time
from datetime import datetime

async def send_message(ws, action, payload):
    unique_id = str(int(time.time() * 1000))
    msg = [2, unique_id, action, payload]
    await ws.send(json.dumps(msg))
    response = await ws.recv()
    return response

async def run_scenario(ws, scenario_name):
    if scenario_name == "normal":
        await run_normal(ws)
    elif scenario_name == "S1":
        await run_monotonicity_violation(ws)
    else:
        await run_normal(ws)

async def run_normal(ws):
    # Start Transaction
    await send_message(ws, "StartTransaction", {
        "connectorId": 1,
        "idTag": "TAG_001",
        "meterStart": 0,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Meter Values
    for i in range(1, 6):
        await asyncio.sleep(1)
        await send_message(ws, "MeterValues", {
            "connectorId": 1,
            "transactionId": 1, # Mock ID
            "meterValue": [{
                "timestamp": datetime.utcnow().isoformat(),
                "sampledValue": [{"value": str(i * 100)}]
            }]
        })
        
    # Stop Transaction
    await send_message(ws, "StopTransaction", {
        "transactionId": 1,
        "meterStop": 600,
        "timestamp": datetime.utcnow().isoformat(),
        "reason": "Local"
    })

async def run_monotonicity_violation(ws):
    # Start Transaction
    await send_message(ws, "StartTransaction", {
        "connectorId": 1,
        "idTag": "TAG_001",
        "meterStart": 0,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    # Meter Values (Increasing)
    for i in range(1, 4):
        await asyncio.sleep(1)
        await send_message(ws, "MeterValues", {
            "connectorId": 1,
            "transactionId": 1,
            "meterValue": [{
                "timestamp": datetime.utcnow().isoformat(),
                "sampledValue": [{"value": str(i * 100)}]
            }]
        })
        
    # Meter Values (Decreasing - Anomaly)
    await asyncio.sleep(1)
    await send_message(ws, "MeterValues", {
        "connectorId": 1,
        "transactionId": 1,
        "meterValue": [{
            "timestamp": datetime.utcnow().isoformat(),
            "sampledValue": [{"value": "250"}] # Drop from 300 to 250
        }]
    })
        
    # Stop Transaction
    await send_message(ws, "StopTransaction", {
        "transactionId": 1,
        "meterStop": 250,
        "timestamp": datetime.utcnow().isoformat(),
        "reason": "Local"
    })
