def load_historical_data(file_path):
    historical_data = []
    with open(file_path, 'r') as file:
        # Skip the header line
        header = file.readline().strip().split(',')
        for line in file:
            values = line.strip().split(',')
            entry = dict(zip(header, values))
            historical_data.append(entry)
    return historical_data


def calculate_indicators(data):
    sma_5 = []  # Simple Moving Averages for a 5-day window
    rsi_14 = []  # Relative Strength Index (RSI) for a 14-day window
    close_prices = [float(entry['Close']) for entry in data]

    # Calculate SMA for a 5-day window
    for i in range(4, len(close_prices)):
        sma_5_value = sum(close_prices[i-4:i+1]) / 5
        sma_5.append(sma_5_value)

    # Calculate RSI for a 14-day window
    for i in range(13, len(close_prices)):
        gains = [close_prices[j+1] - close_prices[j] for j in range(i-13, i) if close_prices[j+1] > close_prices[j]]
        losses = [-min(0, close_prices[j+1] - close_prices[j]) for j in range(i-13, i) if close_prices[j+1] < close_prices[j]]

        avg_gain = (sum(gains) + 13 * rsi_14[-1][0] if rsi_14 else 0) / 14
        avg_loss = (sum(losses) + 13 * rsi_14[-1][1] if rsi_14 else 0) / 14

        if avg_loss == 0:
            rsi_14_value = 100
        else:
            relative_strength = avg_gain / avg_loss
            rsi_14_value = 100 - (100 / (1 + relative_strength))

        rsi_14.append((avg_gain, avg_loss))

    return sma_5, rsi_14


def write_to_file(file_name, headers, data):
    with open(file_name, 'w') as file:
        file.write(','.join(headers) + '\n')
        for i in range(len(data)):
            file.write(f"{data[i]['Date']},{data[i]['Value']}\n")

