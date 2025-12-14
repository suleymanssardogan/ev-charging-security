import os
import asyncio
import websockets
import json
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from shared.utils.logger import get_logger
from scenarios import run_scenario

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = get_logger("CP")

TARGET_WS = os.getenv("TARGET_WS", "ws://proxy:9100/ocpp/CP_001")

@app.post("/start/{scenario_name}")
async def start_scenario(scenario_name: str, background_tasks: BackgroundTasks):
    logger.info(f"Received request to start scenario: {scenario_name}")
    background_tasks.add_task(execute_scenario, scenario_name)
    return {"status": "started", "scenario": scenario_name}

async def execute_scenario(scenario_name: str):
    logger.info(f"Connecting to {TARGET_WS} for scenario {scenario_name}")
    try:
        async with websockets.connect(TARGET_WS) as ws:
            await run_scenario(ws, scenario_name)
    except Exception as e:
        logger.error(f"Scenario failed: {e}")

# Run default scenario on startup if needed, or just wait for API
# For this lab, let's wait for API or run default if env var is set
@app.on_event("startup")
async def startup_event():
    default_scenario = os.getenv("SCENARIO")
    if default_scenario and default_scenario != "manual":
        asyncio.create_task(execute_scenario(default_scenario))
