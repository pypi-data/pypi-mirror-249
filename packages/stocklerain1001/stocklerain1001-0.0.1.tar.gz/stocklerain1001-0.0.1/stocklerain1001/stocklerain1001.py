import os

class StockInfo:
    def __init__(self):
        self.Data = []

    def load_data(self, file_name="orcl.csv"):
        """
        Load historical data from a CSV file.
        """
        file_path = os.path.join(os.path.dirname(__file__), "data", file_name)
        with open(file_path, "rt") as file:
            next(file)
            for row in file:
                date, opent, high, low, close, adj, volume = row.strip().split(",")
                dicto = {
                    "Date": date,
                    "Open": float(opent),
                    "High": float(high),
                    "Low": float(low),
                    "Close": float(close),
                    "Volume": int(volume)
                }
                self.Data.append(dicto)

    def calculate_sma(self, window_size=5):
        """
        Calculate Simple Moving Averages (SMA).
        """
        sma_list = []
        for i in range(len(self.Data)):
            if i < window_size - 1:
                sma_list.append(None)
            else:
                window_prices = [self.Data[j]["Close"] for j in range(i, i - window_size, -1)]
                sma_amount = sum(window_prices) / window_size
                sma_list.append(sma_amount)
        return sma_list

    def calculate_rsi(self, window_size=14):
        """
        Calculate Relative Strength Index (RSI).
        """
        rsi_list = []
        for i in range(len(self.Data)):
            gain = []
            loss = []
            if i < window_size - 1:
                rsi_list.append(None)
            else:
                for j in range(i, i - window_size, -1):
                    price_diff = self.Data[j]["Close"] - self.Data[j - 1]["Close"]
                    if price_diff > 0:
                        gain.append(price_diff)
                        loss.append(0)
                    else:
                        gain.append(0)
                        loss.append(abs(price_diff))
                avg_gain = sum(gain) / window_size
                avg_loss = sum(loss) / window_size
                rs = avg_gain / (avg_loss + 1e-10)
                rsi = 100 - (100 / (1 + rs))
                rsi_list.append(rsi)
        return rsi_list

    def write_file(self, file_name, header, data, output_dir="output"):
        """
        Write data to a CSV file.
        """
        output_path = os.path.join(os.path.dirname(__file__), output_dir)
        os.makedirs(output_path, exist_ok=True)

        file_path = os.path.join(output_path, file_name)
        with open(file_path, "w") as file:
            file.write(",".join(header) + "\n")
            for row in data:
                file.write(",".join(str(value) for value in row) + "\n")


if __name__ == "__main__":
    stock_info = StockInfo()

    stock_info.load_data("orcl.csv")

    sma_values = stock_info.calculate_sma(window_size=5)

    sma_header = ['Date', 'Close', 'SMA']
    sma_data = [(stock_info.Data[i]["Date"], stock_info.Data[i]['Close'], sma) for i, sma in enumerate(sma_values)]
    stock_info.write_file("orcl-sma.csv", sma_header, sma_data)

    rsi_values = stock_info.calculate_rsi(window_size=14)

    rsi_header = ['Date', 'Close', 'RSI']
    rsi_data = [(stock_info.Data[i]["Date"], stock_info.Data[i]['Close'], rsi) for i, rsi in enumerate(rsi_values)]
    stock_info.write_file("orcl-rsi.csv", rsi_header, rsi_data)
