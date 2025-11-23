import asyncio
import logging
import can
import websockets
from datetime import datetime, timezone

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16 import call_result
from ocpp.v16.enums import RegistrationStatus
from ocpp.routing import on

logging.basicConfig(level=logging.INFO)

# vcan0 arayüzünü kullan
try:
    can_bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    logging.info("vcan0 arayüzü başarıyla bağlandı.")
except Exception as e:
    logging.error(f"vcan0 arayüzü bağlanamadı: {e}")
    # Sanal makine dışında test ediliyorsa devam etsin diye exit() kaldırılabilir
    # exit()

class ChargePoint(cp):
    
    @on('RemoteStartTransaction')
    async def on_remote_start_transaction(self, id_tag, connector_id, **kwargs):
        logging.info(f"\nCP: CSMS'den RemoteStartTransaction komutu alındı (Connector {connector_id}).")
        
        # --- KÖPRÜ İŞLEMİ (OCPP -> CAN Mapping) ---
        cp_id = 1 
        start_cmd = 1
        
        can_msg = can.Message(
            arbitration_id=0x200, # RemoteStart
            data=[cp_id, connector_id, start_cmd],
            is_extended_id=False
        )
        
        try:
            logging.info(f"CP: CAN Mesajı vcan0'a gönderiliyor: ID=0x200, Data={can_msg.data}")
            can_bus.send(can_msg)
            return call_result.RemoteStartTransactionPayload(status="Accepted")
        except Exception as e:
            logging.error(f"CP: CAN Mesajı gönderilirken hata: {e}")
            return call_result.RemoteStartTransactionPayload(status="Rejected")
    
    @on('RemoteStopTransaction')
    async def on_remote_stop_transaction(self, transaction_id, **kwargs):
        logging.info(f"\nCP: CSMS'den RemoteStopTransaction komutu alındı (TX ID: {transaction_id}).")
        
        # --- KÖPRÜ İŞLEMİ (OCPP -> CAN Mapping) ---
        stop_cmd = 1
        
        # Gelen transactionId'yi CAN verisine ekle
        can_msg = can.Message(
            arbitration_id=0x201, # RemoteStop
            data=[transaction_id % 256, stop_cmd], 
            is_extended_id=False
        )
        
        try:
            logging.info(f"CP: CAN Mesajı vcan0'a gönderiliyor: ID=0x201, Data={can_msg.data}")
            can_bus.send(can_msg)
            return call_result.RemoteStopTransactionPayload(status="Accepted")
        except Exception as e:
            logging.error(f"CP: CAN Mesajı gönderilirken hata: {e}")
            return call_result.RemoteStopTransactionPayload(status="Rejected")

async def main():
    # Bağlantı adresi PROXY (Mitmproxy) portuna (8081) yönlendirilmiş durumda
    async with websockets.connect(
        "ws://localhost:8081/CP_12345", 
        subprotocols=["ocpp1.6"]
    ) as ws:
        
        cp = ChargePoint("CP_12345", ws)
        
        # Dinleyiciyi ayrı bir görev olarak başlat (Deadlock çözümü)
        listener_task = asyncio.create_task(cp.start())
        
        boot_payload = call.BootNotificationPayload(
            charge_point_model="SanalCP_v1",
            charge_point_vendor="Proje"
        )
        
        logging.info("CP: CSMS'ye bağlanıldı. BootNotification gönderiliyor...")
        response = await cp.call(boot_payload)
        
        if response.status == RegistrationStatus.accepted:
            logging.info("CP: BootNotification kabul edildi. Komut bekleniyor...")
        else:
            logging.warning("CP: BootNotification reddedildi.")
            
        await listener_task 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"İstemci çalışırken ana bir hata oluştu: {e}")