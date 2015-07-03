#!/usr/bin/python
# vim: set tabstop=4 shiftwidth=4 expandtab
import datetime
import sys
#from datetime import datetime
from peewee import *
from readconfig import *

database = MySQLDatabase(None)
db_ujala = MySQLDatabase(None)
db_quote = MySQLDatabase(None)


class BaseModel(Model):

    def print_all(self, save_tostring = False):
        class_name = self.__class__.__name__
        all_entries = self.select()
        all_str = ""
        all_str = "\n"+ "Dumping entries for " + class_name + "\n"
        if save_tostring == False:
           print all_str
        for entry in all_entries:
            if save_tostring == False:
               print entry
            all_str += str(entry) + "\n"
        sys.stdout.flush()
        return all_str
    class Meta:
        database = database

class DbAccountInfo(BaseModel):
    account_broker = CharField(db_column='Account_Broker', null=True)
    account_name = CharField(db_column='Account_Name', null=True)
    account_config_id = CharField(db_column='account_config_id', null=True)
    account_number = CharField(db_column='Account_Number', primary_key=True)
    program_name = CharField(default="ibtrader.py", null=False)
    account_value = IntegerField(db_column='Account_Value', null=True)
    minimum_account_value = IntegerField(default = 0, null=True)
    gw_tcp_ip_addr = CharField(db_column='GW_TCP_IP_ADDR', null=True)
    gw_tcp_port_num = IntegerField(db_column='GW_TCP_PORT_NUM', null=True)
    tws_tcp_ip_addr = CharField(db_column='TWS_TCP_IP_ADDR', null=True)
    tws_tcp_port_num = IntegerField(db_column='TWS_TCP_PORT_NUM', null=True)
    timeout_in_seconds = IntegerField(null=False, default=180)
    timelastsynced = DateTimeField(default=datetime.datetime.now, db_column='TimeLastSynced')
    hostname = CharField(null = True)
    nextvalidorderid = IntegerField(null=False, default=100)
    portnumber = IntegerField(default=0, null = True)

    def __str__(self):
        mystr = ""
        newline = ""  # "\n" 
        mystr += newline + " account_number " +  self.account_number
        mystr += newline + " account_broker " +  self.account_broker
        mystr += newline + " account_name " +  self.account_name
        mystr += newline + " account_config_id " +  self.account_config_id
        mystr += newline + " account_value " +  str(self.account_value)
        mystr += newline + " minimum_account_value " +  str(self.minimum_account_value)
        mystr += newline + " gw_tcp_ip_addr " +  self.gw_tcp_ip_addr
        mystr += newline + " gw_tcp_port_num " +  str(self.gw_tcp_port_num)
        mystr += newline + " tws_tcp_ip_addr " +  self.tws_tcp_ip_addr
        mystr += newline + " tws_tcp_port_num " +  str(self.tws_tcp_port_num)
        mystr += newline + " timelastsynced " +  str(self.timelastsynced)
        mystr += newline + " hostname " +  str(self.hostname)
        mystr += newline + " portnumber " +  str(self.portnumber)
        mystr += newline + " nextvalidorderid " +  str(self.nextvalidorderid)
        return mystr



    class Meta:
        db_table = 'DB_ACCOUNT_INFO'

#{"execid": "0001f4e8.5563fa39.01.01", "exchange": "IDEALPRO", "exectime": "20150526  13:47:31", "primaryExchange": "", "clientid": 8899, "qty": 30000, "localsymbol": "EUR.USD", "execshares": 30000, "accountName": "DU226708", "orderid": 38, "execprice": 1.0879, "permid": 1894681312, "secType": "CASH", "avgprice": 1.0879, "commission": 2.0, "symbol": "EUR", "expiry": "", "side": "SLD"}, 
class DbBrokerExecReport(BaseModel):
    ib_orderid = IntegerField(index=True, db_column='IB_orderid', null=True)
    account_number = CharField(null=True)
    avgprice = DoubleField( null=True)
    clientid = IntegerField(null=True)
    exchange = CharField(null=True)
    primary_exchange = CharField(null=True)
    execid = CharField(primary_key=True, null=True)
    execprice = DoubleField( null=True, default = 0)
    commissions = DoubleField(null=True, default = 0)
    execshares = IntegerField(null=True, default = 0)
    exectime = DateTimeField(null=False)
    expiry = CharField(null=True)
    permid = IntegerField(null=True)
    qty_filled = IntegerField(null=True)
    side = CharField(null=True)
    symbol = CharField(null=True)
    localsymbol = CharField(null=True)
    sectype = CharField(null=True)

    def __str__ (self):
        mystr = ""
        newline = ""  # "\n" 
        mystr +=  newline + " execid " +  self.execid
        mystr +=  newline + " ib_orderid " +  str(self.ib_orderid)
        mystr +=  newline + " account_number " +  self.account_number
        mystr +=  newline + " exchange " +  self.exchange
        mystr +=  newline + " primary_exchange " +  self.primary_exchange
        mystr +=  newline + " clientid " +  str(self.clientid)
        mystr +=  newline + " qty_filled " +  str(self.qty_filled)
        mystr +=  newline + " localsymbol " +  self.localsymbol
        mystr +=  newline + " execshares " +  str(self.execshares)
        mystr +=  newline + " execprice " +  str(self.execprice)
        mystr +=  newline + " exectime " +  str(self.exectime)
        mystr +=  newline + " permid " +  str(self.permid)
        mystr +=  newline + " sectype " +  self.sectype
        mystr +=  newline + " avgprice " +  str(self.avgprice)
        mystr +=  newline + " commissions " +  str(self.commissions)
        mystr +=  newline + " symbol " +  self.symbol
        mystr +=  newline + " expiry " +  self.expiry
        mystr +=  newline + " side " +  self.side
        return mystr

    class Meta:
        db_table = 'DB_BROKER_EXEC_REPORT'

