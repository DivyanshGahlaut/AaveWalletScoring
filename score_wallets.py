import sys
import json
import math
import csv
from collections import defaultdict

# Usage: python score_wallets.py input.json output.csv

if len(sys.argv) != 3:
    print("Usage: python score_wallets.py <input_json> <output_csv>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

# Load JSON
with open(input_file, 'r') as f:
    data = json.load(f)

print(f"Loaded {len(data)} transactions")  # ✅ Debug print

# Aggregate features per wallet
wallets = defaultdict(lambda: {
    'num_deposits': 0,
    'total_deposit_usd': 0.0,
    'num_borrows': 0,
    'total_borrow_usd': 0.0,
    'num_repayments': 0,
    'total_repay_usd': 0.0,
    'num_liquidations': 0,
    'timestamps': []
})

for record in data:
    w = record.get('userWallet')
    action = record.get('action', '').lower()
    ts = record.get('timestamp')
    action_data = record.get('actionData', {})

    amount = float(action_data.get('amount', 0))
    price = float(action_data.get('assetPriceUSD', 0))
    amount_usd = amount * price

    if w is None or ts is None:
        continue

    wallets[w]['timestamps'].append(ts)

    if action == 'deposit':
        wallets[w]['num_deposits'] += 1
        wallets[w]['total_deposit_usd'] += amount_usd
    elif action == 'borrow':
        wallets[w]['num_borrows'] += 1
        wallets[w]['total_borrow_usd'] += amount_usd
    elif action == 'repay':
        wallets[w]['num_repayments'] += 1
        wallets[w]['total_repay_usd'] += amount_usd
    elif action == 'liquidationcall':
        wallets[w]['num_liquidations'] += 1

# Compute scores
results = []

for w, f in wallets.items():
    deposit_score = math.log1p(f['total_deposit_usd'])
    repay_score = math.log1p(f['total_repay_usd'])

    if f['total_borrow_usd'] > 0:
        repay_ratio = f['total_repay_usd'] / f['total_borrow_usd']
        repay_ratio = min(repay_ratio, 1.0)
    else:
        repay_ratio = 1.0

    liquidation_penalty = f['num_liquidations'] * 0.1

    ts = sorted(f['timestamps'])
    if len(ts) > 1:
        gaps = [ts[i+1] - ts[i] for i in range(len(ts)-1)]
        avg_gap_days = sum(gaps) / len(gaps) / (60*60*24)
    else:
        avg_gap_days = 999

    bot_penalty = 0.0
    if avg_gap_days < 1:
        bot_penalty = 0.1

    raw_score = (
        deposit_score * 0.3
        + repay_score * 0.3
        + repay_ratio * 0.2
        - liquidation_penalty * 0.1
        - bot_penalty * 0.1
    )

    score = max(0, min(1000, raw_score * 100))

    results.append((w, int(score)))

# Write CSV
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['wallet_id', 'score'])
    for row in results:
        writer.writerow(row)

print(f"Done. Scored {len(results)} wallets → {output_file}")
