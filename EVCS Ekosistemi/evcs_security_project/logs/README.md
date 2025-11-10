# LOGS KLASÖRÜ - Veri Kaynağı ve Açıklamalar

Bu klasör, EVCS Güvenlik Projesi'nin simülasyon ve analiz aşamalarındaki tüm ham ve işlenmiş çıktıları içerir.

## 1. Ham Log Dosyaları

| Dosya Adı | Oluşturan Kaynaklar | Amaç | İçerik Örneği |
| :--- | :--- | :--- | :--- |
| **`evcs_system_detailed.log`** | Tüm simülatörler ve saldırı/savunma betikleri. | **Temel Veri Kaynağı:** Sistemdeki tüm OCPP (CSMS/CP) ve CAN (0x200, 0x300) olaylarını kronolojik sırayla kaydeder. **Saldırı anındaki CAN frame yoğunluğunun kanıtını içerir.** | `[2025-11-09 23:21:04,321] - CP_SIM - INFO - OCPP -> CAN (0x200) çevrildi...` |
| **`analyzer_results.log`** | `log_anomaly_analyzer.py` | Analizörün kendi iç çalışma sürecini, log okuma başarı durumunu, tespit edilen ilk anomali zaman damgasını ve nicel karşılaştırmalarını kaydeder. | `[2025-11-09 23:22:10,000] - ANALYZER - CRITICAL - İlk Anomali Tespit Zamanı: ...` |

## 2. İşlenmiş Veri Setleri (Veri Analizi Çıktıları)

Bu dosyalar, `log_anomaly_analyzer.py` betiği çalıştırıldığında oluşturulur.

| Dosya Adı | Kaynak Log | Format | Açıklama |
| :--- | :--- | :--- | :--- |
| **`attack_flow_data.csv`** | `evcs_system_detailed.log` | CSV | Saldırı anını da içeren, **yapılandırılmış CAN frame verisi setidir.** Her satırda Timestamp, CAN ID, Frame Tipi, Kaynak (Entity) ve **is\_attack\_frame (1/0)** gibi analiz sütunları bulunur. |
| **`normal_flow_data.csv`** | `evcs_system_detailed.log` (Veya ayrı bir normal akış simülasyonu) | CSV | Yalnızca normal (saldırısız) akışa ait CAN frame verilerini içerir. Bu, **saldırı frekansını kıyaslamak** için bir referans noktası sağlar. |

## 3. Log Kaynağı (Entity) Açıklamaları

`evcs_system_detailed.log` dosyasındaki her satırda bulunan `[ENTITY]` etiketi, verinin hangi sistem bileşeninden geldiğini belirtir:

| ENTITY Etiketi | Kaynak Kod | Rolü |
| :--- | :--- | :--- |
| **`CSMS`** | `csms_simulator.py` | Merkezi Yönetim Sistemi (WebSocket sunucusu). |
| **`CP_SIM`** | `cp_simulator.py` | Şarj İstasyonu (OCPP istemcisi); OCPP'yi CAN'e çeviren **'Köprü'** görevini simüle eder. |
| **`CAN_CHGR`** | `can_charger_module.py` | Fiziksel Şarj/Röle Modülü; 0x200'ü dinler, 0x300 (MeterValues) ile yanıt verir. |
| **`ATTACK_SIM`** | `coordinated_demand_mitm.py` | Saldırganın kodu; yüzlerce 0x200 (Başlatma) frame'ini **ani ve koordine** şekilde enjekte eder. |
| **`CAN-IDS`** | `can_ids_detector.py` | Savunma mekanizması; **0x200 frekansındaki anomalileri tespit eder.** |

## 4. Kritik CAN ID'leri

| CAN ID | Anlamı | Kaynak (Sender) | Etkisi |
| :--- | :--- | :--- | :--- |
| **0x200** | RemoteStart/Başlatma Komutu | CP Agent veya Saldırgan | Saldırı anında frekansı aniden yükselir. |
| **0x300** | MeterValues/Ölçüm Verisi | CAN Charger Modülü | 0x200'e yanıt olarak gönderilir; saldırı anında frekansı dolaylı olarak yükselir. |