class DbBrokerPortfolio(BaseModel):
    accountname = CharField(db_column='accountName', null=True)
    averagecost = DoubleField( db_column='averageCost', null=True)
    local_symbol = CharField(primary_key=True)
    costprice = DoubleField( db_column='costPrice', null=True)
    gnloss = DoubleField( null=True)
    unrealizedpnl = DoubleField(null=True)
    holding_type = CharField(null=True)
    curr_action = CharField(null=True)
    flip_action = CharField(null=True)
    sectype = CharField(null=True)
    marketprice = DoubleField( db_column='marketPrice', null=True)
    marketvalue = DoubleField( db_column='marketValue', null=True)
    quantity = IntegerField(null=True)
    symbol = CharField(index=True, null=True)
    expiry = CharField(null=True)
    currency = CharField(null=True)
    exchange = CharField(null=True)
    primary_exchange = CharField(null=True)

    def __str__ (self):
        mystr = ""
        newline = ""  # "\n" 
        mystr += newline + " accountname " + self.accountname
        mystr += newline + " averagecost " + str(self.averagecost)
        mystr += newline + " local_symbol " + self.local_symbol
        mystr += newline + " costprice " + str(self.costprice)
        mystr += newline + " gnloss " + str(self.gnloss)
        mystr += newline + " holding_type " + self.holding_type
        mystr += newline + " marketprice " + str(self.marketprice)
        mystr += newline + " marketvalue " + str(self.marketvalue)
        mystr += newline + " quantity " + str(self.quantity)
        mystr += newline + " symbol " + self.symbol
        mystr += newline + " curr_action " + self.curr_action
        mystr += newline + " flip_action " + self.flip_action
        mystr += newline + " sectype " + self.sectype
        mystr += newline + " expiry " + self.expiry
        mystr += newline + " currency " + self.currency
        mystr += newline + " exchange " + self.exchange
        mystr += newline + " primary_exchange " + self.primary_exchange
        mystr += newline + " unrealizedpnl " + str(self.unrealizedpnl)
        return mystr

    class Meta:
        db_table = 'DB_BROKER_PORTFOLIO'

class DbAllQuote(BaseModel):
    symbol = CharField(null=False, index=True)
    high_price = DoubleField( null=True, default = 0)
    low_price = DoubleField( null=True, default = 0)
    open_price = DoubleField( null=True, default = 0)

    last_bid_price = DoubleField( null=True)
    last_bid_time = DateTimeField(null=True)
    last_ask_price = DoubleField( null=True)
    last_ask_time = DateTimeField(null=True)
    last_trade_price = DoubleField( null=True)
    last_trade_time = DateTimeField(null=True)
    diffbidtradetime = IntegerField(null=True)
    volume = IntegerField(null=True)
    
    def __str__ (self):
        mystr = ""
        newline = ""  # "\n" 
        mystr += newline + " symbol " +  self.symbol
        mystr += newline + " high_price " +  str(self.high_price)
        mystr += newline + " low_price " +  str(self.low_price)
        mystr += newline + " open_price " +  str(self.open_price)
        mystr += newline + " last_bid_price " +  str(self.last_bid_price)
        mystr += newline + " last_bid_time " +  str(self.last_bid_time)
        mystr += newline + " last_ask_price " +  str(self.last_ask_price)
        mystr += newline + " last_ask_time " +  str(self.last_ask_time)
        mystr += newline + " last_trade_price " +  str(self.last_trade_price)
        mystr += newline + " last_trade_time " +  str(self.last_trade_time)
        mystr += newline + " volume " +  str(self.volume)
        #self.diffbidtradetime = datetime.datetime.strptime(self.last_bid_time, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(self.last_trade_time, "%Y-%m-%d %H:%M:%S")
        mystr += newline + " diffbidtradetime " +  str(self.diffbidtradetime) #+  str(self.diffbidtradetime.total_seconds())
        return mystr

    class Meta:
        db_table = 'DB_ALL_QUOTE'
        database = db_quote

class DbCurrentQuote(DbAllQuote):
    symbol = CharField(primary_key=True)


    class Meta:
        db_table = 'DB_CURRENT_QUOTE'
        database = db_quote

class DbCommandsFromATS(BaseModel):
      uniqid = CharField(null=True)
      command = CharField(null=True)
      account_config_id = CharField(null=True, index=True)
      account_number = CharField(null=True, index=True)
      data = TextField(null=True)
      more_data = TextField(null=True)
      output_data = TextField(null=True)
      output_more_data = TextField(null=True)
      command_created = IntegerField(index=True, default = True, null = False)
      command_processed = IntegerField(index=True, default = False, null = True)
      command_created_time = DateTimeField(default=datetime.datetime.now)
      command_processed_time = DateTimeField(null=True)

      def __str__ (self):
          mystr = ""
          newline = ""  # "\n" 
          mystr += newline + " account_number = " + self.account_number
          mystr += newline + " account_config_id = " + self.account_config_id
          mystr += newline + " command = " + self.command
          mystr += newline + " data = " + str(self.data)
          mystr += newline + " more_data = " + str(self.more_data)
          mystr += newline + " output_data = " + str(self.output_data)
          mystr += newline + " output_more_data = " + str(self.output_more_data)
          mystr += newline + " command_created = " + str(self.command_created)
          mystr += newline + " command_processed = " + str(self.command_processed)
          mystr += newline + " command_created_time = " + str(self.command_created_time)
          mystr += newline + " command_processed_time = " + str(self.command_processed)
          mystr += newline + " uniqid = " + str(self.uniqid)
          return mystr

      class Meta:
        db_table = 'DB_COMMAND_ATS'
        database = db_ujala

