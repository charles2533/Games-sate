# 🍢 Go Sate! - Juragan Level Up

Game simulasi berjualan sate ala *cooking/time-management game*, dibuat murni dengan **Python + Pygame** (desktop).

Pemain berperan sebagai juragan sate yang harus memanggang sate, menyusun piring pesanan, dan melayani pelanggan sebelum kesabaran mereka habis — sambil mengejar target omzet dan jumlah porsi terjual di setiap level.

---

## 🎮 Cara Bermain

1. **Panggang Sate** — Klik panggangan (grill) yang kosong untuk mulai memanggang (butuh stok daging).
   - Sate akan berubah dari **Mentah → Matang → Gosong** seiring waktu. Ambil saat sudah matang!
2. **Susun Piring** — Klik sate yang sudah matang di grill untuk memindahkannya ke piring kosong, lalu klik tombol **Lontong** dan **Bumbu Kacang** untuk melengkapi pesanan.
3. **Layani Pelanggan** — Klik pelanggan yang datang saat ada piring lengkap (sate + lontong + bumbu) untuk menyajikannya dan dapat uang. Jangan biarkan bar kesabaran mereka habis, atau kamu akan didenda.
4. **Belanja** — Buka **Toko** untuk membeli tambahan stok daging, lontong, dan bumbu kacang menggunakan uang hasil jualan.
5. **Buang Pesanan Salah** — Klik tempat sampah untuk mengosongkan piring yang salah susun.
6. Capai **target uang** dan **target porsi terjual** sebelum waktu habis untuk menang di level tersebut.

### Kontrol
| Input | Aksi |
|---|---|
| Klik kiri mouse | Semua interaksi (menu, grill, piring, topping, pelanggan, toko) |
| `ESC` | Keluar dari game (versi desktop) |

---

## 🏆 Daftar Level

| Level | Nama | Target Uang | Target Porsi | Waktu | Kesabaran Pelanggan | Spawn Rate |
|---|---|---|---|---|---|---|
| 1 | Kampung Sebelah | Rp 20.000 | 10 porsi | 60 dtk | 15 dtk | tiap 4 dtk |
| 2 | Alun-Alun Kota | Rp 35.000 | 15 porsi | 90 dtk | 12 dtk | tiap 3 dtk |
| 3 | Festival Kuliner | Rp 50.000 | 20 porsi | 120 dtk | 10 dtk | tiap 2.5 dtk |

Setiap level dimulai dengan modal Rp 5.000 dan stok awal 8 daging, 8 lontong, 8 bumbu kacang.

---

## 📁 Struktur Folder

Game membaca semua aset dari folder `assets/` yang berada satu level dengan file utama:

```
project/
├── main.py              # file game ini
└── assets/
    ├── latar home.png
    ├── latar game.png
    ├── meja game.png
    ├── character1.png
    ├── character2.png
    ├── character3.png
    ├── speechBubble.png
    ├── logo.png
    ├── tombolStart.png
    ├── logoBelanja.png
    ├── tombolBack.png
    ├── grill.png
    ├── piring.png
    ├── piringLengkap.png
    ├── sampah.png
    ├── tombolLontong.png
    ├── tombolBumbuKacang.png
    ├── lontong.png
    ├── bumbuKacang.png
    ├── SateGosong.png
    ├── sateMatang.png
    ├── SateMentah.png
    ├── click.ogg
    └── bgm.ogg
```

> ⚠️ Jika salah satu file gambar tidak ditemukan, game tidak akan crash — sebagai gantinya akan menampilkan kotak magenta pengganti (placeholder) agar mudah dikenali aset mana yang hilang. File suara yang hilang akan diabaikan secara diam-diam (tanpa suara, tanpa error).

---

## 💻 Menjalankan di Desktop (Lokal)

Butuh Python 3.8+ dan library Pygame.

```bash
pip install pygame
python main.py
```

Pastikan folder `assets/` ada di direktori yang sama dengan `main.py`.

---

## 📝 Catatan Teknis

- Resolusi game tetap (statis) di **900x600**.
- Font menggunakan `comicsans`, dengan fallback ke `Arial` jika tidak tersedia di sistem.
- `pygame.quit(); sys.exit()` dipanggil saat klik tombol close atau tekan `ESC` untuk keluar dari game.
- Alur state game: `MENU → LEVEL_SELECT → GAME ⇄ SHOP → RESULT → LEVEL_SELECT`.

---

## 🛠️ Ide Pengembangan Selanjutnya

- Tambah animasi transisi antar-state.
- Simpan skor tertinggi / progres level (persisten).
- Tambah level baru dengan variasi menu (misalnya sate ayam vs sate kambing).
- Efek suara terpisah untuk memanggang, menyajikan, dan pelanggan marah.
