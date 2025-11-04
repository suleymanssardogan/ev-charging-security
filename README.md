# ⚡ EV-Charging-Security  
### Anomaly Detection and Security Analysis for Electric Vehicle Charging Systems  

---

## 🧭 Proje Özeti  
Bu çalışma, **elektrikli araç şarj istasyonlarında (EVSE)** kullanılan iletişim protokolleri ve güvenlik standartlarının analiz edilerek **anomali tespiti ve güvenlik zafiyetlerinin belirlenmesini** amaçlamaktadır.  
Araştırma süreci, uluslararası standartlar (OCPP, ISO/IEC 15118, IEC 61851) ve güvenlik çerçeveleri (ISO/IEC 27001, NIST SP 800-53, GDPR) üzerine odaklanmıştır.

Proje çıktıları; akademik makalelerin analiziyle oluşturulan **anomali tespit tablosu** ve **SWOT analizi** sonuçlarını içermektedir.

---

## 🎯 Amaç  
Elektrikli araç altyapısı büyüdükçe, şarj istasyonları potansiyel siber saldırı hedefleri haline gelmektedir.  
Bu nedenle proje, aşağıdaki hedefleri gerçekleştirmek üzere tasarlandı:

- 🔍 EVSE iletişim protokollerindeki güvenlik açıklarını analiz etmek,  
- ⚙️ Mevcut güvenlik standartlarına göre zafiyetleri sınıflandırmak,  
- 🧠 Anomali tespitine yönelik makine öğrenimi yaklaşımlarını değerlendirmek,  
- 📊 Elde edilen bulguları SWOT analiziyle stratejik olarak yorumlamak.

---

## 🧩 Kullanılan Teknolojiler ve Kaynaklar  

| Araç / Kaynak | Açıklama |
|----------------|----------|
| 🧠 **ResearchRabbit** | Akademik makaleleri keşfetmek ve ilişkisel bağlantılarını analiz etmek için kullanıldı. |
| 🤖 **Google NotebookLM** | İngilizce makaleler yüklenerek Türkçe tablo ve SWOT analizi üretildi. |
---

## 📚 İncelenen Standartlar ve Protokoller  
- 🔌 **OCPP (Open Charge Point Protocol)**  
- ⚡ **ISO/IEC 15118**  
- ⚙️ **IEC 61851**  
- 🔒 **ISO/IEC 27001**  
- 🧱 **NIST SP 800-53**  
- 🧾 **GDPR (General Data Protection Regulation)**  
- 🧠 **EVSE / IoT Sistem Güvenliği İlkeleri**

---

## 📊 1️⃣ Anomali Teşhis Tablosu  
| Protokol / Standart | Tespit Edilen Anomali veya Güvenlik Açığı | Kullanılan Tespit Yöntemi | Tespit Edilen Sinyal / Veri | Önerilen Çözüm / Savunma | Kaynak (Yıl, Yazar) |
|----------------------|--------------------------------------------|-----------------------------|-----------------------------|---------------------------|----------------------|
| OCPP (Genel) | Man-in-the-Middle (MitM), Replay attacks | OCPP trafik ayrıştırıcısı (Wireshark entegreli CheckOCPP) | OCPP versiyonları (1.6, 2.0, 2.0.1) | Gerçek zamanlı paket işaretleme | Boussaha, S. et al. (2025) |
| OCPP (Genel) | Message tampering, DoS, yetkilendirme kusurları | Aktif güvenlik analizi (paket yükü değiştirme) | OCPP yükleri, şarj cihazı ID’leri | Paket yükü değiştirme denetimi | S. R. Team (2023) |
| EV Şarjı (T6/T7) | Enerji tüketiminde sapmalar (dolandırıcılık, arıza) | ML tabanlı CADS4CS (CatBoost, XGBoost) | Şarj seansı enerji verileri | ML modellerinin yeniden eğitimi | Cumplido, J. et al. (2022) |
| E-Mobilite | Şebeke anomalileri | Regresyon modelleri (Decision Tree, Gradient Boosting) | Güç tüketimi verileri | IDS sistemleriyle anomali tespiti | (Yazar belirtilmemiş) |
| EV/IoT | Zayıf kimlik doğrulama, bozuk şifreleme | Statik ve dinamik analiz | CWE-327, CWE-295 açıkları | OWASP/CWE Top 10 önlemleri | Muhammad, Z. et al. (2025) |
| IoT/ASR | Üyelik çıkarımı (MIA) | Gölge sistem + TF-IDF denetçi | Semantik benzerlik skorları | Etiketlenmemiş üyelik tespiti | Miao, Y. et al. (2022) |
| GDPR/IoT | Veri politikası tutarsızlıkları | IoTPrivComp (BERT + MNB) | Konum, sağlık, ödeme verileri | Veri akış tutarlılık analizi | Ahmad, J. et al. (2022) |
| IoT Sistemleri | ROP (Kod Yeniden Kullanım) saldırıları | Fonksiyon Tabanlı ASLR (fASLR) | Rastgeleleştirme entropisi (~80) | Fonksiyonların taşınmasıyla ROP tahmin zorluğu artırımı | Shao, X. et al. (2022) |

