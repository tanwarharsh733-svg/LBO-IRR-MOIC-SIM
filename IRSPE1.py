# import pandas as pd
import numpy_financial as npf
import streamlit as st
import numpy as np


st.title("LBO IRR MOIC SIMULATOR")
st.write("Leverage buy out internal rate of return, Multiple on Invested capital simulator")

with st.expander("Knowledege box"):
   st.write("""
**What this project does**  
This model helps explore a basic idea of IRR and MOIC based on debt scenarios and user inputs.

**What is an LBO?**  
An LBO is when a company is bought using a mix of equity and debt. The goal is to earn strong returns by repaying the debt using the company's cash flows.

**Key Outputs**  
- **IRR (Internal Rate of Return):** Annual return on equity investment.  
- **MOIC (Multiple on Invested Capital):** Total return relative to equity invested.

**Inputs Explained**  
- **Industry**: for reference and exit multiples and expected EBITDA growth.  
- **Purchase Price**: Value of the business being bought.     
- **Interest Rate**: Cost of debt (in decimal, e.g., 0.08 for 8%).  
- **Exit Year**: When the investor plans to sell.  

    """)


exit_multiples = {
    "it services": {"metric": "EV/EBITDA", "value": 18.0},
    "consumer staples": {"metric": "EV/EBITDA", "value": 20.0},
    "consumer discretionary": {"metric": "EV/EBITDA", "value": 15.5},
    "healthcare (pharma)": {"metric": "EV/EBITDA", "value": 17.0},
    "auto components": {"metric": "EV/EBITDA", "value": 11.5},
    "automobiles": {"metric": "EV/EBITDA", "value": 12.5},
    "fmcg": {"metric": "EV/EBITDA", "value": 20.5},
    "retail (apparel & electronics)": {"metric": "EV/EBITDA", "value": 14.0},
    "logistics": {"metric": "EV/EBITDA", "value": 13.0},
    "chemicals": {"metric": "EV/EBITDA", "value": 14.5},
    "real estate": {"metric": "EV/EBITDA", "value": 11.0},
    "infrastructure": {"metric": "EV/EBITDA", "value": 10.5},
    "airlines": {"metric": "EV/EBITDA", "value": 8.0},
    "hospitality (hotels & travel)": {"metric": "EV/EBITDA", "value": 13.0},
    "education (private k12 & edtech)": {"metric": "EV/EBITDA", "value": 16.0},
    "telecom": {"metric": "EV/EBITDA", "value": 9.5},
    "industrial goods & engineering": {"metric": "EV/EBITDA", "value": 13.5},
    "construction materials (cement, etc.)": {"metric": "EV/EBITDA", "value": 14.0},
    "energy (renewables)": {"metric": "EV/EBITDA", "value": 11.0},
    "energy (oil & gas)": {"metric": "EV/EBITDA", "value": 8.5},
    "metals & mining": {"metric": "EV/EBITDA", "value": 6.5},
    "banking (private)": {"metric": "P/BV", "value": 2.5},
    "banking (psu)": {"metric": "P/BV", "value": 1.2},
    "nbfcs": {"metric": "P/BV", "value": 2.8},
    "insurance": {"metric": "P/BV", "value": 3.0},
    "fintech (revenue generating)": {"metric": "EV/Revenue", "value": 6.0},
    "fintech (early stage)": {"metric": "EV/Revenue", "value": 8.0},
    "saas (enterprise software)": {"metric": "EV/Revenue", "value": 10.0},
    "internet/e-commerce": {"metric": "EV/Revenue", "value": 5.0},
    "gaming & media tech": {"metric": "EV/Revenue", "value": 4.5}
}


# EV = float(input("Enter the purchasing price (EV): "))
# Int_rate = float(input("Enter the Interest rate on Debt (%): "))

# EBITDA = float(input("Enter the current annual EBITDA of the target company: "))
# Hold = int(input("Enter your Duration: "))
EV = st.number_input("Enter the purchasing price (EV): ",min_value = 1)
if EV:
   try:
      EV = float(EV)
   except ValueError:
      st.error("Please enter a valid number: ")

EBITDA = st.number_input("Enter the current annual EBITDA of the target company: ",min_value =1)
if EBITDA:
   try:
      EBITDA = float(EBITDA)
   except ValueError:
    st.error("Please enter a valid number: ")

Int_rate = st.number_input("Please select the interest rate on Debt (%) example: 0.08,0.12",min_value =0.0000000001)
if Int_rate:
   try:
      Int_rate = float(Int_rate)
   
      if 0 < Int_rate < 1:
            Int_rate = Int_rate
      else:
            st.error("Please enter a decimal **between 0 and 1** (e.g., 0.08 for 8%)")
   except ValueError:
        st.error("Invalid input! Please enter a valid decimal number (e.g., 0.08)")

   

   
      
