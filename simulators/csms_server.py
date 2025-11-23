import asyncio
import logging
import websockets
from datetime import datetime, timezone

from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result
from ocpp.v16.enums import RegistrationStatus
from ocpp.routing import on

logging.basicConfig(level=logging.INFO)

class SimpleCSMS(cp):
    @on('BootNotification')
    async def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        """CP'den gelen BootNotification mesajını işler."""
        logging.info(f"CSMS: {charge_point_vendor} model {charge_point_model} bağlandı.")
        return call_result.BootNotificationPayload(
            current_time=datetime.now(timezone.utc).isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    async def send_remote_start(self, connector_id):
        """CP'ye RemoteStartTransaction isteği gönderir."""
        from ocpp.v16 import call
        request = call.RemoteStartTransactionPayload(
            connector_id=connector_id,
            id_tag="test_tag_123"
        )
        logging.info(f"CSMS: RemoteStartTransaction gönderiliyor (Connector {connector_id})")
        response = await self.call(request)
        logging.info(f"CSMS: CP'den yanıt alındı: {response}")

# Bağlı olan tüm CP'leri (Charge Point) bu sözlükte tutacağız
connected_charge_points = {}

async def on_connect(websocket, path): 
    """Yeni bir şarj noktası bağlandığında çalışır."""
    try:
        # ID'yi URL'den alıyoruz (path düzeltmesi)
        charge_point_id = path.strip('/') 
        charge_point = SimpleCSMS(charge_point_id, websocket)
        connected_charge_points[charge_point_id] = charge_point

        logging.info(f"{charge_point_id} bağlandı.")
        await charge_point.start()
    except Exception as e:
        logging.error(f"Bağlantı hatası: {e}")
    finally:
        # Bağlantı kesildiğinde listeden kaldır
        if 'charge_point_id' in locals() and charge_point_id in connected_charge_points:
            del connected_charge_points[charge_point_id]
            logging.info(f"{charge_point_id} bağlantısı kesildi.")

async def main():
    # 'async with' bloğu sunucuyu sürekli çalışır halde tutar
    async with websockets.serve(on_connect, "0.0.0.0", 9000, subprotocols=['ocpp1.6']):
        logging.info("CSMS Sunucusu 9000 portunda dinlemede...")
        await send_commands_loop()

async def send_commands_loop():
    """Belirli aralıklarla bağlı cihazlara komut göndermek için örnek döngü"""
    while True:
        await asyncio.sleep(10)
        
        if connected_charge_points:
            try:
                # Sözlükteki ilk CP'yi al
                cp_id = list(connected_charge_points.keys())[0]
                cp = connected_charge_points[cp_id]
                
                # Ona komut gönder
                await cp.send_remote_start(connector_id=1)
            except Exception as e:
                logging.warning(f"Komut gönderme döngüsünde hata: {e}")

if __name__ == "__main__":
    logging.info("CSMS Sunucusu başlatılıyor...")
    asyncio.run(main())