class DbGetAllExecutions(BaseModel):
    ib_orderid = IntegerField(index = True, db_column='IB_orderid')
    avgprice = DoubleField( null=True, default = 0)
    signalprice = DoubleField( null=True, default = 0)
    commissions = DoubleField( null=True, default = 0)
    group_number = IntegerField(null=True, default = 0)
    last_exectime = DateTimeField(null=True)
    numexec = IntegerField(null=True, default = 0)
    order_number = IntegerField(null=True, default = 0)
    qty_filled = IntegerField(null=True, default = 0)
    side = CharField(null=True)
    symbol = CharField(index=True, null=True)
    localsymbol = CharField(index=True, null=True)
    total_value = IntegerField(null=True, default = 0)

    def __str__ (self):
        mystr = ""
        newline = ""  # "\n" 
        mystr += newline + " ib_orderid " +  str(self.ib_orderid)
        mystr += newline + " avgprice " +  str(self.avgprice)
        mystr += newline + " commissions " +  str(self.commissions)
        mystr += newline + " group_number " +  str(self.group_number)
        mystr += newline + " last_exectime " +  str(self.last_exectime)
        mystr += newline + " numexec " +  str(self.numexec)
        mystr += newline + " order_number " +  str(self.order_number)
        mystr += newline + " qty_filled " +  str(self.qty_filled)
        mystr += newline + " side " +  self.side
        mystr += newline + " symbol " +  self.symbol
        mystr += newline + " localsymbol " +  self.localsymbol
        mystr += newline + " total_value " +  str(self.total_value)
        return mystr

    class Meta:
        db_table = 'DB_GET_ALL_EXECUTIONS'


