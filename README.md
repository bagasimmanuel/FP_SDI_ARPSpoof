# Final Project Sistem Deteksi Intrusi

## ARP Spoofing Detection to prevent MITM attack

### Requirement

1. Bisa run as Root
2. Memiliki modul `Netifaces` dan `Scappy` telah terinstall
3. OS dari Host adalah Linux
4. Account Twilio (SID_Token & Token_Auth)

### Cara Kerja

Pertama tama program akan mencari IP Address dan MAC Address dari Gateway suatu jaringan, Selanjutnya akan diikuti dengan melihat MAC Address dan IP Address dari source (asal) paket yang diterima. Ketika Packet yang diterima tidak berasal dari MAC Address dari default gateway, hal ini menandakan bahwa terjadi spoofing attack dan akan segera diberikan notifikasi melalui Whatsapp.

### Penggunaan

Jalankan program arpshield.py dan biarkan berjalan di background, ketika ada spoof attack, maka akan log di terminal "ARP Attack Detected" diikuti dengan message ke Nomor HP Anda yang telah terdaftar di Twilio.

### Run Program

![Gambar Running](/img/running.png)
