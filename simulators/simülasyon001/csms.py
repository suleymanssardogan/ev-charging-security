#!/usr/bin/env python3
# csms.py (KESİN DÜZELTİLMİŞ SON VERSİYON)
import asyncio
import logging
from datetime import datetime, timezone
from websockets.server import serve

from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as BaseChargePoint
from ocpp.routing import on
from ocpp.v16.enums import RegistrationStatus

# Loglamayı açalım, PyCharm'da daha net görünür
logging.basicConfig(level=logging.INFO)


class ChargePoint(BaseChargePoint):
    @on('BootNotification')
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        logging.info(f"[CSMS] BootNotification from {self.id} model={charge_point_model} vendor={charge_point_vendor}")

        # Düzeltme (datetime.utcnow() uyarısı için):
        iso_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        # *** KESİN DÜZELTME (AttributeError için) ***
        # Cevap sınıfının adı 'BootNotification', 'BootNotificationPayload' değil.
        return call_result.BootNotification(
            current_time=iso_time,
            interval=300,
            status=RegistrationStatus.accepted
        )


async def handler(websocket, path):
    cp_id = path.strip('/') or 'CP_001'
    cp = ChargePoint(cp_id, websocket)
    logging.info(f"[CSMS] New connect: {cp_id} (from path: {path})")

    async def delayed_start():
        await asyncio.sleep(5)  # Bağlantı kurulduktan 5 sn sonra
        try:
            # *** KESİN DÜZELTME (AttributeError için) ***
            # İstek (call) sınıfının adı 'RemoteStartTransaction', 'Payload' eki yok.
            payload = call.RemoteStartTransaction(
                id_tag="TEST_TAG",
                connector_id=1
            )
            logging.info(f"[CSMS] >>> Sending RemoteStartTransaction to {cp_id}")
            resp = await cp.call(payload)
            logging.info(f"[CSMS] <<< RemoteStartTransaction response: {resp}")
        except Exception as e:
            logging.error(f"[CSMS] Error while sending RemoteStartTransaction: {e}")

    asyncio.create_task(delayed_start())

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