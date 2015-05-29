#!/usr/bin/python
import datetime
from peewee import *

database = MySQLDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database

class DbAccountInfo(BaseModel):
    account_broker = CharField(db_column='Account_Broker', null=True)
    account_name = CharField(db_column='Account_Name', null=True)
    account_number = CharField(db_column='Account_Number', primary_key=True)
    program_name = CharField(default="ibtrader.py", null=False)
    account_value = IntegerField(db_column='Account_Value', null=True)
    gw_tcp_ip_addr = CharField(db_column='GW_TCP_IP_ADDR', null=True)
    gw_tcp_port_num = IntegerField(db_column='GW_TCP_PORT_NUM', null=True)
    tws_tcp_ip_addr = CharField(db_column='TWS_TCP_IP_ADDR', null=True)
    tws_tcp_port_num = IntegerField(db_column='TWS_TCP_PORT_NUM', null=True)
    timelastsynced = DateTimeField(default=datetime.datetime.now, db_column='TimeLastSynced')

    hostname = CharField(null = True)
    portnumber = IntegerField(default=0, null = True)



    class Meta:
        db_table = 'DB_ACCOUNT_INFO'

#{"execid": "0001f4e8.5563fa39.01.01", "exchange": "IDEALPRO", "exectime": "20150526  13:47:31", "primaryExchange": "", "clientid": 8899, "qty": 30000, "localsymbol": "EUR.USD", "execshares": 30000, "accountName": "DU226708", "orderid": 38, "execprice": 1.0879, "permid": 1894681312, "secType": "CASH", "avgprice": 1.0879, "commission": 2.0, "symbol": "EUR", "expiry": "", "side": "SLD"}, 
class DbBrokerExecReport(BaseModel):
    ib_orderid = IntegerField(db_column='IB_orderid', null=True)
    account_number = CharField(null=True)
    avgprice = DecimalField(max_digits=10, decimal_places=5, null=True)
    clientid = IntegerField(null=True)
    exchange = CharField(null=True)
    primary_exchange = CharField(null=True)
    execid = CharField(primary_key=True, null=True)
    execprice = DecimalField(max_digits=10, decimal_places=5, null=True)
    commission = DecimalField(max_digits=10, decimal_places=3, null=True)
    execshares = IntegerField(null=True)
    exectime = DateTimeField(null=False)
    expiry = CharField(null=True)
    permid = IntegerField(null=True)
    qty_filled = IntegerField(null=True)
    side = CharField(null=True)
    symbol = CharField(null=True)
    localsymbol = CharField(null=True)
    sectype = CharField(null=True)

    class Meta:
        db_table = 'DB_BROKER_EXEC_REPORT'

class DbBrokerPortfolio(BaseModel):
    accountname = CharField(db_column='accountName', null=True)
    averagecost = DecimalField(max_digits=10, decimal_places=4, db_column='averageCost', null=True)
    local_symbol = CharField(primary_key=True)
    costprice = DecimalField(max_digits=10, decimal_places=2, db_column='costPrice', null=True)
    gnloss = DecimalField(max_digits=10, decimal_places=2, null=True)
    unrealizedpnl = DecimalField(max_digits=10, decimal_places=2, null=True)
    holding_type = CharField(null=True)
    curr_action = CharField(null=True)
    flip_action = CharField(null=True)
    sectype = CharField(null=True)
    marketprice = DecimalField(max_digits=10, decimal_places=4, db_column='marketPrice', null=True)
    marketvalue = DecimalField(max_digits=10, decimal_places=2, db_column='marketValue', null=True)
    quantity = IntegerField(null=True)
    symbol = CharField(null=True)
    expiry = CharField(null=True)
    currency = CharField(null=True)
    exchange = CharField(null=True)
    primary_exchange = CharField(null=True)

    class Meta:
        db_table = 'DB_BROKER_PORTFOLIO'

class DbCurrentQuote(BaseModel):
    symbol = CharField(primary_key=True)
    last_bid_price = DecimalField(max_digits=10, decimal_places=4, null=True)
    last_bid_time = DateTimeField(null=True)
    last_ask_price = DecimalField(max_digits=10, decimal_places=4, null=True)
    last_ask_time = DateTimeField(null=True)
    last_trade_price = DecimalField(max_digits=10, decimal_places=4, null=True)
    last_trade_time = DateTimeField(null=True)
    diffbidtradetime = DateTimeField(null=True)
    volume = IntegerField(null=True)

    class Meta:
        db_table = 'DB_CURRENT_QUOTE'

class DbGetAllExecutions(BaseModel):
    ib_orderid = PrimaryKeyField(db_column='IB_orderid')
    avgprice = DecimalField(max_digits=10, decimal_places=4, null=True)
    commissions = DecimalField(max_digits=10, decimal_places=2, null=True)
    group_number = IntegerField(null=True)
    last_exectime = DateTimeField(null=True)
    numexec = IntegerField(null=True)
    order_number = IntegerField(null=True)
    qty_filled = IntegerField(null=True)
    side = CharField(null=True)
    symbol = CharField(null=True)
    total_value = IntegerField(null=True)

    class Meta:
        db_table = 'DB_GET_ALL_EXECUTIONS'

