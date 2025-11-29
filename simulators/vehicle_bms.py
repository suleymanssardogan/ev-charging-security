import can
import time
import random

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
print("--- ARAC (BMS) BASLATILDI ---")
print("Batarya durumu (SoC) yayinlaniyor...")

try:
    while True:
        # Senaryo: Batarya %10 ile %100 arasi rastgele bir degerde
        soc = random.randint(10, 100)
        
        # ID 0x100: Batarya Bilgisi
        # SWOT Analizi: "Sifreleme eksikligi" - Veri acik (plaintext) gidiyor.
        msg = can.Message(arbitration_id=0x100, 
                          data=[soc, 0, 0, 0, 0, 0, 0, 0], 
                          is_extended_id=False)
        bus.send(msg)
        print(f"Giden Veri (BMS) -> Batarya: %{soc}")
        time.sleep(2) # 2 saniyede bir gönder

except KeyboardInterrupt:
    print("Arac durduruldu.")
