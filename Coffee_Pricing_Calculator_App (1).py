
import streamlit as st

def calculate_price_per_unit(bean_cost, shrinkage, yield_per_pound, water_cost, milk_cost,
                             sweetener_cost, packaging_cost, labor_cost, equipment_cost, 
                             rent, marketing, wages, supplies, waste_percentage, profit_margin, sales_tax, size):
    """
    Calculate the price per unit of coffee.

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
        size (str): Size of the coffee unit (e.g., "cup", "12oz", "1lb", etc.).

    Returns:
        float: Calculated price per unit.
    """
    # Adjusted bean cost after shrinkage
    adjusted_bean_cost = bean_cost / (1 - shrinkage / 100)

    # Direct costs per cup
    direct_cost_per_cup = (adjusted_bean_cost / yield_per_pound + water_cost + milk_cost + sweetener_cost +
                           packaging_cost + labor_cost + equipment_cost)

    # Monthly costs distributed per cup (assuming 3,000 cups/month as an example)
    monthly_cups = 3000  # Adjust based on expected sales volume
    overhead_per_cup = (rent + marketing + wages + supplies) / monthly_cups

    # Total cost per cup with waste allowance
    total_cost_per_cup = direct_cost_per_cup + overhead_per_cup
    total_cost_with_waste = total_cost_per_cup * (1 + waste_percentage / 100)

    # Scale costs based on size
    size_multiplier = {
        "cup": 1,
        "12oz": 12 / 16,  # Based on 16oz in a pound
        "16oz": 1,  # Full pound equivalent
        "8oz": 8 / 16,  # Half-pound equivalent
        "1lb": 1,
        "2lb": 2,
        "5lb": 5,
        "10lb": 10
    }.get(size, 1)

    total_cost_with_size = total_cost_with_waste * size_multiplier

    # Adding profit margin
    price_before_tax = total_cost_with_size * (1 + profit_margin / 100)

    # Adding sales tax
    final_price = price_before_tax * (1 + sales_tax / 100)

    return round(final_price, 2)

def adjust_parameters_by_basis(basis, bean_cost, water_cost, milk_cost, sweetener_cost, packaging_cost, labor_cost, equipment_cost):
    """
    Adjust parameters to reflect cost per pound, per cup, or per unit size.

    Parameters:
        basis (str): Basis for calculation ("per pound", "per cup", "per unit size").

    Returns:
        Adjusted parameters.
    """
    if basis == "per pound":
        return bean_cost, 0, 0, 0, 0, 0, 0  # Only bean cost matters for per-pound calculations
    elif basis == "per cup":
        return bean_cost / 40, water_cost, milk_cost, sweetener_cost, packaging_cost, labor_cost, equipment_cost
    else:  # Default assumes per unit size is provided as is
        return bean_cost, water_cost, milk_cost, sweetener_cost, packaging_cost, labor_cost, equipment_cost

st.markdown("""### Coffee Pricing Calculator
Easily determine the cost and pricing for your coffee products at different scales and for wholesale customers.""")

st.sidebar.header("Input Parameters")

# Basis of calculation
basis = st.sidebar.radio("Select Basis of Calculation", ["per pound", "per cup", "per unit size"], index=1)

# User inputs
bean_cost = st.sidebar.number_input("Cost of coffee beans (per pound)", value=15.0)
shrinkage = st.sidebar.slider("Shrinkage during roasting (%)", min_value=0.0, max_value=20.0, value=15.0)
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
waste_percentage = st.sidebar.slider("Waste and spoilage allowance (%)", min_value=0.0, max_value=15.0, value=5.0)
profit_margin = st.sidebar.slider("Desired profit margin (%)", min_value=0.0, max_value=50.0, value=30.0)
sales_tax = st.sidebar.slider("Sales tax rate (%)", min_value=0.0, max_value=15.0, value=7.0)

# Adjust parameters based on basis
bean_cost, water_cost, milk_cost, sweetener_cost, packaging_cost, labor_cost, equipment_cost = adjust_parameters_by_basis(
    basis, bean_cost, water_cost, milk_cost, sweetener_cost, packaging_cost, labor_cost, equipment_cost
)

# Select size of the coffee unit
size = st.sidebar.selectbox("Select coffee size", ["cup", "12oz", "16oz", "8oz", "1lb", "2lb", "5lb", "10lb"])

# Option for wholesale pricing
wholesale_margin = st.sidebar.slider("Wholesale profit margin (%)", min_value=0.0, max_value=30.0, value=20.0)
wholesale_pricing = st.sidebar.checkbox("Show wholesale pricing")

# Calculate price per unit
price_per_unit = calculate_price_per_unit(
    bean_cost, shrinkage, yield_per_pound, water_cost, milk_cost,
    sweetener_cost, packaging_cost, labor_cost, equipment_cost, 
    rent, marketing, wages, supplies, waste_percentage, profit_margin, sales_tax, size
)

st.markdown(f"## Calculated Price for {size}")
st.success(f"The final price for {size} is **${price_per_unit}**.")

# Show wholesale pricing if selected
if wholesale_pricing:
    wholesale_price = calculate_price_per_unit(
        bean_cost, shrinkage, yield_per_pound, water_cost, milk_cost,
        sweetener_cost, packaging_cost, labor_cost, equipment_cost, 
        rent, marketing, wages, supplies, waste_percentage, wholesale_margin, sales_tax, size
    )
    st.info(f"The wholesale price for {size} is **${wholesale_price}**.")

st.sidebar.markdown("""
### How It Works:
- Input the cost components and assumptions on the left.
- Select the basis for calculation (per pound, per cup, or per unit size).
- The tool calculates the selling price based on total costs, profit margin, and sales tax.
- Optionally, it provides wholesale pricing with a separate profit margin.
""")
