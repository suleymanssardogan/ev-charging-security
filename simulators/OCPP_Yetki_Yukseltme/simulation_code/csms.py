#!/usr/bin/env python3
# csms.py (Senaryo 2: SendLocalList - TAM KOD)
import asyncio
import logging
from datetime import datetime, timezone
from websockets.server import serve

from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as BaseChargePoint
from ocpp.routing import on
from ocpp.v16.enums import RegistrationStatus, UpdateType

logging.basicConfig(level=logging.INFO)

class ChargePoint(BaseChargePoint):
    @on('BootNotification')
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        """ BootNotification'a doğru sınıf (call_result.BootNotification) ile cevap verir. """
        logging.info(f"[CSMS] BootNotification from {self.id} model={charge_point_model} vendor={charge_point_vendor}")
        iso_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        return call_result.BootNotification(
            current_time=iso_time,
            interval=300,
            status=RegistrationStatus.accepted
        )

    @on('DataTransfer')
    async def on_data_transfer(self, vendor_id, message_id, data, **kwargs):
        """ cp.py'den gelecek simülasyon logunu yakalar. """
        if message_id == "Authorize":
            logging.warning(f"[CSMS] <<< Gelen Authorize İsteği (Simülasyondan): {data}")
        return call_result.DataTransfer(status="Accepted")


async def handler(websocket, path):
    cp_id = path.strip('/') or 'CP_001'
    cp = ChargePoint(cp_id, websocket)
    logging.info(f"[CSMS] New connect: {cp_id} (from path: {path})")

    # Yeni senaryo: 5 saniye sonra SendLocalList gönder
    async def delayed_send_list():
        await asyncio.sleep(5)
        try:
            # Sadece 1 adet geçerli ID gönder (Saldırgan bunu manipüle edecek)
            valid_list = [
                {
                    "idTag": "VALID_RFID_123",
                    "idTagInfo": {
                        "status": "Accepted",
                        "expiryDate": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                    }
                }
            ]
            payload = call.SendLocalList(
                list_version=1,
                local_authorization_list=valid_list,
                update_type=UpdateType.full
            )

            logging.info(f"[CSMS] >>> Sending SendLocalList (Version 1) to {cp_id} with 1 valid ID.")
            resp = await cp.call(payload)
            logging.info(f"[CSMS] <<< SendLocalList response: {resp}")

        except Exception as e:
            logging.error(f"[CSMS] Error while sending SendLocalList: {e}")

    asyncio.create_task(delayed_send_list())

    try:
        await cp.start()
    except Exception as e:
        logging.error(f"[CSMS] Connection error for {cp_id}: {e}")
    finally:
        logging.info(f"[CSMS] Connection closed for {cp_id}")


async def main():
    logging.info("[CSMS] Starting on ws://0.0.0.0:9000/")
    async with serve(handler, "0.0.0.0", 9000):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())