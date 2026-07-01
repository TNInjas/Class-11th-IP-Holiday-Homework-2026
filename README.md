# ☕ Artisan Roast — Price Modeling Tool

A simple Python script for modeling the pricing waterfall of a boutique coffee product launch. It computes unit cost, wholesale price, suggested retail price (SRP), and final consumer price with sales tax.

---

## 📋 Features

- **11-step sequential pricing waterfall** from raw materials to consumer shelf price
- **True retailer margin formula** for SRP (`Wholesale / (1 − Margin)`)
- **Interactive input** — Enter scenario name and labor hours at runtime
- **Complete pricing audit trail** showing all intermediate calculations
- **Sales tax calculation** applied to suggested retail price

---

## 🚀 Quick Start

**Prerequisites:** Python 3.6 or later. No third-party packages required.

```powershell
# Navigate to the project folder
cd "c:\Users\devel\Desktop\IP HHW"

# Run the tool
python price_modeling_tool.py
```

The script will prompt you to enter:
1. **Scenario Name** — A description of the scenario (e.g., "Baseline", "Machine Breakdown")
2. **Labor Hours** — Number of hours required for production

---

## 📁 Project Structure

```
IP HHW/
├── price_modeling_tool.py   # Main script — all logic and calculations
└── README.md                # This file
```

---

## ⚙️ Configuration

All input parameters are defined as constants at the top of [`price_modeling_tool.py`](./price_modeling_tool.py):

| Constant | Default | Description |
|---|---|---|
| `PROD` | `200` | Number of bags produced |
| `RAW` | `5.50` | Cost of raw materials per bag |
| `RATE` | `25.00` | Hourly labor rate |
| `LOG` | `150.00` | Logistics / shipping cost |
| `MKT` | `100.00` | Marketing spend |
| `WH_MARKUP` | `0.40` | 40% wholesale markup over unit cost |
| `RET_MARGIN` | `0.30` | 30% retailer margin (true margin formula) |
| `TAX` | `0.08` | 8% sales tax rate |

---

## 🧮 Pricing Waterfall (11 Steps)

| Step | Formula | Variable |
|---|---|---|
| 1. Total Material Cost | `Production Volume × Raw Material Cost` | `mat` |
| 2. Total Labor Cost | `Labor Hours × Hourly Labor Rate` | `lab` |
| 3. COGS | `Material Cost + Labor Cost` | `cogs` |
| 4. OpEx | `Logistics + Marketing` | `opex` |
| 5. Total Investment | `COGS + OpEx` | `invest` |
| 6. Unit Cost | `Total Investment / Production Volume` | `unit` |
| 7. Wholesale Price | `Unit Cost × (1 + Wholesale Markup)` | `wholesale` |
| 8. Suggested Retail Price | `Wholesale Price / (1 − Retailer Margin)` | `retail` |
| 9. Sales Tax Amount | `SRP × Sales Tax Rate` | `tax_amt` |
| 10. Final Consumer Price | `SRP + Sales Tax Amount` | `final` |
| 11. Projected Net Profit | `(Wholesale Price × Production Volume) − Total Investment` | `profit` |

---

## 📊 Sample Output

When you run the script, it produces output like this:

```
----------------------------
PRICE MODELING REPORT
----------------------------
Scenario: Baseline
Labor Hours: 10.0 hrs
Material Cost: $ 1100.0
Labor Cost: $ 250.0
COGS (Cost of Goods Sold): $ 1350.0
Operating Expenses: $ 250.0
Total Investment: $ 1600.0
Unit Cost: $ 8.0
Wholesale Price: $ 11.2
Suggested Retail Price (SRP): $ 16.0
Sales Tax Amount: $ 1.28
Final Consumer Price: $ 17.28
Projected Net Profit: $ 640.0
```

---

## 💡 Example Scenarios

Run the script multiple times with different inputs to analyze different scenarios:

| Scenario | Labor Hours | Impact |
|---|---|---|
| **Baseline** | 10 | Normal operating conditions |
| **Machine Breakdown** | 20 | Equipment failure; doubled labor time |
| **Overtime** | 15 | Extra shifts required |

Compare the **Final Consumer Price** and **Projected Net Profit** across scenarios to understand the impact of operational disruptions.

---

## 📝 License

This project is for internal product launch planning purposes.
