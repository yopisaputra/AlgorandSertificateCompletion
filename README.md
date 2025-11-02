# Sertifikat Kompetensi - Algorand Smart Contract

This project contains an Algorand smart contract for managing digital competency certificates (`Sertifikat Kompetensi`). It provides a secure, transparent, and decentralized way to issue, manage, and verify certificates on the blockchain.

This project is built using AlgoKit.

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python** (3.10 or higher)
- **Docker** (for running a local Algorand network)
- **PipX** (for installing Python CLI applications in isolated environments)
  ```bash
  python3 -m pip install --user pipx
  python3 -m pipx ensurepath
  ```

### Installation

1.  **Install AlgoKit**:
    Use `pipx` to install the Algorand AlgoKit CLI.
    ```bash
    pipx install algokit
    ```

2.  **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd sertifikat_kompetensi
    ```

3.  **Bootstrap the Project**:
    This command sets up the Python virtual environment and installs all the necessary dependencies for the project.
    ```bash
    algokit bootstrap all
    ```

## ⚙️ Usage Guide

This project uses AlgoKit to streamline development, testing, and deployment. Here are the most common commands you'll use.

### LocalNet

AlgoKit provides a local Algorand network running in Docker for development and testing.

*   **Start LocalNet**:
    ```bash
    algokit localnet start
    ```

*   **Stop LocalNet**:
    ```bash
    algokit localnet stop
    ```

*   **Explore LocalNet**:
    Once started, you can access the Daffi Web Wallet to manage accounts and the AlgoExplorer to view transactions.

### Smart Contract Development

All smart contract code is located in the `projects/sertifikat_kompetensi-contracts/smart_contracts/` directory.

*   **Build the Contract**:
    Compile the PyTEAL smart contract into TEAL and generate the application specification (`app.json`).
    ```bash
    algokit build
    ```
    The build artifacts will be placed in the `projects/sertifikat_kompetensi-contracts/smart_contracts/artifacts/` directory.

*   **Run Tests**:
    Execute the contract tests located in the `tests/` directory. Make sure your LocalNet is running.
    ```bash
    algokit test
    ```

### Deployment

You can deploy the smart contract to LocalNet, TestNet, or MainNet.

1.  **Set Up Your Deployer Account**:
    Create a `.env` file in the project root by copying the `.env.template` file.
    ```bash
    cp .env.template .env
    ```
    Update the `.env` file with the private key (mnemonic) of the account you want to use for deployment. For LocalNet, you can get pre-funded account mnemonics by running:
    ```bash
    algokit localnet wallet list
    ```

2.  **Deploy the Contract**:
    Run the deploy command. By default, it deploys to `localnet`.
    ```bash
    algokit deploy
    ```
    To deploy to another network like `testnet`, use the `--network` flag:
    ```bash
    algokit deploy --network testnet
    ```
    After a successful deployment, the App ID will be printed to the console and saved in the `.algokit.app.yaml` file for future interactions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.