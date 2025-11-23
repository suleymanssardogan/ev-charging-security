import can
import logging

logging.basicConfig(level=logging.INFO)

try:
    # vcan0 arayüzüne bağlan
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    print("vcan0 dinleniyor... (Mesaj bekleniyor)")

    while True:
        # Mesajı bekle ve al
        message = bus.recv()
        if message is not None:
            # Gelen mesajın ID'sini ve verisini ekrana bas
            print(f"Mesaj Alındı: ID={hex(message.arbitration_id)} | Data={list(message.data)}")

except KeyboardInterrupt:
    print("\nDinleyici durduruldu.")
except Exception as e:
    logging.error(f"Hata oluştu (vcan0 kurulu mu?): {e}")