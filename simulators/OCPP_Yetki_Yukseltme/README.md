OCPP Yetki Yükseltme (Privilege Escalation) SimülasyonuBu proje, OCPP (Open Charge Point Protocol) tabanlı elektrikli araç şarj istasyonlarına (EVSE) yönelik bir "Yerel Yetki Listesi Manipülasyonu" (Local Authorization List Manipulation) siber saldırısını simüle eder.Bu senaryo, docs/ klasöründe bulunan OCPP\_Yetki\_Yükseltme.docx ve Uygulama Senaryosu (1).pdf dosyalarında tanımlanan tehdit modeline dayanmaktadır.Saldırı, Ağ (OCPP) katmanındaki bir mesajın mitmproxy kullanılarak değiştirilmesini, Uygulama (İstasyon Yazılımı) katmanındaki hafızanın manipüle edilmesini ve bunun sonucunda Donanım (CAN-bus) katmanında yetkisiz bir fiziksel eylemin (şarj başlatma) tetiklenmesini gösterir.Simüle Edilen Saldırı AkışıSunucu (csms.py): Geçerli RFID kartlarının bir listesini (SendLocalList) istasyona gönderir (Örn: VALID\_RFID\_123).Saldırgan (mitm\_modify\_ws.py): Bu mesajı yolda yakalar ve listenin içine gizlice sahte bir saldırgan kartı (ATTACKER\_TAG\_999) ekler.İstemci (cp.py): Manipüle edilmiş (sahte) listeyi alır ve ATTACKER\_TAG\_999'u geçerli bir kart zannederek hafızasına kaydeder.Simülasyon: İstemci, 10 saniye sonra bu sahte kartın okutulduğunu simüle eder.Sonuç (Yazılım): İstemci, sahte kartı hafızasında "Accepted" (Kabul Edildi) olarak bulur ve "SALDIRI BAŞARILI!" logunu basar.Sonuç (Donanım): İstemci, bu sahte yetkiye dayanarak vcan0 (CAN-bus) hattına 0x200 (Şarjı Başlat) komutu gönderir.Kanıt (can\_listener.py): Dinleyici, bu yetkisiz 0x200 komutunu yakalar.Başarılı Saldırı Kanıtı (Ekran Görüntüleri)Simülasyon başarıyla tamamlandığında 4 terminaldeki çıktılar (Görüntüler docs/images klasöründedir):1. Sunucu (CSMS)2. Saldırgan (MITM)3. Donanım (CAN Listener)4. İstemci (CP)(Not: Ekran görüntüsü dosya adları sizde farklıysa, README.md içindeki bu yolları güncelleyin.)Proje BileşenleriProje 4 ana Python script'inden oluşur (simulation\_code/ klasöründedir):csms.py (Sunucu): ws://0.0.0.0:9000 portunda dinleyen sahte bir Merkezi Yönetim Sistemidir.cp.py (İstemci / Kurban): Sahte Şarj İstasyonudur. mitmproxy üzerinden sunucuya bağlanır.mitm\_modify\_ws.py (Saldırgan): mitmproxy eklentisidir. SendLocalList mesajını arar ve ATTACKER\_TAG\_999 ID'sini listeye enjekte eder.can\_listener.py (Donanım Dinleyici): vcan0 sanal CAN-bus arayüzünü dinler ve 0x200 mesajını yakalar.Kurulum (Kali Linux / Debian)Gerekli Sistem Paketlerini Kur:Bashsudo apt update

sudo apt install python3 python3-venv python3-pip can-utils mitmproxy -y

Sanal CAN Arayüzünü Oluştur (Kritik Adım):Bashsudo modprobe vcan

sudo ip link add dev vcan0 type vcan

sudo ip link set up vcan0

Projeyi Klonla ve Sanal Ortamı Kur:Bashgit clone https://github.com/suleymanssardogan/ev-charging-security.git

cd ev-charging-security

python3 -m venv .venv

source .venv/bin/activate

Python Kütüphanelerini Kur:Bashpip install -r requirements.txt

Simülasyonun Çalıştırılması (4 Terminal)Simülasyonun çalışması için 4 ayrı terminale ihtiyacın var.Terminal 1: Sunucu (CSMS)Bashsource .venv/bin/activate

python simulation\_code/csms.py

(Beklenen Çıktı: \[CSMS] Starting on ws://0.0.0.0:9000/)Terminal 2: Donanım Dinleyici (CAN)Bashsource .venv/bin/activate

python simulation\_code/can\_listener.py

(Beklenen Çıktı: \[CAN Listener] vcan0 üzerinde dinleme başladı...)Terminal 3: Saldırgan (MITM)Bashsource .venv/bin/activate

mitmproxy -s simulation\_code/mitm\_modify\_ws.py --set block\_global=false

(Beklenen Çıktı: Proxy server listening at http://\*:8080)Terminal 4: İstemci (CP Client)Bu terminal, İstemciyi başlatır ve trafiğini Saldırgana yönlendirir.Bashsource .venv/bin/activate

\# Proxy ayarını bu terminal için yap

export http\_proxy=http://127.0.0.1:8080

export https\_proxy=http://127.0.0.1:8080

\# Script'i çalıştır

python simulation\_code/cp.py

(Beklenen Çıktı: \[CP] Proxy üzerinden bağlanılıyor: http://127.0.0.1:8080)Son Adım: Saldırıyı TetiklemeTerminal 4'ü çalıştırdığın anda, Terminal 3 (MITM) ekranında >> işaretiyle başlayan bir satır belirecek.Hemen Terminal 3 (MITM)'e tıkla ve klavyeden a tuşuna bir kez bas (Akışa izin ver).

