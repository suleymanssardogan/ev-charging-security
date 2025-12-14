#!/usr/bin/env python3
# can_listener.py - CAN Hattı Dinleyicisi
import can
import logging

logging.basicConfig(level=logging.INFO)

def listen_can():
    try:
        bus = can.interface.Bus(channel='vcan0', interface='socketcan')
        logging.info("[CAN Listener] vcan0 dinleniyor...")
        for msg in bus:
            # Gelen veriyi okunaklı hexadecimal formatta yazdır
            data_hex = msg.data.hex().upper()
            logging.warning(f"[CAN <<<] ID: 0x{msg.arbitration_id:X} | DLC: {msg.dlc} | Data: {data_hex}")
            
            # Eğer veri 01F4 (500 decimal) ise uyar
            if "01F4" in data_hex:
                 logging.error(f"!!! [CAN Listener] TEHLİKELİ AKIM DEĞERİ TESPİT EDİLDİ: 500A (Hex: {data_hex}) !!!")

    except Exception as e:
        logging.error(f"[CAN Listener] Hata: {e}")

if __name__ == "__main__":
    listen_can()
