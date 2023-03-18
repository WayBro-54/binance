import asyncio
from binance import AsyncClient, BinanceSocketManager
from core.config import API_KEY, SECRET_KEY


async def get_ethusdt_ticker():
    client = await AsyncClient.create(api_key=API_KEY, secret_key=SECRET_KEY)
    ticker = await client.get_symbol_ticker(symbol='ETHUSDT')
    await client.close_connection()
    return ticker

async def main():
    ticker = await get_ethusdt_ticker()
    print(ticker)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
