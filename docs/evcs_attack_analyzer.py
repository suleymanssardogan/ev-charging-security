#!/usr/bin/env python3
"""
EVCS Saldırı Analiz Sistemi
Gerçek log dosyalarından saldırı tespiti ve analiz raporu
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional

class AttackAnalyzer:
    def __init__(self):
        self.detected_attacks = []

    def analyze_log_file(self, log_file_path: str) -> Dict:
        """Log dosyasını analiz et ve saldırıları tespit et"""
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()

        attacks_found = []

        for line_num, line in enumerate(log_lines, 1):
            line = line.strip()
            if not line:
                continue

            # Her saldırı türü için kontrol et
            attack = self._detect_attack(line, line_num)
            if attack:
                attacks_found.append(attack)

        # Analiz sonuçları
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_lines": len(log_lines),
            "attacks_detected": len(attacks_found),
            "attacks": attacks_found,
            "risk_level": self._calculate_risk_level(attacks_found),
            "recommendations": self._generate_recommendations(attacks_found)
        }

        return analysis

    def _detect_attack(self, line: str, line_num: int) -> Optional[Dict]:
        """Tek satırda saldırı tespiti"""

        # 1. Credential Leak - Açık token
        token_match = re.search(r'auth token=([A-Za-z0-9]{8,})', line)
        if token_match and '*' not in token_match.group(1):
            return {
                "type": "CREDENTIAL_LEAK",
                "line": line_num,
                "content": line,
                "details": f"Açık token tespit edildi: {token_match.group(1)[:8]}...",
                "severity": "HIGH",
                "immediate_action": "Token'ı derhal iptal et ve logları temizle"
            }

        # 2. Command Injection
        cmd_patterns = [
            r'(rm\s+-rf|;\s*reboot|shutdown)',
            r'(cat\s+/etc/passwd|/bin/bash)',
            r'(wget\s+\w+|nc\s+-e)',
            r'(python\s+-c|import\s+os)'
        ]
        for pattern in cmd_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return {
                    "type": "COMMAND_INJECTION",
                    "line": line_num,
                    "content": line,
                    "details": f"Şüpheli komut kalıbı tespit edildi",
                    "severity": "CRITICAL",
                    "immediate_action": "Sistem erişimini kontrol et, güvenlik açığını kapat"
                }

        # 3. Price Manipulation
        if "set_price" in line:
            price_match = re.search(r'price=(\d+)', line)
            if price_match and int(price_match.group(1)) < 10:
                return {
                    "type": "PRICE_MANIPULATION",
                    "line": line_num,
                    "content": line,
                    "details": f"Anormal düşük fiyat: {price_match.group(1)}TL/kWh",
                    "severity": "HIGH",
                    "immediate_action": "Fiyat değişikliklerini geri al, API anahtarlarını kontrol et"
                }

        # 4. DoS Attack
        if "connection_flood" in line or "rate_limit_exceeded" in line:
            return {
                "type": "DOS_ATTACK",
                "line": line_num,
                "content": line,
                "details": "DoS saldırısı tespit edildi",
                "severity": "HIGH",
                "immediate_action": "IP'yi engelle, rate limiting uygula"
            }

        # 5. Unauthorized Access
        if "unauthorized_admin_access" in line:
            return {
                "type": "UNAUTHORIZED_ACCESS",
                "line": line_num,
                "content": line,
                "details": "Yetkisiz yönetici erişimi",
                "severity": "CRITICAL",
                "immediate_action": "Tüm admin oturumlarını sonlandır, şifreleri değiştir"
            }

        return None

    def _calculate_risk_level(self, attacks: List[Dict]) -> str:
        """Risk seviyesi hesapla"""
        if not attacks:
            return "LOW"

        critical_count = sum(1 for a in attacks if a['severity'] == 'CRITICAL')
        high_count = sum(1 for a in attacks if a['severity'] == 'HIGH')

        if critical_count > 0:
            return "CRITICAL"
        elif high_count > 2:
            return "HIGH"
        elif high_count > 0:
            return "MEDIUM"
        else:
            return "LOW"

    def _generate_recommendations(self, attacks: List[Dict]) -> List[str]:
        """Saldırılara göre öneriler oluştur"""
        recommendations = []
        attack_types = set(a['type'] for a in attacks)

        if 'CREDENTIAL_LEAK' in attack_types:
            recommendations.extend([
                "Log maskeleme sistemi uygula",
                "Tüm aktif token'ları yenile",
                "Log erişim kontrollerini artır"
            ])

        if 'COMMAND_INJECTION' in attack_types:
            recommendations.extend([
                "Input validation kurallarını sıkılaştır",
                "Web application firewall (WAF) kur",
                "Sistem güncellemelerini kontrol et"
            ])

        if 'PRICE_MANIPULATION' in attack_types:
            recommendations.extend([
                "API anahtarı yetkilendirmelerini gözden geçir",
                "Fiyat değişiklik onay süreçleri ekle",
                "Mali işlem auditini başlat"
            ])

        if 'DOS_ATTACK' in attack_types:
            recommendations.extend([
                "DDoS koruması aktif et",
                "Rate limiting ayarlarını optimize et",
                "CDN ve load balancer kullan"
            ])

        if 'UNAUTHORIZED_ACCESS' in attack_types:
            recommendations.extend([
                "Multi-factor authentication zorunlu kıl",
                "Kullanıcı erişim haklarını yeniden değerlendir",
                "Sistem güvenlik auditini yap"
            ])

        return recommendations

def main():
    analyzer = AttackAnalyzer()

    # Log dosyasını analiz et
    try:
        analysis = analyzer.analyze_log_file("evcs_system_detailed.log")

        # Sonuçları kaydet
        with open("attack_analysis.json", 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)

        # Özet rapor
        print("🔍 EVCS Saldırı Analizi Tamamlandı")
        print(f"📄 Analiz edilen satır: {analysis['total_lines']}")
        print(f"⚠️  Tespit edilen saldırı: {analysis['attacks_detected']}")
        print(f"🎯 Risk seviyesi: {analysis['risk_level']}")

        if analysis['attacks_detected'] > 0:
            print("\n🚨 TESPİT EDİLEN SALDIRILAR:")
            for attack in analysis['attacks']:
                print(f"   {attack['type']} (Satır {attack['line']}) - {attack['severity']}")
                print(f"   → {attack['immediate_action']}")

        print(f"\n✅ Detaylı analiz: attack_analysis.json")

    except FileNotFoundError:
        print("❌ evcs_system_detailed.log dosyası bulunamadı!")
        print("Önce log simülasyonunu çalıştır.")

if __name__ == "__main__":
    main()