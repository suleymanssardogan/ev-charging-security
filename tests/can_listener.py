import time
import cp  # cp.py dosyasını import ediyoruz

def simulate_card_swipe():
    print("--- [DONANIM] CAN Bus Dinleniyor ---")
    print("[DONANIM] RFID Okuyucu aktif...")
    time.sleep(1)
    
    # Simüle edilmiş bir kart okuma eylemi
    detected_card_id = "USER_REAL_CARD_123"
    print(f"[DONANIM] Kart Algılandı! ID: {detected_card_id}")
    
    # [cite: 14] Şarj istasyonu ile merkezi sistem arasında veri iletimini tetikler.
    print("[DONANIM] CP modülü tetikleniyor...")
    cp.trigger_charge(detected_card_id)

if __name__ == "__main__":
    simulate_card_swipe()