class DbGroup(BaseModel):
    net_equity = IntegerField(null=True, default = 0)
    net_equity_a = IntegerField(null=True, default = 0)
    net_equity_b = IntegerField(null=True, default = 0)
    round_digits_a = IntegerField(db_column='Round_Digits_A', null=True, default = 1)
    round_digits_b = IntegerField(db_column='Round_Digits_B', null=True, default = 1)
    currency_a = CharField(db_column='Currency_A', null=True, default = "USD")
    currency_b = CharField(db_column='Currency_B', null=True, default = "USD")
    currentordernumber = IntegerField(index=True, db_column='CurrentOrderNumber', null=True, default = 0)
    currentorderstate = CharField(default = "None", null=True)
    current_equity = IntegerField(db_column='Current_equity', null=True, default = 0)
    dont_trade = IntegerField(db_column='DONT_TRADE', null=True, default = 0)
    exchange_a = CharField(db_column='Exchange_A', null=True)
    exchange_b = CharField(db_column='Exchange_B', null=True)
    is_pair_trading = IntegerField(index=True, db_column='IS_PAIR_TRADING', null=True)
    initial_equity = IntegerField(db_column='Initial_equity', null=True, default = 0)
    lastiborderid = IntegerField(index=True, db_column='LastIBOrderID', null=True, default = 0)
    leverage_a = DoubleField( db_column='Leverage_A', null=True, default = 1)
    leverage_b = DoubleField( db_column='Leverage_B', null=True, default = 1)
    longallow_a = IntegerField(db_column='LongAllow_A', null=True, default = 1)
    longallow_b = IntegerField(db_column='LongAllow_B', null=True, default = 1)
    market_value_a = IntegerField(db_column='Market_Value_A', null=True, default = 0)
    market_value_b = IntegerField(db_column='Market_Value_B', null=True, default = 0)
    neworderaction = CharField(db_column='NewOrderAction', null=True)
    neworderstate = CharField(db_column='NewOrderState', null=True)
    newordertype = CharField(db_column='NewOrderType', null=True)
    pair_position_type = CharField(index=True, db_column='PAIR_POSITION_TYPE', null=True, default = "CASH")
    partial_fill_a = IntegerField(db_column='Partial_Fill_A', null=True, default = 0)
    partial_fill_b = IntegerField(db_column='Partial_Fill_B', null=True, default = 0)
    pending_hold_ib_orderid = IntegerField(index=True, db_column='PendingHoldIBOrderID', null=True, default = 0)
    pending_hold_order_number = IntegerField(index=True, db_column='PendingHoldOrderNumber', null=True, default = 0)
    position_holdingtype_a = CharField(db_column='Position_HoldingType_A', null=True)
    position_holdingtype_b = CharField(db_column='Position_HoldingType_B', null=True)
    sectype_a = CharField(db_column='SecType_A', null=True)
    sectype_b = CharField(db_column='SecType_B', null=True)
    shares_filled_a = IntegerField(db_column='Shares_Filled_A', null=True, default = 0)
    shares_filled_b = IntegerField(db_column='Shares_Filled_B', null=True, default = 0)
    shares_remaining_a = IntegerField(db_column='Shares_Remaining_A', null=True, default = 0)
    shares_remaining_b = IntegerField(db_column='Shares_Remaining_B', null=True, default = 0)
    shares_requested_a = IntegerField(db_column='Shares_Requested_A', null=True, default = 0)
    shares_requested_b = IntegerField(db_column='Shares_Requested_B', null=True, default = 0)
    shortallow_a = IntegerField(db_column='ShortAllow_A', null=True, default = 0)
    shortallow_b = IntegerField(db_column='ShortAllow_B', null=True, default = 0)
    symbol_a = CharField(db_column='Symbol_A', index=True, null=True)
    symbol_b = CharField(db_column='Symbol_B', index=True, null=True)
    group_handle_broker = IntegerField(index=True, default = 0)
    broker_object_symbol_a = IntegerField(index=True, default = 0)
    broker_object_symbol_b = IntegerField(index=True, default = 0)
    local_symbol_a = CharField(db_column='Local_Symbol_A', index=True, null=True)
    local_symbol_b = CharField(db_column='Local_Symbol_B', index=True, null=True)
    total_commission_a = DoubleField( db_column='Total_Commission_A', null=True, default = 0)
    total_commission_b = DoubleField( db_column='Total_Commission_B', null=True, default = 0)
    signalprice_a = DoubleField( db_column='signal_price_a', null=True, default = 0)
    signalprice_b = DoubleField( db_column='signal_price_b', null=True, default = 0)
    avgprice_a = DoubleField( db_column='avgprice_a', null=True, default = 0)
    avgprice_b = DoubleField( db_column='avgprice_b', null=True, default = 0)
    total_trades_a = DoubleField(  null=True, default = 0)
    total_trades_b = DoubleField(  null=True, default = 0)
    total_slippage_a = DoubleField( db_column='Total_Slippage_A', null=True, default = 0)
    total_slippage_b = DoubleField( db_column='Total_Slippage_B', null=True, default = 0)
    total_slippage_positive_a = DoubleField(  null=True, default = 0)
    total_slippage_positive_b = DoubleField(  null=True, default = 0)
    total_slippage_negative_a = DoubleField(  null=True, default = 0)
    total_slippage_negative_b = DoubleField(  null=True, default = 0)
    current_slippage_a = DoubleField( db_column='current_Slippage_A', null=True, default = 0)
    current_slippage_b = DoubleField( db_column='current_Slippage_B', null=True, default = 0)
    total_marketvalue_buy_a = IntegerField(db_column='Total_MarketValue_BUY_A', null=True, default = 0)
    total_marketvalue_buy_b = IntegerField(db_column='Total_MarketValue_BUY_B', null=True, default = 0)
    total_marketvalue_sell_a = IntegerField(db_column='Total_MarketValue_SELL_A', null=True, default = 0)
    total_marketvalue_sell_b = IntegerField(db_column='Total_MarketValue_SELL_B', null=True, default = 0)
    total_marketvalue_traded_a = IntegerField(db_column='Total_MarketValue_Traded_A', null=True, default = 0)
    total_marketvalue_traded_b = IntegerField(db_column='Total_MarketValue_Traded_B', null=True, default = 0)
    total_shares_buy_a = IntegerField(db_column='Total_Shares_BUY_A', null=True, default = 0)
    total_shares_buy_b = IntegerField(db_column='Total_Shares_BUY_B', null=True, default = 0)
    total_shares_sell_a = IntegerField(db_column='Total_Shares_SELL_A', null=True, default = 0)
    total_shares_sell_b = IntegerField(db_column='Total_Shares_SELL_B', null=True, default = 0)
    total_shares_traded_a = IntegerField(db_column='Total_Shares_Traded_A', null=True, default = 0)
    total_shares_traded_b = IntegerField(db_column='Total_Shares_Traded_B', null=True, default = 0)
    waitingtobefilled = IntegerField(db_column='WaitingTobeFilled', null=True, default = 0)
    timelastsynced = DateTimeField(default=datetime.datetime.now, db_column='TimeLastSynced')
    db_order_open_time = DateTimeField(null=True)
    db_order_filled_time = DateTimeField(null=True)
    db_order_update_time = DateTimeField(null=True)
    db_diff_order_open_to_fill_time = IntegerField(default = 0)
    db_diff_order_open_to_update_time = IntegerField(default = 0)
    group_number = PrimaryKeyField()


    def __str__ (self, nl = True):
       mystr = ""
       if nl:
          newline = "\n"  # "\n" 
       else:
          newline = ""  # "\n" 
       mystr += newline + " group_number " +   str(self.group_number)
       mystr += newline + " initial_equity " +   str(self.initial_equity)
       mystr += newline + " current_equity " +   str(self.current_equity)
       mystr += newline + " net_equity " +   str(self.net_equity)
       mystr += newline + " net_equity_a " +   str(self.net_equity_a)
       mystr += newline + " net_equity_b " +   str(self.net_equity_b)
       mystr += newline + " timelastsynced " +   str(self.timelastsynced)
       mystr += newline + " db_order_open_time " +   str(self.db_order_open_time)
       mystr += newline + " db_order_filled_time " +   str(self.db_order_filled_time)
       mystr += newline + " db_order_update_time " +   str(self.db_order_update_time)
       mystr += newline + " db_diff_order_open_to_fill_time " +   str(self.db_diff_order_open_to_fill_time)
       mystr += newline + " db_diff_order_open_to_update_time " +   str(self.db_diff_order_open_to_update_time)
       mystr += newline + " is_pair_trading " +   str(self.is_pair_trading)
       mystr += newline + " symbol_a " +   self.symbol_a
       mystr += newline + " local_symbol_a " +   self.local_symbol_a
       mystr += newline + " leverage_a " +   str(self.leverage_a)
       mystr += newline + " longallow_a " +   str(self.longallow_a)
       mystr += newline + " shortallow_a " +   str(self.shortallow_a)
       mystr += newline + " currency_a " +   self.currency_a
       mystr += newline + " exchange_a " +   self.exchange_a
       mystr += newline + " sectype_a " +   str(self.sectype_a)
       mystr += newline + " round_digits_a " +   str(self.round_digits_a)
       mystr += newline + " symbol_b " +   str(self.symbol_b)
       mystr += newline + " local_symbol_b " +   str(self.local_symbol_b)
       mystr += newline + " leverage_b " +   str(self.leverage_b)
       mystr += newline + " longallow_b " +   str(self.longallow_b)
       mystr += newline + " shortallow_b " +   str(self.shortallow_b)
       mystr += newline + " currency_b " +   str(self.currency_b)
       mystr += newline + " exchange_b " +   str(self.exchange_b)
       mystr += newline + " sectype_b " +   str(self.sectype_b)
       mystr += newline + " round_digits_b " +   str(self.round_digits_b)
       mystr += newline + " currentordernumber " +   str(self.currentordernumber)
       mystr += newline + " currentorderstate " +   str(self.currentorderstate)
       mystr += newline + " dont_trade " +   str(self.dont_trade)
       mystr += newline + " lastiborderid " +   str(self.lastiborderid)
       mystr += newline + " market_value_a " +   str(self.market_value_a)
       mystr += newline + " market_value_b " +   str(self.market_value_b)
       mystr += newline + " neworderaction " +   str(self.neworderaction)
       mystr += newline + " neworderstate " +   str(self.neworderstate)
       mystr += newline + " newordertype " +   str(self.newordertype)
       mystr += newline + " pair_position_type " +   str(self.pair_position_type)
       mystr += newline + " partial_fill_a " +   str(self.partial_fill_a)
       mystr += newline + " partial_fill_b " +   str(self.partial_fill_b)
       mystr += newline + " pending_hold_ib_orderid " +   str(self.pending_hold_ib_orderid)
       mystr += newline + " pending_hold_order_number " +   str(self.pending_hold_order_number)
       mystr += newline + " position_holdingtype_a " +   str(self.position_holdingtype_a)
       mystr += newline + " position_holdingtype_b " +   str(self.position_holdingtype_b)
       mystr += newline + " shares_filled_a " +   str(self.shares_filled_a)
       mystr += newline + " shares_filled_b " +   str(self.shares_filled_b)
       mystr += newline + " shares_remaining_a " +   str(self.shares_remaining_a)
       mystr += newline + " shares_remaining_b " +   str(self.shares_remaining_b)
       mystr += newline + " shares_requested_a " +   str(self.shares_requested_a)
       mystr += newline + " shares_requested_b " +   str(self.shares_requested_b)
       mystr += newline + " total_commission_a " +   str(self.total_commission_a)
       mystr += newline + " total_trades_a " +   str(self.total_trades_a)
       mystr += newline + " total_trades_b " +   str(self.total_trades_b)
       mystr += newline + " total_commission_b " +   str(self.total_commission_b)
       mystr += newline + " total_slippage_a " +   str(self.total_slippage_a)
       mystr += newline + " total_slippage_b " +   str(self.total_slippage_b)
       mystr += newline + " total_slippage_positive_a " +   str(self.total_slippage_positive_a)
       mystr += newline + " total_slippage_positive_b " +   str(self.total_slippage_positive_b)
       mystr += newline + " total_slippage_negative_a " +   str(self.total_slippage_negative_a)
       mystr += newline + " total_slippage_negative_b " +   str(self.total_slippage_negative_b)
       mystr += newline + " current_slippage_a " +   str(self.current_slippage_a)
       mystr += newline + " current_slippage_b " +   str(self.current_slippage_b)
       mystr += newline + " total_marketvalue_buy_a " +   str(self.total_marketvalue_buy_a)
       mystr += newline + " total_marketvalue_buy_b " +   str(self.total_marketvalue_buy_b)
       mystr += newline + " total_marketvalue_sell_a " +   str(self.total_marketvalue_sell_a)
       mystr += newline + " total_marketvalue_sell_b " +   str(self.total_marketvalue_sell_b)
       mystr += newline + " total_marketvalue_traded_a " +   str(self.total_marketvalue_traded_a)
       mystr += newline + " total_marketvalue_traded_b " +   str(self.total_marketvalue_traded_b)
       mystr += newline + " total_shares_traded_a " +   str(self.total_shares_traded_a)
       mystr += newline + " total_shares_traded_b " +   str(self.total_shares_traded_b)
       mystr += newline + " total_shares_buy_a " +   str(self.total_shares_buy_a)
       mystr += newline + " total_shares_buy_b " +   str(self.total_shares_buy_b)
       mystr += newline + " total_shares_sell_a " +   str(self.total_shares_sell_a)
       mystr += newline + " total_shares_sell_b " +   str(self.total_shares_sell_b)
       mystr += newline + " avgprice_a " +   str(self.avgprice_a)
       mystr += newline + " avgprice_b " +   str(self.avgprice_b)
       mystr += newline + " signalprice_a " +   str(self.signalprice_a)
       mystr += newline + " signalprice_b " +   str(self.signalprice_b)
       mystr += newline + " broker_object_symbol_a " +   str(self.broker_object_symbol_a)
       mystr += newline + " broker_object_symbol_b " +   str(self.broker_object_symbol_b)
       mystr += newline + " group_handle_broker " +   str(self.group_handle_broker)
       mystr += newline + " waitingtobefilled " +   str(self.waitingtobefilled)
       return mystr

    class Meta:
        db_table = 'DB_GROUP'

