import sys
from dataclasses import dataclass
from typing import List

# Force UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Fixed parameters (Can be modified)
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

# ── Formatting and Printing Helpers ──
def print_results(results: List[Result]):
    from dataclasses import fields

    # Define custom labels for the fields to make them highly readable
    labels = {
        "hrs": "Labor Hours",
        "mat": "Material Cost",
        "lab": "Labor Cost",
        "cogs": "COGS (Cost of Goods Sold)",
        "opex": "OpEx (Operating Expenses)",
        "invest": "Total Investment",
        "unit": "Unit Cost",
        "wholesale": "Wholesale Price",
        "retail": "Suggested Retail Price (SRP)",
        "tax_amt": "Sales Tax Amount",
        "final": "Final Consumer Price",
        "profit": "Projected Net Profit",
    }
    
    def format_val(field_name: str, val) -> str:
        if field_name == "hrs":
            return f"{val:.1f} hrs"
        return f"${val:,.2f}"

    for r in results:
        print(f"Scenario: {r.name}")
        for field in fields(Result):
            if field.name == "name":
                continue
            label = labels.get(field.name, field.name)
            val = getattr(r, field.name)
            print(f"  {label}: {format_val(field.name, val)}")
        print()

def main():
    base = compute("Baseline", BASE_HRS)
    breakdown = compute("Machine Breakdown", BASE_HRS * 2)
    
    print("\nARTISAN ROAST — PRICE MODELING REPORT")
    print_results([base, breakdown])

if __name__ == "__main__":
    main()
