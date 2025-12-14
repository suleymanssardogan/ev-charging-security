import time
import can
from can_bus_factory import get_can_bus
from can_ids_rules import ALLOWED_CAN_IDS
from event_logger import log_event

START_CHARGE_ID = 0x200



def main():
    bus = get_can_bus()

    print("[ECU] Legitimate ECU started")

    msg = can.Message(
        arbitration_id=START_CHARGE_ID,
        data=[0x01],
        is_extended_id=False
    )

    bus.send(msg)
    log_event(
    layer="CAN",
    source="ECU",
    event_type="START_CHARGE",
    can_id=START_CHARGE_ID,
    data="01",
    label="normal"
    )

    print(f"[ECU] Sent CAN ID {hex(START_CHARGE_ID)}")

    time.sleep(1)

if __name__ == "__main__":
    main()
