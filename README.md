# WordPress XML-RPC Brute Force Tool

WordPress XML-RPC Brute Force Tool adalah sebuah alat untuk melakukan bruteforce terhadap endpoint `xmlrpc.php` pada situs WordPress. Alat ini dilengkapi dengan fitur kustomisasi password dan mendukung threading untuk eksekusi yang lebih cepat.

## Fitur
- **Custom Password Generator**: Secara otomatis membuat password berdasarkan pola umum username, domain, dan lainnya.
- **Multi-threading**: Mendukung hingga 1200 worker untuk meningkatkan efisiensi.
- **Username Detection**: Mengambil username dari endpoint `wp-json/wp/v2/users`.
- **Error Handling**: Menangani error koneksi, timeout, dan lainnya.
- **SSL Ignored**: Mendukung koneksi HTTPS dengan peringatan SSL dinonaktifkan.

## Instalasi
1. Clone repository ini:
2. Requirement: pip install requests colorama threading
3. jalankan commandnya python fixed.py url.txt
- ganti url dengan sitelist kamu

## Disclaimer Penyalahgunaan

**Alat ini hanya ditujukan untuk tujuan pembelajaran, penelitian keamanan, atau pengujian pada sistem yang Anda miliki atau Anda memiliki izin tertulis untuk mengujinya.**

Segala bentuk penyalahgunaan alat ini untuk menyerang, mengeksploitasi, atau merusak sistem yang tidak Anda miliki atau tanpa izin adalah **tindakan ilegal** dan melanggar hukum. Pengguna bertanggung jawab sepenuhnya atas tindakan mereka, dan pengembang alat ini tidak bertanggung jawab atas kerusakan, pelanggaran hukum, atau konsekuensi apa pun yang timbul dari penggunaan alat ini.

Penggunaan alat ini pada sistem tanpa izin yang sah dapat mengakibatkan konsekuensi hukum serius, termasuk tuntutan pidana dan/atau perdata. Harap gunakan dengan penuh tanggung jawab dan hanya pada sistem yang Anda kelola atau miliki izin eksplisit untuk mengujinya.

**Ingat:** Etika dalam pengujian keamanan adalah bagian penting dari menjaga keamanan dunia maya. Pastikan Anda mematuhi hukum dan aturan setempat saat menggunakan alat ini.
