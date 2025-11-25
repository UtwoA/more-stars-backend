import httpx

BINANCE_API = "https://api.binance.com/api/v3/ticker/price"

async def convert_to_rub(symbol: str, amount: float) -> float:
    async with httpx.AsyncClient() as client:
        if symbol.upper() == "TON":
            r = await client.get(f"{BINANCE_API}?symbol=TONUSDT")
            ton_to_usdt = float(r.json()["price"])
            amount_usdt = amount * ton_to_usdt
        else:
            amount_usdt = amount  # USDT без конвертации

        r = await client.get(f"{BINANCE_API}?symbol=USDTRUB")
        usdt_to_rub = float(r.json()["price"])
        return round(amount_usdt * usdt_to_rub, 2)
