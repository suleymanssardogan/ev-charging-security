import pandas as pd
import re
from datetime import datetime
import logging
import csv

# Loglama ayarları (Analiz loglarını ayrı tutalım)
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - ANALYZER - %(levelname)s - %(message)s',
                    filename='logs/analyzer_results.log',
                    filemode='w')
logger = logging.getLogger('ANALYZER')

# Dosya Yolları
LOG_FILE = 'logs/evcs_system_detailed.log'
OUTPUT_CSV_FILE = 'logs/attack_flow_data.csv'

# Regex desenleri
# Log formatı: [2025-11-09 23:21:04,321] - ENTITY - LEVEL - Message
TIME_FORMAT = '%Y-%m-%d %H:%M:%S,%f'

# CAN Frame loglarını yakalama deseni
# Örn: CAN Frame Enjekte Edildi (CP Simülasyonu): ID=0x200, Data=...
CAN_PATTERN = re.compile(r'\[(?P<timestamp>.*?)\] - (?P<entity>.*?) - (?P<level>.*?) - .*?ID=0x(?P<can_id>[0-9A-F]+).*?Data=(?P<payload>[0-9a-f]+)')

# IDS Anomali tespit logunu yakalama deseni
ANOMALY_DETECTION_PATTERN = re.compile(r'\[(?P<timestamp>.*?)\] - CAN-IDS - CRITICAL - \*\*\* ANOMALİ TESPİT EDİLDİ! \*\*\*')

# Veri Seti Sütunları
COLUMNS = ['timestamp', 'entity', 'can_id', 'frame_type', 'is_attack_frame', 'is_anomaly_detected']