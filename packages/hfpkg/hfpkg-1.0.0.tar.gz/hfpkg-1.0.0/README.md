# Final Project Package

This package is for the final project of AIN1001 by Fatma Hazal Bakırcı

## Overview

This package provides functionalities to calculate Simple Moving Averages (SMA) and Relative Strength Index (RSI) from given data. It includes modules for calculations (`calculations.py`) and file operations (`files.py`).

## Installation

```bash
pip install -e . !!!!!!!!!!!!!!!!!!!değiştirilecek
```

# Usage

## Example Script

```tsx
from hfpkg.src.calculations import calculate_sma, calculate_rsi
from hfpkg.src.files import read_csv, write_to_csv

# Read data from CSV file
file_path = 'path/to/your/orcl.csv'
close_prices = read_csv(file_path)

# Calculate 5-day SMA
sma_5day = calculate_sma(close_prices, value=5) #default value is 5

# Calculate 14-day RSI
rsi = calculate_rsi(close_prices, value=14) #default value is 14

# Write results to CSV files
write_to_csv(sma_5day, 'output_sma.csv')
write_to_csv(rsi, 'output_rsi.csv')

```

## Running Tests

```bash
python -m unittest hfpkg.test.test_calculations
python -m unittest hfpkg.test.test_files
```

# Project Structure

```tsx
│   .gitignore
│   README.md
│   run.py
│   setup.py
│
└───my_package
    │   __init__.py
    │
    ├───src
    │   │   calculations.py
    │   │   files.py
    │   │   __init__.py
    │
    └───test
        │   test_calculations.py
        │   test_files.py
        │   __init__.py


```
