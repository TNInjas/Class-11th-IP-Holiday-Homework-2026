"""
╔══════════════════════════════════════════════════════════════════╗
║          ARTISAN ROAST — Price Modeling Tool v1.0               ║
║  Boutique Coffee Product Launch · Financial Scenario Analysis   ║
╚══════════════════════════════════════════════════════════════════╝

Calculates unit cost, wholesale price, suggested retail price,
final consumer price, and projected net profit for a baseline
scenario and a machine-breakdown (doubled labor) scenario.
"""

import sys
from dataclasses import dataclass

# Ensure box-drawing characters render on Windows consoles (cp1252 → utf-8).
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]


# ── Fixed Input Parameters ───────────────────────────────────────

PRODUCTION_VOLUME: int = 200          # bags
RAW_MATERIAL_COST: float = 5.50      # $/bag
BASELINE_LABOR_HOURS: float = 10.0   # hours
HOURLY_LABOR_RATE: float = 25.00     # $/hour
LOGISTICS_COST: float = 150.00       # flat shipping/freight
MARKETING_COST: float = 100.00       # flat social media spend
WHOLESALE_MARKUP: float = 0.40       # 40%
RETAILER_MARGIN_TARGET: float = 0.30 # 30%
SALES_TAX_RATE: float = 0.08         # 8%


# ── Data Model ───────────────────────────────────────────────────

@dataclass
class ScenarioResult:
    """Holds every computed financial metric for a single scenario."""

    scenario_name: str
    labor_hours: float

    # Cost build-up
    total_material_cost: float
    total_labor_cost: float
    cogs: float
    opex: float
    total_investment: float
    unit_cost: float

    # Pricing chain
    wholesale_price: float
    suggested_retail_price: float
    sales_tax_amount: float
    final_consumer_price: float

    # Profitability
    projected_net_profit: float


# ── Core Calculation Engine ──────────────────────────────────────

def calculate_scenario(
    scenario_name: str,
    labor_hours: float,
    production_volume: int = PRODUCTION_VOLUME,
    raw_material_cost: float = RAW_MATERIAL_COST,
    hourly_labor_rate: float = HOURLY_LABOR_RATE,
    logistics_cost: float = LOGISTICS_COST,
    marketing_cost: float = MARKETING_COST,
    wholesale_markup: float = WHOLESALE_MARKUP,
    retailer_margin_target: float = RETAILER_MARGIN_TARGET,
    sales_tax_rate: float = SALES_TAX_RATE,
) -> ScenarioResult:
    """Run the full pricing waterfall for a given set of parameters.

    Steps executed in strict sequential order:
      1. Total Material Cost
      2. Total Labor Cost
      3. COGS
      4. OpEx
      5. Total Investment
      6. Unit Cost
      7. Wholesale Price
      8. Suggested Retail Price  (true margin formula)
      9. Sales Tax Amount
     10. Final Consumer Price
     11. Projected Net Profit
    """

    # Step 1 – Total Material Cost
    total_material_cost = production_volume * raw_material_cost

    # Step 2 – Total Labor Cost
    total_labor_cost = labor_hours * hourly_labor_rate

    # Step 3 – Cost of Goods Sold
    cogs = total_material_cost + total_labor_cost

    # Step 4 – Operating Expenses
    opex = logistics_cost + marketing_cost

    # Step 5 – Total Investment
    total_investment = cogs + opex

    # Step 6 – Unit Cost
    unit_cost = total_investment / production_volume

    # Step 7 – Wholesale Price (cost-plus markup)
    wholesale_price = unit_cost * (1 + wholesale_markup)

    # Step 8 – Suggested Retail Price (true margin formula)
    #          SRP = Wholesale / (1 − Retailer Margin)
    suggested_retail_price = wholesale_price / (1 - retailer_margin_target)

    # Step 9 – Sales Tax Amount
    sales_tax_amount = suggested_retail_price * sales_tax_rate

    # Step 10 – Final Consumer Price
    final_consumer_price = suggested_retail_price + sales_tax_amount

    # Step 11 – Projected Net Profit
    projected_net_profit = (wholesale_price * production_volume) - total_investment

    return ScenarioResult(
        scenario_name=scenario_name,
        labor_hours=labor_hours,
        total_material_cost=total_material_cost,
        total_labor_cost=total_labor_cost,
        cogs=cogs,
        opex=opex,
        total_investment=total_investment,
        unit_cost=unit_cost,
        wholesale_price=wholesale_price,
        suggested_retail_price=suggested_retail_price,
        sales_tax_amount=sales_tax_amount,
        final_consumer_price=final_consumer_price,
        projected_net_profit=projected_net_profit,
    )


