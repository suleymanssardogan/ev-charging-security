#!/usr/bin/env python3
"""
Test senaryoları - EVCS Log Anomali Simülatörü için
Test Scenarios and Results for EV Charging Station Log Anomaly Detection
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'simulators'))

import unittest
from datetime import datetime
from evcs_log_simulator import EVCSLogSimulator

class TestEVCSLogSimulator(unittest.TestCase):
    """EVCS Log Simülatörü test senaryoları"""

    def setUp(self):
        """Test öncesi kurulum"""
        self.simulator = EVCSLogSimulator(seed=12345)
        self.base_time = datetime.now()

    def test_normal_event_generation(self):
        """Normal olay oluşturma testi"""
        event = self.simulator.create_normal_event(1, self.base_time)

        # Temel alanların varlığını kontrol et
        self.assertIn('event_id', event)
        self.assertIn('timestamp', event)
        self.assertIn('station_id', event)
        self.assertIn('event_type', event)
        self.assertIn('severity', event)

        # Normal olayların severity seviyesi
        self.assertIn(event['severity'], ['INFO', 'WARNING'])

    def test_anomaly_generation(self):
        """Anomali oluşturma testi"""
        anomaly = self.simulator.create_anomaly_event(1, self.base_time)

        # Anomali temel alanları
        self.assertIn('event_id', anomaly)
        self.assertIn('attack_type', anomaly)
        self.assertIn('severity', anomaly)

        # Anomali severity seviyesi
        self.assertEqual(anomaly['severity'], 'CRITICAL')

        # Saldırı tipi geçerliliği
        self.assertIn(anomaly['attack_type'], self.simulator.attack_types)

    def test_credential_leak_detection(self):
        """Kimlik bilgisi sızıntısı testi"""
        # Credential leak anomalisi oluştur
        anomaly = self.simulator.create_specific_anomaly('CREDENTIAL_LEAK', 1, self.base_time)

        self.assertEqual(anomaly['attack_type'], 'CREDENTIAL_LEAK')
        self.assertIn('description', anomaly)
        self.assertIn('kimlik bilgisi', anomaly['description'].lower())

    def test_dos_attack_detection(self):
        """DoS saldırısı testi"""
        anomaly = self.simulator.create_specific_anomaly('DOS_ATTACK', 1, self.base_time)

        self.assertEqual(anomaly['attack_type'], 'DOS_ATTACK')
        self.assertEqual(anomaly['severity'], 'CRITICAL')

    def test_token_generation(self):
        """Token oluşturma testi"""
        token = self.simulator.generate_token(12)

        self.assertEqual(len(token), 12)
        self.assertTrue(token.isalnum())

    def test_ip_generation(self):
        """IP adresi oluşturma testi"""
        ip = self.simulator.generate_ip_address()

        # IP formatı kontrolü
        parts = ip.split('.')
        self.assertEqual(len(parts), 4)

        for part in parts:
            num = int(part)
            self.assertTrue(0 <= num <= 255)

    def test_bulk_log_generation(self):
        """Toplu log oluşturma testi"""
        logs = self.simulator.generate_logs(100, anomaly_ratio=0.2)

        # 100 log oluşturulmalı
        self.assertEqual(len(logs), 100)

        # Anomali oranı kontrolü (yaklaşık %20)
        anomaly_count = sum(1 for log in logs if log.get('attack_type'))
        anomaly_ratio = anomaly_count / len(logs)

        # %15-25 arasında anomali olmalı
        self.assertTrue(0.15 <= anomaly_ratio <= 0.25)

class TestAnomalyScenarios(unittest.TestCase):
    """Spesifik anomali senaryoları"""

    def setUp(self):
        self.simulator = EVCSLogSimulator(seed=54321)
        self.base_time = datetime.now()

    def test_session_hijack_scenario(self):
        """Oturum ele geçirme senaryosu"""
        # Normal oturum başlatma
        normal_session = self.simulator.create_normal_event(1, self.base_time)

        # Oturum ele geçirme anomalisi
        hijack_anomaly = self.simulator.create_specific_anomaly('SESSION_HIJACK', 2, self.base_time)

        self.assertEqual(hijack_anomaly['attack_type'], 'SESSION_HIJACK')
        self.assertIn('oturum', hijack_anomaly['description'].lower())

    def test_price_manipulation_scenario(self):
        """Fiyat manipülasyonu senaryosu"""
        anomaly = self.simulator.create_specific_anomaly('PRICE_MANIPULATION', 1, self.base_time)

        self.assertEqual(anomaly['attack_type'], 'PRICE_MANIPULATION')
        self.assertIn('fiyat', anomaly['description'].lower())

    def test_firmware_tamper_scenario(self):
        """Firmware manipülasyonu senaryosu"""
        anomaly = self.simulator.create_specific_anomaly('FIRMWARE_TAMPER', 1, self.base_time)

        self.assertEqual(anomaly['attack_type'], 'FIRMWARE_TAMPER')
        self.assertIn('firmware', anomaly['description'].lower())

class TestLogPatterns(unittest.TestCase):
    """Log patern analiz testleri"""

    def setUp(self):
        self.simulator = EVCSLogSimulator()
        self.base_time = datetime.now()

    def test_normal_charging_flow(self):
        """Normal şarj akışı testi"""
        # Şarj başlangıcı
        start_event = self.simulator.create_normal_event(1, self.base_time)

        # Şarj devam ediyor
        progress_event = self.simulator.create_normal_event(2, self.base_time)

        # Şarj tamamlandı
        complete_event = self.simulator.create_normal_event(3, self.base_time)

        # Tüm olaylar normal seviyede olmalı
        events = [start_event, progress_event, complete_event]
        for event in events:
            self.assertIn(event['severity'], ['INFO', 'WARNING'])

    def test_anomaly_frequency(self):
        """Anomali frekans testi"""
        logs = self.simulator.generate_logs(1000, anomaly_ratio=0.1)

        anomaly_count = sum(1 for log in logs if log.get('attack_type'))
        normal_count = len(logs) - anomaly_count

        # Normal olaylar daha fazla olmalı
        self.assertGreater(normal_count, anomaly_count)

        # Anomali oranı %5-15 arasında olmalı
        ratio = anomaly_count / len(logs)
        self.assertTrue(0.05 <= ratio <= 0.15)

if __name__ == '__main__':
    print("EVCS Log Anomali Simülatörü - Test Senaryoları")
    print("=" * 50)

    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Test sınıflarını ekle
    suite.addTests(loader.loadTestsFromTestCase(TestEVCSLogSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestAnomalyScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestLogPatterns))

    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Sonuçları özetle
    print(f"\nTest Sonuçları:")
    print(f"Toplam test: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hata: {len(result.errors)}")

    if result.failures:
        print(f"\nBaşarısız testler:")
        for failure in result.failures:
            print(f"- {failure[0]}")

    if result.errors:
        print(f"\nHatalı testler:")
        for error in result.errors:
            print(f"- {error[0]}")