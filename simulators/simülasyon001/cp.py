#!/usr/bin/env python3
# cp.py (KESİN DÜZELTİLMİŞ SON VERSİYON)
import asyncio
import can
import websockets
import os
import logging

from ocpp.v16 import ChargePoint as BaseChargePoint
from ocpp.routing import on
from ocpp.v16 import call, call_result

logging.basicConfig(level=logging.INFO)

# CAN bus (vcan0)
try:
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')
    logging.info("[CP] vcan0 arayüzüne başarıyla bağlandı.")
except Exception as e:
    logging.error(f"[CP] !!! vcan0'a bağlanamadı: {e}")
    logging.error("[CP] !!! Lütfen PyCharm terminalinde 'sudo ip link set up vcan0' komutunu çalıştırdığından emin ol.")
    raise SystemExit(1)


class MyChargePoint(BaseChargePoint):

    async def send_can_message(self, can_id, data):
        try:
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            bus.send(msg)
            logging.warning(f"[CP->CAN] CAN Mesajı Gönderildi >> ID: 0x{can_id:X} | Data: {data.hex()}")
        except Exception as e:
            logging.error(f"[CP->CAN] CAN gönderme hatası: {e}")

    @on('RemoteStartTransaction')
    async def on_remote_start(self, connector_id=1, id_tag=None, **kwargs):
        """ NORMAL DURUM: CSMS'den 'Start' komutu gelirse... """
        logging.info(f"[CP] <<< NORMAL KOMUT: RemoteStartTransaction alındı (ID: {id_tag})")
        await self.send_can_message(0x200, bytes([connector_id, 1]))  # 1 = Başlat
        # Cevap (result) sınıfı 'Payload' eki içerir
        return call_result.RemoteStartTransactionPayload(status='Accepted')

    @on('RemoteStopTransaction')
    async def on_remote_stop(self, transaction_id=0, **kwargs):
        """ SALDIRI DURUMU: MITM 'Start' komutunu 'Stop' olarak değiştirdi... """
        logging.error(f"[CP] <<< SALDIRI ALGILANDI! (MITM) RemoteStopTransaction alındı (ID: {transaction_id})")
        await self.send_can_message(0x201, bytes([1]))  # 1 = Durdur
        # Cevap (result) sınıfı 'Payload' eki içerir
        return call_result.RemoteStopTransactionPayload(status='Accepted')


async def run_cp(ws_uri):
    proxy = os.environ.get('http_proxy')
    if proxy:
        logging.warning(f"[CP] Proxy üzerinden bağlanılıyor: {proxy}")

    async with websockets.connect(ws_uri) as ws:
        cp = MyChargePoint('CP_001', ws)
        logging.info(f"[CP] CSMS'e bağlanılıyor ({ws_uri}) ve BootNotification gönderiliyor...")

        # *** KESİN DÜZELTME (AttributeError için) ***
        # İstek (call) sınıfının adı 'BootNotification', 'Payload' eki yok.
        resp = await cp.call(call.BootNotification(
            charge_point_model="KaliSim-PyCharm",
            charge_point_vendor="Lab"
        ))

        logging.info(f"[CP] BootNotification cevabı: {resp}")
        await cp.start()  # Cevap başarılıysa sürekli dinlemeye geç


if __name__ == '__main__':
    uri = "ws://localhost:9000/CP_001"
    try:
        asyncio.run(run_cp(uri))
    except KeyboardInterrupt:
        logging.info("\n[CP] Çıkış yapılıyor.")
    except Exception as e:
        logging.error(f"[CP] !!! Bağlantı hatası: {e}")
        if "proxy" in str(e).lower():
            logging.error("[CP] !!! Proxy hatası. mitmproxy'nin (Terminal 3) çalıştığından emin misin?")
        elif "connection refused" in str(e).lower():
            logging.error("[CP] !!! Bağlantı reddedildi. CSMS'in (Run 1) çalıştığından emin misin?")
        else:
            logging.error(f"[CP] !!! Beklenmedik hata: {e}")