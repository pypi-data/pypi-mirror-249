#calculate n-day (default = 5) Simple Moving Averages (SMA)
def calculate_sma(close_prices, value=5):
    sma_values = [(sum(close_prices[i - value + 1 : i + 1]) / value) for i in range(value - 1, len(close_prices))]
    return sma_values


#calculate n-day (default = 14) Relative Strength Index (RSI)
def calculate_rsi(close_prices, value=14):
    daily_changes = [close_prices[i] - close_prices[i - 1] for i in range(1, len(close_prices))] #calculate daily price changes
    average_gains = [max(0, daily_changes[i]) for i in range(value)] #initialize average gains for the first 14 days
    average_losses = [max(0, -daily_changes[i]) for i in range(value)] #initialize average losses for the first 14 days

    #calculate average gains and losses for the remaining days
    for i in range(value, len(daily_changes)):
        average_gain = (average_gains[-1] * (value - 1) + max(daily_changes[i], 0)) / value
        average_loss = (average_losses[-1] * (value - 1) + max(-daily_changes[i], 0)) / value
        average_gains.append(average_gain)
        average_losses.append(average_loss)
    
    #calculate Relative Strength (RS) and Relative Strength Index (RSI)
    rs = [average_gain / average_loss if average_loss != 0 else 0 for average_gain, average_loss in zip(average_gains, average_losses)]
    rsi = [100 - (100 / (1 + rs_value)) for rs_value in rs]

    return rsi
