import time
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('localhost', port=502)
if not client.connect():
    print("[HATA] Trafo Sunucusuna (localhost:502) bağlanılamadı.")
    print("Lütfen Terminal 1'de 'transformer_sunucusu.py' script'ini çalıştırdığınızdan emin olun.")
    exit()
    
print("[GÜVENLİK IDS - SCADA] Trafo Sunucusuna (localhost:502) bağlandı.")
print("Veri tutarlılığı kontrol ediliyor... (Log kaydı başlatıldı)")

try:
    while True:
        # 1. GÜVENSİZ (SALDIRILABİLİR) VERİYİ OKU (Register 100)
        # DÜZELTME: (100, 1) yerine (100, count=1)
        result_guvensiz = client.read_holding_registers(100, count=1)
        if not result_guvensiz.isError():
            dijital_veri = result_guvensiz.registers[0]
        else:
            print("[IDS] Register 100 okunamadı!")
            continue

        # 2. GÜVENLİ (FİZİKSEL) VERİYİ OKU (Register 200)
        # DÜZELTME: (200, 1) yerine (200, count=1)
        result_guvenli = client.read_holding_registers(200, count=1)
        if not result_guvenli.isError():
            fiziksel_veri = result_guvenli.registers[0]
        else:
            print("[IDS] Register 200 okunamadı!")
            continue

        print(f"\n--- SCADA KONTROL PANELI --- ({time.strftime('%Y-%m-%d %H:%M:%S')})")
        print(f"Raporlanan Dijital Veri (Reg 100): {dijital_veri}%")
        print(f"Doğrulanan Fiziksel Veri (Reg 200): {fiziksel_veri}%")

        # 3. GÜVENLİK ÖNLEMİ (ÇAPRAZ DOĞRULAMA)
        fark = abs(dijital_veri - fiziksel_veri)
        if fark > 5: # Fark %5'ten fazlaysa
            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"[FDI SALDIRISI TESPİT EDİLDİ!] - TUTARSIZLIK ALARMI!")
            print(f"Fark: {fark}%. Operatör uyarılıyor, dijital veriye güvenme!")
            print("GÜVENLİK ÖNLEMİ: Sistem fiziksel veriye (Güvenli Mod) geçiriliyor.")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            print(f"Durum: NORMAL (Fark: {fark}%)")
            
        time.sleep(2) # Her 2 saniyede bir kontrol et
except KeyboardInterrupt:
    client.close()
    print("\n[GÜVENLİK IDS - SCADA] Bağlantı kapatıldı. Log kaydı durduruldu.")
