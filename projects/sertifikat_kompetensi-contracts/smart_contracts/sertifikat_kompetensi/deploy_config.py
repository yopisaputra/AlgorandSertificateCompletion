import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.account import Account

from smart_contracts.artifacts.sertifikat_kompetensi.contract import SertifikatKompetensiClient


def deploy(
    algod_client: AlgodClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: Account,
) -> None:
    """
    Deploy the SertifikatKompetensi contract
    """

    # Initialize the client
    app_client = SertifikatKompetensiClient(
        algod_client=algod_client,
        signer=deployer,
    )

    # Deploy the contract using the create method
    app_client.create()

    print(f"Contract deployed successfully!")
    print(f"App ID: {app_client.app_id}")
    print(f"Deployer: {deployer.address}")
