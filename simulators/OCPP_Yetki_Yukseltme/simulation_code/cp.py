#!/usr/bin/env python3
# cp.py (Senaryo 2: SendLocalList - TAM KOD)
import asyncio
import can
import websockets
import os
import logging
import json

from ocpp.v16 import ChargePoint as BaseChargePoint
from ocpp.routing import on
from ocpp.v16 import call, call_result
from ocpp.v16.enums import AuthorizationStatus

logging.basicConfig(level=logging.INFO)

try:
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')
    logging.info("[CP] vcan0 arayüzüne başarıyla bağlandı.")
except Exception as e:
    logging.error(f"[CP] !!! vcan0'a bağlanamadı: {e}")
    raise SystemExit(1)


class MyChargePoint(BaseChargePoint):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_auth_list = {}

    async def send_can_message(self, can_id, data):
        try:
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            bus.send(msg)
            logging.warning(f"[CP->CAN] CAN Mesajı Gönderildi >> ID: 0x{can_id:X} | Data: {data.hex()}")
        except Exception as e:
            logging.error(f"[CP->CAN] CAN gönderme hatası: {e}")

    @on('SendLocalList')
    async def on_send_local_list(self, list_version, local_authorization_list, update_type, **kwargs):
        """ Saldırıya uğramış listeyi alır. """
        logging.info(f"[CP] <<< SendLocalList alındı (Type: {update_type}, Version: {list_version})")
        for item in local_authorization_list:
            tag = item['idTag']
            status = item.get('idTagInfo', {}).get('status', 'Invalid')
            self.local_auth_list[tag] = status
            if tag == "ATTACKER_TAG_999":
                logging.error(f"[CP] !!! DİKKAT: Listeye 'ATTACKER_TAG_999' eklendi! (HABERSİZ)")
            else:
                logging.info(f"[CP] +++ Listeye '{tag}' eklendi.")

        asyncio.create_task(self.simulate_attacker_auth(delay=10))
        return call_result.SendLocalListPayload(status='Accepted')

    async def simulate_attacker_auth(self, delay=10):
        """ 10 saniye sonra sahte kartı okutmayı simüle eder. """
        await asyncio.sleep(delay)
        attacker_id = "ATTACKER_TAG_999"
        logging.warning(f"[CP] ??? Simülasyon: '{attacker_id}' kartı okutuldu...")
        auth_status = self.local_auth_list.get(attacker_id, "Invalid")

        if auth_status == "Accepted":
            logging.error(f"[CP] !!! SALDIRI BAŞARILI! (Word Senaryosu)")
            logging.error(f"[CP] !!! '{attacker_id}' yerel listede 'Accepted' bulundu!")
            logging.error("[CP] !!! Yetkisiz şarj başlatılıyor... (CAN 0x200)")
            await self.send_can_message(0x200, bytes([1, 1]))  # CAN 0x200
        else:
            logging.info(f"[CP] Saldırı Başarısız. '{attacker_id}' listede bulunamadı.")

        try:
            await self.call(call.DataTransfer(
                vendor_id="MySim", message_id="Authorize",
                data=json.dumps({"idTag": attacker_id, "status": auth_status})
            ))
        except Exception as e:
            logging.error(f"[CP] Authorize DataTransfer gönderilemedi: {e}")


async def run_cp(ws_uri):
    proxy_url = os.environ.get('http_proxy')
    if proxy_url:
        logging.warning(f"[CP] Proxy üzerinden bağlanılıyor: {proxy_url}")

    async with websockets.connect(ws_uri) as ws:
        cp = MyChargePoint('CP_001', ws)
        logging.info(f"[CP] CSMS'e bağlanılıyor ({ws_uri}) ve BootNotification gönderiliyor...")
        resp = await cp.call(call.BootNotification(
            charge_point_model="KaliSim-PyCharm",
            charge_point_vendor="Lab"
        ))
        logging.info(f"[CP] BootNotification cevabı: {resp}")
        await cp.start()


if __name__ == '__main__':
    uri = "ws://localhost:9000/CP_001"
    try:
        asyncio.run(run_cp(uri))
    except KeyboardInterrupt:
        logging.info("\n[CP] Çıkış yapılıyor.")
    except Exception as e:
        logging.error(f"[CP] !!! Bağlantı hatası: {e}")
        if "proxy" in str(e).lower() or "HTTP" in str(e) or "TypeError" in str(e):
            logging.error("[CP] !!! Proxy hatası. mitmproxy'nin (Terminal 3) çalıştığından emin misin?")
        elif "connection refused" in str(e).lower():
            logging.error("[CP] !!! Bağlantı reddedildi. CSMS'in (Run 1) çalıştığından emin misin?")
        else:
            logging.error(f"[CP] !!! Beklenmedik hata: {e}")