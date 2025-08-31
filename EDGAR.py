#=============================================================================================================
# Net income check
#=============================================================================================================
# import requests
# import pandas as pd

# TICKER = "MSFT"
# API_KEY = "4R5dScWpIEMYrtmF1yrRTrMMDQHIG7zY"  # get free key from https://financialmodelingprep.com

# # Fetch 10 years of annual income statements
# url = f"https://financialmodelingprep.com/api/v3/income-statement/{TICKER}?limit=5&apikey={API_KEY}"
# data = requests.get(url).json()

# # Extract relevant metrics
# records = []
# for report in data:
#     records.append({
#         "date": report['date'],
#         "netIncome": report.get('netIncome'),
#         "eps": report.get('eps'),
#         "operatingIncome": report.get('operatingIncome')
#     })

# df = pd.DataFrame(records)
# df = df.sort_values("date", ascending=True)  # oldest first
# print(df)

# if (df['netIncome'] <= 0).any():
#     print("Earnings Stability: ❌ Not stable (negative earnings detected)")
# else:
#     df['YoY_growth'] = df['netIncome'].pct_change()

#     cv = df['netIncome'].std() / df['netIncome'].mean()
    
#     yoy_std = df['YoY_growth'].iloc[1:].std()

#     if cv < 0.3 and yoy_std < 0.25:
#         stability = "✅ Stable"
#     else:
#         stability = "⚠️ Unstable / volatile"
    
#     print(f"Earnings Stability Check for {TICKER}:")
#     print(f"  - Coefficient of Variation (CV) = {cv:.2f}")
#     print(f"  - YoY growth std deviation = {yoy_std:.2f}")
#     print(f"  => {stability}")

# print("\nFull Income Data with YoY Growth:")
# print(df)

#=============================================================================================================
# # dividend Check
#=============================================================================================================

# import yfinance as yf
# import pandas as pd
# from datetime import datetime

# # Fetch dividend history
# ticker = yf.Ticker("TSLA")
# dividends = ticker.dividends  # Series with date index

# # Convert to DataFrame
# df = dividends.reset_index()
# df.columns = ["Date", "Dividend"]
# df['Year'] = df['Date'].dt.year

# # Group by year and sum dividends
# dividends_by_year = df.groupby('Year')['Dividend'].sum().reset_index()

# # Filter for last 20 years
# current_year = datetime.now().year
# dividends_20y = dividends_by_year[dividends_by_year['Year'] >= current_year - 20]

# print("=== Intel Dividend History (Last 20 Years) ===")
# print(dividends_20y.to_string(index=False))

# years_with_dividends = dividends_20y[dividends_20y['Dividend'] > 0]['Year'].tolist()
# current_year = datetime.now().year
# expected_years = list(range(current_year-20, current_year))
# missing_years=[i for i in expected_years if i not in years_with_dividends]
# if not missing_years:
#     print("Regular dividends for last 20 years")
# else:
#     print(f"Missing dividends in years: {missing_years}")
