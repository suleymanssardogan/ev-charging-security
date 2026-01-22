# BSG-WEB EV Charging Security System

Bu proje, Elektrikli Araç (EV) şarj istasyonları için geliştirilmiş bir güvenlik ve anomali tespit sistemidir. React tabanlı bir frontend ve Python/FastAPI tabanlı bir backend'den oluşur.

## Gereksinimler

Projenin çalıştırılabilmesi için bilgisayarınızda aşağıdakilerin kurulu olması gerekmektedir:

- [Node.js](https://nodejs.org/) (Frontend için)
- [Python 3.8+](https://www.python.org/) (Backend için)

## Kurulum ve Çalıştırma

Projeyi çalıştırmak için iki ayrı terminal penceresi kullanmanız gerekmektedir: biri Backend (Sunucu), diğeri Frontend (Arayüz) için.

### 1. Backend (Sunucu) Kurulumu

Backend, makine öğrenmesi modellerini barındırır ve analiz sonuçlarını frontend'e iletir.

1.  Proje ana dizinindeyken `bsg-web/backend` klasörü yerine, ana dizindeki scriptleri kullanmak için terminali **proje ana dizininde** tutun. Ancak servis `bsg-web/backend` altındadır.
2.  Gerekli Python kütüphanelerini yükleyin:

    ```bash
    pip install fastapi uvicorn pandas numpy joblib scikit-learn
    ```

3.  Backend sunucusunu başlatın:

    ```bash
    # Proje ana dizininden:
    python bsg-web/backend/server.py
    ```
    
    *Alternatif olarak:* `bsg-web/backend` klasörüne gidip `python server.py` komutunu da çalıştırabilirsiniz.
    *Sunucu `http://0.0.0.0:8000` adresinde çalışmaya başlayacaktır.*

### 2. Frontend (Kullanıcı Arayüzü) Kurulumu

Frontend, kullanıcıların sistemi izleyebileceği web arayüzüdür.

1.  Yeni bir terminal açın.
2.  `bsg-web` klasörüne gidin:

    ```bash
    cd bsg-web
    ```

3.  Gerekli paketleri yükleyin:

    ```bash
    npm install
    ```

4.  Uygulamayı başlatın:

    ```bash
    npm run dev
    ```

5.  Terminalde görünen yerel ağ adresine (genellikle `http://localhost:5173`) tarayıcınızdan gidin.

## Proje Yapısı

- **Frontend (`/bsg-web`)**: React ve Vite ile geliştirilmiş modern arayüz.
- **Backend (`/bsg-web/backend`)**: FastAPI ile geliştirilmiş API sunucusu.
- **Modeller**: Anomali tespiti için eğitilmiş makine öğrenmesi modelleri (`.pkl` dosyaları).

## Notlar

- Backend çalışmadan Frontend verileri görüntüleyemez. Lütfen önce Backend'i başlattığınızdan emin olun.
- Frontend portu `5173`, Backend CORS ayarlarında izinli olarak tanımlanmıştır. Farklı bir port kullanmanız durumunda bağlantı hatası alabilirsiniz.
