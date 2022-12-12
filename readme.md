<h1 align="center">Zelda DS Translation</h1>

<p align="center">Tool editing text Game Zelda Ds</p>

# Informasi
ZeldaDSTranslation adalah tool yang dipakai dalam menerjemahkan game The Legends of Zelda dari platform Nintendo DS. Tool ini dapat dipakai untuk seri [Phantom Hourglass](https://en.m.wikipedia.org/wiki/The_Legend_of_Zelda:_Phantom_Hourglass) dan [Spirit Track](https://en.m.wikipedia.org/wiki/The_Legend_of_Zelda:_Spirit_Track). Karena di tulis dalan python3 dan ber-antarmuka Command Line, anda juga dapat memakainya di Android!.

# Pemasangan 
> **Kebutuhan!**
> [Termux](https://f-droid.org/en/packages/com.termux). Memakai aplikasi Termux untuk penggunaan di Android sangat di anjurkan karena tool mengandung kode Argument Vector.

Untuk memulai memasang tool ini, kita perlu memasang beberapa dependeci untuk menjalankan tool ini.

- python3
- ndspy
- xdelta3

• Terrmux
<summary><strong>Install Package Dependecies</strong></summary>

```bash
apt update && apt upgrade
apt install python3 -y
```
<summary><strong>Clone atau Download Repository</strong></summary>

```bash
git clone https://github.com/SuchMioko/ZeldaDSTranslation.git
```
Setelah ini kita hanya perlu memasang library python yang dipakai dalam kode tool ini. Pertama masuk ke directory repo ini yang sudah di download tadi dengan `cd ZeldaDSTranslation` lalu jalankan `python3 -m pip install -r requirements.txt`.

# Menjalankan tool
Pertama kali anda harus menyimpan ROM zelda ke dalam folder **ZeldaDSTranslation** nama file harus dengan nama **zelda.nds** meskipun pada game zelda yang berbeda, program akan otomatis mengenal game tersebut dengan membaca Header ROM.

Anda akan menemukan sebuah file bernama **main.py** ini adalah file utama dalam menjalankan tool, katakan `python3 main.py -h` ke dalam terminal untuk menjalankan tool-nya, maka sebuah options tool akan di tampilkan kedalam layar terminal anda.

Untuk menghentikan atau jangan, membuat patch xdelta cukup tambahkan parameter -i ketika melakukan repack, katakan `python3 main.py -c -i` maka patch tidak akan dibuat.
