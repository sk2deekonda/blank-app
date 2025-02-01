import streamlit as st

def calculate_hra(basic_salary, rent_paid, city_type):
    """
    Calculate HRA exemption based on basic salary, rent paid, and city type.
    """
    if city_type == "metro":
        hra_exemption_limit = 0.5 * basic_salary  # 50% of basic for metro cities
    else:
        hra_exemption_limit = 0.4 * basic_salary  # 40% of basic for non-metro cities

    # HRA exemption is the minimum of:
    # 1. Actual HRA received
    # 2. Rent paid - 10% of basic salary
    # 3. 50% or 40% of basic salary (based on city type)
    hra_exemption = min(
        hra_exemption_limit,  # 50% or 40% of basic
        rent_paid - 0.1 * basic_salary  # Rent paid minus 10% of basic
    )
    return max(hra_exemption, 0)  # Ensure HRA exemption is not negative

def calculate_tax(income, regime='new', deductions_80c=0, hra=0, mediclaim_self=0, mediclaim_parents=0):
    """
    Calculate tax liability under the old or new tax regime.
    """
    if regime == 'new':
        # Updated new tax regime slabs (FY 2024-25)
        slabs = [
            (400000, 0),
            (800000, 0.05),
            (1200000, 0.10),
            (1600000, 0.15),
            (2000000, 0.20),
            (2400000, 0.25),
            (float('inf'), 0.30)
        ]
        if income <= 1275000:
            return 0  # No tax for income up to ₹12,00,000 prior to standard deduction
        taxable_income = income - 75000  # Updated standard deduction of ₹75,000
    elif regime == 'old':
        slabs = [
            (250000, 0),
            (500000, 0.05),
            (1000000, 0.20),
            (float('inf'), 0.30)
        ]
        # Deduct Section 80C, HRA, and mediclaim benefits
        taxable_income = income - deductions_80c - hra - mediclaim_self - mediclaim_parents
    else:
        raise ValueError("Invalid regime. Choose 'new' or 'old'.")

    tax = 0
    previous_slab = 0
    for slab, rate in slabs:
        if taxable_income > slab:
            tax += (slab - previous_slab) * rate
        else:
            tax += (taxable_income - previous_slab) * rate
            break
        previous_slab = slab

    if regime == 'new' and taxable_income <= 700000:
        tax = 0
    elif regime == 'old' and taxable_income <= 500000:
        tax = 0

    tax += tax * 0.04  # Add 4% cess
    return tax

# Streamlit App
st.title("Income Tax Regime Calculator (India) by Sid D")
st.write("Compare the Old and New Tax Regimes to see which is better for you.")

# Inputs
income = st.number_input("Enter your annual income (₹):", min_value=0.0, step=1000.0)
basic_salary = st.number_input("Enter your basic salary (₹):", min_value=0.0, step=1000.0)
rent_paid = st.number_input("Enter the annual rent paid (₹):", min_value=0.0, step=1000.0)
city_type = st.selectbox("Select your city type:", ["metro", "non-metro"])
deductions_80c = st.number_input("Enter your deductions under Section 80C (₹):", min_value=0.0, step=1000.0)
mediclaim_self = st.number_input("Enter mediclaim premium for self (₹):", min_value=0.0, step=1000.0)
mediclaim_parents = st.number_input("Enter mediclaim premium for parents (₹):", min_value=0.0, step=1000.0)

# Calculate HRA
hra_exemption = calculate_hra(basic_salary, rent_paid, city_type)
st.write(f"Calculated HRA Exemption: ₹{hra_exemption:,.2f}")

# Calculate taxes
new_tax = calculate_tax(income, regime='new')
old_tax = calculate_tax(income, regime='old', deductions_80c=deductions_80c, hra=hra_exemption, mediclaim_self=mediclaim_self, mediclaim_parents=mediclaim_parents)

# Results
st.write("\n--- Tax Analysis ---")
st.write(f"Tax under New Regime: ₹{new_tax:,.2f}")
st.write(f"Tax under Old Regime: ₹{old_tax:,.2f}")

# Calculate total benefit
if new_tax < old_tax:
    total_benefit_yearly = old_tax - new_tax
    total_benefit_monthly = total_benefit_yearly / 12
    st.write("\nConclusion: The **New Tax Regime** is better for you.")
    st.write(f"**Total Benefit (Yearly):** ₹{total_benefit_yearly:,.2f}")
    st.write(f"**Total Benefit (Monthly):** ₹{total_benefit_monthly:,.2f}")
else:
    total_benefit_yearly = new_tax - old_tax
    total_benefit_monthly = total_benefit_yearly / 12
    st.write("\nConclusion: The **Old Tax Regime** is better for you.")
    st.write(f"**Total Benefit (Yearly):** ₹{total_benefit_yearly:,.2f}")
    st.write(f"**Total Benefit (Monthly):** ₹{total_benefit_monthly:,.2f}")
