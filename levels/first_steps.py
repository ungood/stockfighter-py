import logging
import time

logger = logging.getLogger(__name__)

GOAL=100
LIMIT=100

def solve(client, level_info):
    account = level_info['account']
    venue_symbol = level_info['venues'][0]
    stock_symbol = level_info['tickers'][0]

    logger.info("Buying %d shares of %s:%s on account %s with limit %d.",
        GOAL, venue_symbol, stock_symbol, account, LIMIT)
    
    stock = client.venues[venue_symbol].stocks[stock_symbol]
    fill_orders(account, stock, GOAL, LIMIT)
    
    logger.info("Done!")

def get_next_trade(stock):
    while True:
        time.sleep(1)
        try:
            logger.debug("Polling for quote.")
            price = stock.quote()['ask']
            qty = stock.quote()['askSize']
            logger.debug("Found %d shares at price %f.", qty, price)
            return price, qty
        except KeyError:
            continue
#
def fill_orders(account, stock, goal, limit):
    while goal > 0:
        price, qty = get_next_trade(stock)

        qty = min(qty, goal, limit)
        logger.info("Buying {} shares of {} for {}.".format(qty, stock, price))
        filled = stock.buy(account, price, qty, order_type='immediate-or-cancel')['totalFilled']
        logger.info("{} filled.".format(filled))
        goal -= filled