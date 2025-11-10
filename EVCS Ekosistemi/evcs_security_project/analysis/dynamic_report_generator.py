import pandas as pd
import json
import logging
from datetime import datetime

# Loglama ayarları
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - REPORT_GEN - %(levelname)s - %(message)s')
logger = logging.getLogger('REPORT_GEN')

# Dosya Yolları
ANALYSIS_CSV_FILE = 'logs/attack_flow_data.csv'
REPORT_OUTPUT_FILE = 'analysis/dynamic_report.md' 

def generate_report():
    """
    Analiz sonuçlarını okur ve yapılandırılmış bir rapor taslağı oluşturur.
    """
    try:
        # 1. Analiz Verisini Yükle (DataFrame)
        df = pd.read_csv(ANALYSIS_CSV_FILE)
    except FileNotFoundError:
        logger.error(f"HATA: '{ANALYSIS_CSV_FILE}' dosyası bulunamadı. Lütfen analizör betiğini çalıştırın.")
        return
    except Exception as e:
        logger.error(f"Veri yüklenirken hata: {e}")
        return

    if df.empty:
        logger.warning("Veri setinde analiz edilecek satır yok.")
        return

    # --- 2. Kritik Metrikleri Hesapla ---
    
    # Saldırı anını tespit eden ilk IDS logunun zaman damgasını bul
    anomaly_rows = df[df['is_anomaly_detected'] == 1]
    first_anomaly_time = pd.to_datetime(anomaly_rows['timestamp']).min()
    
    # Saldırı frame'lerinin (0x200) toplam sayısı
    total_attack_frames = df[df['is_attack_frame'] == 1].shape[0]
    
    # Saldırı öncesi ve sonrası frame sayıları (IDS başarısını göstermek için)
    normal_frame_rate = 0
    attack_frame_rate = 0
    
    if first_anomaly_time:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        before_attack_df = df[df['timestamp'] < first_anomaly_time]
        attack_window_df = df[df['timestamp'] >= first_anomaly_time]
        
        # Saniyedeki Frame Frekansı (Saldırı Anı)
        time_diff = (attack_window_df['timestamp'].max() - attack_window_df['timestamp'].min()).total_seconds()
        if time_diff > 0:
            attack_frame_rate = attack_window_df.shape[0] / time_diff
        
        # Normal Akış Frame Hızı (Basit hesaplama)
        normal_duration = (before_attack_df['timestamp'].max() - before_attack_df['timestamp'].min()).total_seconds()
        if normal_duration > 0:
            normal_frame_rate = before_attack_df.shape[0] / normal_duration
        
    else:
        # Anomali tespit edilemezse varsayılan değerler
        normal_frame_rate = df.shape[0] / df['timestamp'].dt.to_period('S').nunique()


    # --- 3. Rapor Metnini Oluştur ---
    
    report_content = f"# Koordine Edilmiş Talep Saldırısı Simülasyon Raporu\n\n"
    report_content += f"**Proje Grubu:** [Grup Adı]\n"
    report_content += f"**Rapor Tarihi:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
    report_content += "---"
    
    # A. Saldırı Tanımı ve Hedef (Güvenlik Farkındalığı)
    report_content += f"\n## 1. Anomali ve Tehdit Analizi\n"
    report_content += f"Simüle edilen anomali **'Koordine Edilmiş Talep Taraflı Saldırı'**'dır. Bu saldırıda, MitM zafiyeti kullanılarak {total_attack_frames} adet 'RemoteStartTransaction' komutu (OCPP) kısa sürede farklı CP'lere enjekte edilmiştir.\n"
    report_content += f"Bu durum, bölgesel **güç şebekesinde** ani yük artışı ve potansiyel blackout riski yaratmayı hedeflemektedir.\n"
    
    # B. Simülasyon Bulguları (Teknik Başarı)
    report_content += f"\n## 2. Simülasyon ve Nicel Bulgular\n"
    report_content += f"| Metrik | Değer |\n"
    report_content += f"| :--- | :--- |\n"
    report_content += f"| Toplam Simüle Edilen Frame Sayısı | {len(df)} |\n"
    report_content += f"| Enjekte Edilen Başlatma (0x200) Sayısı | {total_attack_frames} |\n"
    report_content += f"| Normal Akış Frame Hızı (Ortalama) | {normal_frame_rate:.2f} frame/sn |\n"
    report_content += f"| Saldırı Anı Frame Hızı (Yoğunluk) | **{attack_frame_rate:.2f} frame/sn** |\n"
    
    # C. Savunma ve IDS Başarısı (Yenilik/Ek Puanı) - Görseldeki Kısım
    report_content += f"\n## 3. Savunma Mekanizması ve IDS Başarısı\n"
    report_content += f"Saldırıyı tespit etmek amacıyla, CAN bus trafiği üzerinde çalışan basit bir **CAN-IDS** uygulanmıştır.\n"
    
    if first_anomaly_time:
        # (Visual aid from the user's uploaded image)
        report_content += f"* **Tespit Başarısı:** IDS, {first_anomaly_time.strftime('%H:%M:%S.%f')} anında, 0x200 ID frekansındaki ani artışı tespit etmiştir.\n"
        # [cite_end]
    else:
        report_content += f"* **Tespit Durumu:** Saldırı anomalisine dair log (CRITICAL) bulunamadı. (IDS eşiği veya aktivasyon kontrol edilmeli).\n"
    
    # (Visual aid from the user's uploaded image)
    report_content += f"* **Önerilen İyileştirme:** Saldırının merkezden gelmesini önlemek için OCPP kanalında **Mutual TLS** ve CSMS/Gateway seviyesinde komutlar için **Filtering (Whitelisting)** uygulanması temel savunma stratejisidir.\n"
    # [cite_end]
    
    # 4. Raporu Kaydet
    with open(REPORT_OUTPUT_FILE, 'w') as f:
        f.write(report_content)
    
    logger.info(f"Rapor taslağı başarıyla oluşturuldu: '{REPORT_OUTPUT_FILE}'")


if __name__ == "__main__":
    generate_report()