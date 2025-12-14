# 🛡️ EV Charging Security - CAN Bus Simulation & IDS Test Suite

Merhaba Ekip,

Bu dokümantasyon, **Elektrikli Araç (EV) Şarj Güvenliği** projesi kapsamında geliştirdiğimiz **CAN Bus Saldırı ve Tespit Simülasyonu** modülünün kullanımı için hazırlanmıştır. 

Amacımız, Linux tabanlı simülasyon ortamımızda **CAN Bus** protokolünün zayıflıklarını (Weakness) pratik olarak göstermek ve geliştirdiğimiz **IDS (Saldırı Tespit Sistemi)** algoritmalarının etkinliğini test etmektir.

---

## 📋 İçindekiler
- [Proje Mimarisi](#-proje-mimarisi)
- [Linux Ortamı Kurulumu (Önemli!)](#-linux-ortamı-kurulumu-önemli)
- [Test Senaryoları ve Çalıştırma](#-test-senaryoları-ve-çalıştırma)
- [Beklenen Sonuçlar](#-beklenen-sonuçlar)
- [Sorun Giderme](#-sorun-giderme)

---

## 📂 Proje Mimarisi

Aşağıdaki bileşenler, sanal bir CAN ağı üzerinde hem meşru trafiği hem de saldırı trafiğini simüle eder.

| Dosya | Rol | Açıklama |
|-------|-----|----------|
| **`can_bus_factory.py`** | 🏭 Altyapı | İşletim sistemini tanır. Linux ortamında `socketcan` ve `vcan0` arayüzünü, macOS'ta sanal veriyolunu bağlar. |
| **`can_ids_monitor.py`** | 🛡️ Savunma (Blue Team) | **IDS**. Hattı sürekli dinler. Belirli bir zaman penceresinde (Window) aşırı mesaj gönderimi (Frequency Analysis) yaparak spoofing saldırılarını tespit eder. |
| **`can_ecu_legit.py`** | ✅ Normal Trafik | **Meşru ECU**. Normal bir şarj başlatma komutunu (ID: `0x200`) standart aralıklarla gönderir. |
| **`can_attacker.py`** | ⚔️ Saldırı (Red Team) | **Attacker**. OBD-II portu üzerinden sızmış bir saldırganı simüle eder. Yetkili ECU'nun ID'sini taklit ederek (Spoofing) sisteme sahte komut enjekte eder. |
| **`event_logger.py`** | 📝 Kayıt | Tüm aktiviteleri JSON formatında loglar. |

---

## 🐧 Linux Ortamı Kurulumu (Önemli!)

Simülasyon sunucularında veya yerel Linux makinelerinizde **Virtual CAN (vcan)** arayüzünü ayağa kaldırmanız gerekmektedir. Bu adımlar **root** veya **sudo** yetkisi gerektirir.

### 1. Sistem Bağımlılıklarını Yükleyin
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv can-utils
```

### 2. Sanal CAN Arayüzünü (vcan0) Oluşturun
Bu komutlar kernel modülünü yükler ve sanal ağ arayüzünü oluşturur:
```bash
# vcan modülünü yükle
sudo modprobe vcan

# vcan0 arayüzünü ekle
sudo ip link add dev vcan0 type vcan

# Arayüzü aktif et
sudo ip link set up vcan0
```

*Not: Arayüzün çalıştığını `ip link show vcan0` komutu ile doğrulayabilirsiniz.*

### 3. Python Sanal Ortamını Hazırlayın
Proje dizininde (repo root):
```bash
# Virtual environment oluştur
python3 -m venv .venv

# Aktif et
source .venv/bin/activate

# Gerekli kütüphaneleri yükle
pip install -r tests/requirements.txt
```

---

## 🚀 Test Senaryoları ve Çalıştırma

Testleri gerçekleştirmek için 3 ayrı terminal penceresi (veya `tmux`/`screen` oturumu) açmanız gerekmektedir.

### Senaryo: Replay / Spoofing Saldırısı Tespiti

#### Terminal 1: IDS (Gözcü)
Önce savunma sistemini başlatın. Şu an ağ sessizdir.
```bash
source .venv/bin/activate
python3 tests/can_ids_monitor.py
# Çıktı: [IDS] Monitoring CAN traffic...
```

#### Terminal 2: Legitimate ECU (Normal Kullanıcı)
Normal bir şarj döngüsü başlatalım.
```bash
source .venv/bin/activate
python3 tests/can_ecu_legit.py
# Çıktı: [ECU] Sent CAN ID 0x200
```
👀 **Gözlem:** Terminal 1'de (IDS) mesajın loglandığını ancak herhangi bir alarm **verilmediğini** görmelisiniz.

#### Terminal 3: Attacker (Saldırgan)
Şimdi aynı ID'yi kullanarak sisteme arka arkaya mesaj enjekte edelim.
```bash
source .venv/bin/activate
python3 tests/can_attacker.py
# Çıktı: [ATTACKER] Spoofing CAN ID 0x200...
```
👀 **Gözlem:** Terminal 1'de (IDS) artık **Alarm** çaldığını görmelisiniz!

---

## 📊 Beklenen Sonuçlar

Başarılı bir testte IDS terminalinde şuna benzer bir çıktı almalısınız:

```text
[IDS] Received ID=0x200 DATA=bytearray(b'\x01')
[IDS] Received ID=0x200 DATA=bytearray(b'\x01')
🚨 [IDS ALERT] POSSIBLE CAN ID SPOOFING DETECTED!
🚨 ID 0x200 sent 2 times in 2.0s
```

Bu, kural tabanlı motorumuzun **zaman penceresi (time window)** ihlalini başarıyla yakaladığını gösterir.

---

## 🔧 Sorun Giderme

- **Hata:** `OSError: [Errno 19] No such device`
  - **Çözüm:** `vcan0` arayüzü oluşturulmamış. "Linux Ortamı Kurulumu" başlığındaki `ip link` komutlarını tekrar çalıştırın.
  
- **Hata:** `ModuleNotFoundError`
  - **Çözüm:** `.venv` aktif edilmemiş olabilir. `source .venv/bin/activate` komutunu kullandığınızdan emin olun.

---

İyi çalışmalar,
**EV Security Team**
