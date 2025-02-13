# Cursor Hesap Oluşturucu / Cursor Account Generator

[English](#english) | [Türkçe](#türkçe)

## ⚠️ Önemli Uyarı / Important Warning

### 🇹🇷 Türkçe Uyarı
Bu proje **SADECE EĞİTİM AMAÇLIDIR** ve otomatik hesap oluşturma sürecinin teknik olarak nasıl çalıştığını göstermek için hazırlanmıştır. Bu aracın kullanılması etik değildir ve Cursor'un hizmet şartlarına aykırıdır.

**Cursor'u desteklemek ve en iyi deneyimi yaşamak için lütfen resmi web sitesinden lisans satın alın: [cursor.sh](https://cursor.sh)**

Bu projenin amacı:
- Eğitim ve öğrenme
- Teknik süreçleri anlama
- Otomasyon mantığını kavrama

Bu projenin amacı **KESİNLİKLE**:
- Cursor'u ücretsiz kullanmak
- Hizmet şartlarını ihlal etmek
- Ticari kazanç elde etmek **DEĞİLDİR**

## Türkçe

Bu script, Cursor için otomatik hesap oluşturma işlemini gerçekleştirir. Ubuntu ve türevi Linux sistemlerde test edilmiş ve çalışır durumdadır.

### Gereksinimler
- Ubuntu veya türevi bir Linux sistemi
- Python 3.8 veya üzeri
- İnternet bağlantısı

### Kurulum
1. Depoyu klonlayın:
```bash
git clone [repo-url]
cd [repo-directory]
```

2. Çalıştırma scriptini çalıştırılabilir yapın:
```bash
chmod +x run_headless.sh
```

3. Scripti çalıştırın:
```bash
./run_headless.sh
```

Script otomatik olarak şunları yapacaktır:
- Gerekli sistem paketlerini kurar (chromium-browser, chromium-driver, xvfb, vb.)
- Python sanal ortamı oluşturur
- Gerekli Python paketlerini kurar
- Headless modda çalışmak için gerekli ayarları yapar

### Kullanım
Varsayılan olarak script 2 hesap oluşturur. Farklı sayıda hesap oluşturmak için:
```bash
./run_headless.sh --number 5  # 5 hesap oluşturur
```

Çoklu iş parçacığı kullanmak için:
```bash
./run_headless.sh --number 10 --max_workers 3  # 10 hesabı 3 iş parçacığında oluşturur
```

### Çıktılar
Script çalıştığında iki dosya oluşturur:
- `hesaplar_[tarih].csv`: E-posta, şifre ve token bilgilerini içerir
- `tokenler_[tarih].csv`: Sadece token bilgilerini içerir

---

## English

This script automates the account creation process for Cursor. It has been tested and works on Ubuntu and Ubuntu-based Linux systems.

### Requirements
- Ubuntu or Ubuntu-based Linux system
- Python 3.8 or higher
- Internet connection

### Installation
1. Clone the repository:
```bash
git clone [repo-url]
cd [repo-directory]
```

2. Make the run script executable:
```bash
chmod +x run_headless.sh
```

3. Run the script:
```bash
./run_headless.sh
```

The script will automatically:
- Install required system packages (chromium-browser, chromium-driver, xvfb, etc.)
- Create Python virtual environment
- Install required Python packages
- Configure settings for headless mode

### Usage
By default, the script creates 2 accounts. To create a different number of accounts:
```bash
./run_headless.sh --number 5  # creates 5 accounts
```

To use multiple threads:
```bash
./run_headless.sh --number 10 --max_workers 3  # creates 10 accounts using 3 threads
```

### Outputs
The script creates two files:
- `hesaplar_[date].csv`: Contains email, password, and token information
- `tokenler_[date].csv`: Contains only token information 

### 🇬🇧 English Warning
This project is **FOR EDUCATIONAL PURPOSES ONLY** and is designed to demonstrate how the automated account creation process works technically. Using this tool is unethical and violates Cursor's terms of service.

**To support Cursor and get the best experience, please purchase a license from the official website: [cursor.sh](https://cursor.sh)**

The purpose of this project is:
- Education and learning
- Understanding technical processes
- Comprehending automation logic

This project is **ABSOLUTELY NOT** intended for:
- Using Cursor for free
- Violating terms of service
- Commercial gain 