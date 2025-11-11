import can
import time
import logging
from collections import deque
import threading
from can import Message

# Loglama ayarları
# Tüm sistemin ana log dosyasına kritik uyarıları eklemek için 'a' (append) modu kullanılır.
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - CAN-IDS - %(levelname)s - %(message)s',
                    filename='logs/evcs_system_detailed.log',
                    filemode='a') 
logger = logging.getLogger('CAN_IDS')

# --- IDS PARAMETRELERİ ---
CAN_ATTACK_ID = 0x200   # Takip edilecek CAN ID: RemoteStartTransaction karşılığı
TIME_WINDOW_SEC = 1.0   # Analiz penceresi (son 1 saniye)
THRESHOLD_COUNT = 5     # Anomali eşiği: 1 saniyede bu ID'den bu sayıdan fazla gelirse
BUS_CHANNEL = 'vcan0'

# Gelen mesajların zaman damgalarını tutmak için kuyruk (deque) yapısı
frame_timestamps = deque()
anomaly_detected_flag = False # Anomaliyi bir kere tespit ettikten sonra sürekli loglamayı önler

def analyze_can_message(msg):
    """
    Gelen CAN mesajını analiz eder ve frekans bazında anomali tespiti yapar.
    """
    global anomaly_detected_flag
    current_time = time.time()
    
    # Sadece saldırı ile ilişkilendirilen CAN ID'yi kontrol et
    if msg.arbitration_id == CAN_ATTACK_ID:
        
        # 1. Kuyruğa yeni zaman damgasını ekle
        frame_timestamps.append(current_time)
        
        # 2. Zaman penceresi dışındaki (eski) zaman damgalarını temizle
        # (örn: 1.0 saniyeden daha eski olanları çıkar)
        while frame_timestamps and frame_timestamps[0] < current_time - TIME_WINDOW_SEC:
            frame_timestamps.popleft()
            
        # 3. Kalan mesaj sayısını kontrol et (Anomali Tespiti)
        current_count = len(frame_timestamps)
        
        if current_count > THRESHOLD_COUNT and not anomaly_detected_flag:
            # Anomali bulundu!
            logger.critical(f"*** ANOMALİ TESPİT EDİLDİ! *** CAN ID 0x{CAN_ATTACK_ID:X}: Son {TIME_WINDOW_SEC} saniyede {current_count} adet mesaj alındı.")
            logger.critical(f"Eşik ({THRESHOLD_COUNT}) aşıldı. Koordine Talep Saldırısı veya CAN Enjeksiyonu ŞÜPHESİ.")
            anomaly_detected_flag = True # Tekrar tekrar loglamayı durdur
            
        elif current_count <= THRESHOLD_COUNT and anomaly_detected_flag:
            # Anomali durumu sona erdi
            logger.warning("Anormal trafik yoğunluğu normale döndü.")
            anomaly_detected_flag = False
            
        else:
            # Normal akış veya anomali zaten tespit edildi
            logger.info(f"Trafik: 0x{CAN_ATTACK_ID:X} sayım: {current_count}")


def run_can_ids():
    """
    CAN bus'ı sürekli dinleyen ana fonksiyon.
    """
    logger.info(f"CAN-IDS başlatılıyor. Takip ID: 0x{CAN_ATTACK_ID:X}, Eşik: {THRESHOLD_COUNT} adet / {TIME_WINDOW_SEC} sn.")
    
    try:
        # Sanal CAN (vcano) arayüzüne bağlan
        bus = can.interface.Bus(channel=BUS_CHANNEL, bustype='virtual')
        
        # CAN bus'tan mesajları sürekli oku
        while True:
            # Mesaj beklerken CPU'yu aşırı yormamak için timeout kullanılır
            message = bus.recv(timeout=0.1) 
            if message:
                analyze_can_message(message)
                
    except can.exceptions.VirtualBusError:
        logger.error(f"CAN Bus '{BUS_CHANNEL}' bulunamadı. Lütfen kurulum adımlarını kontrol edin.")
    except Exception as e:
        logger.error(f"CAN-IDS çalışma hatası: {e}")
    finally:
        if 'bus' in locals():
            bus.shutdown()

if __name__ == "__main__":
    # IDS'i arka planda çalıştırmak için Threading kullanılır.
    ids_thread = threading.Thread(target=run_can_ids, daemon=True)
    ids_thread.start()
    
    print("CAN-IDS arka planda çalışıyor. Saldırıyı başlatmak için diğer betiği çalıştırın.")
    print("Logları 'logs/evcs_system_detailed.log' dosyasından takip edebilirsiniz.")

    # Main thread'in sonlanmaması için bekleme
    try:
        while ids_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("CAN-IDS manuel olarak durduruldu.")
        print("\nCAN-IDS durduruldu.")
        pass