#from stockfighter import Stockfighter
import os, time

# sf = Stockfighter()
#
# level = sf.levels['chock_a_block']
# info = level.start()
# print(info)
#
# sf = Stockfighter()
# print(sf.heartbeat())
#
# venue = sf.venues['PVIEX']
#
# stock = venue.stocks['SOF']
# for stock in venue.stocks:
#    print(stock)
#
# ORDER_SIZE = 50
# remaining = 100000 - 42823
# goal = 9103
#
# def run():
# while(remaining > 0):
#     quote = stock.quote()
#     size = quote['askSize']
#     if(size < 1):
#         continue
#         time.sleep(1)
#     ask = quote['ask']
#     if(ask > goal):
#         continue
#         time.sleep(1)
#     order = min(remaining, size, ORDER_SIZE)
#     if order > 0:
#         print('Placing order for {} at {}. Remaining: {}'.format(order, ask, remaining))
#         stock.buy(ACCOUNT, ask, order)
#         remaining -= order
#(venue='CENOEX', account='SAS22786391')