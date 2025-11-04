# ev-charging-security

⚡ Ev Charging Security – Team Repository

Bu repo, elektrikli araç / şarj istasyonu güvenliği projesi için ekip çalışması amacıyla oluşturulmuştur.
Her ekip üyesi kendi branch’inde (dalında) çalışır ve değişikliklerini oraya push eder.
main branch sadece final sürüm içindir — doğrudan değişiklik yapılmaz.


## 📂 Proje Yapısı
| Klasör | Açıklama |
|--------|-----------|
| `/simulators` | Şarj istasyonu ve araç simülatörleri |
| `/docs` | Dokümantasyon ve literatür özetleri |
| `/tests` | Test senaryoları ve sonuçlar |

> ⚠️ Bu klasörler tüm branch’lerde otomatik olarak bulunur.  
> Her üye kendi dosyalarını uygun klasörün içine eklemelidir.

👥 Ekip Çalışma Modeli

.Her ekip üyesi kendi adına özel bir branch açanız.

.Sadece kendi branch’ine push yapınız.

.main branch’e doğrudan commit atılmamalıdır.

.Dönem sonunda tüm branch’ler merge edilecektir.

🔹 Branch isimlendirme formatı
suleyman
hilmi
abdullah vb.

💻 GIT BASH Komutları
# 1. Repoyu klonlayın
git clone https://github.com/suleymanssardogan/ev-charging-security.git

# 2. Proje dizinine girin
cd ev-charging-security

# 3. Kendi adınıza bir branch oluşturun
git checkout -b <isim>

# 4. Değişiklikleri ekleyin ve commit atın
git add .
git commit -m "feat: add anomaly scenario draft"

# 5. Kendi branch’inize push yapın
git push origin <isim>



# Güncellemeleri Almak İsterseniz
git pull origin main


### 🧱 Commit Mesaj Formatı

#### Durum – Kullanılacak Örnekler
Commit mesajının başına bu öneklerden birini yazınız:

- **Yeni şey ekliyorsan:** `feat/`
- **Bir hatayı düzeltiyorsan:** `fix/`
- **Sadece belge güncelliyorsan:** `docs/`
- **Klasör / düzenleme yapıyorsan:** `chore/`
- **Yayın öncesi son düzenlemeler:** `release/`

#### 💡 Örnek Commit Mesajları
```bash
git commit -m "feat: yeni anomali senaryosu eklendi"
git commit -m "fix: test hatası düzeltildi"
git commit -m "docs: literatür özeti güncellendi"
git commit -m "chore: klasör yapısı düzenlendi"
```





<img width="900" height="825" alt="image" src="https://github.com/user-attachments/assets/232f3aa8-d7ae-415b-b08b-a4d1380932b5" />



