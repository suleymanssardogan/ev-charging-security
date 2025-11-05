# EV Şarj İstasyonu Log Anomalisi Tespit Sistemi

## 📋 Proje Hakkında

Bu proje, **IEC 61851 İletişim Protokolü** kapsamında EV şarj istasyonlarında karşılaşılan **"Loglarda Açık Metin Kimlik/Jeton (Credential) Sızıntısı"** anomalisini tespit etmek için geliştirilmiştir.

### 🎯 Ana Hedef
**EVSE, CSMS ve ilgili servislerin loglarında** kullanıcı kimlikleri (idTag, RFID UID), yetkilendirme jetonları (API key, session ID) veya temel kimlik bilgilerinin açık metin olarak tutulmasını tespit ederek **KVKK/GDPR uyumluluk** sağlamak.

### ⚡ Log Anomalisi Nedir?
Log anomalisi, sistem loglarında **normal davranış kalıplarından sapan** ve potansiyel güvenlik risklerine işaret eden olaylardır. Bizim odaklandığımız anomali:

**"Hassas verilerin maskelenmeden log kayıtlarında tutulması"**

## 🔍 Tespit Edilen Ana Anomali Türü

### 🚨 **CREDENTIAL_LEAK (Kimlik Bilgisi Sızıntısı)**
- **Pattern:** `auth token=([A-Za-z0-9]{8,})` (maskelenmemiş)
- **Risk:** Yetkisiz erişim, hesap ele geçirme
- **Standart:** ISO/IEC 27001 Madde A.12.4 ihlali
- **Mevzuat:** KVKK/GDPR gizlilik ihlali

## 📁 Proje Yapısı

```
📁 Proje Yapısı/
├── 📁 /simulators          → Şarj istasyonu ve araç simülatörleri
│   ├── evcs_log_simulator.py     → Test log'ları üretir
│   └── auto_log_processor.py     → Otomatik log işleyici
├── 📁 /docs                → Dokümantasyon ve literatür özetleri
│   ├── EV_Log_Anomalisi_Analiz_Raporu.pdf → Sabit akademik rapor
│   ├── LogAnomali.docx.pdf              → Kaynak doküman
│   ├── log_anomaly_detection_bibliography.md → Kapsamlı bibliografya
│   ├── evcs_attack_analyzer.py           → Log anomali pattern'leri tespit eder
│   ├── dynamic_report_generator.py       → Dinamik analiz raporları
│   ├── attack_analysis.json              → Detaylı anomali analizi
│   ├── evcs_analysis_results.json        → Analiz sonuçları
│   ├── evcs_system_detailed.log          → Sistem log dosyası
│   └── 📁 /makaleler        → Akademik makaleler ve araştırmalar
│       ├── LogEDL_Log_Anomaly_Detection_via_Evidential_Deep_Learning.md
│       ├── AI_Driven_EV_Charging_Cybersecurity_Platform.md
│       ├── Online_ML_Intrusion_Detection_EV_Charging.md
│       ├── Deep_Learning_Fusion_Network_Anomaly_Detection.md
│       ├── Knowledge_Graph_Log_Anomaly_Detection.md
│       └── System_Logs_Anomaly_Detection_Review.md
└── 📁 /tests               → Test senaryoları ve sonuçlar
    ├── test_log_simulator.py      → Simülatör birim testleri
    ├── test_anomaly_analyzer.py   → Analiz sistemi testleri
    ├── integration_tests.py       → Entegrasyon testleri
    └── README.md                  → Test dokümantasyonu
```

## 🚀 Nasıl Kullanır?

### 1. Test Log'u Üret
```bash
cd simulators/
python3 evcs_log_simulator.py
```
**Çıktı:** `evcs_system_detailed.log`

### 2. Log Anomalilerini Tespit Et
```bash
cd docs/
python3 evcs_attack_analyzer.py
```
**Çıktı:**
- Terminal'de anomali özeti
- `attack_analysis.json` (detaylı analiz)

### 3. Dinamik Analiz Raporu
```bash
cd docs/
python3 dynamic_report_generator.py
```
**Çıktı:** `Log_Anomali_Dinamik_Rapor.txt` (sadece gerçek veriler)

### 4. Test Senaryolarını Çalıştır
```bash
cd tests/
python3 test_log_simulator.py        # Simülatör testleri
python3 test_anomaly_analyzer.py     # Analiz testleri
python3 integration_tests.py         # Entegrasyon testleri
```

## 🔬 Diğer Tespit Edilen Log Anomali Pattern'leri

### 🔧 **Sistem Güvenliği Anomalileri:**
- **COMMAND_INJECTION** → `(rm\s+-rf|;\s*reboot)`
  - Sistem komutlarının log'a sızması
- **UNAUTHORIZED_ACCESS** → `unauthorized_admin_access`
  - Yetkisiz yönetici erişim denemeleri

### 💰 **İş Mantığı Anomalileri:**
- **PRICE_MANIPULATION** → `set_price.*price=(\d+)`
  - Anormal düşük şarj fiyatları (< 10TL/kWh)

