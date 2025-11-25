import requests

BINANCE_API = "https://api.binance.com/api/v3/ticker/price"

def convert_to_rub(asset: str, amount: float):
    if asset == "RUB":
        return amount
    symbol = f"{asset}RUB"
    r = requests.get(BINANCE_API, params={"symbol": symbol})
    data = r.json()
    price = float(data["price"])
    return amount * price
