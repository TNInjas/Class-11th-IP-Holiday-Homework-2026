# ----------------------------
# Simple Price Modeling Program
# ----------------------------

# Fixed Values
PROD = 200
RAW = 5.50
RATE = 25.00
LOG = 150.00
MKT = 100.00
WH_MARKUP = 0.40
RET_MARGIN = 0.30
TAX = 0.08

# Input
name = input("Enter Scenario Name: ")
hrs = float(input("Enter Labor Hours: "))

# Calculations
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

# Output
report = {
    "Scenario": name,
    "Labor Hours": f"{hrs} hrs",
    "Material Cost": f"${round(mat, 2)}",
    "Labor Cost": f"${round(lab, 2)}",
    "COGS (Cost of Goods Sold)": f"${round(cogs, 2)}",
    "Operating Expenses": f"${round(opex, 2)}",
    "Total Investment": f"${round(invest, 2)}",
    "Unit Cost": f"${round(unit, 2)}",
    "Wholesale Price": f"${round(wholesale, 2)}",
    "Suggested Retail Price (SRP)": f"${round(retail, 2)}",
    "Sales Tax Amount": f"${round(tax_amt, 2)}",
    "Final Consumer Price": f"${round(final, 2)}",
    "Projected Net Profit": f"${round(profit, 2)}"
}

# Print the report
print("\n----------------------------")
print("PRICE MODELING REPORT")
print("----------------------------")

for key, value in report.items():
    print(f"{key}: {value}")