class DbLocalPortfolio(BaseModel):
    ib_orderid = IntegerField(index = True, db_column='IB_orderid')
    account_number = CharField(null=True)
    avgprice = DoubleField( null=True)
    commission = DoubleField( null=True)
    currency = CharField(null=True)
    exchange = CharField(null=True)
    group_number = IntegerField(index=True, null=True)
    holding_type = CharField(null=True)
    limit_price = DoubleField( null=True)
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
    signalprice = DoubleField( db_column='signalPrice', null=True)
    symbol = CharField(index=True, null=True)
    totalvalue = DoubleField( null=True)

    class Meta:
        db_table = 'DB_LOCAL_PORTFOLIO'

class DbNewOrderTable(BaseModel):

    symbol = CharField(index=True, null=True)
    order_number = PrimaryKeyField()
    group_number = IntegerField(default = 0, null=True)
    auto_generated_randomID = CharField(index=True, null=True)
    ib_orderid = IntegerField(index=True, db_column='IB_orderid', null=True)
    action = CharField(null=True)
    currency = CharField(null=True)
    currentprice = DoubleField( default = 0, db_column='currentprice', null=True)
    exchange = CharField(null=True)
    limitprice = DoubleField( default = 0, db_column='limitprice', null=True)
    signalprice = DoubleField(default = 0,  db_column='signalprice', null=True)
    avgprice = DoubleField(default = 0,  db_column='avgprice', null=True)
    ordertype = CharField(db_column='orderType', null=True)
    orderstatus = CharField(index=True, null=True)
    pairsymbol = CharField(null=True)
    pending_hold_order_number = IntegerField(null=True)
    sectype = CharField(db_column='secType', null=True)
    quantity = IntegerField(null=True)
    incoming_order_number = IntegerField(null=True)
    signaltime = DateTimeField(default=datetime.datetime.now, db_column='signalTime', null=True)
    pair_position_type = CharField(index=True, db_column='PAIR_POSITION_TYPE', null=True, default = "CASH")

    def __str__(self):
        mystr = ""
        newline = ""  # "\n" 
        mystr += newline + " symbol " +  self.symbol
        mystr += newline + " order_number " +  str(self.order_number)
        mystr += newline + " group_number " +  str(self.group_number)
        mystr += newline + " incoming_order_number " +  str(self.incoming_order_number)
        mystr += newline + " signaltime " +  str(self.signaltime)
        mystr += newline + " action " +  str(self.action)
        mystr += newline + " orderType " +  self.ordertype
        mystr += newline + " signalprice " +  str(self.signalprice)
        mystr += newline + " avgprice " +  str(self.avgprice)
        mystr += newline + " currentprice " +  str(self.currentprice)
        mystr += newline + " limitprice " +  str(self.limitprice)
        mystr += newline + " ib_orderid " +  str(self.ib_orderid)
        mystr += newline + " quantity " +  str(self.quantity)
        mystr += newline + " orderstatus " +  str(self.orderstatus)
        mystr += newline + " exchange " +  str(self.exchange)
        mystr += newline + " currency " +  str(self.currency)
        mystr += newline + " sectype " +  str(self.sectype)
        mystr += newline + " pending_hold_order_number " +  str(self.pending_hold_order_number)
        mystr += newline + " auto_generated_randomID " +  self.auto_generated_randomID
        mystr += newline + " pairsymbol " +  str(self.pairsymbol)
        return mystr

    class Meta:
        db_table = 'DB_NEW_ORDER_TABLE'