class DbGroup(BaseModel):
    currency_a = CharField(db_column='Currency_A', null=True)
    currency_b = CharField(db_column='Currency_B', null=True)
    currentordernumber = IntegerField(db_column='CurrentOrderNumber', null=True)
    current_equity = IntegerField(db_column='Current_equity', null=True)
    dont_trade = IntegerField(db_column='DONT_TRADE', null=True)
    exchange_a = CharField(db_column='Exchange_A', null=True)
    exchange_b = CharField(db_column='Exchange_B', null=True)
    is_pair_trading = IntegerField(db_column='IS_PAIR_TRADING', null=True)
    initial_equity = IntegerField(db_column='Initial_equity', null=True)
    lastiborderid = IntegerField(db_column='LastIBOrderID', null=True)
    leverage_a = DecimalField(max_digits=5, decimal_places=2, db_column='Leverage_A', null=True)
    leverage_b = DecimalField(max_digits=5, decimal_places=2, db_column='Leverage_B', null=True)
    longallow_a = IntegerField(db_column='LongAllow_A', null=True)
    longallow_b = IntegerField(db_column='LongAllow_B', null=True)
    market_value_a = IntegerField(db_column='Market_Value_A', null=True)
    market_value_b = IntegerField(db_column='Market_Value_B', null=True)
    neworderaction = CharField(db_column='NewOrderAction', null=True)
    neworderstate = CharField(db_column='NewOrderState', null=True)
    newordertype = CharField(db_column='NewOrderType', null=True)
    pair_position_type = CharField(db_column='PAIR_POSITION_TYPE', null=True)
    partial_fill_a = IntegerField(db_column='Partial_Fill_A', null=True)
    partial_fill_b = IntegerField(db_column='Partial_Fill_B', null=True)
    pendingholdiborderid = IntegerField(db_column='PendingHoldIBOrderID', null=True)
    pendingholdordernumber = IntegerField(db_column='PendingHoldOrderNumber', null=True)
    position_holdingtype_a = CharField(db_column='Position_HoldingType_A', null=True)
    position_holdingtype_b = CharField(db_column='Position_HoldingType_B', null=True)
    sectype_a = CharField(db_column='SecType_A', null=True)
    sectype_b = CharField(db_column='SecType_B', null=True)
    shares_filled_a = IntegerField(db_column='Shares_Filled_A', null=True)
    shares_filled_b = IntegerField(db_column='Shares_Filled_B', null=True)
    shares_remaining_a = IntegerField(db_column='Shares_Remaining_A', null=True)
    shares_remaining_b = IntegerField(db_column='Shares_Remaining_B', null=True)
    shares_requested_a = IntegerField(db_column='Shares_Requested_A', null=True)
    shares_requested_b = IntegerField(db_column='Shares_Requested_B', null=True)
    shortallow_a = IntegerField(db_column='ShortAllow_A', null=True)
    shortallow_b = IntegerField(db_column='ShortAllow_B', null=True)
    symbol_a = CharField(db_column='Symbol_A', null=True)
    symbol_b = CharField(db_column='Symbol_B', null=True)
    total_commission_a = DecimalField(max_digits=10, decimal_places=2, db_column='Total_Commission_A', null=True)
    total_commission_b = DecimalField(max_digits=10, decimal_places=2, db_column='Total_Commission_B', null=True)
    total_marketvalue_buy_a = IntegerField(db_column='Total_MarketValue_BUY_A', null=True)
    total_marketvalue_buy_b = IntegerField(db_column='Total_MarketValue_BUY_B', null=True)
    total_marketvalue_sell_a = IntegerField(db_column='Total_MarketValue_SELL_A', null=True)
    total_marketvalue_sell_b = IntegerField(db_column='Total_MarketValue_SELL_B', null=True)
    total_marketvalue_traded_a = IntegerField(db_column='Total_MarketValue_Traded_A', null=True)
    total_marketvalue_traded_b = IntegerField(db_column='Total_MarketValue_Traded_B', null=True)
    total_shares_buy_a = IntegerField(db_column='Total_Shares_BUY_A', null=True)
    total_shares_buy_b = IntegerField(db_column='Total_Shares_BUY_B', null=True)
    total_shares_sell_a = IntegerField(db_column='Total_Shares_SELL_A', null=True)
    total_shares_sell_b = IntegerField(db_column='Total_Shares_SELL_B', null=True)
    waitingtobefilled = IntegerField(db_column='WaitingTobeFilled', null=True)
    timelastsynced = DateTimeField(default=datetime.datetime.now, db_column='TimeLastSynced')
    group_number = PrimaryKeyField()

    class Meta:
        db_table = 'DB_GROUP'

