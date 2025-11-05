# Test Senaryoları ve Sonuçlar

Bu klasör, EVCS (Electric Vehicle Charging Station) Log Anomali Tespit Sistemi için kapsamlı test senaryolarını içermektedir.

## Test Yapısı

### 1. Unit Tests (Birim Testler)

#### `test_log_simulator.py`
**Şarj İstasyonu Simülatörü Test Senaryoları**

- **Normal Event Generation**: Normal sistem olaylarının doğru oluşturulması
- **Anomaly Generation**: Anomali olaylarının tespit edilmesi
- **Token Security**: Güvenlik token'larının geçerliliği
- **Bulk Processing**: Toplu log işleme performansı

**Test Edilen Saldırı Türleri:**
- `CREDENTIAL_LEAK` - Kimlik bilgisi sızıntısı
- `DOS_ATTACK` - Hizmet engelleme saldırısı
- `SESSION_HIJACK` - Oturum ele geçirme
- `PRICE_MANIPULATION` - Fiyat manipülasyonu
- `FIRMWARE_TAMPER` - Firmware manipülasyonu

#### `test_anomaly_analyzer.py`
**Anomali Analiz Sistemi Test Senaryoları**

- **Log Parsing**: Log ayrıştırma doğruluğu
- **Pattern Matching**: Saldırı patern eşleştirme
- **Security Analysis**: Güvenlik etkisi analizi
- **Real-time Monitoring**: Gerçek zamanlı izleme
- **Performance Metrics**: Performans ölçümleri

**Analiz Edilen Güvenlik Kategorileri:**
- **Confidentiality** (Gizlilik)
- **Integrity** (Bütünlük)
- **Availability** (Erişilebilirlik)

### 2. Integration Tests (Entegrasyon Testleri)

#### `integration_tests.py`
**Tam Sistem Entegrasyon Testleri**

- **Complete Workflow**: Simülasyon → Analiz → Rapor iş akışı
- **Real-time Processing**: Gerçek zamanlı işleme simülasyonu
- **Multi-station Correlation**: Çoklu istasyon korelasyon analizi
- **Data Persistence**: Veri kalıcılığı ve depolama
- **Performance Testing**: Büyük veri seti performans testleri
- **Error Handling**: Hata yönetimi ve sistem dayanıklılığı

## Test Kategorileri

### Fonksiyonel Testler
- ✅ Normal log oluşturma
- ✅ Anomali tespit etme
- ✅ Patern eşleştirme
- ✅ Rapor oluşturma
- ✅ JSON/XML export

### Güvenlik Testleri
- ✅ Kimlik bilgisi sızıntısı tespiti
- ✅ DoS saldırısı analizi
- ✅ Oturum güvenliği
- ✅ Fiyat manipülasyonu
- ✅ Firmware güvenliği

### Performans Testleri
- ✅ 10K event/dakika işleme
- ✅ Bellek kulımı optimizasyonu
- ✅ Gerçek zamanlı analiz
- ✅ Batch processing
- ✅ Concurrent işleme

### Entegrasyon Testleri
- ✅ End-to-end workflow
- ✅ Çoklu modül etkileşimi
- ✅ Veri akışı bütünlüğü
- ✅ Sistem dayanıklılığı

## Testleri Çalıştırma

### Tüm Testler
```bash
cd tests/
python -m unittest discover -v
```

### Birim Testler
```bash
python test_log_simulator.py
python test_anomaly_analyzer.py
```

### Entegrasyon Testleri
```bash
python integration_tests.py
```

## Test Metrikleri ve Beklenen Sonuçlar

### Başarı Kriterleri

#### Log Simülatörü
- ✅ Event oluşturma: %100 başarı
- ✅ Anomali oranı: %10-20 arasında
- ✅ Token güvenliği: 12+ karakter
- ✅ IP validasyonu: RFC uyumlu

#### Anomali Analizi
- ✅ Tespit doğruluğu: >%85
- ✅ False positive: <%15
- ✅ Response time: <2 saniye
- ✅ Confidence score: >%80

#### Sistem Performansı
- ✅ Throughput: 10K event/dakika
- ✅ Memory usage: <100MB artış
- ✅ CPU utilization: <%70
- ✅ Processing latency: <1 saniye