class saved_DbNewOrderTable(DbNewOrderTable):

    def copy_from_DbNewOrderTable(self, obj_DbNewOrderTable):
        old_obj = saved_DbNewOrderTable.select().where(saved_DbNewOrderTable.order_number == obj_DbNewOrderTable.order_number)
        try:
            if old_obj is not None:
                old_obj.delete_instance()
        except:
            pass
        self.pair_position_type = obj_DbNewOrderTable.pair_position_type
        self.order_number = obj_DbNewOrderTable.order_number
        self.auto_generated_randomID = obj_DbNewOrderTable.auto_generated_randomID
        self.ib_orderid = obj_DbNewOrderTable.ib_orderid
        self.action = obj_DbNewOrderTable.action
        self.currency = obj_DbNewOrderTable.currency
        self.currentprice = obj_DbNewOrderTable.currentprice
        self.exchange = obj_DbNewOrderTable.exchange
        self.group_number = obj_DbNewOrderTable.group_number
        self.limitprice = obj_DbNewOrderTable.limitprice
        self.signalprice = obj_DbNewOrderTable.signalprice
        self.avgprice = obj_DbNewOrderTable.avgprice
        self.ordertype = obj_DbNewOrderTable.ordertype
        self.orderstatus = obj_DbNewOrderTable.orderstatus
        self.pairsymbol = obj_DbNewOrderTable.pairsymbol
        self.pending_hold_order_number = obj_DbNewOrderTable.pending_hold_order_number
        self.sectype = obj_DbNewOrderTable.sectype
        self.quantity = obj_DbNewOrderTable.quantity
        self.incoming_order_number = obj_DbNewOrderTable.incoming_order_number
        self.signaltime = obj_DbNewOrderTable.signaltime
        self.symbol = obj_DbNewOrderTable.symbol
        try:
            self.save(force_insert = True)
        except:
            pass

    class Meta:
        db_table = 'SAVED_DB_NEW_ORDER_TABLE'

# filled by IB's open orders
class DbOpenOrders(BaseModel):
    ib_orderid = IntegerField(index = True, db_column='IB_orderid')
    local_symbol = CharField(index=True, null=True)
    currency = CharField(null=True)
    exchange = CharField(null=True)
    limitprice = DoubleField( null=True)
    order_action = CharField(null=True)
    order_type = CharField(null=True)
    quantity = IntegerField(null=True)
    sectype = CharField(null=True)
    status = CharField(null=True)
    symbol = CharField(index=True, null=True)
    account_name = CharField(null=True)
    side = CharField(null=True)
    clientid = IntegerField(null=True)

    def __str__ (self):
        mystr = ""
        newline = ""  # "\n" 
        mystr += newline + " ib_orderid " + str(self.ib_orderid)
        mystr += newline + " local_symbol " + self.local_symbol
        mystr += newline + " currency " + self.currency
        mystr += newline + " exchange " + self.exchange
        mystr += newline + " limitprice " + str(self.limitprice)
        mystr += newline + " order_action " + self.order_action
        mystr += newline + " order_type " + self.order_type
        mystr += newline + " quantity " + str(self.quantity)
        mystr += newline + " sectype " + self.sectype
        mystr += newline + " status " + self.status
        mystr += newline + " symbol " + self.symbol
        mystr += newline + " clientid " + str(self.clientid)
        mystr += newline + " account_name " + self.account_name
        mystr += newline + " side " + self.side
        return mystr

    class Meta:
        db_table = 'DB_OPEN_ORDERS'

