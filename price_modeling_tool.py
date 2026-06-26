import sys
from dataclasses import dataclass
from typing import List, Tuple

# Force UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Fixed parameters
PROD = 200
RAW = 5.50
BASE_HRS = 10.0
RATE = 25.00
LOG = 150.00
MKT = 100.00
WH_MARKUP = 0.40
RET_MARGIN = 0.30
TAX = 0.08

@dataclass
class Result:
    name: str
    hrs: float
    mat: float
    lab: float
    cogs: float
    opex: float
    invest: float
    unit: float
    wholesale: float
    retail: float
    tax_amt: float
    final: float
    profit: float

def compute(name: str, hrs: float) -> Result:
    mat = PROD * RAW
    lab = hrs * RATE
    cogs = mat + lab
    opex = LOG + MKT
    invest = cogs + opex
    unit = invest / PROD
    wholesale = unit * (1 + WH_MARKUP)
    retail = wholesale / (1 - RET_MARGIN)
    tax_amt = retail * TAX
    final = retail + tax_amt
    profit = (wholesale * PROD) - invest
    return Result(name, hrs, mat, lab, cogs, opex, invest, unit,
                  wholesale, retail, tax_amt, final, profit)

# ── Pretty printing helpers ──
def fmt(v: float) -> str: return f"${v:,.2f}"
def pct(v: float) -> str: return f"{v * 100:.0f}%"

def print_box(title: str, rows: List[Tuple[str, str, str, str]], width: int = 78):
    """Print a bordered table with header and optional delta column."""
    def line(left, *cols):
        content = f"  {left:<{30}}"
        for col in cols:
            content += f" {col:>{18}}"
        return f"║{content:<{width}}║"

    print("╔" + "═" * width + "╗")
    print(f"║{title:^{width}}║")
    print("╠" + "═" * width + "╣")
    # header
    hdr = line("Metric", "Baseline", "Breakdown") if len(rows[0]) == 3 else line("Step", "Formula", "Value")
    print(hdr)
    print("╟" + "─" * width + "╢")
    for row in rows:
        if len(row) == 3:
            left, a, b = row
            print(line(left, a, b))
        else:
            left, form, val = row
            # For audit, we show two lines per step
            print(f"│  {left:<{30}}  {formula:>{37}}  │" if left else "")
            # Actually adapt: we'll treat differently
    print("╚" + "═" * width + "╝")

