#!/usr/bin/env python3
# cp.py - FINAL SÜRÜM (GitHub Ready)
import asyncio
import can
import websockets
import os
import logging

from ocpp.v16 import ChargePoint as BaseChargePoint
from ocpp.routing import on
from ocpp.v16 import call, call_result
from ocpp.v16.enums import ConfigurationStatus

# Loglama ayarı
logging.basicConfig(level=logging.INFO)

# CAN bus (vcan0) bağlantısını kurmayı dene
try:
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')
    logging.info("[CP] vcan0 bağlantısı başarılı.")
except Exception as e:
    logging.error(f"[CP] vcan0 hatası: {e}")
    # Sanal CAN yoksa bile simülasyonun çökmemesi için devam ediyoruz

class MyChargePoint(BaseChargePoint):

    async def send_can_message(self, can_id, data):
        """Sanal CAN hattına mesaj gönderen yardımcı fonksiyon"""
        try:
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            bus.send(msg)
            logging.warning(f"[CP->CAN] Donanıma İletildi >> ID: 0x{can_id:X} | Data: {data.hex()}")
        except Exception as e:
            logging.error(f"[CP->CAN] Hata: {e}")

    @on('ChangeConfiguration')
    async def on_change_config(self, key, value, **kwargs):
        """CSMS'den gelen konfigürasyon değiştirme komutunu işler"""
        logging.info(f"[CP] <<< KOMUT ALINDI: ChangeConfiguration Key={key}, Value={value}")

        if key == "MaxOutputCurrent":
            try:
                amper_degeri = int(value)
                
                # --- FİZİKSEL RİSK SİMÜLASYONU ---
                # Güvenli sınır (örn: 32A) aşıldı mı?
                if amper_degeri > 32:
                    logging.error(f"\n[!!! ALARM !!!] KRİTİK GÜVENLİK RİSKİ: {amper_degeri}A İSTENDİ!")
                    logging.error("[!!! ALARM !!!] BU DEĞER KABLOLARI ERİTEBİLİR VE YANGIN ÇIKARABİLİR.\n")
                
                # Değeri donanıma (CAN Bus - ID:0x500) iletiyoruz
                # 500 sayısı tek byte'a sığmaz, 2 byte (big endian) gönderiyoruz.
                await self.send_can_message(0x500, amper_degeri.to_bytes(2, 'big'))
                
                # İşlem başarılı cevabı dön (DÜZELTİLDİ: Payload kelimesi kaldırıldı)
                return call_result.ChangeConfiguration(status=ConfigurationStatus.accepted)
            
            except ValueError:
                return call_result.ChangeConfiguration(status=ConfigurationStatus.rejected)

        return call_result.ChangeConfiguration(status=ConfigurationStatus.not_supported)


async def run_cp(ws_uri):
    # Proxy ayarını kontrol et (MITM saldırısı için gerekli)
    proxy = os.environ.get('http_proxy')
    if proxy:
        logging.warning(f"[CP] Proxy devrede: {proxy}")

    async with websockets.connect(ws_uri) as ws:
        # Timeout süresini biraz artırdık (60 sn) ki ağ yavaşsa kopmasın
        cp = MyChargePoint('CP_001', ws, response_timeout=60)
        
        # ÖNEMLİ: Dinleme işlemini (start) arka plana atıyoruz (Concurrency)
        # Böylece aşağıdaki 'call' komutu cevap beklerken kod kilitlenmez.
        listener_task = asyncio.create_task(cp.start())
        
        # Sunucuya (CSMS) BootNotification gönder
        await cp.call(call.BootNotification(
            charge_point_model="KaliSim-PhysicalRisk", 
            charge_point_vendor="Lab"
        ))
        
        logging.info("[CP] BootNotification Başarılı! Komut bekleniyor...")
        
        # Sonsuza kadar dinlemeye devam et
        await listener_task

if __name__ == '__main__':
    # MITM portu üzerinden sunucuya bağlan
    uri = "ws://localhost:9000/CP_001"
    try:
        asyncio.run(run_cp(uri))
    except KeyboardInterrupt:
        logging.info("Çıkış yapıldı.")
