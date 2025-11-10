import asyncio
import websockets
import logging
from ocpp.v16 import ChargePoint
from ocpp.v16.enums import RegistrationStatus
import can
from can import Message

# Loglama ayarları
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - CP_SIM - %(levelname)s - %(message)s',
                    filename='logs/evcs_system_detailed.log',
                    filemode='a')
logger = logging.getLogger('CP_SIM')

# Simülasyon parametreleri
CSMS_URL = "ws://127.0.0.1:9000/{}" 
CAN_START_ID = 0x200 # RemoteStartTransaction -> CAN mapping [cite: 28]

class ChargePointSimulator(ChargePoint):
    def __init__(self, cp_id, connection):
        super().__init__(cp_id, connection)
        self.cp_id = cp_id
        # python-can bus bağlantısını başlat
        try:
            self.can_bus = can.interface.Bus(channel='vcan0', bustype='virtual')
        except Exception:
            self.can_bus = None
            logger.error(f"CP {cp_id}: CAN Bus (vcan0) başlatılamadı.")

    async def send_boot_notification(self):
        """
        CSMS'ye bağlanınca BootNotification gönderir[cite: 45].
        """
        request = call.BootNotification(
            charge_point_model="Simulator",
            charge_point_vendor="GoogleAI"
        )
        response = await self.call(request)

        if response.registration_status == RegistrationStatus.accepted:
            logger.info(f"CP {self.cp_id}: Bağlantı kabul edildi.")
        else:
            logger.error(f"CP {self.cp_id}: Bağlantı reddedildi.")

    async def remote_start_transaction(self, id_tag):
        """
        CSMS'den gelen RemoteStartTransaction komutunu işler.
        Bu, saldırı anında çağrılacak kritik methoddur (CSMS simülatöründe tanımlanmalıdır).
        """
        logger.warning(f"CP {self.cp_id}: CSMS'den RemoteStartTransaction komutu alındı.")
        
        # --- KÖPRÜ GÖREVİ [cite: 4] ---
        if self.can_bus:
            # OCPP komutunu CAN Frame'e çevir 
            # Basit payload: cp_id (i), connector_id (1), start_cmd (0x01)
            # Not: Saldırgan betiği (coordinated_demand_mitm.py) zaten CAN mesajını direkt gönderecektir.
            # Ancak normal akışta CP bunu böyle yapacaktır.
            cp_id_int = int(self.cp_id.split('_')[1]) if '_' in self.cp_id else 1
            payload = bytes([cp_id_int, 1, 0x01]) # [cp_id, connector_id, start_cmd]
            can_msg = Message(
                arbitration_id=CAN_START_ID, 
                data=payload,
                is_extended_id=False
            )
            self.can_bus.send(can_msg)
            logger.info(f"CP {self.cp_id}: OCPP -> CAN (0x{CAN_START_ID:X}) çevrildi ve vcano'ya gönderildi.")
        
        # Normal OCPP cevabı (sadece simülasyon amaçlı)
        return call_result.RemoteStartTransaction(status=RemoteStartStopStatus.accepted)


async def run_cp_simulator(cp_id):
    """
    Belirli bir CP simülatörünü çalıştırır.
    """
    logger.info(f"CP {cp_id} simülatörü başlatılıyor...")
    async with websockets.connect(CSMS_URL.format(cp_id), subprotocols=['ocpp1.6']) as ws:
        cp = ChargePointSimulator(cp_id, ws)
        # BootNotification göndererek bağlantıyı kur
        await cp.send_boot_notification()
        
        # Sonsuza kadar dinle
        await asyncio.gather(
            cp.start() # Gelen OCPP komutlarını dinler (örneğin RemoteStartTransaction)
            # İsteğe bağlı: MeterValues gönderme görevi buraya eklenebilir.
        )


if __name__ == "__main__":
    # Tek bir CP yerine, birden fazla CP'yi başlatmak için kullanılır
    cp_count = 5 
    cp_tasks = [run_cp_simulator(f"CP_{i+1}") for i in range(cp_count)]
    
    try:
        # Tüm CP'leri eş zamanlı olarak başlat
        asyncio.run(asyncio.gather(*cp_tasks))
    except KeyboardInterrupt:
        logger.warning("CP Simülatörleri durduruldu.")