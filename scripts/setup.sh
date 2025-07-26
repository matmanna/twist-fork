#!/bin/bash

# 1. Install dependencies
sudo apt update
sudo apt install -y hostapd dnsmasq python3-pip nodejs npm

# 2. Setup AP configs (copy pre-made configs)
sudo cp scripts/hostapd.conf /etc/hostapd/hostapd.conf
sudo cp scripts/dnsmasq.conf /etc/dnsmasq.conf
sudo cp scripts/dhcpcd.conf /etc/dhcpcd.conf
sudo cp scripts/hostapd /etc/default/hostapd

# 3. Enable services
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq

# 4. Install Python backend requirements
cd backend
pip3 install -r requirements.txt

# 5. Build frontend
cd ../frontend
npm install
npm run build
cp -r dist/* ../backend/static/

# 6. Install and enable the backend service
sudo cp ../scripts/thetwist.service /etc/systemd/system/
sudo systemctl enable thetwist
sudo systemctl restart thetwist

# 7. Reboot to finish
sudo reboot