Hold = st.number_input("Enter your Duration/Exit year: ",min_value = 1,max_value = 1000,step =1)
Industry = st.selectbox("Your Target company belongs to which Industry: ",["it services",
"consumer staples",
"consumer discretionary",
"healthcare (pharma)",
"auto components",
"automobiles",
"fmcg",
"retail (apparel & electronics)",
"logistics",
"chemicals",
"real estate",
"infrastructure",
"airlines",
"hospitality (hotels & travel)",
"education (private k12 & edtech)",
"telecom",
"industrial goods & engineering",
"construction materials (cement, etc.)",
"energy (renewables)",
"energy (oil & gas)",
"metals & mining",
"banking (private)",
"banking (psu)",
"nbfcs",
"insurance",
"fintech (revenue generating)",
"fintech (early stage)",
"saas (enterprise software)",
"internet/e-commerce",
"gaming & media tech",
"Other"
])



IND_INPUT = Industry.lower()
if IND_INPUT not in exit_multiples:
    print("Industry data not available taking default exit multiple: 7")
    exit_multiple = 8
else:
    exit_multiple = exit_multiples[IND_INPUT]["value"]

debt1 = 0.6
debt2 = 0.7
debt3 = 0.8
debt4 = 0.9

equity1 = 1 - debt1
equity2 = 1 - debt2
equity3 = 1 - debt3
equity4 = 1 - debt4

Exit_EV = EBITDA*exit_multiple
Exit_value1 = Exit_EV - debt1*EV
Exit_value2 = Exit_EV - debt2*EV
Exit_value3 = Exit_EV - debt3*EV
Exit_value4 = Exit_EV - debt4*EV

denominator1 = equity1*EV
if denominator1 != 0:
    MOIC1 = Exit_value1 / denominator1
else:
    st.error("Error: Denominator is zero in MOIC1 calculation. Check your Equity and EV inputs.")
    MOIC1 = None 

denominator2 = equity2*EV
if denominator2 != 0:
    MOIC2 = Exit_value2 / denominator2
else:
    st.error("Error: Denominator is zero in MOIC1 calculation. Check your Equity and EV inputs.")
    MOIC2 = None 

denominator3 = equity3*EV
if denominator3 != 0:
    MOIC3 = Exit_value3 / denominator3
else:
    st.error("Error: Denominator is zero in MOIC1 calculation. Check your Equity and EV inputs.")
    MOIC3 = None 
denominator4 = equity4*EV
if denominator4 != 0:
    MOIC4 = Exit_value4 / denominator4
else:
    st.error("Error: Denominator is zero in MOIC1 calculation. Check your Equity and EV inputs.")
    MOIC4 = None 

MOIC1 = Exit_value1/(equity1*EV)
MOIC2 = Exit_value2/(equity2*EV)
MOIC3 = Exit_value3/(equity3*EV)
MOIC4 = Exit_value4/(equity4*EV)

industry_ebitda_growth = {
    "technology": 12.0,
    "healthcare": 9.5,
    "pharmaceuticals": 8.0,
    "fmcg": 6.5,
    "retail": 7.0,
    "automotive": 6.0,
    "logistics": 7.5,
    "manufacturing": 6.0,
    "real estate": 5.5,
    "telecom": 4.0,
    "energy": 4.5,
    "utilities": 3.0,
    "metals & mining": 5.0,
    "banking": 8.5,
    "insurance": 7.5,
    "media & entertainment": 9.0,
    "hospitality": 7.0,
    "construction": 6.5,
    "education": 10.0,
    "e-commerce": 14.0,
    "fintech": 13.0,
    "agribusiness": 5.5,
    "chemical": 6.5,
    "aviation": 4.5,
    "textiles": 5.0
}


if IND_INPUT not in industry_ebitda_growth:
    print("Industry not recognizable, using default EBITDA growth rate: .06")
    EBITDA_GR = .06
else:
    EBITDA_GR = EBITDA_GR = industry_ebitda_growth[IND_INPUT]/100


Cash_flows1 = [-1*equity1*EV]
for i in range(1,Hold+1):
    EBITDA_i = EBITDA*(1+EBITDA_GR)**i
    if i == Hold:
        terminal_value = EBITDA_i + Exit_value2
        Cash_flows1.append(terminal_value)
    else:
     Cash_flows1.append(EBITDA_i)

Cash_flows2 = [-1*equity2*EV]
for i in range(1,Hold+1):
    EBITDA_i = EBITDA*(1+EBITDA_GR)**i
    if i == Hold:
        terminal_value2 = EBITDA_i + Exit_value2
        Cash_flows2.append(terminal_value2)
    else:
     Cash_flows2.append(EBITDA_i)

Cash_flows3 = [-1*equity3*EV]
for i in range(1,Hold+1):
    EBITDA_i = EBITDA*(1+EBITDA_GR)**i
    if i == Hold:
        terminal_value3 = EBITDA_i + Exit_value3
        Cash_flows3.append(terminal_value3)
    else:
     Cash_flows3.append(EBITDA_i)

