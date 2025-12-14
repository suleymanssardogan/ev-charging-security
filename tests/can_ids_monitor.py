"""
CAN Bus IDS - ID Spoofing Detection

Bu script, CAN Bus üzerindeki mesajları izleyerek
aynı CAN ID'nin anormal sıklıkta gönderilip gönderilmediğini kontrol eder.

SWOT Referansı:
- Opportunity: IDS / Secure Gateway altyapısı
- Weakness: CAN Bus'ta kimlik doğrulama yok
"""

import time
import can
from collections import defaultdict
from can_bus_factory import get_can_bus

# IDS parametreleri
TIME_WINDOW = 2.0      # saniye
MAX_MESSAGES = 1       # bu süre içinde izin verilen mesaj sayısı

# CAN ID -> zaman listesi
message_log = defaultdict(list)

def main():
    bus = get_can_bus()
    print("[IDS] CAN IDS started")
    print("[IDS] Monitoring CAN traffic...")

    while True:
        msg = bus.recv(timeout=1)

        # macOS MOCK modunda mesaj gelmez
        if msg is None:
            continue

        now = time.time()
        can_id = msg.arbitration_id

        # Eski zamanları temizle
        message_log[can_id] = [
            t for t in message_log[can_id]
            if now - t <= TIME_WINDOW
        ]

        message_log[can_id].append(now)

        print(f"[IDS] Received ID={hex(can_id)} DATA={msg.data}")

        # Anomali kontrolü
        if len(message_log[can_id]) > MAX_MESSAGES:
            print("🚨 [IDS ALERT] POSSIBLE CAN ID SPOOFING DETECTED!")
            print(f"🚨 ID {hex(can_id)} sent {len(message_log[can_id])} times in {TIME_WINDOW}s")

if __name__ == "__main__":
    main()
