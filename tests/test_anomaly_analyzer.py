#!/usr/bin/env python3
"""
Test senaryoları - EVCS Anomali Analiz Sistemi için
Test Scenarios for EV Charging Station Anomaly Analysis System
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'docs'))

import unittest
import json
from datetime import datetime
from evcs_attack_analyzer import EVCSAttackAnalyzer

class TestEVCSAttackAnalyzer(unittest.TestCase):
    """EVCS Saldırı Analiz Sistemi test senaryoları"""

    def setUp(self):
        """Test öncesi kurulum"""
        self.analyzer = EVCSAttackAnalyzer()

    def test_analyzer_initialization(self):
        """Analiz sistemi başlatma testi"""
        self.assertIsNotNone(self.analyzer)
        self.assertTrue(hasattr(self.analyzer, 'attack_patterns'))

    def test_log_parsing(self):
        """Log ayrıştırma testi"""
        test_log = "2024-11-05 20:00:00 [CRITICAL] EVS001 - CREDENTIAL_LEAK: Kullanıcı kimlik bilgisi açık metin olarak kaydedildi"

        parsed = self.analyzer.parse_log_entry(test_log)

        self.assertIsNotNone(parsed)
        self.assertEqual(parsed['severity'], 'CRITICAL')
        self.assertEqual(parsed['station_id'], 'EVS001')
        self.assertEqual(parsed['attack_type'], 'CREDENTIAL_LEAK')

    def test_anomaly_detection(self):
        """Anomali tespit testi"""
        # Test anomali verisi
        anomaly_log = {
            'timestamp': datetime.now().isoformat(),
            'station_id': 'EVS001',
            'attack_type': 'CREDENTIAL_LEAK',
            'severity': 'CRITICAL',
            'description': 'Kullanıcı kimlik bilgisi sızıntısı tespit edildi'
        }

        result = self.analyzer.detect_anomaly(anomaly_log)

        self.assertTrue(result['is_anomaly'])
        self.assertEqual(result['attack_type'], 'CREDENTIAL_LEAK')
        self.assertGreater(result['confidence'], 0.8)

    def test_pattern_matching(self):
        """Patern eşleştirme testi"""
        # DoS saldırısı pattern
        dos_pattern = {
            'attack_type': 'DOS_ATTACK',
            'frequency': 'HIGH',
            'impact': 'CRITICAL'
        }

        match_result = self.analyzer.match_attack_pattern(dos_pattern)

        self.assertTrue(match_result['pattern_matched'])
        self.assertEqual(match_result['attack_category'], 'AVAILABILITY')

class TestSecurityAnalysis(unittest.TestCase):
    """Güvenlik analizi test senaryoları"""

    def setUp(self):
        self.analyzer = EVCSAttackAnalyzer()

    def test_credential_leak_analysis(self):
        """Kimlik bilgisi sızıntısı analizi"""
        credential_event = {
            'attack_type': 'CREDENTIAL_LEAK',
            'severity': 'CRITICAL',
            'affected_users': ['user001', 'user002'],
            'exposed_data': ['username', 'password', 'token']
        }

        analysis = self.analyzer.analyze_security_impact(credential_event)

        self.assertEqual(analysis['risk_level'], 'HIGH')
        self.assertIn('CONFIDENTIALITY', analysis['cia_impact'])
        self.assertGreater(analysis['business_impact_score'], 7)

    def test_dos_attack_analysis(self):
        """DoS saldırısı analizi"""
        dos_event = {
            'attack_type': 'DOS_ATTACK',
            'severity': 'CRITICAL',
            'affected_stations': ['EVS001', 'EVS002', 'EVS003'],
            'duration': '2 hours'
        }

        analysis = self.analyzer.analyze_security_impact(dos_event)

        self.assertEqual(analysis['risk_level'], 'HIGH')
        self.assertIn('AVAILABILITY', analysis['cia_impact'])
        self.assertGreater(analysis['business_impact_score'], 8)

    def test_price_manipulation_analysis(self):
        """Fiyat manipülasyonu analizi"""
        price_event = {
            'attack_type': 'PRICE_MANIPULATION',
            'severity': 'HIGH',
            'manipulated_amount': 150.50,
            'affected_transactions': 25
        }

        analysis = self.analyzer.analyze_security_impact(price_event)

        self.assertEqual(analysis['risk_level'], 'MEDIUM')
        self.assertIn('INTEGRITY', analysis['cia_impact'])

class TestReportGeneration(unittest.TestCase):
    """Rapor oluşturma test senaryoları"""

    def setUp(self):
        self.analyzer = EVCSAttackAnalyzer()

    def test_json_report_generation(self):
        """JSON rapor oluşturma testi"""
        test_events = [
            {
                'event_id': 1,
                'attack_type': 'CREDENTIAL_LEAK',
                'severity': 'CRITICAL',
                'timestamp': datetime.now().isoformat()
            },
            {
                'event_id': 2,
                'attack_type': 'DOS_ATTACK',
                'severity': 'CRITICAL',
                'timestamp': datetime.now().isoformat()
            }
        ]

        report = self.analyzer.generate_json_report(test_events)

        self.assertIsNotNone(report)
        self.assertIn('summary', report)
        self.assertIn('events', report)
        self.assertEqual(len(report['events']), 2)

    def test_statistics_calculation(self):
        """İstatistik hesaplama testi"""
        test_events = [
            {'attack_type': 'CREDENTIAL_LEAK', 'severity': 'CRITICAL'},
            {'attack_type': 'CREDENTIAL_LEAK', 'severity': 'CRITICAL'},
            {'attack_type': 'DOS_ATTACK', 'severity': 'CRITICAL'},
            {'attack_type': 'PRICE_MANIPULATION', 'severity': 'HIGH'}
        ]

        stats = self.analyzer.calculate_statistics(test_events)

        self.assertEqual(stats['total_events'], 4)
        self.assertEqual(stats['critical_events'], 3)
        self.assertEqual(stats['most_common_attack'], 'CREDENTIAL_LEAK')

class TestRealTimeMonitoring(unittest.TestCase):
    """Gerçek zamanlı izleme test senaryoları"""

    def setUp(self):
        self.analyzer = EVCSAttackAnalyzer()

    def test_threshold_monitoring(self):
        """Eşik değer izleme testi"""
        # Yüksek frekanslı olaylar
        events = []
        for i in range(100):
            events.append({
                'timestamp': datetime.now().isoformat(),
                'station_id': 'EVS001',
                'event_type': 'AUTHENTICATION_FAILURE'
            })

        alert = self.analyzer.check_frequency_threshold(events, window_minutes=5)

        self.assertTrue(alert['threshold_exceeded'])
        self.assertEqual(alert['alert_level'], 'HIGH')

    def test_pattern_correlation(self):
        """Patern korelasyon testi"""
        # İlişkili saldırı dizisi
        attack_sequence = [
            {'attack_type': 'RECONNAISSANCE', 'timestamp': '2024-11-05T20:00:00'},
            {'attack_type': 'CREDENTIAL_LEAK', 'timestamp': '2024-11-05T20:05:00'},
            {'attack_type': 'SESSION_HIJACK', 'timestamp': '2024-11-05T20:10:00'},
            {'attack_type': 'DATA_EXFILTRATION', 'timestamp': '2024-11-05T20:15:00'}
        ]

        correlation = self.analyzer.correlate_attack_patterns(attack_sequence)

        self.assertTrue(correlation['correlated_attack'])
        self.assertEqual(correlation['attack_chain_type'], 'ADVANCED_PERSISTENT_THREAT')

class TestPerformanceMetrics(unittest.TestCase):
    """Performans metrik test senaryoları"""

    def setUp(self):
        self.analyzer = EVCSAttackAnalyzer()

    def test_detection_accuracy(self):
        """Tespit doğruluk testi"""
        # Bilinen pozitif ve negatif örnekler
        known_anomalies = [
            {'is_anomaly': True, 'attack_type': 'CREDENTIAL_LEAK'},
            {'is_anomaly': True, 'attack_type': 'DOS_ATTACK'},
            {'is_anomaly': False, 'event_type': 'NORMAL_CHARGING'}
        ]

        accuracy_metrics = self.analyzer.calculate_detection_accuracy(known_anomalies)

        self.assertIn('precision', accuracy_metrics)
        self.assertIn('recall', accuracy_metrics)
        self.assertIn('f1_score', accuracy_metrics)

    def test_processing_performance(self):
        """İşleme performans testi"""
        # Büyük veri seti
        large_dataset = []
        for i in range(10000):
            large_dataset.append({
                'event_id': i,
                'timestamp': datetime.now().isoformat(),
                'station_id': f'EVS{i%50:03d}',
                'event_type': 'NORMAL_OPERATION'
            })

        start_time = datetime.now()
        self.analyzer.batch_process_events(large_dataset)
        end_time = datetime.now()

        processing_time = (end_time - start_time).total_seconds()

        # 10K event < 30 saniyede işlenmeli
        self.assertLess(processing_time, 30)

if __name__ == '__main__':
    print("EVCS Anomali Analiz Sistemi - Test Senaryoları")
    print("=" * 50)

    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Test sınıflarını ekle
    suite.addTests(loader.loadTestsFromTestCase(TestEVCSAttackAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestReportGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestRealTimeMonitoring))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceMetrics))

    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Sonuçları özetle
    print(f"\nTest Sonuçları:")
    print(f"Toplam test: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hata: {len(result.errors)}")

    # Detaylı başarısızlık raporu
    if result.failures:
        print(f"\nBaşarısız Testler:")
        for i, failure in enumerate(result.failures, 1):
            print(f"{i}. {failure[0]}")
            print(f"   Hata: {failure[1][:200]}...")

    if result.errors:
        print(f"\nHatalı Testler:")
        for i, error in enumerate(result.errors, 1):
            print(f"{i}. {error[0]}")
            print(f"   Hata: {error[1][:200]}...")