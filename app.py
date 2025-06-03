import streamlit as st
import pandas as pd
import numpy as np

# Generate sample data (no external CSV needed)
def generate_sample_data():
    np.random.seed(42)
    funds = []
    for i in range(50):
        risk = np.random.choice(['Low', 'Medium', 'High'])
        funds.append({
            'scheme_name': f'Fund {i+1}',
            'amc_name': np.random.choice(['ABC AMC', 'XYZ AMC', 'PQR AMC']),
            'category': np.random.choice(['Equity', 'Debt', 'Hybrid']),
            'sub_category': np.random.choice(['Large Cap', 'Small Cap', 'Corporate Bonds']),
            'fund_age_yr': np.random.randint(1, 15),
            'expense_ratio': round(np.random.uniform(0.1, 2.5), 2),
            'risk_level_encoded': {'Low': 0, 'Medium': 1, 'High': 2}[risk],
            'returns_1yr': round(np.random.uniform(5, 25), 2),
            'returns_3yr': round(np.random.uniform(30, 80), 2),
            'returns_5yr': round(np.random.uniform(50, 120), 2),
            'fund_manager': f"Manager {np.random.choice(['A', 'B', 'C'])}"
        })
    return pd.DataFrame(funds)

df = generate_sample_data()

# UI Setup
st.set_page_config(page_title="Mutual Fund Recommender", layout="centered")
st.title("📈 Mutual Fund Recommendation Platform")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Enter investment amount (₹)", min_value=100, step=100, value=10000)
with col2:
    duration = st.slider("Select investment duration (in years)", 1, 10, 3)

risk = st.selectbox("Choose your risk appetite", ['Low', 'Medium', 'High'])

# Recommendation Logic
risk_map = {'Low': 0, 'Medium': 1, 'High': 2}
risk_encoded = risk_map[risk]
filtered = df[df['risk_level_encoded'] == risk_encoded]

return_col = 'returns_1yr' if duration <= 1 else 'returns_3yr' if duration <= 3 else 'returns_5yr'
recommended = filtered.sort_values(by=return_col, ascending=False).head(3)  # Top 3 recommendations

# Display Results
if not recommended.empty:
    st.success(f"✅ Top {len(recommended)} Recommendations for {risk} Risk Profile")
    
    for idx, fund in recommended.iterrows():
        with st.expander(f"🏆 #{idx+1}: {fund['scheme_name']}"):
            expected_return = fund[return_col] / 100
            future_value = amount * ((1 + expected_return) ** duration)
            
            st.write(f"**AMC:** {fund['amc_name']}")
            st.write(f"**Category:** {fund['category']} | **Sub-category:** {fund['sub_category']}")
            st.write(f"**{duration}-year return:** {fund[return_col]}%")
            st.write(f"**Fund Age:** {fund['fund_age_yr']} years | **Expense Ratio:** {fund['expense_ratio']}%")
            st.metric(f"Projected Value (₹)", f"₹{future_value:,.0f}", delta=f"{fund[return_col]}% CAGR")
            
            st.markdown("---")
            st.markdown(f"**Fund Manager:** {fund['fund_manager']}")
else:
    st.warning("⚠️ No funds match your criteria. Try adjusting risk level.")

# Key Features Explanation
with st.expander("ℹ️ How this recommendation works"):
    st.markdown("""
    - **Risk Matching**: Filters funds matching your risk profile
    - **Performance-Based**: Prioritizes funds with highest historical returns
    - **Time-Adjusted**: Uses 1yr/3yr/5yr returns based on your duration
    - **Cost-Aware**: Shows expense ratio (lower is better)
    """)

# How to Run:
# 1. Save this as mutual_fund_app.py
# 2. Run: streamlit run mutual_fund_app.py