### Test Coverage

| Modül | Unit Tests | Integration | Performance |
|-------|------------|-------------|-------------|
| Log Simulator | ✅ %95 | ✅ %90 | ✅ %85 |
| Anomaly Analyzer | ✅ %90 | ✅ %95 | ✅ %80 |
| Report Generator | ✅ %85 | ✅ %90 | ✅ %75 |
| Data Persistence | ✅ %80 | ✅ %95 | ✅ %70 |

## Test Veri Setleri

### Simülatör Test Verileri
- **Normal Events**: 80% oranında normal işlemler
- **Anomaly Events**: 20% oranında anomali olayları
- **Stations**: 50 adet şarj istasyonu (EVS001-EVS050)
- **Users**: 200 adet kullanıcı (user0001-user0200)

### Gerçek Zaman Senaryoları
- **Peak Hours**: Yoğun kullanım saatleri (08:00-18:00)
- **Off-peak Hours**: Düşük kullanım saatleri (00:00-06:00)
- **Weekend Patterns**: Hafta sonu kullanım desenleri
- **Holiday Periods**: Tatil dönemi anomalileri

## Saldırı Simülasyon Matrisi

| Saldırı Türü | Frequency | Severity | Detection Rate |
|---------------|-----------|----------|----------------|
| CREDENTIAL_LEAK | %15 | CRITICAL | %95 |
| DOS_ATTACK | %20 | CRITICAL | %90 |
| SESSION_HIJACK | %10 | HIGH | %85 |
| PRICE_MANIPULATION | %25 | MEDIUM | %80 |
| FIRMWARE_TAMPER | %5 | CRITICAL | %95 |
| MESSAGE_SPOOFING | %15 | HIGH | %85 |
| UNAUTHORIZED_ACCESS | %8 | HIGH | %90 |
| DATA_EXFILTRATION | %2 | CRITICAL | %98 |

## Raporlama ve Monitoring

### Test Raporu Formatı
```json
{
  "test_summary": {
    "total_tests": 45,
    "passed": 42,
    "failed": 2,
    "skipped": 1,
    "success_rate": "93.3%"
  },
  "performance_metrics": {
    "avg_processing_time": "1.2s",
    "memory_usage": "85MB",
    "throughput": "8500 events/min"
  },
  "security_coverage": {
    "attack_types_tested": 10,
    "detection_accuracy": "87%",
    "false_positive_rate": "12%"
  }
}
```

### Continuous Integration
- **Pre-commit**: Temel syntax ve format kontrolleri
- **Daily Tests**: Günlük otomatik test çalıştırma
- **Performance Regression**: Performans gerileme testleri
- **Security Scanning**: Güvenlik açığı taramaları

## Hata Ayıklama ve Troubleshooting

### Yaygın Test Hataları

1. **Import Error**: Modül yolu hataları
   ```bash
   export PYTHONPATH="${PYTHONPATH}:./simulators:./docs"
   ```

2. **Memory Error**: Büyük veri seti testlerinde
   ```python
   # Batch processing kullanın
   batch_size = 1000
   ```

3. **Timeout Error**: Uzun süren testler için
   ```python
   @timeout(300)  # 5 dakika timeout
   ```

### Test Environment Setup
```bash
# Gerekli bağımlılıklar
pip install unittest2 psutil memory_profiler

# Test veritabanı
mkdir -p test_data/
mkdir -p test_results/
```

## Gelecek Test Planları

### Yeni Test Senaryoları
- [ ] **Load Testing**: Yük testi senaryoları
- [ ] **Stress Testing**: Stres testi koşulları
- [ ] **Chaos Engineering**: Kaos mühendisliği testleri
- [ ] **A/B Testing**: Algoritma karşılaştırma testleri

### Test Otomasyonu
- [ ] **CI/CD Integration**: Jenkins/GitHub Actions
- [ ] **Automated Reporting**: Otomatik test raporlama
- [ ] **Performance Monitoring**: Sürekli performans izleme
- [ ] **Alert System**: Test başarısızlık uyarıları

---

*Son Güncelleme: November 2024*
*Test Framework: Python unittest + Custom Scenarios*