class DbOrdersPlaced(BaseModel):
    ib_orderid = IntegerField(index = True, db_column='IB_orderid')
    order_validated = IntegerField(default = False, null = True)
    account_number = CharField(null=True)
    avgprice = DoubleField(default = 0, null=True)
    commission = DoubleField( null=True)
    currency = CharField(null=True)
    exchange = CharField(null=True)
    group_number = IntegerField(null=True)
    holding_type = CharField(null=True)
    limit_price = DoubleField( null=True)
    order_action = CharField(null=True)
    order_completed = IntegerField(null=True, default=False)
    order_filled_time = DateTimeField(null=True)
    order_number = IntegerField(null=True, default = 6996)
    order_open_time = DateTimeField(default=datetime.datetime.now, null=True)
    order_partial_filled = IntegerField(null=True, default=False)
    order_type = CharField(null=True)
    qty_filled = IntegerField(null=True, default=0)
    qty_requested = IntegerField(default = 0, null=True)
    sectype = CharField(null=True)
    signalprice = DoubleField( default = 0,db_column='signalPrice', null=True)
    slippage = DoubleField( default = 0, null=True)
    symbol = CharField(index=True, null=True)
    localsymbol = CharField(index=True, null=True)
    totalvalue = DoubleField( null=True)

    def __str__(self):
       mystr = ""
       newline = ""  # "\n" 
       mystr += newline + " ib_orderid " +  str(self.ib_orderid)
       mystr += newline + " order_number " + str(self.order_number)
       mystr += newline + " symbol " + self.symbol
       mystr += newline + " localsymbol " + str(self.localsymbol)
       mystr += newline + " group_number " +  str(self.group_number)
       mystr += newline + " order_validated " +  str(self.order_validated)
       mystr += newline + " account_number " +  self.account_number
       mystr += newline + " avgprice " +  str(self.avgprice)
       mystr += newline + " commission " +  str(self.commission)
       mystr += newline + " currency " +  self.currency
       mystr += newline + " exchange " +  self.exchange
       mystr += newline + " holding_type " +  str(self.holding_type)
       mystr += newline + " limit_price " +  str(self.limit_price)
       mystr += newline + " order_action " + self.order_action
       mystr += newline + " order_completed " + str(self.order_completed)
       mystr += newline + " order_filled_time " + str(self.order_filled_time)
       mystr += newline + " order_open_time " + str(self.order_open_time)
       mystr += newline + " order_partial_filled " + str(self.order_partial_filled)
       mystr += newline + " order_type " + self.order_type
       mystr += newline + " qty_filled " + str(self.qty_filled)
       mystr += newline + " qty_requested " + str(self.qty_requested)
       mystr += newline + " sectype " + self.sectype
       mystr += newline + " signalprice " + str(self.signalprice)
       mystr += newline + " slippage " + str(self.slippage)
       mystr += newline + " totalvalue " + str(self.totalvalue)
       return mystr

    class Meta:
        db_table = 'DB_ORDERS_PLACED'

class DbOutstandingOrders(BaseModel):
    ib_orderid = IntegerField(index = True, db_column='IB_orderid')
    group_number = IntegerField(null=True)
    is_order_canceled = IntegerField(index=True, null=True, default = False)
    is_order_open = IntegerField(index=True, null=True, default = True)
    order_filled_time = DateTimeField(null=True)
    order_number = IntegerField(null=True)
    order_open_time = DateTimeField(default=datetime.datetime.now, null=True)
    symbol = CharField(index=True, null=True)

    def __str__(self):
        mystr = ""
        newline = ""  # "\n" 
        mystr += newline + " ib_orderid " + str(self.ib_orderid)
        mystr += newline + " symbol " + self.symbol
        mystr += newline + " group_number " + str(self.group_number)
        mystr += newline + " order_open_time " + str(self.order_open_time)
        mystr += newline + " is_order_canceled " + str(self.is_order_canceled)
        mystr += newline + " is_order_open " + str(self.is_order_open)
        mystr += newline + " order_filled_time " + str(self.order_filled_time)
        mystr += newline + " order_number " + str(self.order_number)
        return mystr
        
    class Meta:
        db_table = 'DB_OUTSTANDING_ORDERS'

class DbNextValidOrderID(BaseModel):
      account_number = CharField(null=True, primary_key = True)
      nextvalidorderid = IntegerField(default=100, null=True)

      def __str__ (self):
          mystr = ""
          newline = ""  # "\n" 
          mystr += " account_number " + str(self.account_number)
          mystr += " nextvalidorderid " + str(self.nextvalidorderid)

      class Meta:
        db_table = 'DB_NEXT_VALID_ORDER_ID'
        database = db_ujala

class DbIncomingOrders(BaseModel):
      account_number = CharField(null=True)
      account_config_id = CharField(null=True)
      symbol = CharField(index=True, null=False)
      order_action = CharField(null=False)
      order_type = CharField(null=False)
      trade_instrument_type = CharField(default = "None", null=True)
      sectype = CharField(null=False)
      exchange = CharField(null=False)
      currency = CharField(null=False)
      limit_price = DoubleField(default=0, null=True)
      signal_price = DoubleField(default=0, null=True)
      quantity = IntegerField(default=0, null=True)
      order_open_time = DateTimeField(default=datetime.datetime.now, null=True)
      order_start_time = DateTimeField(null=True)
      order_end_time = DateTimeField(null=True)
      order_number = PrimaryKeyField()
      # order_created is set to True when the entry is created by the signal method
      order_created = IntegerField(index=True, default = True, null = False)
      # order_processed is False and when the SM1/2/3 copies the order from this table into
      # the new order table entry, then its set to True
      # the SM1/2/3 will loop DbIncomingOrders for all the entries where order_processed is False
      order_processed = IntegerField(index=True, default = False, null = True)

      def __str__ (self):
          mystr = ""
          newline = ""  # "\n" 
          mystr += newline + " account_number " + self.account_number
          mystr += newline + " order_number " + str(self.order_number)
          mystr += newline + " symbol " + self.symbol
          mystr += newline + " order_action " + self.order_action
          mystr += newline + " order_type " + self.order_type
          mystr += newline + " trade_instrument_type " + str(self.trade_instrument_type)
          mystr += newline + " sectype " + self.sectype
          mystr += newline + " exchange " + self.exchange
          mystr += newline + " currency " + self.currency
          mystr += newline + " limit_price " + str(self.limit_price)
          mystr += newline + " signal_price " + str(self.signal_price)
          mystr += newline + " quantity " + str(self.quantity)
          mystr += newline + " order_open_time " + str(self.order_open_time)
          mystr += newline + " order_start_time " + str(self.order_start_time)
          mystr += newline + " order_end_time " + str(self.order_end_time)
          mystr += newline + " order_created " + str(self.order_created)
          mystr += newline + " order_processed " + str(self.order_processed)
          return mystr

      class Meta:
        db_table = 'DB_INCOMING_ORDERS'
        database = db_ujala

