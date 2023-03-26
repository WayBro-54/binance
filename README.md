# Торговый робот для Binance

#### Бот берет данные котировок с Binance. <br>
Бот анализирует данные 3 стохастиков м15, м5 и м1 со стандартной настройкой для токена ETHUSDT<br>
Бот непрерывно получает цену монеты, и сохраняет в базу данных в случае если цена изменилась за час более чем на 1 процент, выводится сообщение в консоль.
Бот выдает сигналы в консоль, если: Значение стохастика пересекается на м15 и м1 выше 83,  м5  выше 65, выдает сигнал на продажу, сигнал на покупку бот выдает в случае если пересечение стохастика, для м15 и м1 было ниже 17, для м5 ниже 35.
 

#### Технологии:
* Python3.10
* Binance-python
* SQLAlchemy
* Numpy
* TA-lib

#### Установка:
Выполните следующие команды:
```
git clone git@github.com:WayBro-54/binance.git
```

#### Создайте в корневой папке файл .env
```
API_KEY=nbcX80iPChLIAJQRqBG4IDsiyM62uLEqsXYOuI4gyMgSWW2XQCTXHaLEjj4js4Qx
SECRET_KEY=55vLHUNUQ0ICj2eFCQNul0aqBEGje3Dy8NpAGevur6OQP2K6iu6yj1loybLWN2yw
```
#### Установка зависимостей
```
python3 -m venv vev
. venv/bin/activate
pip install -r requirements.txt
```

#### Для запуска выполните команду
```
python3 main.py
```