---

## 🧠 2️⃣ SWOT Analizi  

| Güçlü Yönler | Zayıf Yönler | Fırsatlar | Tehditler |
|---------------|--------------|------------|------------|
| ✅ CheckOCPP gibi araçlar, protokol uygunluğunu gerçek zamanlı doğrular. | ❌ ISO/IEC 27001 uygulamada düşük doğruluk sağlayabilir. | 💡 Kuantum dirençli (TOPRF, Lattice-based) sistemler geliştirilebilir. | ⚠️ Kritik altyapı saldırıları (blackouts, enerji hırsızlığı). |
| 🧩 ML tabanlı sistemler enerji anomalilerini yüksek doğrulukla tespit eder. | 📱 Mobil uygulamalarda zayıf kimlik doğrulama, hardcoded kimlik bilgileri. | ⚙️ Dinamik izolasyon sistemleri (DyPrIs). | 🔐 GDPR ihlalleri ve üyelik çıkarımı saldırıları. |
| 🔎 IDS sistemleri sıfırıncı gün saldırılarını yakalayabilir. | 🧱 GDPR mimari eksiklikleri (veri silme, rıza yönetimi). | 🚀 OCPP aktif güvenlik denetimi ile trafik kontrolü. | 🧭 IoT gizlilik politikası tutarsızlıkları. |

---

## 🧪 Sonuç  
Bu proje, elektrikli araç şarj altyapısında kullanılan protokollerin güvenlik açıklarını ortaya koyarak **akademik temelli bir güvenlik çerçevesi** sunmaktadır.  
OCPP ve ISO/IEC 15118 protokollerinin güvenliği, ML tabanlı tespit modelleriyle desteklenmiştir.  
Gelecekte, kuantum dirençli şifreleme ve dinamik izolasyon tekniklerinin EV altyapısına entegre edilmesi önerilmektedir.  

---

## 📚 Kaynakça  
- Boussaha, S. et al. (2025). *CheckOCPP: Automatic OCPP Packet Dissection and Compliance Check.*  
- Cumplido, J. et al. (2022). *Collaborative Anomaly Detection in Smart Charging Systems.*  
- Miao, Y. et al. (2022). *Membership Inference Attacks in IoT Voice Systems.*  
- Shao, X. et al. (2022). *Function-Based ASLR for IoT Systems.*  
- Ahmad, J. et al. (2022). *IoT Privacy Compliance Framework (IoTPrivComp).*  
- ISO/IEC 27001, NIST SP 800-53, IEC 61851, GDPR Resmî Standart Belgeleri.  

---

## 👤 Katkıda Bulunanlar  
**Muhammed Hilmi Kılavuz**  
🎓 Fırat Üniversitesi — Yazılım Mühendisliği  
💻 Araştırma, Analiz, Veri Hazırlığı, Raporlama  

---


