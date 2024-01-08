# stock_indicators_package

This package calculates Simple Moving Averages (SMA) and Relative Strength Index (RSI) based on historical data.

## Installation

```bash
pip install stock-indicators-package


## Basic Usage

```python
from stock_indicators.stock_indicators import load_historical_data, calculate_indicators, write_to_file

# Load data from orcl.csv
file_path = 'orcl.csv'
historical_data = load_historical_data(file_path)

# Calculate indicators
sma_5, rsi_14 = calculate_indicators(historical_data)

# Write indicators to files
sma_headers = ['Date', 'Value']
sma_data = [{'Date': historical_data[i+4]['Date'], 'Value': sma_5[i]} for i in range(len(sma_5))]
write_to_file('orcl-sma.csv', sma_headers, sma_data)

rsi_headers = ['Date', 'Value']
rsi_data = [{'Date': historical_data[i+13]['Date'], 'Value': rsi_14[i][0]} for i in range(len(rsi_14))]
write_to_file('orcl-rsi.csv', rsi_headers, rsi_data)
