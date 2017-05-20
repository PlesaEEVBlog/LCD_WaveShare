#!/bin/sh
cd /boot/overlays
sudo wget https://raw.githubusercontent.com/PlesaEEVBlog/LCD_WaveShare/master/waveshare35a-overlay.dtb
sudo wget https://raw.githubusercontent.com/PlesaEEVBlog/LCD_WaveShare/master/waveshare35b-overlay.dtb
sudo apt-get -y install xvkbd  xinput xinput-calibrator screentest
sudo bash -c 'printf "dtoverlay=waveshare35b\n" >> /boot/config.txt'
