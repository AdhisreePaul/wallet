import json
import pandas as pd
import numpy as np
from collections import defaultdict
from typing import Any, Dict


def compute_score(row):
    score = 0

    # Repay ratio (max 1) → 0–300 points
    repay_ratio = min(row['repay_ratio'], 1.0)
    score += 300 * repay_ratio

    # Redeem ratio (max 1) → 0–200 points
    redeem_ratio = min(row['redeem_ratio'], 1.0)
    score += 200 * redeem_ratio

    # No liquidation → +100
    score += 100 if row['num_liquidation'] == 0 else 0

    # Transaction volume → log-scaled 0–150
    tx_score = min(np.log1p(row['total_tx']) / np.log(500) * 150, 150)
    score += tx_score

    # Duration of activity → log-scaled 0–150
    duration_score = min(np.log1p(row['tx_duration_sec']) / np.log(1e7) * 150, 150)
    score += duration_score

    # Asset diversity → up to 100
    diversity_score = min(row['num_assets'], 10) / 10 * 100
    score += diversity_score

    return round(min(score, 1000))


def usd_amount(action):
    try:
        amount = float(action["actionData"]["amount"])
        price = float(action["actionData"]["assetPriceUSD"])
        return amount * price
    except (KeyError, ValueError):
        return 0.0


def extract_features(transactions):
    wallet_features: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
        "total_tx": 0,
        "deposit_usd": 0.0,
        "borrow_usd": 0.0,
        "repay_usd": 0.0,
        "redeem_usd": 0.0,
        "num_deposit": 0,
        "num_borrow": 0,
        "num_repay": 0,
        "num_redeem": 0,
        "num_liquidation": 0,
        "assets_used": set(),
        "timestamps": []
    })

    for tx in transactions:
        wallet = tx["userWallet"]
        action = tx["action"]
        data = tx.get("actionData", {})
        usd = usd_amount(tx)
        asset = data.get("assetSymbol", "")
        ts = tx.get("timestamp")

        wallet_features[wallet]["total_tx"] += 1
        wallet_features[wallet]["assets_used"].add(asset)
        if ts: wallet_features[wallet]["timestamps"].append(ts)

        if action == "deposit":
            wallet_features[wallet]["deposit_usd"] += usd
            wallet_features[wallet]["num_deposit"] += 1
        elif action == "borrow":
            wallet_features[wallet]["borrow_usd"] += usd
            wallet_features[wallet]["num_borrow"] += 1
        elif action == "repay":
            wallet_features[wallet]["repay_usd"] += usd
            wallet_features[wallet]["num_repay"] += 1
        elif action == "redeemunderlying":
            wallet_features[wallet]["redeem_usd"] += usd
            wallet_features[wallet]["num_redeem"] += 1
        elif action == "liquidationcall":
            wallet_features[wallet]["num_liquidation"] += 1

    records = []
    for wallet, feats in wallet_features.items():
        timestamps = sorted(feats["timestamps"])
        duration = (timestamps[-1] - timestamps[0]) if len(timestamps) > 1 else 0
        avg_gap = (duration / (len(timestamps) - 1)) if len(timestamps) > 1 else 0

        records.append({
            "wallet": wallet,
            "total_tx": feats["total_tx"],
            "num_assets": len(feats["assets_used"]),
            "deposit_usd": feats["deposit_usd"],
            "borrow_usd": feats["borrow_usd"],
            "repay_usd": feats["repay_usd"],
            "redeem_usd": feats["redeem_usd"],
            "num_deposit": feats["num_deposit"],
            "num_borrow": feats["num_borrow"],
            "num_repay": feats["num_repay"],
            "num_redeem": feats["num_redeem"],
            "num_liquidation": feats["num_liquidation"],
            "repay_ratio": feats["repay_usd"] / feats["borrow_usd"] if feats["borrow_usd"] > 0 else 0,
            "redeem_ratio": feats["redeem_usd"] / feats["deposit_usd"] if feats["deposit_usd"] > 0 else 0,
            "tx_duration_sec": duration,
            "avg_tx_gap_sec": avg_gap
        })

    return pd.DataFrame(records)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to user-wallet-transactions.json")
    parser.add_argument("--output", default="wallet_scores.csv", help="Output CSV file")
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        transactions = json.load(f)

    df = extract_features(transactions)
    df["credit_score"] = df.apply(compute_score, axis=1)
    df[["wallet", "credit_score"]].to_csv(args.output, index=False)
    print(f"Saved scores to {args.output}")


if __name__ == "__main__":
    main()
