import logging
import algokit_utils

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy() -> None:
    # Impor argumen untuk metode yang ADA di kontrak Anda,
    # bukan 'HelloArgs'
    from smart_contracts.artifacts.sertifikat_kompetensi.sertifikat_kompetensi_client import (
        IssueCertificateArgs,
        VerifyCertificateArgs,
        SertifikatKompetensiFactory,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer_ = algorand.account.from_environment("DEPLOYER")

    factory = algorand.client.get_typed_app_factory(
        SertifikatKompetensiFactory, default_sender=deployer_.address
    )

    # --- PERBAIKAN DI SINI ---
    # Mengganti strategi 'on_update' dan 'on_schema_break'.
    # 'ReplaceApp' akan menghapus app lama dan membuat yang baru.
    # Ini menghindari error 'update' pada kontrak ARC4 yang tidak memiliki
    # metode @abimethod(update="...")
    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.ReplaceApp,
        on_schema_break=algokit_utils.OnSchemaBreak.ReplaceApp,
    )

    # Pendanaan 1 ALGO ke akun aplikasi ini baik untuk MBR
    if result.operation_performed in [
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ]:
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer_.address,
                receiver=app_client.app_address,
            )
        )

    # GANTI dengan panggilan ke metode Anda yang sebenarnya.
    # Saat deploy, 'deployer_' adalah 'creator', dan 'creator'
    # otomatis ditambahkan sebagai 'issuer' oleh fungsi create() Anda.
    # Jadi, 'deployer_' bisa langsung menerbitkan sertifikat.

    logger.info("Mencoba menerbitkan sertifikat pertama setelah deploy...")

    cert_hash = "hash_unik_sertifikat_pertama_abc123"

    # Panggil 'issue_certificate'
    issue_response = app_client.send.issue_certificate(
        args=IssueCertificateArgs(certificate_hash=cert_hash)
    )
    new_id = issue_response.abi_return

    logger.info(
        f"Berhasil memanggil issue_certificate pada {app_client.app_name} ({app_client.app_id}). "
        f"Hash={cert_hash}, ID Sertifikat Baru: {new_id}"
    )

    # (Opsional) Anda juga bisa langsung memverifikasinya
    logger.info("Mencoba memverifikasi sertifikat yang baru dibuat...")
    verify_response = app_client.send.verify_certificate(
        args=VerifyCertificateArgs(certificate_id=new_id, certificate_hash=cert_hash)
    )
    logger.info(f"Hasil verifikasi: {verify_response.abi_return}")