### 🌐 **Ağ Güvenliği Anomalileri:**
- **DOS_ATTACK** → `connection_flood|rate_limit_exceeded`
  - Aşırı bağlantı istekleri (> 100 req/sec)

## 🏗️ Sistem Mimarisi

### 📊 **Log Anomali Tespit Süreci:**
1. **Log Üretimi** → Gerçekçi EV şarj istasyonu logları simüle edilir
2. **Pattern Analizi** → Regex tabanlı anomali pattern'leri taranır
3. **Risk Değerlendirmesi** → Ciddiyet seviyesi (HIGH/CRITICAL) belirlenir
4. **Raporlama** → Dinamik analiz sonuçları üretilir

### 🔍 **Anomali Tespit Algoritması:**
```python
# Örnek: Credential Leak Tespiti
token_pattern = r"auth token=([A-Za-z0-9]{8,})"
if re.search(token_pattern, log_line) and "*" not in log_line:
    return {
        "type": "CREDENTIAL_LEAK",
        "severity": "HIGH",
        "action": "Token'ı derhal iptal et ve logları temizle"
    }
```

## 📊 Örnek Çıktı

```
🔍 EVCS Log Anomali Analizi Tamamlandı
📄 Analiz edilen log satırı: 500
⚠️  Tespit edilen anomali: 39
🎯 Log anomali seviyesi: CRITICAL

🚨 TESPİT EDİLEN LOG ANOMALİLERİ:
   CREDENTIAL_LEAK (Satır 45) - HIGH
   → Pattern: Maskelenmemiş token tespit edildi

   COMMAND_INJECTION (Satır 128) - CRITICAL
   → Pattern: Şüpheli komut kalıbı bulundu
```

## 📊 Kapsamlı Rapor Sistemi

### 📋 **Akademik Rapor** (Sabit İçerik)
`EV_Log_Anomalisi_Analiz_Raporu.pdf` - 35KB
- ✅ **SWOT Analizi:** Log anomali sisteminin güçlü/zayıf yönleri
- ✅ **Test Metodolojisi:** Regex pattern matching yaklaşımı
- ✅ **Veri Analizi:** Log format analizi ve istatistikler
- ✅ **Güvenlik Önerileri:** Maskeleme, SIEM entegrasyon, TLS 1.3
- ✅ **Matematik Formülleri:** LADR hesaplama, algoritma karmaşıklığı

### 📈 **Dinamik Analiz Raporu** (Gerçek Veriler)
`Log_Anomali_Dinamik_Rapor.txt` - 1KB
- 🔄 **Gerçek zamanlı anomali sayıları** (39/500 örneğinde)
- 🔄 **Risk seviyesi değerlendirmesi** (CRITICAL/HIGH/MEDIUM)
- 🔄 **Pattern türü dağılımı** (CREDENTIAL_LEAK %20.5, COMMAND_INJECTION %23.1)
- 🔄 **Performance metrikleri** (işlem hızı, bellek kullanımı)

## 🎓 Akademik Katkılar

### 📚 **Bilimsel Yaklaşım:**
- **Anomali Tespit Oranı (LADR):** (39/500) × 100 = 7.80%
- **Optimal Clustering:** k = √(39/2) ≈ 4 cluster
- **Algoritma Karmaşıklığı:** O(n × m × k) = 250,000 operasyon
- **95% Güven Aralığı:** ±2.1% anomali tespit hassasiyeti

### 🏛️ **Mevzuat Uyumluluğu:**
- **ISO/IEC 27001:** Madde A.12.4 log maskeleme gerekliliği
- **KVKK/GDPR:** Kişisel veri koruma uyumluluğu
- **OWASP:** Logging Cheat Sheet standartları
- **IEC 61851:** EV şarj protokol güvenliği

## 💡 Proje Kullanımı

### 🚀 **Hızlı Başlangıç** (Tek Komut):
```bash
cd simulators/
python3 auto_log_processor.py
```

### 📝 **Manuel Adımlar:**
1. **Log üret:** `cd simulators/ && python3 evcs_log_simulator.py`
2. **Anomali tespit et:** `cd docs/ && python3 evcs_attack_analyzer.py`
3. **Dinamik rapor:** `cd docs/ && python3 dynamic_report_generator.py`
4. **Test çalıştır:** `cd tests/ && python3 integration_tests.py`

### 📁 **Kendi Log Dosyası ile:**
1. Log dosyanı `evcs_system_detailed.log` olarak kaydet
2. Anomali analizini çalıştır
3. Sonuçları akademik rapor ile karşılaştır

**Gereksinim:** `pip3 install reportlab`

---

## 🎯 Proje Özeti

Bu sistem, **EV şarj istasyonu log anomalisi** tespitinde **akademik standartlarda** çözüm sunar. Özellikle **kimlik bilgisi sızıntısı** odaklı yaklaşımıyla **KVKK/GDPR uyumluluğu** destekler ve **gerçek zamanlı anomali tespiti** sağlar.