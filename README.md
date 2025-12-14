# OCPP Anomaly Detection & Billing Simulation ⚡🔍

**Elektrikli Araç Şarj (OCPP 1.6J/2.0.1) Kurulumlarında Fiyat ve Faturalandırma Manipülasyonlarını Tespit Etmek İçin Agent Tabanlı Simülasyon Ortamı.**

Bu proje, monotoniklik ihlalleri, enerji-süre uyuşmazlıkları ve tarife manipülasyonları gibi potansiyel dolandırıcılık senaryolarını göstermek ve tespit etmek için eksiksiz bir EV şarj ekosistemini (Şarj İstasyonları, Merkezi Sistem, Faturalandırma vb.) simüle eder.

## 🚀 Özellikler

*   **Mikroservis Mimarisi:** CSMS, Şarj İstasyonu, Proxy, Faturalandırma, Tespit ve Web Paneli için ayrı servislere sahip modüler tasarım.
*   **OCPP Desteği:** OCPP JSON mesajlarını (StartTransaction, MeterValues, StopTransaction) simüle eder.
*   **Gerçek Zamanlı Anomali Tespiti:** Canlı veri akışlarında kuralları (örn. K1: Monotoniklik) uygulayarak alarmlar üretir.
*   **Faturalandırma Motoru:** Esnek tarifelere dayalı olarak oturum maliyetlerini hesaplar ve faturalar oluşturur.
*   **Gelişmiş Dashboard (v2):** Tüm simülasyonu, metrikleri ve analizleri tek bir ekranda birleştiren modern arayüz.
    *   **Canlı Grafikler:** Enerji tüketimi ve alarm yoğunluk grafikleri.
    *   **Detay Paneli (Drawer):** Herhangi bir işleme tıklayarak kanıt (evidence) ve JSON verilerini inceleme.

## 🏗️ Mimari

Sistem, aşağıdaki Dockerize edilmiş servislerden oluşur:

| Servis | Yol | Açıklama | Erişim |
| :--- | :--- | :--- | :--- |
| **CSMS** | `/services/csms` | Merkezi Sistem (WebSocket Sunucusu). CP bağlantılarını yönetir. | `ws://localhost:9000` |
| **Proxy** | `/services/proxy` | WebSocket Proxy. Trafiği yakalar ve manipüle edebilir. | `ws://localhost:9100` |
| **CP** | `/services/cp` | Şarj İstasyonu Simülatörü. Kullanım verisi üretir. | `http://localhost:9400` |
| **Billing** | `/services/billing` | Maliyetleri hesaplar ve faturaları saklar. | `http://localhost:9200` |
| **Detect** | `/services/detect` | Olayları anomaliler için analiz eder (K1-K6 Kuralları). | `http://localhost:9300` |
| **Web** | `/services/web` | Ana Kullanıcı Arayüzü (Next.js/React). | `http://localhost:3000` |

## 🛠️ Ön Gereksinimler

*   Makinenizde **Docker** ve **Docker Compose** kurulu olmalıdır.
*   *Her şey konteynerlerde çalıştığı için yerel Node.js veya Python kurulumuna gerek yoktur.*

## 🏁 Başlarken

1.  **Depoyu klonlayın:**
    ```bash
    git clone <repo-url>
    cd simulation-ocpp-billing-anomaly
    ```

2.  **Ortamı başlatın:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Panele Erişin:**
    Tarayıcınızı açın ve şu adrese gidin:
    👉 **[http://localhost:3000](http://localhost:3000)**

## 🧪 Kullanım & Arayüz (UI v2)

Yeni tek sayfa tasarımı ile tüm kontrol elinizin altında:

### 1. Simülasyon Kontrolü (Top Bar)
Ekranın en üstündeki kontrol çubuğundan senaryo seçip (örn. `S1: Monotonicity Violation`) **Run Simulation** butonuna basarak süreci başlatın.

### 2. Canlı İzleme (Charts & KPI)
Simülasyon başladığında:
*   **KPI Strip:** Toplam Alacak, Enerji ve Aktif Alarm sayıları güncellenir.
*   **Grafikler:** Enerji akışı (kWh) ve oluşan alarmlar zaman çizelgesi üzerinde belirir.

### 3. Detaylı Analiz (Master Grid & Drawer)
Alt kısımdaki tablo üç sekmeye (Sessions, Invoices, Alerts) ayrılmıştır.
*   Herhangi bir satıra tıkladığınızda sağdan **Detay Paneli (Drawer)** açılır.
*   Bu panelde olaya ait ham JSON verisi, kanıtlar (evidence) ve teknik detaylar yer alır.

### Mevcut Senaryolar

*   **S0: Normal Oturum (Baz)**
    *   Standart bir şarj oturumu. Sayaç değerleri doğrusal artar.
    *   **Sonuç:** Fatura kesilir ✅, Alarm Yok 🟢.

*   **S1: Monotoniklik İhlali (K1)**
    *   Sayaç değerleri aniden düşer (örn. 300 -> 250).
    *   **Sonuç:** Tespit Motoru **YÜKSEK** seviyeli alarm üretir 🚨.

## 🚨 Anomali Tespit Kuralları

*   **K1 - Monotoniklik:** `MeterValue` (n) >= `MeterValue` (n-1) kuralını denetler. Düşüş varsa manipülasyon olarak işaretler.
*   *(Geliştiriliyor)* **K2 - Enerji/Zaman:** Fiziksel sınır (kW) kontrolü.
*   *(Geliştiriliyor)* **K3 - Tarife Kaydırma:** Zaman damgası manipülasyonu tespiti.

## 📂 Proje Yapısı

```
.
├── docker-compose.yml       # Orkestrasyon
├── services/
│   ├── web/                 # Dashboard (Next.js/React - UI v2)
│   │   ├── src/pages/       # Single Page Layout
│   │   ├── src/components/  # Widgets, Charts, Drawers
│   ├── csms/                # Merkezi Sistem
│   ├── cp/                  # Şarj Simülatörü
│   ├── detect/              # Tespit Motoru
│   └── billing/             # Fatura Motoru
└── shared/                  # Ortak Şemalar
```
