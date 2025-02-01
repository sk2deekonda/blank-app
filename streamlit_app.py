import streamlit as st

def calculate_tax(income, regime='new', deductions_80c=0, hra=0):
    """
    Calculate tax liability under the old or new tax regime.
    """
    if regime == 'new':
        slabs = [
            (400000, 0),
            (800000, 0.05),
            (120000, 0.10),
            (1600000, 0.15),
            (2000000, 0.20),
            (2500000, 0.25),
            (float('inf'), 0.30)
        ]
        taxable_income = income - 50000  # Standard deduction
    elif regime == 'old':
        slabs = [
            (250000, 0),
            (500000, 0.05),
            (1000000, 0.20),
            (float('inf'), 0.30)
        ]
        taxable_income = income - deductions_80c - hra
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
st.title("Income Tax Regime Calculator (India)")
st.write("Compare the Old and New Tax Regimes to see which is better for you.")

# Inputs
income = st.number_input("Enter your annual income (₹):", min_value=0.0, step=1000.0)
deductions_80c = st.number_input("Enter your deductions under Section 80C (₹):", min_value=0.0, step=1000.0)
hra = st.number_input("Enter your House Rent Allowance (HRA) (₹):", min_value=0.0, step=1000.0)

# Calculate taxes
new_tax = calculate_tax(income, regime='new')
old_tax = calculate_tax(income, regime='old', deductions_80c=deductions_80c, hra=hra)

# Results
st.write("\n--- Tax Analysis ---")
st.write(f"Tax under New Regime: ₹{new_tax:,.2f}")
st.write(f"Tax under Old Regime: ₹{old_tax:,.2f}")

if new_tax < old_tax:
    st.write("\nConclusion: The **New Tax Regime** is better for you.")
else:
    st.write("\nConclusion: The **Old Tax Regime** is better for you.")
