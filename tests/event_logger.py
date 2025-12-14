import csv
import time
from pathlib import Path

# Ortak log dosyası
LOG_FILE = Path("datasets/can_events.csv")

# CSV header (ilk çalışmada yazılır)
CSV_HEADER = [
    "timestamp",
    "layer",
    "source",
    "event_type",
    "can_id",
    "data",
    "label"
]

def log_event(layer, source, event_type, can_id, data, label):
    """
    Ortak log fonksiyonu (TÜM ekip için standart)

    layer      : CAN / OCPP / API / CLOUD
    source     : ECU / ATTACKER / SERVER
    event_type : START_CHARGE / STOP_CHARGE / AUTH
    can_id     : 0x200 gibi
    data       : payload
    label      : normal / anomaly
    """

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(CSV_HEADER)

        writer.writerow([
            int(time.time()),
            layer,
            source,
            event_type,
            hex(can_id) if isinstance(can_id, int) else can_id,
            data,
            label
        ])
