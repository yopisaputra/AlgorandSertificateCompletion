# Smart Contract Sertifikat Kompetensi

Proyek ini adalah contoh _smart contract_ di blockchain Algorand untuk menerbitkan dan memverifikasi sertifikat kompetensi digital. Dibangun menggunakan `algopy` dan `AlgoKit`.

## Konsep Dasar

_Smart contract_ ini memiliki dua fungsi utama:

1.  **`issue_certificate`**: Untuk menerbitkan sertifikat baru. Hanya pembuat kontrak (_creator_) yang dapat memanggil fungsi ini.
2.  **`verify_certificate`**: Untuk memverifikasi keaslian sertifikat berdasarkan ID uniknya. Siapa pun dapat memanggil fungsi ini.

## Setup & Instalasi

Pastikan Anda sudah menginstal [Docker](https://www.docker.com/) dan [AlgoKit](https://github.com/algorandfoundation/algokit-cli#install).

1.  **Clone Repository**
    ```bash
    git clone <URL_REPOSITORY_ANDA>
    cd sertifikat_kompetensi
    ```

2.  **Bootstrap Proyek**
    Perintah ini akan menginstal semua dependensi yang diperlukan untuk backend dan frontend.
    ```bash
    algokit project bootstrap all
    ```

3.  **Build Smart Contract**
    Masuk ke direktori kontrak dan kompilasi _smart contract_ Anda.
    ```bash
    cd projects/sertifikat_kompetensi-contracts
    algokit project run build
    ```
    Jika berhasil, artefak kontrak (file `application.json`, `approval.teal`, dan `clear.teal`) akan dibuat di dalam direktori `sertifikat_kompetensi-contracts/smart_contracts/artifacts/sertifikat_kompetensi`.

## Menjalankan & Berinteraksi dengan Kontrak

Anda dapat men-deploy dan berinteraksi dengan kontrak ini di jaringan `localnet` yang disediakan oleh AlgoKit.

1.  **Deploy Kontrak**
    Gunakan perintah `deploy` dari AlgoKit. Anda bisa menambahkan `--create-args` untuk memanggil metode `create` saat deploy.
    ```bash
    # Contoh deploy
    algokit project run deploy localnet
    ```

2.  **Memanggil Metode Kontrak**
    Setelah di-deploy, Anda bisa menggunakan `goal` atau _script_ untuk memanggil metode `issue_certificate` dan `verify_certificate`.

    **Contoh Menerbitkan Sertifikat (menggunakan `goal`):**
    ```bash
    # Ganti APP_ID dengan ID aplikasi Anda
    goal app method --app-id APP_ID --from <ALAMAT_KREATOR> --method "issue_certificate(string,string,uint64)uint64" --arg '"Nama Peserta"' --arg '"Developer Python"' --arg 1672531200
    ```

    **Contoh Memverifikasi Sertifikat (menggunakan `goal`):**
    ```bash
    goal app method --app-id APP_ID --from <ALAMAT_SIAPAPUN> --method "verify_certificate(uint64)string" --arg 1
    ```

## Langkah Selanjutnya

- **Kembangkan Frontend**: Gunakan starter frontend di `projects/sertifikat_kompetensi-frontend` untuk membuat antarmuka pengguna yang dapat berinteraksi dengan _smart contract_ ini.
- **Deploy ke TestNet**: Setelah pengujian di `localnet` berhasil, Anda dapat men-deploy kontrak ini ke `TestNet` agar dapat diakses secara publik.
- **Tambahkan Fitur**: Pertimbangkan untuk menambahkan fitur baru seperti pencabutan sertifikat (`revoke_certificate`) atau transfer kepemilikan.
