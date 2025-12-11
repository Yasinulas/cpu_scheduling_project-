# CPU Scheduling Algorithms Simulation

Bu proje, işletim sistemlerinde kullanılan çeşitli CPU zamanlama algoritmalarını simüle eden bir Python uygulamasıdır.

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Algoritmalar](#algoritmalar)
- [Proje Yapısı](#proje-yapısı)
- [CSV Formatı](#csv-formatı)
- [Çıktılar](#çıktılar)
- [Örnekler](#örnekler)

## ✨ Özellikler

- **6 Farklı Scheduling Algoritması:**
  - FCFS (First Come First Served)
  - Non-Preemptive SJF (Shortest Job First)
  - Preemptive SJF (Shortest Remaining Time First)
  - Round Robin (Quantum=4)
  - Non-Preemptive Priority
  - Preemptive Priority

- **Detaylı İstatistikler:**
  - Ortalama ve maksimum bekleme süreleri
  - Ortalama ve maksimum turnaround süreleri
  - Throughput (T=50, 100, 150, 200 için)
  - CPU verimliliği
  - Context switch sayıları

- **Görselleştirme:**
  - Timeline dosyaları
  - Detaylı sonuç raporları
  - Karşılaştırmalı analiz raporları

## 🔧 Gereksinimler

- Python 3.7 veya üzeri
- matplotlib (görselleştirme için)

## 📦 Kurulum

1. Projeyi klonlayın veya indirin:
```bash
git clone <repository-url>
cd cpu_scheduling_project
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `data` klasörüne CSV dosyalarınızı ekleyin (örnek: `case1.csv`, `case2.csv`)

## 🚀 Kullanım

Projeyi çalıştırmak için:

```bash
python main.py
```

Program çalıştığında:
1. `data` klasöründeki CSV dosyalarını listeler
2. Hangi dosyayı kullanmak istediğinizi seçmenizi ister
3. Seçilen dosyadaki process'leri yükler
4. Tüm algoritmaları sırayla çalıştırır
5. Sonuçları `outputs/` klasörüne kaydeder
6. Karşılaştırmalı raporu `reports/` klasörüne oluşturur

## 🔄 Algoritmalar

### 1. FCFS (First Come First Served)
- En basit algoritma
- Process'ler varış sırasına göre işlenir
- Preemptive değildir

### 2. Non-Preemptive SJF
- En kısa iş süresine sahip process önce işlenir
- Preemptive değildir
- Daha düşük ortalama bekleme süresi sağlar

### 3. Preemptive SJF (SRTF)
- En kısa kalan süreye sahip process öncelik alır
- Preemptive algoritma
- Daha iyi response time sağlar

### 4. Round Robin
- Her process'e eşit zaman dilimi (quantum=4) verilir
- Adil paylaşım sağlar
- Time-sharing sistemler için idealdir

### 5. Non-Preemptive Priority
- Yüksek öncelikli process'ler önce işlenir
- Priority: high > normal > low
- Preemptive değildir

### 6. Preemptive Priority
- Yüksek öncelikli process'ler her zaman öncelik alır
- Preemptive algoritma
- Real-time sistemler için uygundur

## 📁 Proje Yapısı

```
cpu_scheduling_project/
├── data/                  # CSV input dosyaları
│   ├── case1.csv
│   └── case2.csv
├── outputs/              # Algoritma sonuçları
│   ├── case1/
│   │   ├── FCFS_results.txt
│   │   ├── FCFS_timeline.txt
│   │   └── ...
│   └── case2/
│       └── ...
├── reports/              # Karşılaştırmalı raporlar
│   ├── case1_report.txt
│   └── case2_report.txt
├── main.py               # Ana program
├── scheduler.py          # Scheduling algoritmaları
├── process.py            # Process sınıfı
├── utils.py              # Yardımcı fonksiyonlar
├── requirements.txt      # Python bağımlılıkları
└── README.md            # Bu dosya
```

## 📄 CSV Formatı

CSV dosyası şu formatta olmalıdır:

```csv
Process_ID,Arrival_Time,CPU_Burst_Time,Priority
P001,0,5,high
P002,2,3,normal
P003,4,8,low
P004,5,2,high
```

**Alanlar:**
- `Process_ID`: Process tanımlayıcısı (örn: P001, P002)
- `Arrival_Time`: Varış zamanı (tam sayı)
- `CPU_Burst_Time`: CPU burst süresi (tam sayı)
- `Priority`: Öncelik seviyesi (`high`, `normal`, `low`)

**Not:** İlk satır başlık satırı olabilir, program otomatik olarak algılar.

## 📊 Çıktılar

### Timeline Dosyaları
Her algoritma için timeline dosyası oluşturulur:
```
[0] - P001 - [5]
[5] - P002 - [8]
[8] - IDLE - [10]
[10] - P003 - [18]
```

### Sonuç Dosyaları
Her algoritma için detaylı sonuç dosyası:
- Bekleme süreleri (ortalama, maksimum)
- Turnaround süreleri (ortalama, maksimum)
- Throughput değerleri
- CPU verimliliği
- Context switch sayıları
- Process detayları

### Rapor Dosyaları
Karşılaştırmalı analiz raporu:
- Tüm algoritmaların performans karşılaştırması
- En iyi performans gösteren algoritmalar
- Genel analiz ve sonuçlar

## 💡 Örnekler

### Örnek Process Seti

```csv
Process_ID,Arrival_Time,CPU_Burst_Time,Priority
P1,0,5,high
P2,1,3,normal
P3,2,8,low
P4,3,6,high
P5,4,4,normal
```

### Örnek Çıktı

```
Algorithm                  Avg Wait     Avg Turn     CPU Eff%   
------------------------------------------------------------
FCFS                       8.50         15.20        85.30      
Non-Preemptive SJF         5.20         12.10        92.50      
Preemptive SJF             4.80         11.70        94.20      
Round Robin (Q=4)          6.30         13.20        88.10      
Non-Preemptive Priority    5.50         12.40        91.80      
Preemptive Priority        4.60         11.50        95.10      
```

## 🎓 Eğitim Bilgisi

Bu proje **Istanbul Nişantaşı University** - **EBLM341 Operating Systems** dersi kapsamında geliştirilmiştir.

## 📝 Notlar

- Tüm zamanlar tam sayı birimlerindedir
- Priority değerleri: `high` (1), `normal` (2), `low` (3)
- Round Robin algoritması için quantum değeri 4 olarak ayarlanmıştır
- IDLE zamanları timeline'da gösterilir

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👨‍💻 Geliştirici

Istanbul Nişantaşı University - EBLM341 Operating Systems Course Project

---

**Not:** Herhangi bir sorun veya öneri için issue açabilirsiniz.

