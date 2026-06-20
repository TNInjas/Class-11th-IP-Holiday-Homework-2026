# ☕ Artisan Roast — Price Modeling Tool

A clean, production-ready Python script for modeling the full pricing waterfall of a boutique coffee product launch. It computes unit cost, wholesale price, suggested retail price (SRP), final consumer price, and projected net profit — then runs a **Machine Breakdown Scenario** side-by-side for risk analysis.

---

## 📋 Features

- **11-step sequential pricing waterfall** from raw materials to consumer shelf price
- **True retailer margin formula** for SRP (`Wholesale / (1 − Margin)`)
- **Scenario Analysis** — Baseline vs. Machine Breakdown (doubled labor hours)
- **Formatted terminal UI** — ASCII-bordered tables with side-by-side comparison
- **Step-by-step formula audit** trail showing inputs and outputs for every calculation
- **Modular design** — `calculate_scenario()` can be imported and reused in other scripts

---

## 🚀 Quick Start

**Prerequisites:** Python 3.10 or later. No third-party packages required.

```powershell
# Navigate to the project folder
cd "c:\Users\devel\Desktop\IP HHW"

# Run the tool
python price_modeling_tool.py
```

---

## 📁 Project Structure

```
IP HHW/
├── price_modeling_tool.py   # Main script — all logic, calculations, and output
└── README.md                # This file
```

---

## ⚙️ Configuration

All input parameters are defined as constants at the top of [`price_modeling_tool.py`](./price_modeling_tool.py) (lines 22–30). Edit these values to model your own product launch:

| Constant | Default | Description |
|---|---|---|
| `PRODUCTION_VOLUME` | `200` | Number of bags produced |
| `RAW_MATERIAL_COST` | `$5.50` | Cost of raw materials per bag |
| `BASELINE_LABOR_HOURS` | `10.0` | Labor hours under normal conditions |
| `HOURLY_LABOR_RATE` | `$25.00` | Cost per labor hour |
| `LOGISTICS_COST` | `$150.00` | Flat shipping / freight cost |
| `MARKETING_COST` | `$100.00` | Flat social media marketing spend |
| `WHOLESALE_MARKUP` | `0.40` | 40% markup over unit cost |
| `RETAILER_MARGIN_TARGET` | `0.30` | 30% retailer margin (true margin formula) |
| `SALES_TAX_RATE` | `0.08` | 8% sales tax applied to SRP |

---

## 🧮 Pricing Waterfall (11 Steps)

| Step | Formula |
|---|---|
| 1. Total Material Cost | `Production Volume × Raw Material Cost` |
| 2. Total Labor Cost | `Labor Hours × Hourly Labor Rate` |
| 3. COGS | `Total Material Cost + Total Labor Cost` |
| 4. OpEx | `Logistics + Marketing` |
| 5. Total Investment | `COGS + OpEx` |
| 6. Unit Cost | `Total Investment / Production Volume` |
| 7. Wholesale Price | `Unit Cost × (1 + Wholesale Markup)` |
| 8. Suggested Retail Price | `Wholesale Price / (1 − Retailer Margin)` |
| 9. Sales Tax Amount | `SRP × Sales Tax Rate` |
| 10. Final Consumer Price | `SRP + Sales Tax Amount` |
| 11. Projected Net Profit | `(Wholesale Price × Production Volume) − Total Investment` |

---

## 📊 Sample Output (Baseline Values)

```
║  Metric                         Baseline        Breakdown       ║
╟─────────────────────────────────────────────────────────────────╢
║  ▸ COST BUILD-UP                                                ║
║  Labor Hours                     10 hrs           20 hrs        ║
║  Total Material Cost          $1,100.00        $1,100.00        ║
║  Total Labor Cost               $250.00          $500.00        ║
║  COGS                         $1,350.00        $1,600.00        ║
║  OpEx (Logistics + Mktg)        $250.00          $250.00        ║
║  Total Investment             $1,600.00        $1,850.00        ║
║  Unit Cost                        $8.00            $9.25        ║
╟─────────────────────────────────────────────────────────────────╢
║  ▸ PRICING CHAIN                                                ║
║  Wholesale Price                 $11.20           $12.95        ║
║  Suggested Retail Price          $16.00           $18.50        ║
║  Sales Tax Amount                 $1.28            $1.48        ║
║  Final Consumer Price            $17.28           $19.98        ║
╟─────────────────────────────────────────────────────────────────╢
║  ▸ PROFITABILITY                                                ║
║  Projected Net Profit           $640.00          $740.00        ║
╚═════════════════════════════════════════════════════════════════╝
```

---

## 🔌 Programmatic Usage

`calculate_scenario()` can be imported into any other Python script for custom analysis:

```python
from price_modeling_tool import calculate_scenario

result = calculate_scenario(
    scenario_name="Holiday Launch",
    labor_hours=15.0,
    production_volume=500,
)

print(f"Final Consumer Price: ${result.final_consumer_price:.2f}")
print(f"Projected Net Profit: ${result.projected_net_profit:.2f}")
```

All results are returned as a `ScenarioResult` dataclass with named fields for every metric (e.g. `result.unit_cost`, `result.wholesale_price`, `result.suggested_retail_price`).

---

## 🧪 Scenario Analysis

The script automatically runs two scenarios back-to-back:

| Scenario | Labor Hours | Key Difference |
|---|---|---|
| **Baseline** | 10 hrs | Normal operating conditions |
| **Machine Breakdown** | 20 hrs | Equipment failure doubles labor time |

The profit impact of the disruption is printed at the bottom of the comparison table.

---

## 📝 License

This project is for internal product launch planning purposes.
