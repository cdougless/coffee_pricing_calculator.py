
import streamlit as st

def calculate_price_per_cup(bean_cost, shrinkage, yield_per_pound, water_cost, milk_cost,
                            sweetener_cost, packaging_cost, labor_cost, equipment_cost, 
                            rent, marketing, wages, supplies, waste_percentage, profit_margin, sales_tax):
    """
    Calculate the price per cup of coffee.

    Parameters:
        bean_cost (float): Cost of coffee beans per pound.
        shrinkage (float): Shrinkage during roasting (%).
        yield_per_pound (float): Yield (cups per roasted pound).
        water_cost (float): Cost of water per cup.
        milk_cost (float): Cost of milk or alternative per cup.
        sweetener_cost (float): Cost of sweeteners/additives per cup.
        packaging_cost (float): Cost of cups/packaging per cup.
        labor_cost (float): Barista labor cost per cup.
        equipment_cost (float): Brewing equipment cost per cup.
        rent (float): Monthly rent and utilities.
        marketing (float): Monthly marketing expenses.
        wages (float): Monthly wages.
        supplies (float): Monthly miscellaneous supplies.
        waste_percentage (float): Waste and spoilage allowance (%).
        profit_margin (float): Desired profit margin (%).
        sales_tax (float): Sales tax rate (%).

    Returns:
        float: Calculated price per cup.
    """
    # Adjusted bean cost after shrinkage
    adjusted_bean_cost = bean_cost / (1 - shrinkage / 100) / yield_per_pound

    # Direct costs per cup
    direct_cost_per_cup = (adjusted_bean_cost + water_cost + milk_cost + sweetener_cost +
                           packaging_cost + labor_cost + equipment_cost)

    # Monthly costs distributed per cup (assuming 3,000 cups/month as an example)
    monthly_cups = 3000  # Adjust based on expected sales volume
    overhead_per_cup = (rent + marketing + wages + supplies) / monthly_cups

    # Total cost per cup with waste allowance
    total_cost_per_cup = direct_cost_per_cup + overhead_per_cup
    total_cost_with_waste = total_cost_per_cup * (1 + waste_percentage / 100)

    # Adding profit margin
    price_before_tax = total_cost_with_waste * (1 + profit_margin / 100)

    # Adding sales tax
    final_price = price_before_tax * (1 + sales_tax / 100)

    return round(final_price, 2)

# Streamlit app for interactive tool
st.title("Coffee Pricing Calculator")

st.sidebar.header("Input Parameters")

# User inputs
bean_cost = st.sidebar.number_input("Cost of coffee beans (per pound)", value=15.0)
shrinkage = st.sidebar.number_input("Shrinkage during roasting (%)", value=15.0)
yield_per_pound = st.sidebar.number_input("Yield per pound (cups)", value=40.0)
water_cost = st.sidebar.number_input("Cost of water (per cup)", value=0.02)
milk_cost = st.sidebar.number_input("Cost of milk or alternative (per cup)", value=0.30)
sweetener_cost = st.sidebar.number_input("Cost of sweeteners/additives (per cup)", value=0.05)
packaging_cost = st.sidebar.number_input("Cost of cups/packaging (per cup)", value=0.10)
labor_cost = st.sidebar.number_input("Barista labor cost (per cup)", value=0.25)
equipment_cost = st.sidebar.number_input("Brewing equipment cost (per cup)", value=0.05)
rent = st.sidebar.number_input("Monthly rent and utilities", value=2000.0)
marketing = st.sidebar.number_input("Monthly marketing expenses", value=500.0)
wages = st.sidebar.number_input("Monthly wages", value=5000.0)
supplies = st.sidebar.number_input("Monthly miscellaneous supplies", value=300.0)
waste_percentage = st.sidebar.number_input("Waste and spoilage allowance (%)", value=5.0)
profit_margin = st.sidebar.number_input("Desired profit margin (%)", value=30.0)
sales_tax = st.sidebar.number_input("Sales tax rate (%)", value=7.0)

# Calculate price per cup
price_per_cup = calculate_price_per_cup(
    bean_cost, shrinkage, yield_per_pound, water_cost, milk_cost,
    sweetener_cost, packaging_cost, labor_cost, equipment_cost, 
    rent, marketing, wages, supplies, waste_percentage, profit_margin, sales_tax
)

st.header("Calculated Price Per Cup")
st.write(f"The final price per cup of coffee is **${price_per_cup}**.")

st.sidebar.markdown("""
### How It Works:
- Input the cost components and assumptions on the left.
- The tool calculates the selling price based on total costs, profit margin, and sales tax.
""")
