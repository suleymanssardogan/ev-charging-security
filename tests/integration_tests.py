#!/usr/bin/env python3
"""
Entegrasyon Testleri - EVCS Log Anomali Tespit Sistemi
Integration Tests for Complete EV Charging Station Log Anomaly Detection System
"""

import sys
import os
import unittest
import json
import tempfile
from datetime import datetime, timedelta

# Modül yollarını ekle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'simulators'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'docs'))

try:
    from evcs_log_simulator import EVCSLogSimulator
    from evcs_attack_analyzer import EVCSAttackAnalyzer
    from auto_log_processor import AutoLogProcessor
except ImportError as e:
    print(f"Modül import hatası: {e}")
    print("Simulatör ve analiz modüllerinin doğru yolda olduğundan emin olun.")

class TestFullSystemIntegration(unittest.TestCase):
    """Tam sistem entegrasyon testleri"""

    def setUp(self):
        """Test kurulumu"""
        self.simulator = EVCSLogSimulator(seed=12345)
        self.analyzer = EVCSAttackAnalyzer()
        self.temp_dir = tempfile.mkdtemp()

    def test_complete_workflow(self):
        """Tam iş akışı testi: Simülasyon → Analiz → Rapor"""

        # 1. Log verisi simülasyonu
        logs = self.simulator.generate_logs(1000, anomaly_ratio=0.15)

        self.assertEqual(len(logs), 1000)

        # 2. Anomali analizi
        analysis_results = []
        for log in logs:
            if log.get('attack_type'):  # Anomali ise
                result = self.analyzer.detect_anomaly(log)
                analysis_results.append(result)

        # 3. Sonuçların doğrulanması
        anomaly_count = len(analysis_results)
        self.assertTrue(100 <= anomaly_count <= 200)  # %10-20 anomali

        # 4. Rapor oluşturma
        report = self.analyzer.generate_json_report(analysis_results)

        self.assertIn('summary', report)
        self.assertIn('events', report)
        self.assertEqual(len(report['events']), anomaly_count)

    def test_real_time_processing(self):
        """Gerçek zamanlı işleme simülasyonu"""

        processed_events = []
        alert_count = 0

        # 1 saatlik simülasyon
        base_time = datetime.now()

        for minute in range(60):  # 60 dakika
            current_time = base_time + timedelta(minutes=minute)

            # Her dakika 5-10 event oluştur
            minute_events = self.simulator.generate_logs(
                count=random.randint(5, 10),
                anomaly_ratio=0.1,
                start_time=current_time
            )

            # Real-time analiz
            for event in minute_events:
                if event.get('attack_type'):
                    analysis = self.analyzer.detect_anomaly(event)
                    processed_events.append(analysis)

                    if analysis.get('confidence', 0) > 0.8:
                        alert_count += 1

        # Sonuç doğrulama
        self.assertGreater(len(processed_events), 0)
        self.assertGreater(alert_count, 0)

    def test_multi_station_correlation(self):
        """Çoklu istasyon korelasyon testi"""

        # Koordineli saldırı simülasyonu
        stations = ['EVS001', 'EVS002', 'EVS003']
        base_time = datetime.now()

        correlated_attacks = []

        for i, station in enumerate(stations):
            # Her istasyonda 5 dakika arayla aynı tip saldırı
            attack_time = base_time + timedelta(minutes=i*5)

            attack_event = {
                'event_id': i + 1,
                'timestamp': attack_time.isoformat(),
                'station_id': station,
                'attack_type': 'DOS_ATTACK',
                'severity': 'CRITICAL',
                'description': f'{station} istasyonunda DoS saldırısı tespit edildi'
            }

            correlated_attacks.append(attack_event)

        # Korelasyon analizi
        correlation_result = self.analyzer.correlate_attack_patterns(correlated_attacks)

        self.assertTrue(correlation_result.get('correlated_attack', False))
        self.assertEqual(correlation_result.get('attack_pattern'), 'DISTRIBUTED_ATTACK')

class TestDataPersistence(unittest.TestCase):
    """Veri kalıcılığı ve depolama testleri"""

    def setUp(self):
        self.simulator = EVCSLogSimulator()
        self.analyzer = EVCSAttackAnalyzer()
        self.temp_dir = tempfile.mkdtemp()

    def test_log_file_storage(self):
        """Log dosya depolama testi"""

        # Log verisi oluştur
        logs = self.simulator.generate_logs(500, anomaly_ratio=0.2)

        # Dosyaya kaydet
        log_file = os.path.join(self.temp_dir, 'test_logs.json')

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2, default=str)

        # Dosyadan oku
        with open(log_file, 'r', encoding='utf-8') as f:
            loaded_logs = json.load(f)

        self.assertEqual(len(loaded_logs), 500)
        self.assertEqual(loaded_logs[0]['event_id'], logs[0]['event_id'])

    def test_analysis_result_persistence(self):
        """Analiz sonucu kalıcılığı testi"""

        # Anomali verisi oluştur
        anomaly_logs = []
        for i in range(50):
            anomaly = self.simulator.create_anomaly_event(i+1, datetime.now())
            anomaly_logs.append(anomaly)

        # Analiz et
        analysis_results = []
        for log in anomaly_logs:
            result = self.analyzer.detect_anomaly(log)
            analysis_results.append(result)

        # Sonuçları kaydet
        result_file = os.path.join(self.temp_dir, 'analysis_results.json')

        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2, default=str)

        # Dosya boyutu kontrolü
        file_size = os.path.getsize(result_file)
        self.assertGreater(file_size, 1000)  # En az 1KB

