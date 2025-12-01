import asyncio
import websockets
import logging
from datetime import datetime

from ocpp.v16 import call_result
from ocpp.v16.enums import RegistrationStatus, Action
from ocpp.v16 import ChargePoint

logging.basicConfig(level=logging.INFO)

connected_cps = {}


class CentralSystemSimulator(ChargePoint):
    
    async def route_call(self, connection, call):
        """CP'den gelen komutları işler."""
        
        if call.action == Action.BootNotification:
            response = call_result.BootNotification(
                current_time=datetime.utcnow().isoformat(),
                interval=300,
                status=RegistrationStatus.accepted
            )
            return response

        return await super().route_call(connection, call)


async def on_connect(websocket, path):
    """Yeni CP bağlandığında çalışır."""
    cp_id = path.strip("/")
    logging.info(f"{cp_id} bağlandı.")

    cp = CentralSystemSimulator(cp_id, websocket)
    connected_cps[cp_id] = cp

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        "0.0.0.0",
        9000,
        subprotocols=['ocpp1.6']
    )

    logging.info("CSMS Simülatörü 9000 portunda çalışıyor...")
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

