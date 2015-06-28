usage: ibtrader.py [-h] [-iboid] [-qt] [-wt WAIT_TIME] [-gw] [-tws] [-new]
                   [-ts] [-tf] [-to] [-ll] [-lm] [-sl] [-sm] [-sym SYMBOL]
                   [-ot ORDER_SECTYPE] [-oe ORDER_EXCHANGE]
                   [-ope ORDER_PRIMARYEXCHANGE] [-oc ORDER_CURRENCY]
                   [-oa ORDER_ACTION] [-ol ORDER_LIMIT_PRICE] [-oo ORDER_TYPE]
                   [-oid ORDER_ID] [-oq ORDER_QUANTITY] [-pf] [-pc] [-pp]
                   [-ps] [-pe] [-pse] [-pid] [-po] [-pso] [-d] [-nod]
                   [-tcp TCP_PORT] [-clid TWS_CLIENTID] [-host TWS_HOST]
                   [-cal] [-cso] [-cid CANCEL_ORDERID] [-clo] [-cls] [-nw]
                   [-acnum ACCOUNT_NUMBER]

optional arguments:
  -h, --help            show this help message and exit
  -iboid, --use_ib_orderid_call
                        Use IB Orderid mechanism
  -qt, --quote          Get quote for the symbol
  -wt WAIT_TIME, --wait_time WAIT_TIME
                        Wait time in seconds for completion
  -gw, --gateway        Use gateway tcp port 4001 by default
  -tws, --tws           Use TWS tcp port 7496 by default
  -new, --new_order     Place a new order
  -ts, --trade_stock    Place a stock order [STK,SMART,USD]
  -tf, --trade_forex    Place a forex order [CASH,IDEALPRO,USD]
  -to, --trade_options  Place an options order [OPT,SMART,USD]
  -ll, --long_lmt       Place a Long Limit order
  -lm, --long_mkt       Place a Long Market order
  -sl, --short_lmt      Place a Short Limit order
  -sm, --short_mkt      Place a Short Market order
  -sym SYMBOL, --symbol SYMBOL
                        Symbol
  -ot ORDER_SECTYPE, --order_secType ORDER_SECTYPE
                        Security Type [CASH|STK|FUT|OPT|etc]
  -oe ORDER_EXCHANGE, --order_exchange ORDER_EXCHANGE
                        Exchange [IDEALPRO|SMART]
  -ope ORDER_PRIMARYEXCHANGE, --order_primaryexchange ORDER_PRIMARYEXCHANGE
                        Primary Exchange [IDEALPRO|SMART]
  -oc ORDER_CURRENCY, --order_currency ORDER_CURRENCY
                        Currency USD
  -oa ORDER_ACTION, --order_action ORDER_ACTION
                        Order action BUY|SELL
  -ol ORDER_LIMIT_PRICE, --order_limit_price ORDER_LIMIT_PRICE
                        Limit Price for the order, ignored in case of market
                        order
  -oo ORDER_TYPE, --order_type ORDER_TYPE
                        Order Type LMT|MKT -- can be more
  -oid ORDER_ID, --order_id ORDER_ID
                        Order ID - used to search execution
  -oq ORDER_QUANTITY, --order_quantity ORDER_QUANTITY
                        Order Quantity
  -pf, --print_portfolio
                        Print Portfolio
  -pc, --print_cash     Print Cash in Portfolio
  -pp, --print_positions
                        Print ALL Positions
  -ps, --print_sym_position
                        Print Position for Symbol
  -pe, --print_executions
                        Print Executions
  -pse, --print_sym_executions
                        Print Executions for Symbol
  -pid, --print_order_id
                        Print Executions By Order ID
  -po, --print_open_orders
                        Print Open Orders
  -pso, --print_open_sym_orders
                        Print Open Orders for Symbol
  -d, --debug           Debug enable
  -nod, --no-debug      Debug disable
  -tcp TCP_PORT, --tcp_port TCP_PORT
                        Tcp port to use, default is 4001
  -clid TWS_CLIENTID, --tws_clientid TWS_CLIENTID
                        TWS Client ID, default is 8899
  -host TWS_HOST, --tws_host TWS_HOST
                        host name/address to use, default is localhost
  -cal, --cancel_all_orders
                        Cancel ALL open orders
  -cso, --cancel_sym_order
                        Cancel open orders for Symbol
  -cid CANCEL_ORDERID, --cancel_orderid CANCEL_ORDERID
                        Cancel IB order id
  -clo, --close_all_positions
                        Close ALL positions
  -cls, --close_sym_position
                        Close positions for Symbol
  -nw, --no_wait_for_complete
                        Dont wait for completion, just exit after placing
                        order
  -acnum ACCOUNT_NUMBER, --account_number ACCOUNT_NUMBER
                        Account Number
