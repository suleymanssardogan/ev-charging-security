import asyncio
import websockets
import json

#  TLS kullanılmadığı için ws:// protokolü kullanılıyor (wss:// değil).
# Normalde CSMS 9000'de ama biz 9001'e (MITM'e) bağlanıyoruz veya ağ trafiğimiz oradan geçiyor.
CSMS_URI = "ws://localhost:9001" 
STATION_ID = "CP_001"

async def start_charging_session(id_tag):
    async with websockets.connect(f"{CSMS_URI}/{STATION_ID}") as websocket:
        print(f"[CP] Sunucuya bağlanıldı. Kart ID: {id_tag}")

        # 1. BootNotification (Açılış)
        boot_msg = [2, "msg_1", "BootNotification", {
            "chargePointVendor": "VendorX",
            "chargePointModel": "ModelY"
        }]
        await websocket.send(json.dumps(boot_msg))
        response = await websocket.recv()
        print(f"[CP] Boot Cevabı: {response}")

        # 2. StartTransaction (Şarj Başlatma)
        # [cite: 15] Kullanıcı kimlik bilgileri (idTag) iletiliyor.
        start_msg = [2, "msg_2", "StartTransaction", {
            "connectorId": 1,
            "idTag": id_tag,
            "meterStart": 0,
            "timestamp": "2023-10-27T10:00:00Z"
        }]
        print(f"[CP] Şarj başlatma isteği gönderiliyor... (ID: {id_tag})")
        await websocket.send(json.dumps(start_msg))
        
        # Cevabı bekle
        response = await websocket.recv()
        print(f"[CP] İşlem Cevabı Alındı: {response}")

# Bu fonksiyon dışarıdan (can_listener tarafından) tetiklenebilir
def trigger_charge(card_id):
    asyncio.run(start_charging_session(card_id))

if __name__ == "__main__":
    # Test için manuel çalıştırma
    trigger_charge("USER_REAL_CARD_123")