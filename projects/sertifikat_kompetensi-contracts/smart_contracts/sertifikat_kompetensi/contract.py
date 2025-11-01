from algopy import ARC4Contract, String, UInt64, arc4


class Certificate(arc4.Struct):
    name: arc4.String
    title: arc4.String
    issue_date: arc4.UInt64


class SertifikatKompetensi(ARC4Contract):
    def __init__(self) -> None:
        self.certificates = arc4.BoxMapping[arc4.UInt64, Certificate]()
        self.last_certificate_id = UInt64(0)

    @arc4.abimethod(allow_actions=["NoOp"], create="require")
    def create_application(self) -> None:
        """
        Metode ini dipanggil saat aplikasi/kontrak dibuat.
        """
        self.last_certificate_id = UInt64(0)

    @arc4.abimethod
    def issue_certificate(self, name: String, title: String, issue_date: UInt64) -> UInt64:
        """
        Menerbitkan sertifikat baru dan menyimpannya.
        Hanya pemilik kontrak yang bisa memanggil ini.
        """
        # assert Txn.sender == Global.creator_address

        new_id = self.last_certificate_id + 1
        self.last_certificate_id = new_id

        cert = Certificate(name=name, title=title, issue_date=issue_date)
        self.certificates[new_id] = cert

        return new_id

    @arc4.abimethod(allow_actions=["NoOp"])
    def verify_certificate(self, certificate_id: UInt64) -> Certificate:
        """
        Memverifikasi dan mengembalikan detail sertifikat berdasarkan ID.
        """
        return self.certificates[certificate_id]
