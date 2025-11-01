from algopy import ARC4Contract, GlobalState, BoxMap, UInt64, Account, Txn, Global
from algopy.arc4 import abimethod, String


class SertifikatKompetensi(ARC4Contract):
    def __init__(self) -> None:
        # Menyimpan jumlah total sertifikat yang diterbitkan
        self.total_certificates = GlobalState(UInt64(0))
        # Menyimpan sertifikat berdasarkan ID (UInt64 → String berisi hash unik sertifikat)
        self.certificates = BoxMap(UInt64, String)
        # Menyimpan penerbit (Account → Boolean-like UInt64)
        self.approved_issuers = BoxMap(Account, UInt64)

    @abimethod(create="require")
    def create(self) -> None:
        """
        Dipanggil saat kontrak dibuat.
        Menandai creator sebagai issuer yang sah.
        """
        self.approved_issuers[Global.creator_address] = UInt64(1)

    @abimethod
    def add_issuer(self, new_issuer: Account) -> String:
        """
        Menambahkan akun yang diizinkan untuk menerbitkan sertifikat.
        Hanya creator yang bisa menambah issuer.
        """
        assert Txn.sender == Global.creator_address, "Only creator can add issuers"
        self.approved_issuers[new_issuer] = UInt64(1)
        return String("Issuer added successfully")

    @abimethod
    def issue_certificate(self, certificate_hash: String) -> UInt64:
        """
        Menerbitkan sertifikat baru dengan hash unik (misalnya hash SHA256 dari file PDF).
        """
        # Pastikan hanya issuer sah yang bisa menerbitkan
        is_issuer, valid = self.approved_issuers.maybe(Txn.sender)
        assert valid and is_issuer == UInt64(1), "Unauthorized issuer"

        # Naikkan total sertifikat dan buat ID baru
        new_id = self.total_certificates.value + UInt64(1)
        self.total_certificates.value = new_id

        # Simpan hash sertifikat
        self.certificates[new_id] = certificate_hash

        return new_id

    @abimethod
    def verify_certificate(self, certificate_id: UInt64, certificate_hash: String) -> String:
        """
        Memverifikasi apakah hash sertifikat sesuai dengan yang tersimpan.
        """
        stored_hash = self.certificates[certificate_id]
        if stored_hash == certificate_hash:
            return String("Sertifikat valid dan terdaftar.")
        else:
            return String("Sertifikat tidak valid atau telah dipalsukan.")

    @abimethod
    def get_certificate(self, certificate_id: UInt64) -> String:
        """
        Mengambil hash sertifikat berdasarkan ID (misalnya untuk menampilkan data di front-end).
        """
        return self.certificates[certificate_id]