class saved_DbIncomingOrders(DbIncomingOrders):
    def copy_from_DbIncomingOrders(self, obj_DbIncomingOrders):

        self.account_number = obj_DbIncomingOrders.account_number
        self.account_config_id = obj_DbIncomingOrders.account_config_id
        self.symbol = obj_DbIncomingOrders.symbol
        self.order_action = obj_DbIncomingOrders.order_action
        self.order_type = obj_DbIncomingOrders.order_type
        self.trade_instrument_type = obj_DbIncomingOrders.trade_instrument_type
        self.sectype = obj_DbIncomingOrders.sectype
        self.exchange = obj_DbIncomingOrders.exchange
        self.currency = obj_DbIncomingOrders.currency
        self.limit_price = obj_DbIncomingOrders.limit_price
        self.signal_price = obj_DbIncomingOrders.signal_price
        self.quantity = obj_DbIncomingOrders.quantity
        self.order_open_time = obj_DbIncomingOrders.order_open_time
        self.order_start_time = obj_DbIncomingOrders.order_start_time
        self.order_end_time = obj_DbIncomingOrders.order_end_time
        self.order_number = obj_DbIncomingOrders.order_number
        self.order_created = obj_DbIncomingOrders.order_created
        self.order_processed = obj_DbIncomingOrders.order_processed
        self.save(force_insert = True)

class Database():
	account_database = None
	account_user = None
	account_passwd = None
	database_ujala = Config.get("Common", "database_ujala")
	USERNAME_UJALA = Config.get("Common", "USERNAME_UJALA")
	PASSWD_UJALA = Config.get("Common", "PASSWD_UJALA")
	database_quote = Config.get("Common", "database_quote")
	USERNAME_QUOTE = Config.get("Common", "USERNAME_quote")
	PASSWD_QUOTE = Config.get("Common", "PASSWD_quote")

	def __init__(self, db_name, _user, _passwd, only_ujala = False):

            self.account_database = db_name
            self.account_user = _user
            self.account_passwd = _passwd
            if only_ujala == False:
                    database.init(self.account_database, user= self.account_user, password= self.account_passwd)
                    database.connect()
                    database.set_autocommit(True);

            if self.account_user is None:
                    self.account_user = self.USERNAME_UJALA
            if self.account_passwd is None:
                    self.account_passwd = self.PASSWD_UJALA

            db_ujala.init(self.database_ujala, user = self.account_user, password=self.account_passwd)
            db_ujala.connect()
            db_ujala.set_autocommit(True);
            db_quote.init(self.database_quote, user = self.account_user, password=self.account_passwd)
            db_quote.connect()
            db_quote.set_autocommit(True);
            self.create_all_tables(only_ujala);

	def create_all_tables(self, only_ujala):

            if DbIncomingOrders.table_exists() == False:
               DbIncomingOrders.create_table()

            if DbNextValidOrderID.table_exists() == False:
               DbNextValidOrderID.create_table()

            if DbCurrentQuote.table_exists() == False:
               DbCurrentQuote.create_table()

            if DbAllQuote.table_exists() == False:
               DbAllQuote.create_table()

            if DbCommandsFromATS.table_exists() == False:
               DbCommandsFromATS.create_table()

            if only_ujala:
               return

            if DbAccountInfo.table_exists() == False:
               DbAccountInfo.create_table()

            if DbGroup.table_exists() == False:
               DbGroup.create_table()


            if saved_DbNewOrderTable.table_exists() == False:
               saved_DbNewOrderTable.create_table()

            if DbNewOrderTable.table_exists() == False:
               DbNewOrderTable.create_table()

            if DbOrdersPlaced.table_exists() == False:
               DbOrdersPlaced.create_table()

            if DbOutstandingOrders.table_exists() == False:
               DbOutstandingOrders.create_table()

            if DbBrokerExecReport.table_exists() == False:
               DbBrokerExecReport.create_table()

            if DbBrokerPortfolio.table_exists() == False:
               DbBrokerPortfolio.create_table()

            if DbOpenOrders.table_exists() == False:
               DbOpenOrders.create_table()

            if DbGetAllExecutions.table_exists() == False:
               DbGetAllExecutions.create_table()


	def print_portfolio_groups(self, only_ujala, save_tostring = True):
            all_str = ""
            all_str += DbBrokerPortfolio().print_all(save_tostring)
            all_str += DbGroup().print_all(save_tostring)
            return all_str

	def print_all_tables(self, only_ujala, save_tostring = False):

            all_str = ""
            if save_tostring == False:
               print "*** START print ALL tables ***"
            all_str += DbIncomingOrders().print_all(save_tostring)
            #all_str += DbCurrentQuote().print_all(save_tostring)
            all_str += DbCommandsFromATS().print_all(save_tostring)
            sys.stdout.flush()

            if only_ujala:
               return all_str

            all_str += DbAccountInfo().print_all(save_tostring)
            all_str += DbGroup().print_all(save_tostring)
            all_str += saved_DbNewOrderTable().print_all(save_tostring)
            all_str += DbNewOrderTable().print_all(save_tostring)
            all_str += DbOrdersPlaced().print_all(save_tostring)
            all_str += DbOutstandingOrders().print_all(save_tostring)
            all_str += DbBrokerExecReport().print_all(save_tostring)
            all_str += DbBrokerPortfolio().print_all(save_tostring)
            all_str += DbOpenOrders().print_all(save_tostring)
            all_str += DbGetAllExecutions().print_all(save_tostring)
            if save_tostring == False:
               print "*** END print ALL tables ***"
            #sys.stdout.flush()
            return all_str
