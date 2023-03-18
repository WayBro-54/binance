from sqlalchemy import Column, String, Integer, DECIMAL, ForeignKey

from .db import Base


class InfoEthusdt(Base):
    __tablename__ = 'info_ethusdt'
    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    price = Column(DECIMAL(precision=4, scale=8))
    quantity = Column(DECIMAL(precision=4, scale=8))
    # symbol = Column(Integer, ForeignKey('symbol.id'))

# class Symbol(Base):
#     __tablename__ = 'symbol'
#     id = Column(Integer, primary_key=True)
#     ticker = Column(String, unique=True)
