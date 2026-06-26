import sys

# Force UTF‑8 output on Windows (so box‑drawing characters display correctly)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# ─── FIXED INPUT PARAMETERS ──────────────────────────────────────
PRODUCTION_VOLUME = 200          # bags
RAW_MATERIAL_COST = 5.50         # $/bag
BASELINE_LABOR_HOURS = 10.0      # hours
HOURLY_LABOR_RATE = 25.00        # $/hour
LOGISTICS_COST = 150.00          # flat shipping
MARKETING_COST = 100.00          # flat social media spend
WHOLESALE_MARKUP = 0.40          # 40%
RETAILER_MARGIN_TARGET = 0.30    # 30%
SALES_TAX_RATE = 0.08            # 8%

# ─── HELPER FORMATTING FUNCTIONS ────────────────────────────────
def fmt(value):
    """Return a dollar string with two decimals."""
    return f"${value:,.2f}"

def pct(value):
    """Return a percentage string (e.g., 0.40 → '40%')."""
    return f"{value * 100:.0f}%"

# ─── CORE CALCULATION ─────────────────────────────────────────────
def calculate_scenario(name, labor_hours):
    """
    Compute all metrics for a given scenario name and labor hours.
    Returns a dictionary with all results.
    """
    # 1. Total material cost
    total_material = PRODUCTION_VOLUME * RAW_MATERIAL_COST

    # 2. Total labor cost
    total_labor = labor_hours * HOURLY_LABOR_RATE

    # 3. Cost of Goods Sold (COGS)
    cogs = total_material + total_labor

    # 4. Operating expenses
    opex = LOGISTICS_COST + MARKETING_COST

    # 5. Total investment
    total_investment = cogs + opex

    # 6. Cost per bag (unit cost)
    unit_cost = total_investment / PRODUCTION_VOLUME

    # 7. Wholesale price (cost‑plus markup)
    wholesale = unit_cost * (1 + WHOLESALE_MARKUP)

    # 8. Suggested retail price (true margin formula)
    retail = wholesale / (1 - RETAILER_MARGIN_TARGET)

    # 9. Sales tax amount
    sales_tax = retail * SALES_TAX_RATE

    # 10. Final consumer price (including tax)
    final_price = retail + sales_tax

    # 11. Projected net profit
    profit = (wholesale * PRODUCTION_VOLUME) - total_investment

    # Return all values in a dictionary
    return {
        "name": name,
        "labor_hours": labor_hours,
        "total_material": total_material,
        "total_labor": total_labor,
        "cogs": cogs,
        "opex": opex,
        "total_investment": total_investment,
        "unit_cost": unit_cost,
        "wholesale": wholesale,
        "retail": retail,
        "sales_tax": sales_tax,
        "final_price": final_price,
        "profit": profit,
    }

# ─── DISPLAY FUNCTIONS ────────────────────────────────────────────

def print_inputs():
    """Show the fixed input parameters in a simple table."""
    print("\n" + "=" * 60)
    print("  ARTISAN ROAST — Price Modeling Tool")
    print("  Boutique Coffee · Product Launch Analysis")
    print("=" * 60)
    print("  INPUT PARAMETERS")
    print("-" * 60)
    print(f"  Production Volume       {PRODUCTION_VOLUME} bags")
    print(f"  Raw Material Cost       {fmt(RAW_MATERIAL_COST)} / bag")
    print(f"  Baseline Labor Hours    {BASELINE_LABOR_HOURS:.0f} hrs")
    print(f"  Hourly Labor Rate       {fmt(HOURLY_LABOR_RATE)} / hr")
    print(f"  Logistics (Shipping)    {fmt(LOGISTICS_COST)}")
    print(f"  Marketing (Social)      {fmt(MARKETING_COST)}")
    print(f"  Wholesale Markup        {pct(WHOLESALE_MARKUP)}")
    print(f"  Retailer Margin Target  {pct(RETAILER_MARGIN_TARGET)}")
    print(f"  Sales Tax Rate          {pct(SALES_TAX_RATE)}")
    print("=" * 60)

