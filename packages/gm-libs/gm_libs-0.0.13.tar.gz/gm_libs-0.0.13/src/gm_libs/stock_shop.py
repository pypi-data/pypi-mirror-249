# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


# 买指定数量的股票
def buy_count(stock: str, count: int, price: float):
    return order_volume(symbol=stock, volume=count, price=price, order_type=OrderType_Market, side=OrderSide_Buy,
                        position_effect=PositionEffect_Open)


# 买指定数量的股票
def l_buy_count(stock: str, count: int, price: float):
    return order_volume(symbol=stock, volume=count, price=price, order_type=OrderType_Market, side=OrderSide_Buy,
                        position_effect=PositionEffect_Open)


# 卖指定数量的股票
def sell_count(stock: str, count: int, price: float):
    return order_volume(symbol=stock, volume=count, price=price, order_type=OrderType_Market, side=OrderSide_Sell,
                        position_effect=PositionEffect_Open)


# 卖指定数量的股票
def l_sell_count(stock: str, count: int, price: float):
    return order_volume(symbol=stock, volume=count, price=price, order_type=OrderType_Market, side=OrderSide_Sell,
                        position_effect=PositionEffect_Open)


# 调整仓位（到特定数量）
def order_target_count(stock: str, volume: int, price: float):
    order_cancel_all()
    return order_target_volume(symbol=stock, volume=volume, price=price, order_type=OrderType_Market,
                               position_side=PositionSide_Long)


# 调整仓位（到特定数量）
def l_order_target_count(stock: str, volume: int, price: float):
    order_cancel_all()
    return order_target_volume(symbol=stock, volume=volume, price=price, order_type=OrderType_Market,
                               position_side=PositionSide_Long)


# 调整仓位（到特定价值）
def order_target_money(stock: str, worth: int, price: float):
    order_cancel_all()
    return order_target_value(symbol=stock, value=worth, price=price, order_type=OrderType_Market,
                              position_side=PositionSide_Long)


# 调整仓位（到特定价值）
def l_order_target_money(stock: str, worth: int, price: float):
    order_cancel_all()
    return order_target_value(symbol=stock, value=worth, price=price, order_type=OrderType_Market,
                              position_side=PositionSide_Long)
