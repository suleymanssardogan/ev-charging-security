import can

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

print("!!! SALDIRGAN BAGLANDI - DINLEME BASLADI (SNIFFING) !!!")
print("SWOT Analizi: 'Sifreleme eksikligi tespiti kolay' maddesi test ediliyor...")

def decode_msg(msg):
    if msg.arbitration_id == 0x100:
        soc = msg.data[0]
        print(f"[YAKALANDI] ID: 0x100 -> Arac Bataryasi: %{soc} (Sifresiz Veri!)")
        
    elif msg.arbitration_id == 0x200:
        voltage = (msg.data[0] << 8) | msg.data[1]
        print(f"[YAKALANDI] ID: 0x200 -> Sarj Voltaji: {voltage}V (Sifresiz Veri!)")

try:
    for msg in bus:
        decode_msg(msg)
except KeyboardInterrupt:
    print("Dinleme bitti.")
