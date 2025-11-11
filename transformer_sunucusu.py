import threading
import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

# --- 1. FİZİKSEL MODEL (Gerçek Dünya) ---
gercek_fiziksel_yuk = 50.0 # Yük %50'den başlar
FX_CODE_HOLDING_REGISTER = 3 # Modbus fonksiyon kodu (Holding Register için 3)

def fiziksel_modeli_guncelle(context):
    global gercek_fiziksel_yuk
    while True:
        time.sleep(5)
        gercek_fiziksel_yuk += 1.0 # Yük yavaş yavaş artar
        
        yuk_int = int(gercek_fiziksel_yuk)
        
        # --- DÜZELTİLMİŞ KISIM ---
        
        # Kaynak 2 (Güvenli Register 200): "Fiziksel/İmzalı" veriyi yazar.
        # DÜZELTME: setValues(fx, address, values) -> setValues(3, 200, [yuk_int])
        context[0].setValues(FX_CODE_HOLDING_REGISTER, 200, [yuk_int])
        
        # Kaynak 1 (Güvensiz Register 100): Saldırganın hedefi budur.
        
        # DÜZELTME: getValues(fx, address, count) -> getValues(3, 100, 1)
        mevcut_guvensiz_deger = context[0].getValues(FX_CODE_HOLDING_REGISTER, 100, 1)[0]
        
        if mevcut_guvensiz_deger == 0: # Sadece başlangıçta ayarla
             # DÜZELTME: setValues(fx, address, values) -> setValues(3, 100, [yuk_int])
             context[0].setValues(FX_CODE_HOLDING_REGISTER, 100, [yuk_int])
        
        print(f"[TRAFO FİZİKSEL MODELİ] Gerçek Yük: {gercek_fiziksel_yuk:.1f}%")
        if gercek_fiziksel_yuk > 90.0:
            print("[TRAFO FİZİKSEL MODELİ] !!! FELAKET !!! TRAFO AŞIRI YÜKLENDİ VE YANDI!")

# --- 2. SİBER MODEL (Modbus Sunucusu) ---
def siber_modeli_baslat():
    # 'hr' (holding registers) kullandığımız için fx=3'ü kullandık
    store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0]*256))
    context = ModbusServerContext(slaves=store, single=True)
    
    t = threading.Thread(target=fiziksel_modeli_guncelle, args=(context,), daemon=True)
    t.start()
    
    print("[TRAFO SİBER MODELİ] Modbus TCP Sunucusu Port 502'de başlatılıyor...")
    StartTcpServer(context=context, address=("localhost", 502))

if __name__ == "__main__":
    siber_modeli_baslat()