Cash_flows4 = [-1*equity4*EV]
for i in range(1,Hold+1):
    EBITDA_i = EBITDA*(1+EBITDA_GR)**i
    if i == Hold:
        terminal_value4 = EBITDA_i + Exit_value4
        Cash_flows4.append(terminal_value4)
    else:
     Cash_flows4.append(EBITDA_i)

IRR1 = npf.irr(Cash_flows1)
IRR2 = npf.irr(Cash_flows2)
IRR3 = npf.irr(Cash_flows3)
IRR4 = npf.irr(Cash_flows4)



# print(f"The IRR with 60% Debt is {IRR1:.2%} and The multiple on Invested Capital is {MOIC1:.2}x.")
# print(f"The IRR with 70% Debt is {IRR2:.2%} and The multiple on Invested Capital is {MOIC2:.2}x.")
# print(f"The IRR with 80% Debt is {IRR3:.2%} and The multiple on Invested Capital is {MOIC3:.2}x.")
# print(f"The IRR with 90% Debt is {IRR4:.2%} and The multiple on Invested Capital is {MOIC4:.2}x.")
# print("Thanks")
# st.write(f"The IRR with 60% Debt is {IRR1:.2%} and The multiple on Invested Capital is {MOIC1:.2}x.")
# st.write(f"The IRR with 70% Debt is {IRR2:.2%} and The multiple on Invested Capital is {MOIC2:.2}x.")
# st.write(f"The IRR with 80% Debt is {IRR3:.2%} and The multiple on Invested Capital is {MOIC3:.2}x.")
# st.write(f"The IRR with 90% Debt is {IRR4:.2%} and The multiple on Invested Capital is {MOIC4:.2}x.")
# st.write("Thanks")

# if npf.isnan(IRR1):
#     st.write(f"The IRR with 60% Debt is not computable (EBITDA too low), and the MOIC is {MOIC1:.2f}x.")
# else:
#     st.write(f"The IRR with 60% Debt is {IRR1:.2%} and the MOIC is {MOIC1:.2f}x.")

# if np.isnan(IRR1):
#     st.error("IRR with 60% Debt could not be computed due to invalid cash flows (EBITDA too low).")
# else:
#     st.write(f"The IRR with 60% Debt is {IRR1:.2%} and The multiple on Invested Capital is {MOIC1:.2}x.")

# if np.isnan(IRR2):
#     st.error("IRR with 70% Debt could not be computed due to invalid cash flows (EBITDA too low).")
# else:
#     st.write(f"The IRR with 70% Debt is {IRR2:.2%} and The multiple on Invested Capital is {MOIC2:.2}x.")

# if np.isnan(IRR3):
#     st.error("IRR with 80% Debt could not be computed due to invalid cash flows (EBITDA too low).")
# else:
#     st.write(f"The IRR with 80% Debt is {IRR3:.2%} and The multiple on Invested Capital is {MOIC3:.2}x.")

# if np.isnan(IRR4):
#     st.error("IRR with 90% Debt could not be computed due to invalid cash flows (EBITDA too low).")
# else:
#     st.write(f"The IRR with 90% Debt is {IRR4:.2%} and The multiple on Invested Capital is {MOIC4:.2}x.")

# st.text("Thank you")
     
if np.isnan(IRR1):
    st.error("IRR with 60% Debt could not be computed due to invalid cash flows (EBITDA too low).")
else:
    st.write(f"The IRR with 60% Debt is {IRR1:.2%} and The multiple on Invested Capital is {MOIC1:.2}x WITH annual interest payment of {debt1*EV*Int_rate}.")

st.text(f"The cash flow:  {Cash_flows1}")
if np.isnan(IRR2):
    st.error("IRR with 70% Debt could not be computed due to invalid cash flows (EBITDA too low).")
else:
    st.write(f"The IRR with 70% Debt is {IRR2:.2%} and The multiple on Invested Capital is {MOIC2:.2}x WITH annual interest payment of {debt2*EV*Int_rate}.")
st.text(f"The cash flow:  {Cash_flows2}")

if np.isnan(IRR3):
    st.error("IRR with 80% Debt could not be computed due to invalid cash flows (EBITDA too low).")
else:
    st.write(f"The IRR with 80% Debt is {IRR3:.2%} and The multiple on Invested Capital is {MOIC3:.2}x WITH annual interest payment of {debt3*EV*Int_rate}.")
st.text(f"The cash flow:  {Cash_flows3}")

if np.isnan(IRR4):
    st.error("IRR with 90% Debt could not be computed due to invalid cash flows (EBITDA too low).")
else:
    st.write(f"The IRR with 90% Debt is {IRR4:.2%} and The multiple on Invested Capital is {MOIC4:.2}x WITH annual interest payment of {debt4*EV*Int_rate}.")
st.text(f"The cash flow:  {Cash_flows4}")

st.text("Thank you")








