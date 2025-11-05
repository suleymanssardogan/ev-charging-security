#!/usr/bin/env python3
"""
Dinamik Log Analizi Rapor Oluşturucu
Sadece gerçek log analizinden gelen veriler için PDF oluşturur
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os
import json
from typing import Dict

class DynamicLogReporter:
    def __init__(self):
        self.width, self.height = A4
        self.margin = 50
        self.used_font = self._setup_font()

    def _setup_font(self) -> str:
        """Font kurulumu"""
        font_candidates = [
            "/System/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]

        for fpath in font_candidates:
            if os.path.exists(fpath):
                try:
                    if fpath.endswith('.ttf'):
                        pdfmetrics.registerFont(TTFont("TurkishFont", fpath))
                    elif fpath.endswith('.ttc'):
                        pdfmetrics.registerFont(TTFont("TurkishFont", fpath, subfontIndex=0))
                    return "TurkishFont"
                except:
                    continue
        return "Helvetica"

    def generate_dynamic_summary(self, attack_data: Dict) -> str:
        """Sadece dinamik verilerin özet raporu"""

        # Gerçek verilerden hesaplamalar
        total_lines = attack_data.get('total_lines', 0)
        attacks_detected = attack_data.get('attacks_detected', 0)
        risk_level = attack_data.get('risk_level', 'UNKNOWN')

        # Anomali türü dağılımı
        attacks = attack_data.get('attacks', [])
        attack_types = {}
        for attack in attacks:
            attack_type = attack.get('type', 'UNKNOWN')
            attack_types[attack_type] = attack_types.get(attack_type, 0) + 1

        # Dinamik rapor metni
        report = f"""
=== EV ŞARJ İSTASYONU LOG ANOMALİSİ DİNAMİK RAPORU ===
Analiz Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}

📊 GERÇEK ANALİZ SONUÇLARI:
• İşlenen log satırı: {total_lines:,}
• Tespit edilen anomali: {attacks_detected}
• Anomali oranı: {(attacks_detected/total_lines*100):.2f}%
• Risk seviyesi: {risk_level}

📈 ANOMALİ TÜRÜ DAĞILIMI:"""

        for attack_type, count in attack_types.items():
            percentage = (count / len(attacks) * 100) if attacks else 0
            report += f"\n• {attack_type}: {count} adet ({percentage:.1f}%)"

        # Matematik hesaplamaları
        report += f"""

🧮 DİNAMİK MATEMATİK HESAPLAMALARI:
• LADR = ({attacks_detected}/{total_lines}) × 100 = {(attacks_detected/total_lines*100):.2f}%
• İşlem karmaşıklığı: {total_lines * 10 * 50:,} operasyon
• Optimal clustering k = √({attacks_detected}/2) ≈ {int((attacks_detected/2)**0.5) if attacks_detected > 0 else 0}

⚡ PERFORMANS METRİKLERİ:
• Bellek kullanımı: ~{total_lines * 100} bytes (log)
• Sonuç boyutu: ~{attacks_detected * 200} bytes
• İşleme hızı hedefi: >1000 satır/saniye

📋 ANOMALİ ÖRNEKLER (İlk 5):"""

        # İlk 5 anomali örneği
        for i, attack in enumerate(attacks[:5], 1):
            report += f"""
{i}. {attack.get('type', 'UNKNOWN')} (Satır {attack.get('line', 'N/A')})
   Pattern: {attack.get('details', 'N/A')[:60]}..."""

        report += f"""

✅ Bu rapor {datetime.now().strftime('%H:%M:%S')} saatinde otomatik oluşturulmuştur.
📁 Detaylı analiz: attack_analysis.json
"""

        return report

    def save_dynamic_report(self, attack_data: Dict, output_path: str = "Log_Anomali_Dinamik_Rapor.txt"):
        """Dinamik raporu metin dosyasına kaydet"""

        report_content = self.generate_dynamic_summary(attack_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"📄 Dinamik log raporu: {output_path}")
        return report_content

def main():
    """Ana fonksiyon - sadece dinamik veriler"""
    try:
        with open("attack_analysis.json", 'r', encoding='utf-8') as f:
            attack_data = json.load(f)
    except FileNotFoundError:
        print("❌ attack_analysis.json dosyası bulunamadı!")
        print("Önce evcs_attack_analyzer.py'yi çalıştır.")
        return

    # Dinamik rapor oluşturucu
    reporter = DynamicLogReporter()

    # Sadece dinamik verileri işle
    report_content = reporter.save_dynamic_report(attack_data)

    # Terminal'de özet göster
    print("\n" + "="*60)
    print("DİNAMİK LOG ANALİZİ ÖZETİ")
    print("="*60)
    print(f"Anomali tespit: {attack_data.get('attacks_detected', 0)}/{attack_data.get('total_lines', 0)}")
    print(f"Risk seviye: {attack_data.get('risk_level', 'UNKNOWN')}")
    print(f"Rapor dosyası: Log_Anomali_Dinamik_Rapor.txt")
    print("="*60)

if __name__ == "__main__":
    main()