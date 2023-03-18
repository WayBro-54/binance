import asyncio
import os
from pprint import pprint
import numpy as np
from core.config import API_KEY, SECRET_KEY, DB_NAME
from core.db import create_database, async_session
from core.table import InfoEthusdt
from binance import AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException


async def get_stoch():
    client = await AsyncClient.create(api_key=API_KEY, api_secret=SECRET_KEY)

    try:
        klines = await client.get_klines(symbol='ETHUSDT', interval=client.KLINE_INTERVAL_1MINUTE, limit=14)
        closes = np.array([float(x[4]) for x in klines])
        highs = np.array([float(x[2]) for x in klines])
        lows = np.array([float(x[3]) for x in klines])
        highest_high = np.max(highs[:-1])
        lowest_low = np.min(lows[:-1])
        k_value = ((closes[-1] - lowest_low) / (highest_high - lowest_low)) * 100
        d_value = np.mean(k_value[-3:])
        # return k_value, d_value
        print(d_value, k_value)
    except BinanceAPIException as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        await client.close_connection()


# async def get_ethusdt_ticker(session):
#     client = await AsyncClient.create(api_key=API_KEY, api_secret=SECRET_KEY)
#     bm = BinanceSocketManager(client)
#     ts = bm.trade_socket('ETHUSDT')
#     async with ts as tscm:
#         while True:
#             res = await tscm.recv()
#             ticker_data = {
#                 'price': res['p'],
#                 'timestamp': res['T'],
#             }
#             tecker = InfoEthusdt(**ticker_data)
#             session.add(tecker)
#             await session.commit()
#             await client.close_connection()


async def main():
    async with async_session() as session:
        # await get_ethusdt_ticker(session)
        await get_stoch()


if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
        create_database()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()
