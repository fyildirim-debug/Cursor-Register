#!/bin/bash

# Gerekli sistem paketlerinin kurulumu
echo "Sistem paketleri kontrol ediliyor ve kuruluyor..."
sudo apt-get update
sudo apt-get install -y python3-venv python3-pip xvfb chromium-browser chromium-chromedriver

# Virtual environment kurulumu ve aktivasyonu
if [ ! -d "venv" ]; then
    echo "Virtual environment kuruluyor..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Xvfb ve headless mod ayarları
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x16 &
export ENABLE_HEADLESS=true

# Scripti çalıştır
python cursor_register_v2.py "$@"

# Virtual environment'ı deaktive et
deactivate 