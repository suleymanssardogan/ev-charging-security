from pydantic import BaseModel
from typing import Optional, List, Any, Dict

class OCPPMessage(BaseModel):
    messageTypeId: int
    uniqueId: str
    action: str
    payload: Dict[str, Any]

class StartTransactionPayload(BaseModel):
    connectorId: int
    idTag: str
    meterStart: int
    timestamp: str

class MeterValue(BaseModel):
    timestamp: str
    sampledValue: List[Dict[str, Any]]

class MeterValuesPayload(BaseModel):
    connectorId: int
    transactionId: Optional[int] = None
    meterValue: List[MeterValue]

class StopTransactionPayload(BaseModel):
    transactionId: int
    idTag: Optional[str] = None
    timestamp: str
    meterStop: int
    reason: Optional[str] = None
    transactionData: Optional[List[Dict[str, Any]]] = None
