
**El Hareketiyle Hesap Makinesi**

---

**Genel Bakış**  
Bu Python betiği, MediaPipe ve OpenCV kullanarak el hareketleriyle çalışan interaktif bir hesap makinesi uygular. Web kamerası aracılığıyla el hareketlerini algılar, parmak sayısıyla sayıları belirler ve temel işlemleri (toplama, çıkarma, çarpma, bölme) gerçekleştirir.

---

**Özellikler**

- **El Algılama:** MediaPipe HandLandmarker ile el konumlarını tespit eder.  
- **Hareket Tanıma:** Parmak sayısını kullanarak 1 ile 5 arası sayı girişi sağlar.  
- **Parmak Durumu Tespiti:** Açık veya kapalı parmakları doğru şekilde analiz eder.  
- **Etkileşimli Arayüz:** İşlem başlatma, işlem seçme ve menüye dönme gibi düğmeler içerir.  
- **Durum Makinesi:** Kullanıcının etkileşim durumlarını (örneğin sayı bekleme, işlem seçme) yönetir.  
- **Görsel Geri Bildirim:** Video akışında el hareketlerini, işlemleri ve sonuçları gösterir.

---

**Gereksinimler**

- Python 3.x  
- Gerekli Kütüphaneler: `mediapipe`, `opencv-python`, `numpy`  
- Web kamerası  
- MediaPipe `hand_landmarker.task` dosyası (MediaPipe web sitesinden indirilmeli)

---

**Kurulum**

1. Bu depoyu indirin veya klonlayın.  
2. Gerekli Python kütüphanelerini yükleyin:  
   ```bash
   pip install mediapipe opencv-python numpy
   ```  
3. `hand_landmarker.task` dosyasını betikle aynı dizine yerleştirin.  
4. Bilgisayarınıza bir web kamerasının bağlı olduğundan emin olun.

---

**Kullanım**

Betiği çalıştırmak için terminale şu komutu yazın:  
```bash
python mehmet_akif_erol_goruntuisleme_vize.py
```

Web kamerası açıldığında şu adımları izleyin:

- **Başlat:** Sol üst köşedeki “İşlem Yap” düğmesine işaret edin.  
- **Birinci Sayıyı Girin:** Sağ elinizle 1–5 parmak gösterin. Onay için yaklaşık 3 saniye bekleyin.  
- **İkinci Sayıyı Girin:** Aynı işlemi ikinci sayı için tekrar edin.  
- **İşlem Seçin:** Toplama, çıkarma, çarpma veya bölme düğmesine işaret edin.  
- **Sonucu Görüntüleyin:** Ekranda işlem sonucu gösterilir.  
- **Ana Menüye Dön:** Sağ üstteki "Main’e Dön" düğmesine işaret ederek sıfırlayın.  
- Uygulamadan çıkmak için `q` veya `Q` tuşuna basın.

---

**Nasıl Çalışır**

---

**El Takibi:**  
MediaPipe en fazla iki eli algılayabilir. Ancak sayı girişi için yalnızca sağ el kullanılır.

---

**Parmak Sayımı ve Durumu:**  
`finger_acik_mi` fonksiyonu, işaret, orta, yüzük ve serçe parmakların açık mı kapalı mı olduğunu belirler. Parmak ucu ile parmak eklemi ve bilek arasındaki mesafeye göre değerlendirme yapılır.  
`basparmak_acik_mi` fonksiyonu, başparmağın açık olup olmadığını açı ve konum bilgisine göre analiz eder.  
Açık parmakların toplamı kullanıcıdan alınan sayıyı ifade eder (1-5 arası).

---

**Durum Makinesi:**

- **Main:** Başlangıç durumu  
- **Sayi1 Bekleniyor:** Birinci sayı bekleniyor  
- **Sayi1 Alindi:** Birinci sayı onaylandı  
- **Sayi2 Bekleniyor:** İkinci sayı bekleniyor  
- **Sayi2 Alindi:** İkinci sayı onaylandı, işlem seçimi yapılabilir  
- **Sonuc:** Hesaplama sonucu gösterilir

---

**Düğme Etkileşimi:**  
İşaret parmağı (landmark 8), düğme üzerine geldiğinde tıklama işlemi tetiklenir.

---

**Notlar**

- Sayı girişi için yaklaşık 3 saniyelik (90 kare) bekleme süresi uygulanır.  
- Sıfıra bölme durumunda sonuç “Tanımsız” olarak gösterilir.  
- Arayüz Türkçedir.  
- Doğru algılama için iyi ışıklandırma ve net bir el görünürlüğü gereklidir.

---

**Sınırlamalar**

- Sadece 1 ile 5 arası sayılar desteklenir.  
- Sayı girişi sadece sağ elle yapılır.  
- Zayıf ışık veya karmaşık arka planlarda algılama performansı düşebilir.  
- `hand_landmarker.task` dosyası gereklidir ve depoya dahil değildir.

---

**Sorun Giderme**

- **Web kamerası algılanmıyor:** Kameranın bağlı ve çalışır durumda olduğundan emin olun.  
- **MediaPipe hataları:** `hand_landmarker.task` dosyasının doğru konumda olduğundan emin olun.  
- **Hareket algılanmıyor:** Elinizin net görünür ve kamera çerçevesi içinde olduğundan emin olun.

---

**Lisans**  
Bu proje eğitim amaçlı geliştirilmiştir ve ticari kullanım için lisanslanmamıştır. MediaPipe ve OpenCV lisans koşullarına uyulmalıdır.

---

**Yazar**  
Mehmet Akif Erol

---