class DbLocalPortfolio(BaseModel):
    ib_orderid = PrimaryKeyField(db_column='IB_orderid')
    account_number = CharField(null=True)
    avgprice = DecimalField(max_digits=10, decimal_places=4, null=True)
    commission = DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = CharField(null=True)
    exchange = CharField(null=True)
    group_number = IntegerField(null=True)
    holding_type = CharField(null=True)
    limit_price = DecimalField(max_digits=10, decimal_places=4, null=True)
    order_action = CharField(null=True)
    order_completed = IntegerField(null=True)
    order_filled_time = DateTimeField(null=True)
    order_number = IntegerField(null=True)
    order_open_time = DateTimeField(null=True)
    order_partial_filled = IntegerField(null=True)
    order_type = CharField(null=True)
    qty_filled = IntegerField(null=True)
    qty_requested = IntegerField(null=True)
    sectype = CharField(null=True)
    signalprice = DecimalField(max_digits=10, decimal_places=4, db_column='signalPrice', null=True)
    symbol = CharField(null=True)
    totalvalue = DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'DB_LOCAL_PORTFOLIO'

class DbNewOrderTable(BaseModel):
    order_number = PrimaryKeyField()
    auto_generated_randomID = CharField(null=True)
    ib_orderid = IntegerField(db_column='IB_orderid', null=True)
    action = CharField(null=True)
    currency = CharField(null=True)
    currentprice = DecimalField(max_digits=10, decimal_places=4, db_column='currentPrice', null=True)
    exchange = CharField(null=True)
    group_number = IntegerField(null=True)
    limitprice = DecimalField(max_digits=10, decimal_places=4, db_column='limitPrice', null=True)
    ordertype = CharField(db_column='orderType', null=True)
    orderstatus = CharField(null=True)
    pairsymbol = CharField(null=True)
    pending_hold_order_number = IntegerField(null=True)
    sectype = CharField(db_column='secType', null=True)
    sharestotrade = IntegerField(null=True)
    signalprice = DecimalField(max_digits=10, decimal_places=4, db_column='signalPrice', null=True)
    signaltime = DateTimeField(default=datetime.datetime.now, db_column='signalTime', null=True)
    symbol = CharField(null=True)

    class Meta:
        db_table = 'DB_NEW_ORDER_TABLE'

# filled by IB's open orders
class DbOpenOrders(BaseModel):
    ib_orderid = PrimaryKeyField(db_column='IB_orderid')
    local_symbol = CharField(null=True)
    currency = CharField(null=True)
    exchange = CharField(null=True)
    limitprice = DecimalField(max_digits=10, decimal_places=4, null=True)
    order_action = CharField(null=True)
    order_type = CharField(null=True)
    quantity = IntegerField(null=True)
    sectype = CharField(null=True)
    status = CharField(null=True)
    symbol = CharField(null=True)
    account_name = CharField(null=True)
    side = CharField(null=True)
    clientid = IntegerField(null=True)

    class Meta:
        db_table = 'DB_OPEN_ORDERS'

class DbOrdersPlaced(BaseModel):
    ib_orderid = PrimaryKeyField(db_column='IB_orderid')
    account_number = CharField(null=True)
    avgprice = DecimalField(max_digits=10, decimal_places=4, null=True)
    commission = DecimalField(max_digits=10, decimal_places=2, null=True)
    currency = CharField(null=True)
    exchange = CharField(null=True)
    group_number = IntegerField(null=True)
    holding_type = CharField(null=True)
    limit_price = DecimalField(max_digits=10, decimal_places=4, null=True)
    order_action = CharField(null=True)
    order_completed = IntegerField(null=True, default=False)
    order_filled_time = DateTimeField(null=True)
    order_number = IntegerField(null=True, default = 6996)
    order_open_time = DateTimeField(default=datetime.datetime.now, null=True)
    order_partial_filled = IntegerField(null=True, default=False)
    order_type = CharField(null=True)
    qty_filled = IntegerField(null=True, default=0)
    qty_requested = IntegerField(null=True)
    sectype = CharField(null=True)
    signalprice = DecimalField(max_digits=10, decimal_places=4, db_column='signalPrice', null=True)
    symbol = CharField(null=True)
    totalvalue = DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        db_table = 'DB_ORDERS_PLACED'

class DbOutstandingOrders(BaseModel):
    ib_orderid = PrimaryKeyField(db_column='IB_orderid')
    group_number = IntegerField(null=True)
    is_order_canceled = IntegerField(null=True, default = False)
    is_order_open = IntegerField(null=True, default = True)
    order_filled_time = DateTimeField(null=True)
    order_number = IntegerField(null=True)
    order_open_time = DateTimeField(default=datetime.datetime.now, null=True)
    symbol = CharField(null=True)

    class Meta:
        db_table = 'DB_OUTSTANDING_ORDERS'

