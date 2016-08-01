import logging
import time

logger = logging.getLogger(__name__)

GOAL=100
LIMIT=25

def solve(client, level_info):
    account = level_info['account']
    venue_symbol = level_info['venues'][0]
    stock_symbol = level_info['tickers'][0]

    logger.info("Buying %d shares of %s:%s on account %s with limit %d.",
        GOAL, venue_symbol, stock_symbol, account, LIMIT)
    
    stock = client.venues[venue_symbol].stocks[stock_symbol]
    fill_orders(account, stock, GOAL, LIMIT)
    
    logger.info("Done!")

def get_price(stock):
    price = 0
    while price < 1:
        time.sleep(1)
        try:
            logger.debug("Polling for quote.")
            price = stock.quote()['last']
            logger.debug("Found price %f.", price)
        except KeyError:
            continue
    return price
#
def fill_orders(account, stock, goal, limit):
    while goal > 0:
        price = get_price(stock)

        qty = min(goal, limit)
        logger.info("Buying {} shares of {} for {}.".format(qty, stock, price))
        filled = stock.buy(account, price, qty, order_type='immediate-or-cancel')['totalFilled']
        logger.info("{} filled.".format(filled))
        goal -= filled