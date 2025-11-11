import asyncio
import websockets
import logging
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result
import json
import time

# Loglama ayarları
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - CSMS - %(levelname)s - %(message)s',
                    filename='logs/evcs_system_detailed.log',
                    filemode='a') # Mevcut log dosyasına ekleme yap
logger = logging.getLogger('CSMS')

# Bağlı CP'leri takip etmek için bir set
connected_cps = set()

async def csms_handler(websocket, path):
    """
    CP'lerden gelen bağlantıları yöneten ve mesajları işleyen ana fonksiyon.
    """
    # path genellikle CP'nin kimliğini içerir (örneğin: /CP_1)
    cp_id = path.strip('/')
    connected_cps.add(websocket)
    logger.info(f"Yeni CP bağlandı: {cp_id}")

    try:
        async for message in websocket:
            # Gelen OCPP mesajını parse et
            incoming_message = json.loads(message)
            message_type_id = incoming_message[0]
            
            # Sadece Çağrı (Call) mesajlarını (tip 2) işle
            if message_type_id == 2:
                unique_id = incoming_message[1]
                action = incoming_message[2]
                payload = incoming_message[3]

                logger.info(f"CP {cp_id} -> CSMS: Action={action}, Payload={json.dumps(payload)}")

                response = None
                
                # BootNotification cevabı gönder
                if action == Action.BootNotification:
                    response = call_result.BootNotification(
                        current_time=datetime.now().isoformat(),
                        interval=300, # 5 dakika aralıklarla heartbeat
                        status=RegistrationStatus.accepted
                    )
                # MeterValues cevabı gönder (Saldırı sonrası yoğunlaşır)
                elif action == Action.MeterValues:
                    response = call_result.MeterValues()
                    
                # Diğer tüm çağrılara varsayılan cevap
                else:
                    # Diğer çağrı tipleri (Heartbeat vb.)
                    response = call_result.Heartbeat() 

                if response:
                    # Cevabı JSON formatına dönüştür
                    response_message = [3, unique_id, response.action, response.to_json()]
                    await websocket.send(json.dumps(response_message))
                    logger.info(f"CSMS -> CP {cp_id}: Cevap gönderildi: {response.action}")
            
    except websockets.exceptions.ConnectionClosedOK:
        logger.warning(f"CP {cp_id} bağlantıyı normal şekilde kapattı.")
    except Exception as e:
        logger.error(f"CP {cp_id} ile iletişim hatası: {e}")
    finally:
        connected_cps.remove(websocket)
        logger.info(f"CP {cp_id} bağlantısı kesildi.")

async def start_csms_server(host, port):
    """
    CSMS sunucusunu başlatır.
    """
    logger.info(f"CSMS sunucusu başlatılıyor: ws://{host}:{port}")
    # OCPP alt protokolünü belirtmek önemlidir
    async with websockets.serve(csms_handler, host, port, subprotocols=['ocpp1.6']):
        await asyncio.Future() # Sunucunun sürekli çalışmasını sağlar

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 9000
    try:
        from datetime import datetime
        asyncio.run(start_csms_server(HOST, PORT))
    except KeyboardInterrupt:
        logger.warning("CSMS sunucusu manuel olarak durduruldu.")