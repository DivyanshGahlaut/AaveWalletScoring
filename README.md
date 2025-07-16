# AaveWalletScoring

## 📌 Project Overview

This project develops a simple **credit scoring model** for wallets interacting with the **Aave V2 protocol** using raw transaction-level DeFi data.

Each wallet gets a score between **0 and 1000**:
- **Higher score:** indicates reliable & responsible usage.
- **Lower score:** indicates risky, bot-like, or exploitative behavior.

---

## ⚙️ How It Works

1. **Input:**  
   - `user-wallet-transactions.json`  
   - Contains raw transactions: `deposit`, `borrow`, `repay`, `redeemunderlying`, `liquidationcall`.

2. **Feature Engineering:**  
   - Total deposits & borrows (USD value)
   - Total repayments
   - Number of liquidations
   - Transaction frequency (to detect bots)

3. **Scoring Logic:**  
   - More deposits & repayments → higher score.
   - More liquidations & bot-like patterns → lower score.
   - Scores normalized between **0–1000** for easy interpretation.

4. **Output:**  
   - `scores.csv`  
   - Contains: `wallet_id, score`.

---

## 🚀 How To Run

```bash
python score_wallets.py user-wallet-transactions.json scores.csv

AaveWalletScoring/
 ├── score_wallets.py
 ├── user-wallet-transactions.json
 ├── scores.csv
 ├── README.md
 ├── analysis.md


📈 Deliverables
.score_wallets.py → Python script to generate wallet scores.

.README.md → this file.

.analysis.md → describes score distribution & wallet behavior in each score range.

.scores.csv → output with all wallet scores.

#OUTPUT

<img width="1539" height="521" alt="Image" src="https://github.com/user-attachments/assets/b9857df6-f4b2-429f-9fd2-1422feaf306f" />
