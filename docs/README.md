# Snake AI Projesi Dokümantasyonu

## Proje Genel Bakış
Bu proje, **Deep Q-Learning (DQN)** kullanarak **Snake** oyununu oynamayı öğrenen bir yapay zeka uygulamasıdır. **OpenAI Gym** framework'ü üzerine inşa edilmiş ve **Pygame** kullanılarak görselleştirilmiştir.

## Sistem Gereksinimleri
- Python 3.7 ve üzeri
- `pygame`
- `numpy`
- `gym`
- `tensorflow/keras` (DQN Ajansı için)

## Proje Yapısı
Proje, ana bileşenleri, eğitim süreci ve yapılandırma dosyalarını içerir. Proje dosya yapısı aşağıdaki gibidir:
- `main.py`: Projeyi başlatan ana dosya
- `config/`: Yapılandırma dosyalarının bulunduğu klasör
- `game/`: Oyun mantığı ve görselleştirme dosyaları
  - `game_logic.py`: Oyun mantığını içeren dosya
  - `renderer.py`: Oyun görselleştirme dosyası
- `ai/`: Yapay zeka ajanı ve hafıza dosyaları
  - `agents.py`: DQN ajanını içeren dosya
  - `memory.py`: Deneyim tekrar oynatma hafızasını içeren dosya
  - `networks.py`: Sinir ağı modelini içeren dosya
- `docs/`: Dokümantasyon dosyaları

## Ana Bileşenler

### SnakeGame Sınıfı
`SnakeGame` sınıfı, OpenAI Gym çerçevesini kullanarak oyun ortamını oluşturur.

#### Önemli Metodlar:
- `reset()`: Oyunu başlangıç durumuna getirir.
- `step(action)`: Belirli bir aksiyonu uygular ve yeni durum ile ödülü döndürür.
- `render()`: Oyun durumunu görselleştirir.

### Durum Uzayı (State Space)
Oyun durumu 7 boyutlu bir vektör ile temsil edilir:
1. Yukarı yönde tehlike (0/1)
2. Aşağı yönde tehlike (0/1)
3. Sol yönde tehlike (0/1)
4. Sağ yönde tehlike (0/1)
5. Yemeğin X koordinatı (normalize edilmiş)
6. Yemeğin Y koordinatı (normalize edilmiş)
7. Yılanın normalize edilmiş uzunluğu

### Aksiyon Uzayı (Action Space)
Oyundaki 4 olası aksiyon şunlardır:
- 0: Yukarı
- 1: Aşağı
- 2: Sol
- 3: Sağ

### Ödül Sistemi
- Yemek yeme: +10 puan
- Çarpışma: -10 puan
- Her hareket: -0.1 puan

## Eğitim Süreci
Eğitim süreci şu adımları takip eder:
1. Ortamı sıfırla
2. Mevcut durumu gözlemle
3. Epsilon-greedy stratejisi ile aksiyon seç
4. Aksiyonu uygula ve yeni durumu gözlemle
5. Deneyimi hafızaya kaydet
6. Belirli aralıklarla öğrenme
7. Bölüm bitene kadar 2-6 adımlarını tekrarla

## Kullanım
Projeyi çalıştırmak için terminal ya da komut satırına aşağıdaki komutu yazabilirsiniz:
```bash
python main.py
```

## Yapılandırma
`config/config.py` dosyasından aşağıdaki parametreler ayarlanabilir:
- Oyun pencere boyutları
- Hücre boyutu
- FPS (Frames Per Second)
- Batch size
- Öğrenme oranı, gamma, epsilon gibi DQN öğrenme parametreleri

## Performans Metrikleri
Projenin eğitim ve değerlendirilmesi sırasında aşağıdaki metrikler takip edilir:
- **Skor**: Yılanın yediği yemek sayısı
- **Toplam Ödül**: Bölüm boyunca toplanan toplam ödül
- **Yüksek Skor**: Şimdiye kadarki en yüksek skor