# ── Terminal Presentation ────────────────────────────────────────

def _fmt(value: float) -> str:
    """Format a float as a dollar string with two decimal places."""
    return f"${value:,.2f}"


def _pct(value: float) -> str:
    """Format a decimal fraction as a percentage string."""
    return f"{value * 100:.0f}%"


def print_input_parameters() -> None:
    """Display the fixed configuration block."""
    w = 62
    print()
    print("╔" + "═" * w + "╗")
    print("║" + " ARTISAN ROAST — Price Modeling Tool ".center(w) + "║")
    print("║" + " Boutique Coffee · Product Launch Analysis ".center(w) + "║")
    print("╠" + "═" * w + "╣")
    print("║" + " INPUT PARAMETERS".ljust(w) + "║")
    print("╠" + "═" * w + "╣")

    params = [
        ("Production Volume", f"{PRODUCTION_VOLUME} bags"),
        ("Raw Material Cost", f"{_fmt(RAW_MATERIAL_COST)} / bag"),
        ("Baseline Labor Hours", f"{BASELINE_LABOR_HOURS:.0f} hrs"),
        ("Hourly Labor Rate", f"{_fmt(HOURLY_LABOR_RATE)} / hr"),
        ("Logistics (Shipping)", _fmt(LOGISTICS_COST)),
        ("Marketing (Social)", _fmt(MARKETING_COST)),
        ("Wholesale Markup", _pct(WHOLESALE_MARKUP)),
        ("Retailer Margin Target", _pct(RETAILER_MARGIN_TARGET)),
        ("Sales Tax Rate", _pct(SALES_TAX_RATE)),
    ]

    for label, value in params:
        print(f"║  {label:<28s} {value:>30s}  ║")

    print("╚" + "═" * w + "╝")


def print_comparison(baseline: ScenarioResult, breakdown: ScenarioResult) -> None:
    """Print a side-by-side comparison table of both scenarios."""
    w = 78
    col_label = 30
    col_val = 18

    def row(label: str, val_a: str, val_b: str, delta: str = "") -> str:
        """Build one formatted table row."""
        content = f"  {label:<{col_label}s} {val_a:>{col_val}s}  {val_b:>{col_val}s}"
        if delta:
            content += f"  {delta:>6s}"
        return f"║{content:<{w}s}║"

    def divider(char: str = "─") -> str:
        return "╟" + char * w + "╢"

    print()
    print("╔" + "═" * w + "╗")
    print("║" + " SCENARIO COMPARISON — Cost & Pricing Waterfall ".center(w) + "║")
    print("╠" + "═" * w + "╣")

    # Column headers
    hdr = f"  {'Metric':<{col_label}s} {'Baseline':>{col_val}s}  {'Breakdown':>{col_val}s}"
    print(f"║{hdr:<{w}s}║")
    print(divider())

    # ── Cost Build-Up Section ──
    print(f"║{'  ▸ COST BUILD-UP':<{w}s}║")
    print(divider("·"))

    rows = [
        ("Labor Hours",
         f"{baseline.labor_hours:.0f} hrs",
         f"{breakdown.labor_hours:.0f} hrs"),
        ("Total Material Cost",
         _fmt(baseline.total_material_cost),
         _fmt(breakdown.total_material_cost)),
        ("Total Labor Cost",
         _fmt(baseline.total_labor_cost),
         _fmt(breakdown.total_labor_cost)),
        ("COGS",
         _fmt(baseline.cogs),
         _fmt(breakdown.cogs)),
        ("OpEx (Logistics + Mktg)",
         _fmt(baseline.opex),
         _fmt(breakdown.opex)),
        ("Total Investment",
         _fmt(baseline.total_investment),
         _fmt(breakdown.total_investment)),
        ("Unit Cost",
         _fmt(baseline.unit_cost),
         _fmt(breakdown.unit_cost)),
    ]

    for label, va, vb in rows:
        print(row(label, va, vb))

    # ── Pricing Chain Section ──
    print(divider())
    print(f"║{'  ▸ PRICING CHAIN':<{w}s}║")
    print(divider("·"))

    pricing_rows = [
        ("Wholesale Price",
         _fmt(baseline.wholesale_price),
         _fmt(breakdown.wholesale_price)),
        ("Suggested Retail Price",
         _fmt(baseline.suggested_retail_price),
         _fmt(breakdown.suggested_retail_price)),
        ("Sales Tax Amount",
         _fmt(baseline.sales_tax_amount),
         _fmt(breakdown.sales_tax_amount)),
        ("Final Consumer Price",
         _fmt(baseline.final_consumer_price),
         _fmt(breakdown.final_consumer_price)),
    ]

    for label, va, vb in pricing_rows:
        print(row(label, va, vb))

    # ── Profitability Section ──
    print(divider())
    print(f"║{'  ▸ PROFITABILITY':<{w}s}║")
    print(divider("·"))

    profit_delta = breakdown.projected_net_profit - baseline.projected_net_profit
    delta_str = f"({'−' if profit_delta < 0 else '+'}{_fmt(abs(profit_delta))})"

    print(row(
        "Projected Net Profit",
        _fmt(baseline.projected_net_profit),
        _fmt(breakdown.projected_net_profit),
    ))

    print(f"║{'':>{w}s}║")
    delta_line = f"  Profit Impact of Breakdown:  {delta_str}"
    print(f"║{delta_line:<{w}s}║")

    print("╚" + "═" * w + "╝")


