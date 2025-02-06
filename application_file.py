# import streamlit as st
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import spacy
# 
# # Load NLP model
# nlp = spacy.load("en_core_web_sm")
# 
# def extract_equation_params(text):
#     """
#     Extracts demand and supply equation parameters from a structured natural language query.
#     """
#     doc = nlp(text.lower())
#     numbers = [float(token.text) for token in doc if token.like_num]
# 
#     if len(numbers) < 12:
#         return None
# 
#     demand_intercept_corn, demand_slope_corn, supply_intercept_corn, supply_slope_corn, \
#     demand_intercept_cleaned, demand_slope_cleaned, supply_intercept_cleaned, supply_slope_cleaned, \
#     demand_intercept_no_loading, demand_slope_no_loading, supply_intercept_no_loading, supply_slope_no_loading = numbers[:12]
# 
#     demand_slope_corn = -abs(demand_slope_corn)
#     demand_slope_cleaned = -abs(demand_slope_cleaned)
#     demand_slope_no_loading = -abs(demand_slope_no_loading)
# 
#     return demand_intercept_corn, demand_slope_corn, supply_intercept_corn, supply_slope_corn, \
#            demand_intercept_cleaned, demand_slope_cleaned, supply_intercept_cleaned, supply_slope_cleaned, \
#            demand_intercept_no_loading, demand_slope_no_loading, supply_intercept_no_loading, supply_slope_no_loading
# 
# def calculate_equilibrium(demand_intercept, demand_slope, supply_intercept, supply_slope):
#     """
#     Computes Competitive Equilibrium: Quantity and Price.
#     Also calculates CS, PS, and SW for the competitive market.
#     """
#     quantity_eq = (demand_intercept - supply_intercept) / (supply_slope - demand_slope)
#     price_eq = demand_intercept + demand_slope * quantity_eq
# 
#     cs_eq = (demand_intercept - price_eq) * quantity_eq / 2
#     ps_eq = (price_eq - supply_intercept) * quantity_eq / 2
#     sw_eq = cs_eq + ps_eq
# 
#     return round(quantity_eq, 2), round(price_eq, 2), round(cs_eq, 2), round(ps_eq, 2), round(sw_eq, 2)
# 
# def plot_market(demand_intercept, demand_slope, supply_intercept, supply_slope, quantity_eq, price_eq, market_name, supply_intercept_alt=None, supply_slope_alt=None):
#     """
#     Plots the supply and demand curves for a given market.
#     """
#     q_range = np.linspace(0, quantity_eq * 1.5, 100)
#     demand_curve = demand_intercept + demand_slope * q_range
#     supply_curve_primary = supply_intercept + supply_slope * q_range
#     supply_curve_alt = supply_intercept_alt + supply_slope_alt * q_range if supply_intercept_alt is not None else None
# 
#     plt.figure(figsize=(8, 6))
#     plt.plot(q_range, demand_curve, label="Demand Curve", color="blue")
#     plt.plot(q_range, supply_curve_primary, label="Supply Curve (Cleaned-Up)", color="green")
#     if supply_curve_alt is not None:
#         plt.plot(q_range, supply_curve_alt, label="Supply Curve (No-Loading)", color="red", linestyle="dashed")
# 
#     plt.xlabel("Quantity")
#     plt.ylabel("Price")
#     plt.title(f"Market Equilibrium: {market_name}")
#     plt.legend()
#     st.pyplot(plt)
# 
# # Streamlit Interface
# st.title("Market Equilibrium Solver")
# 
# st.write("Enter a question in natural language (e.g., 'Corn demand has an intercept of 100 and slope of -2, and the corn supply has an intercept of 20 and slope of 3. The cleaned-up water demand has an intercept of 200 and slope of -4, and the cleaned-up water supply has an intercept of 64.38 and slope of 2.1. The hypothetical no-loading demand has an intercept of 200 and slope of -4 and the hypothetical no-loading slope has an intercept of 44.91 and slope of 2.1.')")
# user_query = st.text_area("Type your question here:", "")
# 
# if st.button("Solve"):
#     params = extract_equation_params(user_query)
# 
#     if params:
#         demand_intercept_corn, demand_slope_corn, supply_intercept_corn, supply_slope_corn, \
#         demand_intercept_cleaned, demand_slope_cleaned, supply_intercept_cleaned, supply_slope_cleaned, \
#         demand_intercept_no_loading, demand_slope_no_loading, supply_intercept_no_loading, supply_slope_no_loading = params
# 
#         # Compute Equilibria
#         quantity_eq_corn, price_eq_corn, cs_eq_corn, ps_eq_corn, sw_eq_corn = \
#             calculate_equilibrium(demand_intercept_corn, demand_slope_corn, supply_intercept_corn, supply_slope_corn)
# 
#         quantity_eq_cleaned, price_eq_cleaned, cs_eq_cleaned, ps_eq_cleaned, sw_eq_cleaned = \
#             calculate_equilibrium(demand_intercept_cleaned, demand_slope_cleaned, supply_intercept_cleaned, supply_slope_cleaned)
# 
#         quantity_eq_no_loading, price_eq_no_loading, cs_eq_no_loading, ps_eq_no_loading, sw_eq_no_loading = \
#             calculate_equilibrium(demand_intercept_no_loading, demand_slope_no_loading, supply_intercept_no_loading, supply_slope_no_loading)
# 
#         # Display Equilibrium Prices and Quantities
#         st.write("\n**Equilibrium Prices and Quantities:**")
#         st.write(f"- **Corn Market:** Price: ${price_eq_corn}, Quantity: {quantity_eq_corn} units")
#         st.write(f"- **Cleaned-Up Water Market:** Price: ${price_eq_cleaned}, Quantity: {quantity_eq_cleaned} units")
#         st.write(f"- **No-Loading Water Market:** Price: ${price_eq_no_loading}, Quantity: {quantity_eq_no_loading} units")
# 
#         # Display Surplus Table
#         surplus_data = pd.DataFrame({
#             "Scenario": ["Cleaned-Up Water Market", "No-Loading Water Market", "Difference"],
#             "Consumer Surplus": [cs_eq_cleaned, cs_eq_no_loading, cs_eq_no_loading - cs_eq_cleaned],
#             "Producer Surplus": [ps_eq_cleaned, ps_eq_no_loading, ps_eq_no_loading - ps_eq_cleaned],
#             "Total Social Welfare": [sw_eq_cleaned, sw_eq_no_loading, sw_eq_no_loading - sw_eq_cleaned]
#         })
#         st.table(surplus_data)
# 
#         # Plot Graphs
#         plot_market(demand_intercept_corn, demand_slope_corn, supply_intercept_corn, supply_slope_corn, quantity_eq_corn, price_eq_corn, "Corn Market")
#         plot_market(demand_intercept_cleaned, demand_slope_cleaned, supply_intercept_cleaned, supply_slope_cleaned, quantity_eq_cleaned, price_eq_cleaned, "Water Market", supply_intercept_no_loading, supply_slope_no_loading)
