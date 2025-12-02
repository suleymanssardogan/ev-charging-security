#!/usr/bin/env python3
import sys
import time
import logging

try:
    import can
except ImportError:
    print("[HATA] python-can kutuphanesi eksik.")
    print("Lutfen 'pip3 install python-can' komutunu calistirin.")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [IDS] - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

class SwotBasedIDS:
    def __init__(self, interface='vcan0'):
        self.interface = interface
        self.bus = None
        self.transaction_started = False

    def check_interface_exists(self):
        try:
            can.interface.Bus(channel=self.interface, interface='socketcan')
            return True
        except:
            return False

    def start_monitoring(self):
        if not self.check_interface_exists():
            logging.error(f"'{self.interface}' arayuzu bulunamadi.")
            print("-" * 30)
            print("Lutfen terminale su komutlari girin:")
            print("1. sudo modprobe vcan")
            print(f"2. sudo ip link add dev {self.interface} type vcan")
            print(f"3. sudo ip link set up {self.interface}")
            print("-" * 30)
            sys.exit(1)

        try:
            self.bus = can.interface.Bus(channel=self.interface, interface='socketcan')
            print(f"\nIDS MONITORING BASLATILDI: {self.interface}\n")

            for msg in self.bus:
                can_id = msg.arbitration_id
                
                if can_id == 0x200:
                    logging.info("NORMAL DURUM: Sarj Baslatma Sinyali (0x200) algilandi.")
                    self.transaction_started = True

                elif can_id == 0x201:
                    print("\n" + "!"*50)
                    logging.critical("ALARM: SINYAL ENJEKSIYONU TESPIT EDILDI (0x201)")
                    logging.critical("ANALIZ: MITM kaynakli DoS saldirisi gerceklesti.")
                    
                    if not self.transaction_started:
                         logging.warning("DETAY: Sarj hic baslamadan durdurma komutu enjekte edildi.")
                    
                    logging.info("AKSIYON: Sistem guvenli moda aliniyor.")
                    print("!"*50 + "\n")

        except KeyboardInterrupt:
            print("\nIDS kapatiliyor.")
        except Exception as e:
            logging.error(f"Beklenmedik hata: {e}")

if __name__ == "__main__":
    ids = SwotBasedIDS()
    ids.start_monitoring()