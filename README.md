# On-Chain Wallet Credit Scoring Engine

This project provides a Python-based framework for calculating a credit score for blockchain wallets based on their on-chain transaction history. The score is derived from various transactional features to gauge the reliability and activity level of a wallet. The project includes scripts to both process transaction data to generate scores and to visualize the resulting score distribution.

## Architecture & Processing Flow

The system is composed of two primary scripts that form a sequential pipeline:

1.  **`score_wallet.py` (The Scoring Engine)**: This is the core component. It ingests raw transaction data from a JSON file, processes it to extract key features for each wallet, and applies a scoring model to calculate a final credit score.
2.  **`plot_scores.py` (The Visualizer)**: This script takes the output from the scoring engine (a CSV file) and generates a histogram to visualize the distribution of credit scores across all wallets.

The end-to-end processing flow is as follows:

```
Input Transactions (JSON)  -->  [ score_wallet.py ]  -->  Wallet Scores (CSV)  -->  [ plot_scores.py ]  -->  Score Distribution Graph (PNG)
```

---

## Credit Scoring Methodology

The credit score is a composite metric calculated on a scale of 0 to 1000. It is derived from a weighted model that evaluates several aspects of a wallet's on-chain behavior. The model rewards financial reliability, long-term engagement, and protocol interaction diversity.

The final score is a sum of the following components:

| Factor                | Max Points | Rationale                                                                                             |
| --------------------- | :--------: | ----------------------------------------------------------------------------------------------------- |
| **Repay Ratio**       |    300     | Measures the wallet's reliability by comparing the total USD value of repayments to borrows. A higher ratio indicates responsible borrowing. |
| **Redeem Ratio**      |    200     | Compares the total USD value of redeemed collateral to deposits. It rewards the completion of the deposit/redeem cycle. |
| **No Liquidations**   |    100     | A flat bonus awarded to wallets that have never had a position liquidated, indicating effective collateral management. |
| **Transaction Volume**|    150     | A log-scaled score based on the total number of transactions. It rewards wallets for being active on the protocol. |
| **Activity Duration** |    150     | A log-scaled score based on the time between the first and last transaction. It rewards long-term, consistent engagement. |
| **Asset Diversity**   |    100     | A linear score based on the number of unique assets the wallet has interacted with (capped at 10), rewarding broader protocol usage. |

---

## How to Use

Follow these steps to set up the project and run the analysis.

### 1. Prerequisites
- Python 3.x
- `pip` (Python package installer)

### 2. Setup

First, set up a virtual environment to manage project dependencies.

```shell
# Create a virtual environment
python -m venv .venv

# Activate the environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
# source .venv/bin/activate

# Install the required libraries
pip install pandas numpy matplotlib
```

### 3. Run the Scoring Engine

Use `score_wallet.py` to process your transaction data and generate scores. You must provide the path to your input JSON file.

```shell
python score_wallet.py --input path/to/your/transactions.json
```
This will create a `wallet_scores.csv` file in your project directory.

### 4. Generate the Visualization

After the scores have been generated, run `plot_scores.py` to create a histogram of the results.

```shell
python plot_scores.py
```
This will read `wallet_scores.csv`, save a graph named `credit_score_distribution.png`, and display the plot on your screen.

