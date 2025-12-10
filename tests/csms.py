import asyncio
import websockets
import json

# [cite: 2] CSMS, istasyonlar ile merkezi sistem arasındaki iletişimi yönetir.
async def on_connect(websocket, path):
    print(f"[CSMS] Yeni bir istasyon bağlandı: {path}")
    try:
        async for message in websocket:
            data = json.loads(message)
            # OCPP Mesaj Yapısı: [MessageType, UniqueId, Action, Payload]
            msg_type = data[0]
            unique_id = data[1]
            action = data[2]
            payload = data[3]

            print(f"[CSMS] Gelen Mesaj ({action}): {payload}")

            if action == "BootNotification":
                # İstasyon açılış onayı
                response = [3, unique_id, {"status": "Accepted", "interval": 300}]
                await websocket.send(json.dumps(response))
            
            elif action == "StartTransaction":
                #  Oturum tokenlarının kontrol edildiği kritik nokta.
                id_tag = payload.get("idTag")
                print(f"[CSMS] !!! DİKKAT !!! İşlem Başlatan Kart ID: {id_tag}")
                
                # Eğer saldırgan ID'yi değiştirdiyse burada HACKER_TOKEN göreceğiz.
                response = [3, unique_id, {"transactionId": 12345, "idTagInfo": {"status": "Accepted"}}]
                await websocket.send(json.dumps(response))

    except websockets.exceptions.ConnectionClosed:
        print("[CSMS] Bağlantı koptu.")

async def main():
    # CSMS 9000 portunda dinliyor
    print("[CSMS] Sunucu başlatıldı (ws://localhost:9000)...")
    async with websockets.serve(on_connect, "localhost", 9000):
        await asyncio.Future()  # Sonsuz döngü

if __name__ == "__main__":
    asyncio.run(main())