def display_all(base: Result, breakd: Result):
    # Input parameters
    w = 62
    print("\n╔" + "═" * w + "╗")
    print(f"║{' ARTISAN ROAST — Price Modeling Tool '.center(w)}║")
    print(f"║{' Boutique Coffee · Product Launch Analysis '.center(w)}║")
    print("╠" + "═" * w + "╣")
    print("║ INPUT PARAMETERS".ljust(w) + "║")
    print("╠" + "═" * w + "╣")
    params = [
        ("Production Volume", f"{PROD} bags"),
        ("Raw Material Cost", f"{fmt(RAW)} / bag"),
        ("Baseline Labor Hours", f"{BASE_HRS:.0f} hrs"),
        ("Hourly Labor Rate", f"{fmt(RATE)} / hr"),
        ("Logistics (Shipping)", fmt(LOG)),
        ("Marketing (Social)", fmt(MKT)),
        ("Wholesale Markup", pct(WH_MARKUP)),
        ("Retailer Margin Target", pct(RET_MARGIN)),
        ("Sales Tax Rate", pct(TAX)),
    ]
    for label, val in params:
        print(f"║  {label:<28s} {val:>30s}  ║")
    print("╚" + "═" * w + "╝")

    # Comparison table
    w = 78
    rows = [
        ("Labor Hours", f"{base.hrs:.0f} hrs", f"{breakd.hrs:.0f} hrs"),
        ("Total Material Cost", fmt(base.mat), fmt(breakd.mat)),
        ("Total Labor Cost", fmt(base.lab), fmt(breakd.lab)),
        ("COGS", fmt(base.cogs), fmt(breakd.cogs)),
        ("OpEx (Logistics + Mktg)", fmt(base.opex), fmt(breakd.opex)),
        ("Total Investment", fmt(base.invest), fmt(breakd.invest)),
        ("Unit Cost", fmt(base.unit), fmt(breakd.unit)),
        ("", "", ""),  # spacer
        ("Wholesale Price", fmt(base.wholesale), fmt(breakd.wholesale)),
        ("Suggested Retail Price", fmt(base.retail), fmt(breakd.retail)),
        ("Sales Tax Amount", fmt(base.tax_amt), fmt(breakd.tax_amt)),
        ("Final Consumer Price", fmt(base.final), fmt(breakd.final)),
        ("", "", ""),
        ("Projected Net Profit", fmt(base.profit), fmt(breakd.profit)),
    ]
    print("\n╔" + "═" * w + "╗")
    print(f"║{' SCENARIO COMPARISON — Cost & Pricing Waterfall '.center(w)}║")
    print("╠" + "═" * w + "╣")
    print(f"║  {'Metric':<{30}} {'Baseline':>{18}}  {'Breakdown':>{18}} ║")
    print("╟" + "─" * w + "╢")
    for label, a, b in rows:
        if label == "":
            print("╟" + "─" * w + "╢")
        else:
            print(f"║  {label:<{30}} {a:>{18}}  {b:>{18}} ║")
    # profit impact line
    delta = breakd.profit - base.profit
    sign = "−" if delta < 0 else "+"
    print("╟" + "─" * w + "╢")
    print(f"║{'  Profit Impact of Breakdown:':<{w}}║")
    print(f"║  {sign}{fmt(abs(delta)):>74} ║")
    print("╚" + "═" * w + "╝")

    # Formula audits (one per scenario)
    for res in (base, breakd):
        w = 72
        print("\n┌" + "─" * w + "┐")
        print(f"│{f'  FORMULA AUDIT — {res.name}':<{w}}│")
        print("├" + "─" * w + "┤")
        steps = [
            ("1. Total Material Cost", f"{PROD} × {fmt(RAW)}", fmt(res.mat)),
            ("2. Total Labor Cost", f"{res.hrs:.0f} hrs × {fmt(RATE)}", fmt(res.lab)),
            ("3. COGS", f"{fmt(res.mat)} + {fmt(res.lab)}", fmt(res.cogs)),
            ("4. OpEx", f"{fmt(LOG)} + {fmt(MKT)}", fmt(res.opex)),
            ("5. Total Investment", f"{fmt(res.cogs)} + {fmt(res.opex)}", fmt(res.invest)),
            ("6. Unit Cost", f"{fmt(res.invest)} / {PROD}", fmt(res.unit)),
            ("7. Wholesale Price", f"{fmt(res.unit)} × (1 + {pct(WH_MARKUP)})", fmt(res.wholesale)),
            ("8. SRP (margin)", f"{fmt(res.wholesale)} / (1 − {pct(RET_MARGIN)})", fmt(res.retail)),
            ("9. Sales Tax", f"{fmt(res.retail)} × {pct(TAX)}", fmt(res.tax_amt)),
            ("10. Final Consumer Price", f"{fmt(res.retail)} + {fmt(res.tax_amt)}", fmt(res.final)),
            ("11. Projected Net Profit", f"({fmt(res.wholesale)} × {PROD}) − {fmt(res.invest)}", fmt(res.profit)),
        ]
        for step, form, val in steps:
            print(f"│  {step:<{30}} {form:>{28}}  =  {val:>{10}} │")
        print("└" + "─" * w + "┘")

def main():
    base = compute("Baseline", BASE_HRS)
    breakdown = compute("Machine Breakdown (2× Labor)", BASE_HRS * 2)
    display_all(base, breakdown)
    print()

if __name__ == "__main__":
    main()
