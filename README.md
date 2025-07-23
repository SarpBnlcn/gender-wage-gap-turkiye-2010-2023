# Türkiye'de Cinsiyetler Arası Ücret Farkı Analizi: Meslek Gruplarına Göre Eğilimler
Türkiye'de Cinsiyetler Arası Ücret Farkı Analizi: Meslek Gruplarına Göre Eğilimler
🎯 Proje Amacı
Bu projenin temel amacı, Türkiye İstatistik Kurumu (TÜİK) benzeri simüle edilmiş veri setini kullanarak, 2010-2023 yılları arasında Türkiye'deki meslek gruplarına göre kadın ve erkek çalışanların saatlik brüt ücretleri arasındaki farkları derinlemesine analiz etmektir. Çalışma, ücret eşitsizliklerinin zaman içindeki değişimini ve hangi meslek gruplarında daha belirgin olduğunu ortaya koymayı hedeflemektedir.

❓ Ana Araştırma Soruları
Hangi meslek gruplarında kadın ve erkek arasındaki saatlik ücret farkı daha fazladır?

Ücret farkları, 2010'dan 2023'e kadar zaman içinde nasıl bir değişim göstermiştir (artış, azalış, stabil kalma)?

En yüksek ücret farkı hangi yıl ve hangi meslek grubunda gözlemlenmiştir?

Belirli meslek gruplarında cinsiyet bazlı ücret eğilimleri nelerdir?

📊 Veri Seti
Bu projede kullanılan veri seti, meslek gruplarına göre yıllık ortalama saatlik brüt ücretleri içermektedir. Veriler, kadın ve erkek çalışanlar için ayrı ayrı sunulmuş olup, 2010, 2014, 2018, 2022 ve 2023 yıllarını kapsamaktadır. Veri seti, Türkiye İstatistik Kurumu (TÜİK) verilerine benzer şekilde simüle edilmiştir.

🚀 Analiz Adımları
Proje, aşağıdaki ana adımları takip etmektedir:

Veri Yükleme ve Ön İşleme:

Ham veri dosyası (data.csv) yüklenir.

Çoklu başlık satırları ve gereksiz sütunlar temizlenir.

Türkçe/İngilizce meslek adları ayrıştırılır ve İngilizce adlar kullanılır.

Erkek ve kadın ücret verileri tek bir yapıya dönüştürülür ve 'Cinsiyet' sütunu eklenir.

Eksik değerler (örn. (0) veya None) uygun şekilde işlenir ve sayısal sütunlar dönüştürülür.

'Toplam' ve 'Temel meslekler' gibi genel kategoriler analizden çıkarılır.

Keşifçi Veri Analizi (EDA) ve Görselleştirmeler:

Veri setinin genel yapısı ve dağılımı incelenir.

Cinsiyetler arası ücret farkları hesaplanır.

Aşağıdaki görselleştirmeler oluşturularak temel içgörüler elde edilir:

Yıllara göre ortalama saatlik brüt ücretlerin cinsiyete göre değişimi.

Meslek gruplarına göre ortalama ücret farkları.

Belirli meslek gruplarında cinsiyet bazlı ücret eğilimleri.

Makine Öğrenimi Modeli (RandomForestRegressor):

Saatlik brüt ücretleri tahmin etmek amacıyla bir RandomForestRegressor modeli eğitilir.

Veri seti eğitim ve test setlerine ayrılır.

Modelin performansı Ortalama Mutlak Hata (MAE) ve R-kare (R²) metrikleri ile değerlendirilir.

<img width="1200" height="800" alt="meslek_bazli_ucret_farklari" src="https://github.com/user-attachments/assets/1eecf004-da87-43ed-b19a-1b5d38faf757" />
<img width="1200" height="600" alt="ortalama_ucretler_yillara_gore" src="https://github.com/user-attachments/assets/787e22e6-259f-4d17-8a85-f73ab5ad91d4" />
<img width="1400" height="800" alt="secili_meslekler_ucret_egilimleri" src="https://github.com/user-attachments/assets/37c2d0fe-0c43-4668-99a4-58768c63614a" />




