#!/usr/bin/env python3
# can_listener.py (Değişiklik Gerekmiyor - TAM KOD)
import can
import logging

logging.basicConfig(level=logging.INFO)


def listen_can():
    try:
        bus = can.interface.Bus(channel='vcan0', interface='socketcan') # 'interface' kullan
        logging.info("[CAN Listener] vcan0 üzerinde dinleme başladı...")

        for msg in bus:
            logging.warning(f"[CAN <<<] ID: 0x{msg.arbitration_id:X} | DLC: {msg.dlc} | Data: {msg.data.hex()}")

    except Exception as e:
        logging.error(f"[CAN Listener] !!! HATA: {e}")
        logging.error(
            "[CAN Listener] !!! vcan0 arayüzünün 'sudo ip link set up vcan0' ile aktif olduğundan emin misin?")


if __name__ == "__main__":
    listen_can()