
usage: ibtrader.py [-h] [-wt WAIT_TIME] [-new] [-os ORDER_SYMBOL]
                   [-ot ORDER_SECTYPE] [-oe ORDER_EXCHANGE]
                   [-oc ORDER_CURRENCY] [-oa ORDER_ACTION]
                   [-ol ORDER_LIMIT_PRICE] [-oo ORDER_TYPE]
                   [-oq ORDER_QUANTITY] [-pf] [-pp] [-ps] [-pe] [-pse] [-po]
                   [-d] [-nod] [-tcp TCP_PORT] [-cal] [-cso] [-clo] [-cls]
                   [-nw]

optional arguments:
  -h, --help            show this help message and exit
  -wt WAIT_TIME, --wait_time WAIT_TIME
                        Wait time in seconds for completion
  -new, --new_order     Place a new order
  -os ORDER_SYMBOL, --order_symbol ORDER_SYMBOL
                        Order Symbol
  -ot ORDER_SECTYPE, --order_secType ORDER_SECTYPE
                        Security Type [CASH|STK|FUT|OPT|etc]
  -oe ORDER_EXCHANGE, --order_exchange ORDER_EXCHANGE
                        Exchange [IDEALPRO|SMART]
  -oc ORDER_CURRENCY, --order_currency ORDER_CURRENCY
                        Currency USD
  -oa ORDER_ACTION, --order_action ORDER_ACTION
                        Order action BUY|SELL
  -ol ORDER_LIMIT_PRICE, --order_limit_price ORDER_LIMIT_PRICE
                        Limit Price for the order, ignored in case of market
                        order
  -oo ORDER_TYPE, --order_type ORDER_TYPE
                        Order Type LMT|MKT -- can be more
  -oq ORDER_QUANTITY, --order_quantity ORDER_QUANTITY
                        Order Quantity
  -pf, --print_portfolio
                        Print Portfolio
  -pp, --print_positions
                        Print ALL Positions
  -ps, --print_sym_position
                        Print Position for order_symbol
  -pe, --print_executions
                        Print Executions
  -pse, --print_sym_executions
                        Print Executions for order_symbol
  -po, --print_open_orders
                        Print Open Orders
  -d, --debug           Debug enable
  -nod, --no-debug      Debug disable
  -tcp TCP_PORT, --tcp_port TCP_PORT
                        Tcp port to use, default is 4001
  -cal, --cancel_all_orders
                        Cancel ALL open orders
  -cso, --cancel_sym_order
                        Cancel open orders for order_symbol
  -clo, --close_all_positions
                        Close ALL positions
  -cls, --close_sym_position
                        Close positions for order_symbol
  -nw, --no_wait_for_complete
                        Dont wait for completion, just exit after placing
                        order

