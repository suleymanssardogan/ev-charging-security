Bu proje, "OCPP Oturum Bilgilerinin Ele Geçirilmesi" raporunda belirtilen güvenlik zafiyetlerini simüle eder.
[cite_start]**İlgili Tehditler:** MITM Saldırıları [cite: 5][cite_start], Kimlik Hırsızlığı [cite: 36][cite_start], Şifrelenmemiş Veri İletimi[cite: 23].

## Kurulum
1. Python yüklü olduğundan emin olun.
2. Gereksinimleri yükleyin:
   `pip install -r requirements.txt`

## Simülasyon Adımları (Sırasıyla 3 farklı terminalde çalıştırın)

### Adım 1: Merkezi Sistemi (CSMS) Başlat
Bu, meşru sunucudur. 9000 portunu dinler.
`python csms.py`

### Adım 2: Saldırganı (MITM) Başlat
Bu script, 9001 portunu dinler ve trafiği 9000'e (CSMS) yönlendirirken **veriyi değiştirir**.
`python mitm_modify_ws.py`

### Adım 3: Şarj İşlemini Tetikle (Kurban)
Bu script, donanım seviyesinde kart okumayı simüle eder ve şarj istasyonunun 9001 (Saldırgan) portuna bağlanmasını sağlar.
`python can_listener.py`

## Beklenen Sonuç (Anomali Kanıtı)
1. **CP (İstasyon):** `USER_REAL_CARD_123` ile işlem başlatmaya çalışır.
2. **MITM (Saldırgan):** Bu ID'yi yakalar ve `HACKER_TOKEN_999` olarak değiştirir.
3. **CSMS (Merkez):** Ekranda `USER_REAL_CARD_123` yerine `HACKER_TOKEN_999` ile işlem başladığını görür.
   
[cite_start]Bu durum, raporda belirtilen "Oturum tokenlarının çalınarak şarj işlemlerinin taklit edilmesi"  riskini doğrular.