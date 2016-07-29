#!/usr/local/bin/python

# from stockfighter import Stockfighter
# import time
#
# #sf = Stockfighter()
#
# #level = sf.levels['first_steps']
# #info = level.start()
# #print(info)
#
# #account = info['account']
# #venue = sf.venues[info['venues'][0]]
# #stock = venue.stocks[info['tickers'][0]]
#
# def get_price():
#     price = 0
#     while price < 1:
#         time.sleep(1)
#         try:
#             price = stock.quote()['last']
#         except KeyError:
#             continue
#     return price
#
# def fill_orders(amount, max_amount=25):
#     while amount > 0:
#         price = get_price()
#
#         qty = min(amount, max_amount)
#         print("Buying {} shares of {} for {}.".format(qty, stock, price))
#         filled = stock.buy(account, price, qty, order_type='immediate-or-cancel')['totalFilled']
#         print("{} filled.".format(filled))
#         amount -= filled
#
# def solve():
#     fill_orders(100)