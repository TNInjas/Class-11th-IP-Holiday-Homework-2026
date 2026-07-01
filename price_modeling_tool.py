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
print("\n----------------------------")
print("PRICE MODELING REPORT")
print("----------------------------")
print("Scenario:", name)
print("Labor Hours:", hrs, "hrs")
print("Material Cost: $", round(mat, 2))
print("Labor Cost: $", round(lab, 2))
print("COGS (Cost of Goods Sold): $", round(cogs, 2))
print("Operating Expenses: $", round(opex, 2))
print("Total Investment: $", round(invest, 2))
print("Unit Cost: $", round(unit, 2))
print("Wholesale Price: $", round(wholesale, 2))
print("Suggested Retail Price (SRP): $", round(retail, 2))
print("Sales Tax Amount: $", round(tax_amt, 2))
print("Final Consumer Price: $", round(final, 2))
print("Projected Net Profit: $", round(profit, 2))
