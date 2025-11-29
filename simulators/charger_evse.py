import can
import time
import random

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
print("--- SARJ ISTASYONU (EVSE) BASLATILDI ---")

try:
    while True:
        # Voltaj 380V-400V arasi degisiyor
        voltage = random.randint(380, 400)
        current = 32 # Amper sabit
        
        # Voltaj 2 byte kaplar (High Byte, Low Byte)
        # 400 sayisi hex olarak 0x0190 eder.
        # Data[0] = 01, Data[1] = 90 olarak gider.
        
        data = [(voltage >> 8) & 0xFF, voltage & 0xFF, current, 0, 0, 0, 0, 0]
        
        msg = can.Message(arbitration_id=0x200, 
                          data=data, 
                          is_extended_id=False)
        bus.send(msg)
        print(f"Giden Veri (EVSE) -> Voltaj: {voltage}V, Akim: {current}A")
        time.sleep(1)

except KeyboardInterrupt:
    print("Sarj istasyonu durduruldu.")
