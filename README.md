El Hareketiyle Hesap Makinesi

Genel Bakış

Bu Python betiği, MediaPipe ve OpenCV kullanarak el hareketleriyle çalışan bir hesap makinesi uygular. Web kamerası aracılığıyla el işaretlerini algılar, parmak hareketlerini tanıyarak sayıları ve işlemleri seçer ve temel aritmetik hesaplamalar (toplama, çıkarma, çarpma, bölme) yapar. Sistem, giriş sürecini yönetmek için bir durum makinesi kullanır ve sonuçları video akışında gösterir.
Özellikler

El Algılama: MediaPipe'ın HandLandmarker modülünü kullanarak el işaretlerini algılar ve takip eder.
Hareket Tanıma: Açık parmakları (başparmak dahil) sayarak 1-5 arasındaki sayıları girer.
Parmak Durumu Kontrolü: Her parmağın açık veya kapalı olduğunu hassas bir şekilde belirler.
Etkileşimli Arayüz: Hesaplamayı başlatmak, işlem seçmek ve ana duruma dönmek için düğmeler gösterir.
Durum Yönetimi: Sayı bekleme, işlem seçme ve sonuç gösterme gibi durumları yönetir.
Görsel Geri Bildirim: Video akışında el işaretlerini, parmak sayısını ve hesaplama detaylarını kaplar.

Gereksinimler

Python 3.x
Kütüphaneler:
mediapipe
opencv-python
numpy


Bir web kamerası
MediaPipe'ın hand_landmarker.task model dosyası (MediaPipe adresinden indirin)

Kurulum

Bu depoyu klonlayın veya indirin.
Gerekli Python kütüphanelerini yükleyin:pip install mediapipe opencv-python numpy


hand_landmarker.task model dosyasını indirin ve betiğin bulunduğu dizine yerleştirin.
Cihazınıza bir web kamerasının bağlı olduğundan emin olun.

Kullanım

Betiği çalıştırın:python mehmet_akif_erol_goruntuisleme_vize.py


Web kamerası akışı, etkileşimli bir arayüzle açılacaktır.
Hesaplama yapmak için şu adımları izleyin:
Başlat: Sol üst köşedeki "İşlem Yap" düğmesine işaret ederek başlayın.
Birinci Sayıyı Gir: Sağ elinizle 1-5 parmak (başparmak dahil) gösterin. Onay için ~3 saniye tutun.
İkinci Sayıyı Gir: İkinci sayı için hareketi tekrarlayın.
İşlem Seç: İşlem düğmelerinden birine (Toplama, Çıkarma, Çarpma, Bölme) işaret edin.
Sonucu Görüntüle: Sonuç ekranda gösterilir.
Ana Menüye Dön: Sağ üst köşedeki "Main'e Dön" düğmesine işaret ederek sıfırlayın.


Uygulamadan çıkmak için q veya Q tuşuna basın.

Nasıl Çalışır

El Takibi: MediaPipe, en fazla iki eli algılar, ancak sayı girişi için yalnızca sağ el kullanılır.
Parmak Sayımı ve Durum Kontrolü:
Parmakların Açık/Kapalı Kontrolü: finger_acik_mi fonksiyonu, işaret, orta, yüzük ve serçe parmakların açık olup olmadığını belirler. Her parmak için, parmak ucu (tip) ve bir kontrol noktası (örneğin, parmak eklemi) bilekten (landmark 0) olan mesafeleri karşılaştırılır. Eğer parmak ucu bilekten kontrol noktasından daha uzaksa, parmak açık kabul edilir (1 döndürür, aksi halde 0).
Başparmak Kontrolü: basparmak_acik_mi fonksiyonu, başparmağın açık olup olmadığını belirlemek için daha karmaşık bir yöntem kullanır. Başparmak ucu (landmark 4), eklem (landmark 2) ve bir kontrol noktası (landmark 5) arasındaki açıyı hesaplar. Ayrıca, başparmak ucunun avuç içine (landmark 9) yakınlığını değerlendirir. Açı 40 dereceden büyükse ve avuç yakınlık oranı 0.8'den fazlaysa, başparmak açık kabul edilir (1 döndürür, aksi halde 0).
Toplam Sayı: Açık parmakların toplamı (1-5) sayı girişi olarak kullanılır.


Durum Makinesi:
Main: Başlangıç durumu, kullanıcının başlamasını bekler.
Sayi1 Bekleniyor: Birinci sayıyı bekler.
Sayi1 Alindi: Birinci sayı onaylandı.
Sayi2 Bekleniyor: İkinci sayıyı bekler.
Sayi2 Alindi: İkinci sayı onaylandı, işlem düğmeleri gösterilir.
Sonuc: Hesaplama sonucunu gösterir.


Düğme Etkileşimi: İşaret parmağı (landmark 8), düğmelere "tıklamak" için üzerlerinde gezinir.

Notlar

Sayı girişini onaylamak için 3 saniyelik bir bekleme süresi (BEKLEME_SURESI = 90 kare) kullanılır.
Sıfıra bölme durumu işlenir ve "Tanimsiz" olarak gösterilir.
Arayüz Türkçe metin kullanır (ör. "Toplama" için toplama, "İşlem Yap" için hesapla).
Doğru algılama için iyi aydınlatma ve net el görünürlüğü sağlayın.

Sınırlamalar

Yalnızca 1-5 arasındaki sayıları parmak sayısına göre destekler.
Sayı girişi için sağ el hareketi gerektirir.
Zayıf aydınlatma veya karmaşık arka planlarda sorun yaşayabilir.
hand_landmarker.task model dosyası gereklidir ve depoda yer almaz.

Sorun Giderme

Web kamerası algılanmadı: Web kameranızın bağlı ve erişilebilir olduğundan emin olun.
MediaPipe hataları: hand_landmarker.task dosyasının doğru dizinde olduğunu doğrulayın.
Hareket tanınmadı: Elinizin net bir şekilde göründüğünden ve web kamerası çerçevesi içinde olduğundan emin olun.

Lisans
Bu proje eğitim amaçlıdır ve ticari kullanım için lisanslanmamıştır. MediaPipe ve OpenCV lisanslarına uyumluluğu sağlayın.
Yazar
Mehmet Akif Erol
