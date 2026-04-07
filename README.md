Berikut versi yang sudah diperbaiki format Markdown-nya saja tanpa mengubah isi:

# Auto-Heal — Auto Correct Typo untuk Python

Auto-Heal adalah tool untuk memperbaiki typo pada kode Python secara otomatis.

![Preview](preview.png)

## Instalasi

### Linux / WSL / macOS / Termux

```bash
git clone https://github.com/nandaanomi/auto-heal.git
cd auto-heal
chmod +x autoheal
```
Install ke Sistem

Linux / WSL / macOS
```bash
sudo cp autoheal /usr/local/bin/
```
Termux
```bash
cp autoheal $PREFIX/bin/
```
Tanpa Install (langsung jalankan)
```bash
python3 main.py script.py
```
Cara Pakai

# Memperbaiki satu file
 ```bash
autoheal script.py
```
# Memperbaiki semua file dalam folder
 ```bash
autoheal folder/
 ```
# Memperbaiki folder saat ini
 ```bash
autoheal .
 ```
# Melihat perubahan tanpa mengubah file
 ```bash
autoheal script.py --dry-run
 ```
# Membuat backup sebelum perbaikan
 ```bash
autoheal script.py --backup
 ```
# Menampilkan detail proses
 ```bash
autoheal script.py --verbose
 ```
Contoh

Sebelum:
```bash
defi halo():
    prin("hello")
    inport os
```
Jalankan:
```bash
autoheal script.py

Sesudah:

def halo():
    print("hello")
    import os
```
Uninstall
```bash
Linux / WSL / macOS

sudo rm /usr/local/bin/autoheal

Termux

rm $PREFIX/bin/autoheal

Hapus folder project

rm -rf ~/auto-heal
```
Author

Nanda
