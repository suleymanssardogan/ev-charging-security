import can
import time
import logging
import threading
import random

# Loglama ayarları
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - CAN_CHGR - %(levelname)s - %(message)s',
                    filename='logs/evcs_system_detailed.log',
                    filemode='a')
logger = logging.getLogger('CAN_CHARGER')

# --- CAN PARAMETRELERİ (Dökümandan) ---
CAN_START_ID = 0x200   # Gelen şarj başlatma komutu 
CAN_METER_ID = 0x300   # Geri gönderilen enerji ölçüm (MeterValues) verisi [cite: 31]
BUS_CHANNEL = 'vcan0'

def create_meter_value_message(cp_id_int, current_power):
    """
    MeterValues simülasyon mesajını oluşturur (CAN ID 0x300).
    Payload: [cp_id, power_value_msb, power_value_lsb]
    """
    # Güç değeri (kWh cinsinden, basitlik için random)
    meter_value = current_power * random.uniform(0.9, 1.1)
    meter_val_int = int(meter_value * 100) # 2 byte'a sığdırmak için x100 yapalım

    power_msb = (meter_val_int >> 8) & 0xFF
    power_lsb = meter_val_int & 0xFF
    
    # Basit payload: CP ID (1 Byte), Güç MSB (1 Byte), Güç LSB (1 Byte)
    payload = bytes([cp_id_int, power_msb, power_lsb])
    
    return Message(
        arbitration_id=CAN_METER_ID, 
        data=payload,
        is_extended_id=False
    )

def run_can_charger_module():
    """
    CAN bus'ı dinler ve 0x200 komutuna 0x300 MeterValues ile cevap verir.
    """
    logger.info(f"CAN Şarj Modülü simülatörü başlatılıyor. Dinlenen ID: 0x{CAN_START_ID:X}")

    try:
        # Sanal CAN (vcano) arayüzüne bağlan
        bus = can.interface.Bus(channel=BUS_CHANNEL, bustype='virtual')
        
        # CAN bus'tan mesajları sürekli oku
        while True:
            # Gelen mesajı bekle
            message = bus.recv(timeout=0.1) 
            
            if message and message.arbitration_id == CAN_START_ID:
                
                # 1. Gelen Başlatma Komutunu İşle (0x200)
                # Payload: [cp_id, connector_id, start_cmd, power_flag]
                cp_id_int = message.data[0]
                power_flag = message.data[3] # Saldırganın enjekte ettiği yüksek güç talebi

                logger.warning(f"0x{CAN_START_ID:X} (RemoteStart) alındı. Hedef CP ID: {cp_id_int}, Talep: {power_flag}A")
                
                # Gerçek hayatta burada röle açılır ve şarj başlar.
                
                # 2. Cevap Mesajı Gönder (MeterValues Simülasyonu) (0x300)
                # Şarj başladığı için MeterValues gönderme simülasyonu
                
                meter_msg = create_meter_value_message(
                    cp_id_int=cp_id_int, 
                    current_power=power_flag 
                )
                bus.send(meter_msg)
                
                logger.info(f"0x{CAN_METER_ID:X} (MeterValues) gönderildi. Güç: {power_flag}A'ya yakın.")

    except can.exceptions.VirtualBusError:
        logger.error(f"CAN Bus '{BUS_CHANNEL}' bulunamadı.")
    except Exception as e:
        logger.error(f"CAN Şarj Modülü çalışma hatası: {e}")
    finally:
        if 'bus' in locals():
            bus.shutdown()
            logger.warning("CAN Şarj Modülü durduruldu.")

if __name__ == "__main__":
    # Modülü sürekli dinlemesi için ayrı bir iş parçacığında başlatın
    charger_thread = threading.Thread(target=run_can_charger_module, daemon=True)
    charger_thread.start()
    
    print("CAN Şarj Modülü arka planda çalışıyor. CAN trafiği bekliyor.")

    # Main thread'in sonlanmaması için bekleme
    try:
        while charger_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("CAN Şarj Modülü simülasyonu manuel olarak durduruldu.")
        pass