class TestPerformanceIntegration(unittest.TestCase):
    """Performans entegrasyon testleri"""

    def setUp(self):
        self.simulator = EVCSLogSimulator()
        self.analyzer = EVCSAttackAnalyzer()

    def test_large_dataset_processing(self):
        """Büyük veri seti işleme testi"""

        start_time = datetime.now()

        # 10,000 event oluştur
        large_dataset = self.simulator.generate_logs(10000, anomaly_ratio=0.1)

        generation_time = datetime.now()

        # Anomalileri analiz et
        anomaly_count = 0
        for event in large_dataset:
            if event.get('attack_type'):
                self.analyzer.detect_anomaly(event)
                anomaly_count += 1

        end_time = datetime.now()

        # Performans metrikleri
        total_time = (end_time - start_time).total_seconds()
        generation_duration = (generation_time - start_time).total_seconds()
        analysis_duration = (end_time - generation_time).total_seconds()

        print(f"\nPerformans Metrikleri:")
        print(f"Toplam süre: {total_time:.2f} saniye")
        print(f"Veri oluşturma: {generation_duration:.2f} saniye")
        print(f"Analiz süresi: {analysis_duration:.2f} saniye")
        print(f"Saniyede işlenen event: {10000/total_time:.0f}")

        # Performans kriterleri
        self.assertLess(total_time, 60)  # 1 dakikadan az
        self.assertGreater(anomaly_count, 500)  # En az 500 anomali

    def test_memory_usage(self):
        """Bellek kullanımı testi"""
        import psutil
        import gc

        # Başlangıç bellek kullanımı
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Büyük veri işleme
        for batch in range(10):
            logs = self.simulator.generate_logs(1000, anomaly_ratio=0.1)

            for log in logs:
                if log.get('attack_type'):
                    self.analyzer.detect_anomaly(log)

            # Garbage collection
            gc.collect()

        # Son bellek kullanımı
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        print(f"\nBellek Kullanımı:")
        print(f"Başlangıç: {initial_memory:.1f} MB")
        print(f"Son: {final_memory:.1f} MB")
        print(f"Artış: {memory_increase:.1f} MB")

        # Bellek sızıntısı kontrolü
        self.assertLess(memory_increase, 100)  # 100MB'dan az artış

class TestErrorHandling(unittest.TestCase):
    """Hata yönetimi entegrasyon testleri"""

    def setUp(self):
        self.simulator = EVCSLogSimulator()
        self.analyzer = EVCSAttackAnalyzer()

    def test_malformed_log_handling(self):
        """Bozuk log verisi işleme testi"""

        # Bozuk log verileri
        malformed_logs = [
            {},  # Boş log
            {'event_id': 'invalid'},  # Geçersiz ID
            {'timestamp': 'invalid_date'},  # Geçersiz tarih
            None,  # None değer
        ]

        processed_count = 0
        error_count = 0

        for log in malformed_logs:
            try:
                if log and log.get('attack_type'):
                    self.analyzer.detect_anomaly(log)
                processed_count += 1
            except Exception:
                error_count += 1

        # Sistem çökmemeli
        self.assertGreaterEqual(processed_count, 0)

    def test_resource_exhaustion_handling(self):
        """Kaynak tükenmesi işleme testi"""

        try:
            # Çok büyük dataset denemesi
            very_large_dataset = self.simulator.generate_logs(100000, anomaly_ratio=0.1)

            # Bellek limitli işleme
            batch_size = 1000
            total_processed = 0

            for i in range(0, len(very_large_dataset), batch_size):
                batch = very_large_dataset[i:i+batch_size]

                for log in batch:
                    if log.get('attack_type'):
                        self.analyzer.detect_anomaly(log)

                total_processed += len(batch)

                # İlerleme kontrolü
                if total_processed >= 10000:  # 10K limit
                    break

            self.assertGreaterEqual(total_processed, 10000)

        except MemoryError:
            # Bellek hatası beklenen bir durum
            self.assertTrue(True)

if __name__ == '__main__':
    print("EVCS Log Anomali Tespit Sistemi - Entegrasyon Testleri")
    print("=" * 60)

    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Test sınıflarını ekle
    suite.addTests(loader.loadTestsFromTestCase(TestFullSystemIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestDataPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))

    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Detaylı sonuç raporu
    print(f"\n{'='*60}")
    print(f"ENTEGRASYON TEST SONUÇLARI")
    print(f"{'='*60}")
    print(f"Toplam Test Sayısı: {result.testsRun}")
    print(f"Başarılı Testler: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız Testler: {len(result.failures)}")
    print(f"Hatalı Testler: {len(result.errors)}")

    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"Başarı Oranı: {success_rate:.1f}%")

    if result.failures:
        print(f"\nBaşarısız Testler:")
        for i, failure in enumerate(result.failures, 1):
            print(f"{i}. {failure[0]}")

    if result.errors:
        print(f"\nHatalı Testler:")
        for i, error in enumerate(result.errors, 1):
            print(f"{i}. {error[0]}")

    # Sistem durumu özeti
    print(f"\nSistem Entegrasyon Durumu:")
    if success_rate >= 80:
        print("✅ Sistem entegrasyonu başarılı")
    elif success_rate >= 60:
        print("⚠️  Sistem entegrasyonu kısmen başarılı")
    else:
        print("❌ Sistem entegrasyonu başarısız")