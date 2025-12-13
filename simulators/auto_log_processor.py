#!/usr/bin/env python3
"""
Otomatik Log Anomali İşleyici
Log oluştur → Anomali tespit et → Rapor üret (tek komut)
"""

import subprocess
import os
from datetime import datetime


class AutoLogProcessor:
    """Simülasyon + analiz pipeline'ını çalıştıran basit yardımcı sınıf."""

    def __init__(self):
        self.started_at = datetime.now()

    def run(self):
        """Tam pipeline'ı çalıştır."""
        return run_log_anomaly_pipeline()

def run_log_anomaly_pipeline():
    """Tam log anomali pipeline'ını otomatik çalıştır"""

    print("🚀 EV Şarj İstasyonu Log Anomali Pipeline Başlatılıyor...")
    print("="*60)

    try:
        # 1. Log Oluştur
        print("📄 1/3: Test logları oluşturuluyor...")
        result1 = subprocess.run(["python3", "evcs_log_simulator.py"],
                               capture_output=True, text=True)
        if result1.returncode == 0:
            print("✅ Log dosyası oluşturuldu")
        else:
            print(f"❌ Log oluşturma hatası: {result1.stderr}")
            return

        # 2. Anomali Tespit Et
        print("\n🔍 2/3: Log anomali tespiti yapılıyor...")
        result2 = subprocess.run(["python3", "evcs_attack_analyzer.py"],
                               capture_output=True, text=True)
        if result2.returncode == 0:
            print("✅ Anomali analizi tamamlandı")
            # Anomali sonuçlarını göster
            lines = result2.stdout.strip().split('\n')
            for line in lines[-8:]:  # Son 8 satırı göster
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"❌ Anomali tespit hatası: {result2.stderr}")
            return

        # 3. Dinamik Rapor Oluştur
        print("\n📊 3/3: Dinamik rapor oluşturuluyor...")
        result3 = subprocess.run(["python3", "dynamic_report_generator.py"],
                               capture_output=True, text=True)
        if result3.returncode == 0:
            print("✅ Dinamik rapor hazır")
            # Rapor sonuçlarını göster
            lines = result3.stdout.strip().split('\n')
            for line in lines[-4:]:  # Son 4 satırı göster
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"❌ Rapor oluşturma hatası: {result3.stderr}")
            return

        print("\n" + "="*60)
        print("🎯 LOG ANOMALI PİPELİNE TAMAMLANDI!")
        print("="*60)

        # Dosya durumunu kontrol et
        files_to_check = [
            "evcs_system_detailed.log",
            "attack_analysis.json",
            "Log_Anomali_Dinamik_Rapor.txt",
            "EV_Log_Anomalisi_Analiz_Raporu.pdf"
        ]

        print("\n📁 Oluşturulan Dosyalar:")
        for file in files_to_check:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"✅ {file} ({size:,} bytes)")
            else:
                print(f"❌ {file} (bulunamadı)")

        print(f"\n⏰ İşlem zamanı: {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"❌ Pipeline hatası: {e}")

if __name__ == "__main__":
    run_log_anomaly_pipeline()
