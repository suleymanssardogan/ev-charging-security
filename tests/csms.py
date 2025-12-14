#!/usr/bin/env python3
# csms.py - Güvenli Komut Gönderici (16A)
import asyncio
import logging
from datetime import datetime, timezone
from websockets.server import serve

from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as BaseChargePoint
from ocpp.routing import on
from ocpp.v16.enums import RegistrationStatus

logging.basicConfig(level=logging.INFO)

class ChargePoint(BaseChargePoint):
    @on('BootNotification')
    async def on_boot_notification(self, charge_point_model, charge_point_vendor, **kwargs):
        logging.info(f"[CSMS] BootNotification alındı: {self.id}")
        iso_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        return call_result.BootNotification(
            current_time=iso_time,
            interval=300,
            status=RegistrationStatus.accepted
        )

async def handler(websocket, path):
    cp_id = path.strip('/') or 'CP_001'
    cp = ChargePoint(cp_id, websocket)
    logging.info(f"[CSMS] Yeni bağlantı: {cp_id}")

    async def delayed_command():
        await asyncio.sleep(5)  # Bağlantıdan 5 sn sonra
        try:
            # GÜVENLİ KOMUT: Max Akım 16 Amper olsun
            logging.info(f"[CSMS] >>> GÜVENLİ KOMUT GÖNDERİLİYOR: ChangeConfiguration (MaxCurrent=16)")
            payload = call.ChangeConfiguration(key="MaxOutputCurrent", value="16")
            resp = await cp.call(payload)
            logging.info(f"[CSMS] <<< İstasyon Cevabı: {resp}")
        except Exception as e:
            logging.error(f"[CSMS] Hata: {e}")

    asyncio.create_task(delayed_command())

    try:
        await cp.start()
    except Exception as e:
        logging.error(f"[CSMS] Bağlantı koptu: {e}")

async def main():
    logging.info("[CSMS] Sunucu başlatılıyor: ws://0.0.0.0:9000/")
    async with serve(handler, "0.0.0.0", 9000):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
