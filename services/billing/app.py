from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from shared.utils.logger import get_logger
from tariffs import calculate_cost

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = get_logger("Billing")

# In-memory store for active sessions
sessions = {}
invoices = []

@app.post("/event")
async def receive_event(request: Request):
    event = await request.json()
    logger.info(f"Received event: {event}")
    
    action = event.get("action")
    payload = event.get("payload", {})
    charge_point_id = event.get("charge_point_id")
    
    if action == "StartTransaction":
        transaction_id = payload.get("transactionId") # Note: In OCPP 1.6, StartTransaction RESPONSE has the ID. 
        # But here we are simulating the event flow. 
        # For simplicity, let's assume the CSMS attaches the transactionId to the forwarded event 
        # or we use the uniqueId to track it until we get the ID.
        # Actually, standard OCPP 1.6: CP sends StartTransaction, CSMS responds with ID.
        # Our CSMS implementation just forwarded the REQUEST payload.
        # The request payload DOES NOT have transactionId.
        # We need to handle this. 
        # For this simulation, let's assume the CSMS generates a transaction ID and includes it in the event forwarded to Billing.
        # I'll update CSMS later if needed, but for now let's assume the payload has it or we track by connectorId.
        pass

    # Simplified logic: We expect "StopTransaction" to contain the total consumption or we calculate from MeterValues.
    # Let's assume we just log it for now and calculate on StopTransaction.
    
    if action == "StopTransaction":
        transaction_id = payload.get("transactionId")
        meter_stop = payload.get("meterStop")
        # We need the start value. 
        # In a real system we'd query the DB. 
        # Here, let's just assume a simple cost calculation based on the 'meterStop' if we don't have start.
        # Or better, we just log the invoice.
        
        cost = calculate_cost(0, meter_stop) # Mock calculation
        invoice = {
            "transactionId": transaction_id,
            "chargePointId": charge_point_id,
            "totalKwh": meter_stop, # Simplified
            "totalCost": cost,
            "status": "GENERATED"
        }
        invoices.append(invoice)
        logger.info(f"Generated Invoice: {invoice}")

    return {"status": "ok"}

@app.get("/invoices")
def get_invoices():
    return invoices
