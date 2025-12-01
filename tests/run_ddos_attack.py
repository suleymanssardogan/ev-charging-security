import asyncio
import subprocess
import logging
import time
import os
import signal
from datetime import datetime

# --- YAPILANDIRMA PARAMETRELERİ ---
# Kaç adet CP'yi aynı anda başlatacağımız (Saldırı Boyutu)
NUM_CHARGE_POINTS = 100 
CSMS_URL = "localhost:9000"
CAN_CHANNEL = "vcan0"
CP_SIMULATOR_PATH = "../simulators/cp_sim_template.py"
LOG_FILE = "logs/ddos_attack_log.txt"

# Tek bir CP'nin tahmini gücü (kW)
CP_POWER_KW = 22 
# ----------------------------------

# Logger ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, mode='w')
    ]
)

# Global CP süreçlerini tutacak liste
cp_processes = []

def setup_vcano():
    """Sanal CAN arayüzünü (vcan0) kurar."""
    logging.info("Sanal CAN (vcan0) arayüzü kuruluyor...")
    try:
        # vcan modülünün yüklenmesi
        subprocess.run(["sudo", "modprobe", "vcan"], check=True, capture_output=True)
        # vcan0 arayüzünün oluşturulması (zaten varsa hata verebilir, bu normal)
        subprocess.run(["sudo", "ip", "link", "add", "dev", CAN_CHANNEL, "type", "vcan"], check=False, capture_output=True)
        # vcan0 arayüzünün etkinleştirilmesi
        subprocess.run(["sudo", "ip", "link", "set", CAN_CHANNEL, "up"], check=True, capture_output=True)
        logging.info(f"{CAN_CHANNEL} başarıyla kuruldu.")
    except subprocess.CalledProcessError as e:
        logging.error(f"vcan0 kurulum hatası: {e.stderr.decode()}")
        logging.warning("Saldırı CAN enjeksiyonları olmadan simüle edilebilir (OCPP/Yük hesaplama devam eder).")
        # Gerçek bir hata durumunda bile script'in devam etmesine izin verilir

async def run_charge_point(cp_index):
    """Her bir CP simülatörünü ayrı bir süreçte başlatır."""
    cp_id = f"CP_DDoS_{cp_index:03d}"
    logging.info(f"CP {cp_id} başlatılıyor...")
    
    # cp_sim_template.py scriptini subprocess olarak başlatma
    process = subprocess.Popen(
        ["python3", CP_SIMULATOR_PATH, cp_id, CSMS_URL, CAN_CHANNEL],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    cp_processes.append(process)
    
    # Process çıktısını loglama (Opsiyonel, çok sayıda log üretecektir)
    # try:
    #     for line in iter(process.stdout.readline, ''):
    #         logging.debug(f"[CP:{cp_id}] {line.strip()}")
    # except Exception:
    #     pass
    
    return process

async def coordinate_ddos_attack():
    """Tüm CP'lerin aynı anda RemoteStartTransaction'ı tetiklemesini sağlar."""
    
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.critical("--- SALDIRI KORDİNASYON AŞAMASI BAŞLIYOR ---")
    logging.critical(f"Hedef CP Sayısı: {NUM_CHARGE_POINTS}")
    logging.critical(f"Tahmini Anlık Yük Artışı: {NUM_CHARGE_POINTS * CP_POWER_KW} kW")
    logging.critical(f"Saldırı Başlangıç Zamanı: {start_time}")
    
    # **Koordinasyon Stratejisi:**
    # 
    # 1. Tüm CP'leri başlat (Burada CP'ler CSMS'e bağlanıp BootNotification gönderir).
    cp_tasks = [run_charge_point(i) for i in range(1, NUM_CHARGE_POINTS + 1)]
    await asyncio.gather(*cp_tasks)
    
    # CP'lerin bağlanması ve BootNotification göndermesi için kısa bir bekleme süresi
    logging.info("Tüm CP'lerin bağlanması için 5 saniye bekleniyor...")
    await asyncio.sleep(5) 
    
    # 2. Saldırıyı Tetikle
    # Not: Eğer CSMS simülatöründe harici bir API olsaydı, onu kullanırdık.
    # Ancak mevcut yapı, CP'nin kendisinin RemoteStartTransaction komutunu almasını
    # taklit etmeli. En basit yol, CP'leri başlattıktan hemen sonra 
    # CSMS'in komutu gönderdiğini varsaymaktır.
    
    # Saldırı başladığı anda tüm CP'ler, CSMS'ten komutu aldıklarını simüle edecek.
    # Bu simülasyon, "cp_sim_template.py" içindeki handle_call metodunda
    # RemoteStartTransaction'ın işlenmesiyle gerçekleşir.
    
    logging.critical(f"ZAMAN T: {datetime.now().strftime('%H:%M:%S.%f')} -> Koordineli RemoteStartTransaction komutları CSMS'ten gönderildi.")
    
    # Burada ek bir bekleme, tüm CP'lerin komutu işleyip CAN frame'ini enjekte etmesi için
    await asyncio.sleep(3) 
    
    logging.critical("Saldırı simülasyonu tamamlandı. CAN-bus üzerindeki (vcan0) anomaliyi izleyin.")

def cleanup():
    """Tüm başlatılan CP süreçlerini sonlandırır ve vcan0 arayüzünü kapatır."""
    logging.info("Temizlik başlatılıyor...")
    for process in cp_processes:
        if process.poll() is None:
            # Süreç hala çalışıyorsa sonlandır
            process.terminate()
            
    # vcan0 arayüzünü kapat
    try:
        subprocess.run(["sudo", "ip", "link", "set", CAN_CHANNEL, "down"], check=True, capture_output=True)
        subprocess.run(["sudo", "ip", "link", "del", "dev", CAN_CHANNEL], check=True, capture_output=True)
        logging.info(f"{CAN_CHANNEL} arayüzü kapatıldı.")
    except Exception as e:
        logging.error(f"vcan0 kapatılamadı: {e}")
        
    logging.info("Temizlik tamamlandı.")


async def main():
    """Ana program akışı."""
    setup_vcano()
    
    # CSMS'in zaten ayrı bir terminalde çalıştırıldığını varsayın
    # Eğer CSMS bu script içinde çalıştırılacaksa, ona göre bir subprocess eklenmelidir.
    logging.info(f"Lütfen '{os.path.abspath(os.path.join(os.path.dirname(__file__), '../simulators/csms_sim.py'))}' dosyasını başka bir terminalde başlatın.")
    input("CSMS başlatıldıktan sonra devam etmek için ENTER tuşuna basın...")
    
    try:
        await coordinate_ddos_attack()
    except Exception as e:
        logging.error(f"Saldırı sırasında genel hata: {e}")
    finally:
        # Kullanıcının sonuçları incelemesi için bekleme
        input("Saldırı logları ve CAN trafiği inceleniyor... Bitirmek için ENTER tuşuna basın.")
        cleanup()

if __name__ == "__main__":
    # Ctrl+C ile kesmeyi yönetme
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.warning("Saldırı simülasyonu kullanıcı tarafından kesildi (Ctrl+C).")
        cleanup()
