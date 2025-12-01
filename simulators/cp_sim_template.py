import asyncio
import websockets
import json
import logging

from ocpp.v16 import call
from ocpp.v16 import ChargePoint   # <-- Doğru import
from ocpp.v16.enums import RegistrationStatus, Action

import can

logging.basicConfig(level=logging.INFO)


# CP Agent sınıfı (OCPP + CAN)
class ChargePointSimulator(ChargePoint):   # <-- Doğru sınıf adı
    def __init__(self, charge_point_id, ws, vcano_channel="vcan0"):
        super().__init__(charge_point_id, ws)
        self.cp_id = charge_point_id

        # CAN-bus bağlantısı (vcan0)
        self.can_bus = can.Bus(channel=vcano_channel, bustype='socketcan')

    async def send_boot_notification(self):
        """CSMS'e BootNotification gönder."""
        request = call.BootNotification(
            charge_point_model="SmartEVCS",
            charge_point_vendor="SimuTech"
        )
        response = await self.call(request)
        logging.info(f"[{self.cp_id}] Boot Notification yanıtı: {response.status}")
        return response.status == RegistrationStatus.accepted

    async def handle_call(self, msg):
        """CSMS'ten gelen OCPP komutlarını işler."""
        call_id, action, payload = msg

        # RemoteStartTransaction tespit edildi
        if action == Action.RemoteStartTransaction:
            logging.warning(f"[{self.cp_id}] SALDIRI: RemoteStartTransaction alındı.")

            # 1- OCPP yanıtı gönder
            response = call.RemoteStartTransactionPayload(status='Accepted')
            await self.send_call_result(call_id, response)

            # 2- CAN saldırı komutunu gönder
            await self.send_can_start_command()

        else:
            await super().handle_call(msg)

    async def send_can_start_command(self):
        """OCPP -> CAN enjeksiyon saldırısı."""
        can_id = 0x200
        payload = bytes([int(self.cp_id[-2:]), 1, 1])

        message = can.Message(
            arbitration_id=can_id,
            data=payload,
            is_extended_id=False
        )

        self.can_bus.send(message)
        logging.critical(
            f"[{self.cp_id}] CAN ENJEKSİYONU GÖNDERİLDİ → ID: 0x{can_id:X}, Data: {payload}"
        )


async def start_cp(cp_id, csms_url, vcano_channel="vcan0"):
    uri = f"ws://{csms_url}/{cp_id}"

    try:
        async with websockets.connect(uri, subprotocols=['ocpp1.6']) as ws:
            cp_sim = ChargePointSimulator(cp_id, ws, vcano_channel)

            if await cp_sim.send_boot_notification():
                await cp_sim.start()

    except Exception as e:
        logging.error(f"[{cp_id}] Bağlantı hatası: {e}")


if __name__ == '__main__':
    CSMS_URL = "localhost:9000"
    CP_ID = "CPT_001"
    CAN_CHANNEL = "vcan0"

    asyncio.run(start_cp(CP_ID, CSMS_URL, CAN_CHANNEL))

