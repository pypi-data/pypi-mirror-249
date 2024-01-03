# StockInfo

StockInfo is a Python package for loading historical stock data, calculating Simple Moving Averages (SMA) and Relative Strength Index (RSI), and writing the results to CSV files.

## Installation

You can install StockInfo using pip:

```bash
pip install stockinfoain1001
```
## Usage
### Loading historical data:
```python
from stockinfoain1001 import StockInfo

# Create an instance of the StockInfo class
stock_info = StockInfo()

# Load historical data from a CSV file (default: "orcl.csv" in the 'data' directory)
stock_info.load_data()

# Access the loaded data
data = stock_info.Data
```
### Calculating Simple Moving Averages (SMA):
```python
# Calculate SMA with a specified window size (default: 5)
sma_values = stock_info.calculate_sma(window_size=10)

# Access the calculated SMA values
print(sma_values)
```
### Calculating Relative Strength Index (RSI):
```python
# Calculate RSI with a specified window size (default: 14)
rsi_values = stock_info.calculate_rsi(window_size=14)

# Access the calculated RSI values
print(rsi_values)
```
### Writing Results to CSV:
```python
# Write SMA results to a CSV file
sma_header = ['Date', 'Close', 'SMA']
sma_data = [(stock_info.Data[i]["Date"], stock_info.Data[i]['Close'], sma) for i, sma in enumerate(sma_values)]
stock_info.write_file("sma_results.csv", sma_header, sma_data)

# Write RSI results to a CSV file
rsi_header = ['Date', 'Close', 'RSI']
rsi_data = [(stock_info.Data[i]["Date"], stock_info.Data[i]['Close'], rsi) for i, rsi in enumerate(rsi_values)]
stock_info.write_file("rsi_results.csv", rsi_header, rsi_data)
```
## Examples
### Basic Usage:
```python
from stockinfoain1001 import StockInfo

# Load historical data
stock_info = StockInfo()
stock_info.load_data()

# Calculate SMA and write results to CSV
sma_values = stock_info.calculate_sma(window_size=5)
sma_header = ['Date', 'Close', 'SMA']
sma_data = [(stock_info.Data[i]["Date"], stock_info.Data[i]['Close'], sma) for i, sma in enumerate(sma_values)]
stock_info.write_file("sma_results.csv", sma_header, sma_data)

# Calculate RSI and write results to CSV
rsi_values = stock_info.calculate_rsi(window_size=14)
rsi_header = ['Date', 'Close', 'RSI']
rsi_data = [(stock_info.Data[i]["Date"], stock_info.Data[i]['Close'], rsi) for i, rsi in enumerate(rsi_values)]
stock_info.write_file("rsi_results.csv", rsi_header, rsi_data)
```
### Custom Data File and Output Directory:
```python
from stockinfoain1001 import StockInfo

# Load historical data
stock_info = StockInfo()
stock_info.load_data()

# Calculate SMA and write results to CSV
sma_values = stock_info.calculate_sma(window_size=5)
sma_header = ['Date', 'Close', 'SMA']
sma_data = [(stock_info.Data[i]["Date"], stock_info.Data[i]['Close'], sma) for i, sma in enumerate(sma_values)]
stock_info.write_file("sma_results.csv", sma_header, sma_data)

# Calculate RSI and write results to CSV
rsi_values = stock_info.calculate_rsi(window_size=14)
rsi_header = ['Date', 'Close', 'RSI']
rsi_data = [(stock_info.Data[i]["Date"], stock_info.Data[i]['Close'], rsi) for i, rsi in enumerate(rsi_values)]
stock_info.write_file("rsi_results.csv", rsi_header, rsi_data)
```
## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please create an issue or submit a pull request.

## Licence
This project is licensed under the MIT License