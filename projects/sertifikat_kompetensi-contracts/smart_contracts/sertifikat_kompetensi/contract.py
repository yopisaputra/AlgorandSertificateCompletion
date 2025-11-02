from algopy import ARC4Contract, GlobalState, BoxMap, UInt64, Account, Txn, Global, arc4
from algopy.arc4 import abimethod, String


class SertifikatKompetensi(ARC4Contract):
    def __init__(self) -> None:
        # Menyimpan jumlah total sertifikat yang diterbitkan
        self.total_certificates = GlobalState(UInt64(0))
        # Menyimpan sertifikat berdasarkan ID (UInt64 → String berisi hash unik sertifikat)
        self.certificates = BoxMap(UInt64, String)
        # Menyimpan penerbit (Account → Boolean-like UInt64)
        self.approved_issuers = BoxMap(Account, UInt64)
        # Menyimpan metadata tambahan sertifikat (ID → JSON string)
        self.certificate_metadata = BoxMap(UInt64, String)

    @abimethod(create="require")
    def create(self) -> None:
        """
        Dipanggil saat kontrak dibuat.
        Menandai creator sebagai issuer yang sah.
        Tidak membutuhkan parameter apapun.
        """
        self.approved_issuers[Global.creator_address] = UInt64(1)
        self.total_certificates.value = UInt64(0)

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
    def remove_issuer(self, issuer: Account) -> String:
        """
        Menghapus akun dari daftar issuer yang disetujui.
        Hanya creator yang bisa menghapus issuer.
        """
        assert Txn.sender == Global.creator_address, "Only creator can remove issuers"
        assert issuer != Global.creator_address, "Cannot remove creator as issuer"

        self.approved_issuers[issuer] = UInt64(0)
        return String("Issuer removed successfully")

    @abimethod
    def is_approved_issuer(self, account: Account) -> arc4.Bool:
        """
        Memeriksa apakah akun merupakan issuer yang disetujui.
        """
        is_issuer, exists = self.approved_issuers.maybe(account)
        return arc4.Bool(exists and is_issuer == UInt64(1))

    @abimethod
    def issue_certificate(self, certificate_hash: String, metadata: String) -> UInt64:
        """
        Menerbitkan sertifikat baru dengan hash unik dan metadata.
        """
        # Pastikan hanya issuer sah yang bisa menerbitkan
        is_issuer, valid = self.approved_issuers.maybe(Txn.sender)
        assert valid and is_issuer == UInt64(1), "Unauthorized issuer"

        # Naikkan total sertifikat dan buat ID baru
        new_id = self.total_certificates.value + UInt64(1)
        self.total_certificates.value = new_id

        # Simpan hash sertifikat
        self.certificates[new_id] = certificate_hash

        # Simpan metadata
        self.certificate_metadata[new_id] = metadata

        return new_id

    @abimethod
    def issue_certificate_simple(self, certificate_hash: String) -> UInt64:
        """
        Menerbitkan sertifikat baru tanpa metadata.
        """
        # Pastikan hanya issuer sah yang bisa menerbitkan
        is_issuer, valid = self.approved_issuers.maybe(Txn.sender)
        assert valid and is_issuer == UInt64(1), "Unauthorized issuer"

        # Naikkan total sertifikat dan buat ID baru
        new_id = self.total_certificates.value + UInt64(1)
        self.total_certificates.value = new_id

        # Simpan hash sertifikat
        self.certificates[new_id] = certificate_hash

        # Simpan metadata kosong
        self.certificate_metadata[new_id] = String("")

        return new_id

    @abimethod
    def verify_certificate(self, certificate_id: UInt64, certificate_hash: String) -> arc4.Bool:
        """
        Memverifikasi apakah hash sertifikat sesuai dengan yang tersimpan.
        Mengembalikan boolean.
        """
        stored_hash, exists = self.certificates.maybe(certificate_id)
        if exists and stored_hash == certificate_hash:
            return arc4.Bool(True)
        else:
            return arc4.Bool(False)

    @abimethod
    def get_certificate(self, certificate_id: UInt64) -> String:
        """
        Mengambil hash sertifikat berdasarkan ID.
        """
        stored_hash, exists = self.certificates.maybe(certificate_id)
        if exists:
            return stored_hash
        else:
            return String("")

    @abimethod
    def get_certificate_metadata(self, certificate_id: UInt64) -> String:
        """
        Mengambil metadata sertifikat berdasarkan ID.
        """
        metadata, exists = self.certificate_metadata.maybe(certificate_id)
        if exists:
            return metadata
        else:
            return String("")

    @abimethod
    def update_certificate_metadata(self, certificate_id: UInt64, new_metadata: String) -> String:
        """
        Memperbarui metadata sertifikat.
        Hanya issuer yang menerbitkan sertifikat asli atau creator yang bisa update.
        """
        # Pastikan sertifikat exists
        stored_hash, exists = self.certificates.maybe(certificate_id)
        assert exists, "Certificate does not exist"

        # Pastikan hanya issuer sah atau creator yang bisa update
        is_issuer, valid = self.approved_issuers.maybe(Txn.sender)
        assert (valid and is_issuer == UInt64(1)) or Txn.sender == Global.creator_address, "Unauthorized"

        self.certificate_metadata[certificate_id] = new_metadata
        return String("Metadata updated successfully")

    @abimethod
    def get_total_certificates(self) -> UInt64:
        """
        Mengembalikan total jumlah sertifikat yang telah diterbitkan.
        """
        return self.total_certificates.value

    @abimethod
    def revoke_certificate(self, certificate_id: UInt64) -> String:
        """
        Mencabut sertifikat (menghapus dari storage).
        Hanya creator yang bisa mencabut sertifikat.
        """
        assert Txn.sender == Global.creator_address, "Only creator can revoke certificates"

        # Hapus sertifikat dan metadata
        del self.certificates[certificate_id]
        metadata, exists = self.certificate_metadata.maybe(certificate_id)
        if exists:
            del self.certificate_metadata[certificate_id]

        return String("Certificate revoked successfully")
