import streamlit as st
import plotly.graph_objects as go

#-----------------------------------------------------------

def calculate_sip(principal, rate, time):
    r = rate / 100 / 12
    n = time * 12
    future_value = principal * (((1 + r) ** n) - 1) / r
    return round(future_value, 2)


def calculate_simple_interest(principal, rate, time):
    interest = (principal * rate * time) / 100
    return round(interest, 2), round(principal + interest, 2)

def calculate_compound_interest(principal, rate, time, n=1):
    # n = compounding frequency per year (1=yearly, 4=quarterly, 12=monthly)
    amount = principal * (1 + rate / (100 * n)) ** (n * time)
    return round(amount - principal, 2), round(amount, 2)


#-----------------------------------------------------------

st.title("💰 SIP & Interest Calculator")

option = st.sidebar.selectbox(
    "Choose Calculator",
    ("SIP Calculator", "Simple Interest", "Compound Interest")
)


st.markdown("---")

if option == "SIP Calculator":
    st.header("📈 SIP Calculator")
    principal = st.number_input("Monthly Investment (₹)", min_value=0, step=100, value=1000)
    rate = st.number_input("Expected Annual Return (%)", min_value=0.0, step=0.1, value=12.0)
    time = st.number_input("Investment Duration (Years)", min_value=1, step=1, value=10)

    if principal > 0 and rate > 0 and time > 0:
        future_value = calculate_sip(principal, rate, time)
        invested_amount = principal * time * 12
        gain = future_value - invested_amount

        st.success(f"💸 Invested Amount: ₹{invested_amount:,.2f}")
        st.success(f"📈 Total Gain: ₹{gain:,.2f}")
        st.success(f"🏁 Future Value: ₹{future_value:,.2f}")

        # Line chart
        months = list(range(1, time * 12 + 1))
        values = []
        r = rate / 100 / 12
        for n in months:
            fv = principal * (((1 + r) ** n - 1) * (1 + r)) / r
            values.append(fv)

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=months, y=values, mode='lines', name='SIP Value'))
        fig_line.update_layout(title="📈 SIP Growth Over Time", xaxis_title="Months", yaxis_title="Value (₹)")
        st.plotly_chart(fig_line, use_container_width=True)

        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=["Invested Amount", "Gain"],
            values=[invested_amount, gain],
            hole=0.4
        )])
        fig_pie.update_layout(title="📊 Investment vs Gain")
        st.plotly_chart(fig_pie, use_container_width=True)
  

elif option == "Simple Interest":
    st.header("📉 Simple Interest Calculator")
    principal = st.number_input("Principal Amount (₹)", min_value=0, step=100, value=10000)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.1, value=5.0)
    time = st.number_input("Time Period (Years)", min_value=1, step=1, value=3)

    if st.button("Calculate Simple Interest"):
        interest, total = calculate_simple_interest(principal, rate, time)
        st.success(f"Interest: ₹{interest} | Total Amount: ₹{total}")

elif option == "Compound Interest":
    st.header("📊 Compound Interest Calculator")
    principal = st.number_input("Principal Amount (₹)", min_value=0, step=100, value=10000)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.1, value=5.0)
    time = st.number_input("Time Period (Years)", min_value=1, step=1, value=3)
    freq = st.selectbox("Compounding Frequency", ("Yearly", "Half-Yearly", "Quarterly", "Monthly"))

    freq_map = {"Yearly": 1, "Half-Yearly": 2, "Quarterly": 4, "Monthly": 12}
    n = freq_map[freq]

    if st.button("Calculate Compound Interest"):
        interest, total = calculate_compound_interest(principal, rate, time, n)
        st.success(f"Interest: ₹{interest} | Total Amount: ₹{total}")








