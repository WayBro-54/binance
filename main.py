import asyncio
import os
from datetime import datetime, timedelta
from decimal import Decimal

import talib
import numpy as np
from binance import AsyncClient, BinanceSocketManager
from sqlalchemy import select

from core.config import (API_KEY, SECRET_KEY, DB_NAME, EVERY_5MINUTES,
                         EVERY_15MINUTES, CLOSE, HIGH, LOW, INDEX_FOR_1MIN,
                         INDEX_FOR_5MIN, INDEX_FOR_15MIN)
from core.db import create_database, AsyncSessionLocal
from core.table import InfoEthusdt


async def percent_price_one_hour(session, timestamp, price):
    """Расчитывем процент изменения цена за 1 час."""
    timestamp = timestamp-3600
    price_old = await session.execute(
        select(InfoEthusdt.price).where(InfoEthusdt.timestamp == timestamp)
    )
    price_old = price_old.scalar()
    if price_old:
        price_old = price_old
        percent = abs((Decimal(price) - price_old) / price_old * 100)
        if percent >= 1:
            print(f'Цена изменилась на {percent:.2f} процентов.')


async def get_now100_bars(data_bars100, client, current_time):
    """Получаем новые данные о 100 новых баров."""

    if current_time.second == 0:
        # получаем данные 100 баров 1м т.ф.
        new_data_m1 = await client.futures_klines(symbol='ETHUSDT',
                                                  interval=client.KLINE_INTERVAL_1MINUTE,
                                                  limit=100),
        data_bars100[INDEX_FOR_1MIN] = new_data_m1[0]

    if (current_time.minute in EVERY_5MINUTES) and (current_time.second == 0):
        # получаем данные 100 баров 5м т.ф.
        new_data_m5 = await client.futures_klines(symbol='ETHUSDT',
                                                  interval=client.KLINE_INTERVAL_5MINUTE,
                                                  limit=100),
        data_bars100[INDEX_FOR_5MIN] = new_data_m5[0]

    if (current_time.minute in EVERY_15MINUTES) and (current_time.second == 0):
        # получаем данные 100 баров 15м т.ф.
        new_data_m15 = await client.futures_klines(symbol='ETHUSDT',
                                                   interval=client.KLINE_INTERVAL_15MINUTE,
                                                   limit=100),
        data_bars100[INDEX_FOR_15MIN] = new_data_m15[0]

    return data_bars100


async def get_stoch_now(klines):
    """Функция получения текущих данных стохастика."""
    closes = np.array([float(x[4]) for x in klines])
    highs = np.array([float(x[2]) for x in klines])
    lows = np.array([float(x[3]) for x in klines])
    fastk, fastd = talib.STOCH(
        close=closes,
        high=highs,
        low=lows,
        fastk_period=14,
        slowk_period=1,
        slowd_period=3
    )
    return fastk[-1], fastd[-1]


async def analysis_stoch(data):
    """Функция анализа данных стохастика."""
    # получаем значение стохастика
    res = await asyncio.gather(
        get_stoch_now(data[INDEX_FOR_1MIN]),
        get_stoch_now(data[INDEX_FOR_5MIN]),
        get_stoch_now(data[INDEX_FOR_15MIN]),
    )

    # присваиваем переменные значениям стохастика
    m1_k, m1_d = res[INDEX_FOR_1MIN]
    m5_k, m5_d = res[INDEX_FOR_5MIN]
    m15_k, m15_d = res[INDEX_FOR_15MIN]

    if (m1_k >= m1_d >= 83) and (m5_k and m5_d >= 65) and (m15_k >= m15_d >= 83):
        print('Рассматриваем вход в sell')

    if (m1_k <= m1_d <= 17) and (m5_k and m5_d <= 35) and (m15_k <= m15_d <= 17):
        print('Рассматриваем вход в buy')


async def get_kline_(bm, bars):
    """Функция обновляет значение текущего бара."""
    async with bm as bm_:
        res = await bm_.recv()
        bars[-1][HIGH] = res['k']['h']
        bars[-1][CLOSE] = res['k']['c']
        bars[-1][LOW] = res['k']['l']
        return bars


async def analysis_eth(bm, client):
    # объявляем сокеты для получения данных
    tsm1 = bm.kline_futures_socket('ETHUSDT', client.KLINE_INTERVAL_1MINUTE)
    tsm5 = bm.kline_futures_socket('ETHUSDT', client.KLINE_INTERVAL_5MINUTE)
    tsm15 = bm.kline_futures_socket('ETHUSDT', client.KLINE_INTERVAL_15MINUTE)

    # загружаем историю
    get_100bars = await asyncio.gather(
        client.futures_klines(symbol='ETHUSDT', interval=client.KLINE_INTERVAL_1MINUTE, limit=100),
        client.futures_klines(symbol='ETHUSDT', interval=client.KLINE_INTERVAL_5MINUTE, limit=100),
        client.futures_klines(symbol='ETHUSDT', interval=client.KLINE_INTERVAL_15MINUTE, limit=100)
    )
    while True:
        # обновляем 100 полседних баров
        # знаю, что это не камельфо...
        curr_date = datetime.now()
        get_100bars = await get_now100_bars(get_100bars, client, curr_date)

        # обновляем данные таймфреймов для последнего бара
        res = await asyncio.gather(
            get_kline_(tsm1, get_100bars[INDEX_FOR_1MIN]),
            get_kline_(tsm5, get_100bars[INDEX_FOR_5MIN]),
            get_kline_(tsm15, get_100bars[INDEX_FOR_15MIN])
        )

        # проводим анализ стохастика
        await analysis_stoch(res)


async def get_history_price(client, session):
    """Получаем историю баров"""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)
    start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

    klines = await client.futures_historical_klines(symbol='ETHUSDT',
                                                    interval=client.KLINE_INTERVAL_1MINUTE,
                                                    start_str=start_str,
                                                    limit=60)
    for i in klines:
        price = i[1]
        timestamp = int(str(i[0])[:-3])

        data_ticker = {
            'price': price,
            'timestamp': timestamp
        }
        ticker = InfoEthusdt(**data_ticker)
        session.add(ticker)
        await session.commit()


async def get_price_eth(bm, session, client):
    """Функция непрерывно считывает цену с биржи"""
    await get_history_price(client, session)
    ts_p = bm.kline_futures_socket('ETHUSDT', client.KLINE_INTERVAL_1MINUTE)
    async with ts_p as tsbm:
        while True:
            res = await tsbm.recv()

            price = res['k']['c']
            timestamp = int(str(res['k']['t'])[:-3])
            data_ticker = {
                'price': price,
                'timestamp': timestamp
            }

            is_exists = await session.execute(
                select(InfoEthusdt.id).where(InfoEthusdt.timestamp == timestamp).limit(1)
            )
            is_exists_id = is_exists.scalar()
            if not is_exists_id:
                ticker = InfoEthusdt(**data_ticker)
                session.add(ticker)
                await session.commit()
            await percent_price_one_hour(session, timestamp, price)


async def main():
    client = await AsyncClient.create(api_key=API_KEY, api_secret=SECRET_KEY)
    bm = BinanceSocketManager(client)
    async with AsyncSessionLocal() as session:
        await asyncio.gather(
            analysis_eth(bm, client),
            get_price_eth(bm, session, client)
        )


if __name__ == '__main__':
    if not os.path.exists(DB_NAME):
        create_database()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()
