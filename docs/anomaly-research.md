# Anomaly Research: Fiyat ve Fatura Manipülasyonu

## K1: Monotonicity Violation
**Tanım:** Sayaç değerlerinin zamanla artması gerekirken azalması.
**Tespit:** `E[t+1] < E[t] - ε`
**Etki:** Negatif tüketim veya fatura manipülasyonu.

## K2: Süre–Enerji Uyumsuzluğu
**Tanım:** Transfer edilen enerjinin geçen süreye ve maksimum güce oranla fiziksel olarak imkansız olması.
**Tespit:** `ΔkWh > Pmax * Δt`
**Etki:** Hızlı şarj gösterip az ödeme veya tam tersi.

## K3: Zaman Tutarlılığı
**Tanım:** Mesajların zaman damgalarının sırasız veya gelecekte olması.
**Tespit:** `Timestamp[t+1] < Timestamp[t]`
**Etki:** Tarife manipülasyonu (Pahalı saatten ucuz saate kaydırma).

## K4: CS Spoofing
**Tanım:** Aynı istasyon kimliği ile birden fazla bağlantı.
**Tespit:** Aynı `stationId` için aktif socket sayısı > 1.

## K5: CV Storm
**Tanım:** Kritik konfigürasyon değişkenlerinin (Critical Variables) sık sık değiştirilmesi.
**Tespit:** Belirli bir sürede >N değişiklik.

## K6: mTLS İhlali
**Tanım:** Güvenli bağlantı gereksinimlerinin karşılanmaması.
**Tespit:** TLS handshake hatası veya geçersiz sertifika.