def print_comparison(baseline, breakdown):
    """Side‑by‑side comparison of the two scenarios."""
    print("\n" + "=" * 76)
    print("  SCENARIO COMPARISON — Cost & Pricing Waterfall")
    print("=" * 76)
    print(f"  {'Metric':<30} {'Baseline':>18}  {'Breakdown':>18}")
    print("-" * 76)

    rows = [
        ("Labor Hours", f"{baseline['labor_hours']:.0f} hrs", f"{breakdown['labor_hours']:.0f} hrs"),
        ("Total Material Cost", fmt(baseline['total_material']), fmt(breakdown['total_material'])),
        ("Total Labor Cost", fmt(baseline['total_labor']), fmt(breakdown['total_labor'])),
        ("COGS", fmt(baseline['cogs']), fmt(breakdown['cogs'])),
        ("OpEx (Logistics + Mktg)", fmt(baseline['opex']), fmt(breakdown['opex'])),
        ("Total Investment", fmt(baseline['total_investment']), fmt(breakdown['total_investment'])),
        ("Unit Cost", fmt(baseline['unit_cost']), fmt(breakdown['unit_cost'])),
        ("", "", ""),   # separator
        ("Wholesale Price", fmt(baseline['wholesale']), fmt(breakdown['wholesale'])),
        ("Suggested Retail Price", fmt(baseline['retail']), fmt(breakdown['retail'])),
        ("Sales Tax Amount", fmt(baseline['sales_tax']), fmt(breakdown['sales_tax'])),
        ("Final Consumer Price", fmt(baseline['final_price']), fmt(breakdown['final_price'])),
        ("", "", ""),
        ("Projected Net Profit", fmt(baseline['profit']), fmt(breakdown['profit'])),
    ]

    for label, a, b in rows:
        if label == "":
            print("-" * 76)
        else:
            print(f"  {label:<30} {a:>18}  {b:>18}")

    # Show the profit impact of the breakdown scenario
    delta = breakdown['profit'] - baseline['profit']
    sign = "−" if delta < 0 else "+"
    print("-" * 76)
    print(f"  Profit Impact of Breakdown:  {sign}{fmt(abs(delta))}")
    print("=" * 76)

def print_audit(scenario):
    """Step‑by‑step formula audit for one scenario."""
    print("\n" + "-" * 70)
    print(f"  FORMULA AUDIT — {scenario['name']}")
    print("-" * 70)

    steps = [
        ("1. Total Material Cost", f"{PRODUCTION_VOLUME} × {fmt(RAW_MATERIAL_COST)}", fmt(scenario['total_material'])),
        ("2. Total Labor Cost", f"{scenario['labor_hours']:.0f} hrs × {fmt(HOURLY_LABOR_RATE)}", fmt(scenario['total_labor'])),
        ("3. COGS", f"{fmt(scenario['total_material'])} + {fmt(scenario['total_labor'])}", fmt(scenario['cogs'])),
        ("4. OpEx", f"{fmt(LOGISTICS_COST)} + {fmt(MARKETING_COST)}", fmt(scenario['opex'])),
        ("5. Total Investment", f"{fmt(scenario['cogs'])} + {fmt(scenario['opex'])}", fmt(scenario['total_investment'])),
        ("6. Unit Cost", f"{fmt(scenario['total_investment'])} / {PRODUCTION_VOLUME}", fmt(scenario['unit_cost'])),
        ("7. Wholesale Price", f"{fmt(scenario['unit_cost'])} × (1 + {pct(WHOLESALE_MARKUP)})", fmt(scenario['wholesale'])),
        ("8. SRP (margin formula)", f"{fmt(scenario['wholesale'])} / (1 − {pct(RETAILER_MARGIN_TARGET)})", fmt(scenario['retail'])),
        ("9. Sales Tax", f"{fmt(scenario['retail'])} × {pct(SALES_TAX_RATE)}", fmt(scenario['sales_tax'])),
        ("10. Final Consumer Price", f"{fmt(scenario['retail'])} + {fmt(scenario['sales_tax'])}", fmt(scenario['final_price'])),
        ("11. Projected Net Profit", f"({fmt(scenario['wholesale'])} × {PRODUCTION_VOLUME}) − {fmt(scenario['total_investment'])}", fmt(scenario['profit'])),
    ]

    for step, formula, result in steps:
        print(f"  {step:<30} {formula:>34}  =  {result:>10}")

# ─── MAIN PROGRAM ──────────────────────────────────────────────────

def main():
    # Show input parameters
    print_inputs()

    # Run baseline scenario
    baseline = calculate_scenario("Baseline", BASELINE_LABOR_HOURS)

    # Run breakdown scenario (doubled labor)
    breakdown = calculate_scenario("Machine Breakdown (2× Labor)", BASELINE_LABOR_HOURS * 2)

    # Compare both scenarios
    print_comparison(baseline, breakdown)

    # Show detailed audit for each scenario
    print_audit(baseline)
    print_audit(breakdown)

    print()   # final blank line

if __name__ == "__main__":
    main()