def print_formula_audit(result: ScenarioResult) -> None:
    """Print a step-by-step formula audit trail for one scenario."""
    w = 72
    print()
    print("┌" + "─" * w + "┐")
    print(f"│{f'  FORMULA AUDIT — {result.scenario_name}':<{w}s}│")
    print("├" + "─" * w + "┤")

    steps = [
        (
            "1. Total Material Cost",
            f"{PRODUCTION_VOLUME} × {_fmt(RAW_MATERIAL_COST)}",
            _fmt(result.total_material_cost),
        ),
        (
            "2. Total Labor Cost",
            f"{result.labor_hours:.0f} hrs × {_fmt(HOURLY_LABOR_RATE)}",
            _fmt(result.total_labor_cost),
        ),
        (
            "3. COGS",
            f"{_fmt(result.total_material_cost)} + {_fmt(result.total_labor_cost)}",
            _fmt(result.cogs),
        ),
        (
            "4. OpEx",
            f"{_fmt(LOGISTICS_COST)} + {_fmt(MARKETING_COST)}",
            _fmt(result.opex),
        ),
        (
            "5. Total Investment",
            f"{_fmt(result.cogs)} + {_fmt(result.opex)}",
            _fmt(result.total_investment),
        ),
        (
            "6. Unit Cost",
            f"{_fmt(result.total_investment)} / {PRODUCTION_VOLUME}",
            _fmt(result.unit_cost),
        ),
        (
            "7. Wholesale Price",
            f"{_fmt(result.unit_cost)} × (1 + {_pct(WHOLESALE_MARKUP)})",
            _fmt(result.wholesale_price),
        ),
        (
            "8. SRP (margin formula)",
            f"{_fmt(result.wholesale_price)} / (1 − {_pct(RETAILER_MARGIN_TARGET)})",
            _fmt(result.suggested_retail_price),
        ),
        (
            "9. Sales Tax",
            f"{_fmt(result.suggested_retail_price)} × {_pct(SALES_TAX_RATE)}",
            _fmt(result.sales_tax_amount),
        ),
        (
            "10. Final Consumer Price",
            f"{_fmt(result.suggested_retail_price)} + {_fmt(result.sales_tax_amount)}",
            _fmt(result.final_consumer_price),
        ),
        (
            "11. Projected Net Profit",
            f"({_fmt(result.wholesale_price)} × {PRODUCTION_VOLUME}) − {_fmt(result.total_investment)}",
            _fmt(result.projected_net_profit),
        ),
    ]

    for step_label, formula, answer in steps:
        line1 = f"  {step_label}"
        line2 = f"      {formula}  =  {answer}"
        print(f"│{line1:<{w}s}│")
        print(f"│{line2:<{w}s}│")

    print("└" + "─" * w + "┘")


# ── Main Entry Point ─────────────────────────────────────────────

def main() -> None:
    """Execute baseline and breakdown scenarios, then display results."""

    # Display configuration
    print_input_parameters()

    # Run scenarios
    baseline = calculate_scenario(
        scenario_name="Baseline",
        labor_hours=BASELINE_LABOR_HOURS,
    )

    machine_breakdown = calculate_scenario(
        scenario_name="Machine Breakdown (2× Labor)",
        labor_hours=BASELINE_LABOR_HOURS * 2,  # doubled to 20 hours
    )

    # Side-by-side comparison
    print_comparison(baseline, machine_breakdown)

    # Detailed formula audits
    print_formula_audit(baseline)
    print_formula_audit(machine_breakdown)

    print()


if __name__ == "__main__":
    main()
