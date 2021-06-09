#!/bin/bash


wget -q https://kmk.kmk.workers.dev/aria2-1.35.0-static-linux-amd64.tar.gz
tar xf aria2-1.35.0-static-linux-amd64.tar.gz -C /usr/local/bin
chmod +x /usr/local/bin/aria2c
rm -rf aria2-1.35.0-static-linux-amd64.tar.gz

# Create download folder
#mkdir -p downloads

# DHT
wget -q https://github.com/P3TERX/aria2.conf/raw/master/dht.dat
wget -q https://github.com/P3TERX/aria2.conf/raw/master/dht6.dat
