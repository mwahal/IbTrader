#!/usr/bin/python
# pylint: disable=too-many-instance-attributes,fixme,line-too-long,bad-indentation,bad-whitespace,trailing-whitespace,too-many-lines,too-many-arguments,too-many-locals,invalid-name,superfluous-parens,missing-docstring
# vim: set tabstop=4 shiftwidth=4 expandtab
'''IBTrader is based on SWIG generated TWS wrapper to communicate with Interactive Brokers.
https://pypi.python.org/pypi/swigibpy/0.4.1

'''

import sys
import argparse
import time
import datetime
import json
from pprint import pprint
from threading import Event
from Queue import Queue
from random import randint

from swigibpy import (EWrapper, EWrapperVerbose, EPosixClientSocket, Contract, Order, TagValue,
                      TagValueList, ExecutionFilter)
#https://www.interactivebrokers.com/en/software/api/api_Left.htm#CSHID=apiguide%2Fjava%2Ftickprice.htm|StartTopic=apiguide%2Fjava%2Ftickprice.htm|SkinName=ibskin
class IB_Tick_Type():
    BID_SIZE = 0
    BID_PRICE = 1
    ASK_PRICE = 2
    ASK_SIZE = 3
    LAST_PRICE = 4
    LAST_SIZE = 5
    HIGH = 6
    LOW = 7
    VOLUME = 8
    CLOSE_PRICE = 9
    BID_OPTION_COMPUTATION = 10
    ASK_OPTION_COMPUTATION = 11
    LAST_OPTION_COMPUTATION = 12
    MODEL_OPTION_COMPUTATION = 13
    OPEN_TICK = 14
    LOW_13_WEEK = 15
    HIGH_13_WEEK = 16
    LOW_26_WEEK = 17
    HIGH_26_WEEK = 18
    LOW_52_WEEK = 19
    HIGH_52_WEEK = 20
    AVG_VOLUME = 21
    OPEN_INTEREST = 22
    OPTION_HISTORICAL_VOL = 23
    OPTION_IMPLIED_VOL = 24
    OPTION_BID_EXCH = 25
    OPTION_ASK_EXCH = 26
    OPTION_CALL_OPEN_INTEREST = 27
    OPTION_PUT_OPEN_INTEREST = 28
    OPTION_CALL_VOLUME = 29
    OPTION_PUT_VOLUME = 30
    INDEX_FUTURE_PREMIUM = 31
    BID_EXCH = 32
    ASK_EXCH = 33
    AUCTION_VOLUME = 34
    AUCTION_PRICE = 35
    AUCTION_IMBALANCE = 36
    MARK_PRICE = 37
    BID_EFP_COMPUTATION = 38
    ASK_EFP_COMPUTATION = 39
    LAST_EFP_COMPUTATION = 40
    OPEN_EFP_COMPUTATION = 41
    HIGH_EFP_COMPUTATION = 42
    LOW_EFP_COMPUTATION = 43
    CLOSE_EFP_COMPUTATION = 44
    LAST_TIMESTAMP = 45
    SHORTABLE = 46
    FUNDAMENTAL_RATIOS = 47
    RT_VOLUME = 48
    HALTED = 49
    BIDYIELD = 50
    ASKYIELD = 51
    LASTYIELD = 52
    CUST_OPTION_COMPUTATION = 53
    TRADE_COUNT = 54
    TRADE_RATE = 55
    VOLUME_RATE = 56
    SYMBOL = 99
    MAX_TICK_TYPE = 100

    desc = [[] for i in range(MAX_TICK_TYPE)]
    desc[0] = "BID_SIZE"
    desc[1] = "BID_PRICE"
    desc[2] = "ASK_PRICE"
    desc[3] = "ASK_SIZE"
    desc[4] = "LAST_PRICE"
    desc[5] = "LAST_SIZE"
    desc[6] = "HIGH"
    desc[7] = "LOW"
    desc[8] = "VOLUME"
    desc[9] = "CLOSE_PRICE"
    desc[10] = "BID_OPTION_COMPUTATION"
    desc[11] = "ASK_OPTION_COMPUTATION"
    desc[12] = "LAST_OPTION_COMPUTATION"
    desc[13] = "MODEL_OPTION_COMPUTATION"
    desc[14] = "OPEN_TICK"
    desc[15] = "LOW_13_WEEK"
    desc[16] = "HIGH_13_WEEK"
    desc[17] = "LOW_26_WEEK"
    desc[18] = "HIGH_26_WEEK"
    desc[19] = "LOW_52_WEEK"
    desc[20] = "HIGH_52_WEEK"
    desc[21] = "AVG_VOLUME"
    desc[22] = "OPEN_INTEREST"
    desc[23] = "OPTION_HISTORICAL_VOL"
    desc[24] = "OPTION_IMPLIED_VOL"
    desc[25] = "OPTION_BID_EXCH"
    desc[26] = "OPTION_ASK_EXCH"
    desc[27] = "OPTION_CALL_OPEN_INTEREST"
    desc[28] = "OPTION_PUT_OPEN_INTEREST"
    desc[29] = "OPTION_CALL_VOLUME"
    desc[30] = "OPTION_PUT_VOLUME"
    desc[31] = "INDEX_FUTURE_PREMIUM"
    desc[32] = "BID_EXCH"
    desc[33] = "ASK_EXCH"
    desc[34] = "AUCTION_VOLUME"
    desc[35] = "AUCTION_PRICE"
    desc[36] = "AUCTION_IMBALANCE"
    desc[37] = "MARK_PRICE"
    desc[38] = "BID_EFP_COMPUTATION"
    desc[39] = "ASK_EFP_COMPUTATION"
    desc[40] = "LAST_EFP_COMPUTATION"
    desc[41] = "OPEN_EFP_COMPUTATION"
    desc[42] = "HIGH_EFP_COMPUTATION"
    desc[43] = "LOW_EFP_COMPUTATION"
    desc[44] = "CLOSE_EFP_COMPUTATION"
    desc[45] = "LAST_TIMESTAMP"
    desc[46] = "SHORTABLE"
    desc[47] = "FUNDAMENTAL_RATIOS"
    desc[48] = "RT_VOLUME"
    desc[49] = "HALTED"
    desc[50] = "BIDYIELD"
    desc[51] = "ASKYIELD"
    desc[52] = "LASTYIELD"
    desc[53] = "CUST_OPTION_COMPUTATION"
    desc[54] = "TRADE_COUNT"
    desc[55] = "TRADE_RATE"
    desc[56] = "VOLUME_RATE"
    desc[99] = "SYMBOL"

class IBWrapper(EWrapper):
    '''Callback object passed to TWS, these functions will be called directly
    by TWS.

    '''
    handle_ibtrader = None

    def __init__(self, handle_ibtrader):
        super(IBWrapper, self).__init__()
        self.order_filled = Event()
        self.order_ids = Queue()
        self.handle_ibtrader = handle_ibtrader


    def currentTime(self, timevalue):
        if self.handle_ibtrader.debug:
           print "currentTime(timevalue = %d)" % timevalue
        self.handle_ibtrader.ib_server_time = timevalue

    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        """
        Add a row to the portfolio structure
        """

        if self.handle_ibtrader.request_finished == True:
           return

                
        if self.handle_ibtrader.debug:
           print "updatePortfolio  symbol = %s expiry = %s position = %s marketPrice = %s marketValue = %s averageCost = %s unrealizedPNL = %s realizedPNL = %s accountName = %s contract.currency = %s contract.localSymbol = %s contract.conId = %s contract.right = %s contract.strike = %s contract.tradingClass = %s" % (contract.symbol, contract.expiry, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName, contract.currency, contract.localSymbol, contract.conId, contract.right, contract.strike, contract.tradingClass)
        sym = contract.localSymbol.replace(' ', '')
        if position > 0:
            curr_action = "BUY"
            flip_action = "SELL"
        else:
            curr_action = "SELL"
            flip_action = "BUY"

        costPrice = averageCost * position
        gnloss = marketValue - costPrice
        if position > 0:
            hold_type = "LONG"
        else:
            hold_type = "SHORT"
        portdict = dict(localSymbol=contract.localSymbol,symbol=contract.symbol, expiry=contract.expiry, 
                       secType=contract.secType, currency=contract.currency,
                       exchange=contract.exchange,quantity=position,
                       primaryExchange = contract.primaryExchange,
                       marketPrice=marketPrice, marketValue= marketValue, averageCost=averageCost,
                       curr_action=curr_action, flip_action=flip_action,hold_type=hold_type,
                       unrealizedPNL=unrealizedPNL, realizedPNL=realizedPNL, accountName=accountName, costPrice=costPrice, gainloss=gnloss) 

        #portfolio_holdings[sym] = portdict
        self.handle_ibtrader.portfolio_holdings.append(portdict)
        #portfolio_holdings[sym] = (contract.symbol, contract.expiry, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName, contract.currency)
        self.handle_ibtrader.portfolio_structure.append((sym, contract.expiry, position, marketPrice, marketValue, averageCost, 
                                    unrealizedPNL, realizedPNL, accountName, contract.currency, contract.exchange, contract.primaryExchange))

    def error(self, orderid, errorCode, errorString):
        """
        error handling, simple for now
       
        Here are some typical IB errors
        INFO: 2107, 2106
        WARNING 326 - can't connect as already connected
        CRITICAL: 502, 504 can't connect to TWS.
            200 no security definition found
            162 no trades

        """

        ## Any errors not on this list we just treat as information
       
        errorString = errorString.replace('\n', ' ').replace('\r', '')

        self.handle_ibtrader.errors_to_trig = self.handle_ibtrader.is_placing_order and self.handle_ibtrader.ERRORS_TO_TRIGGER_ORDRPLACED or self.handle_ibtrader.ERRORS_TO_TRIGGER
        if self.handle_ibtrader.debug:
           print "errors_to_trig ", self.handle_ibtrader.errors_to_trig
           print "ERROR errorCode = %d errorString = %s" % (errorCode, errorString)
        if errorCode in self.handle_ibtrader.errors_to_trig:
            self.handle_ibtrader.global_errorString = errorString
            self.handle_ibtrader.global_errorCode = errorCode
            self.handle_ibtrader.iserror=True
            self.handle_ibtrader.errormsg="Code=%d IB error id %d errorcode %d string %s" %(errorCode, orderid, errorCode, errorString)
            #if is_placing_order == False:
            #    print errormsg
            self.handle_ibtrader.finished=True  
            self.handle_ibtrader.request_finished=True  
           
        ## Wrapper functions don't have to return anything this is to tidy
        return 0
      
    def updateAccountValue(self, key, value, currency, accountName):
        """
        Populates account value dictionary
        """
        if self.handle_ibtrader.request_finished == True:
           return
        if self.handle_ibtrader.debug:
           print "updateAccountValue portfolio_finished = %d key = %s value = %s currency = %s accountName = %s" % (self.handle_ibtrader.request_finished, key, value, currency, accountName)
        if key == "AccountCode":
            accountName = value
        self.handle_ibtrader.account_value.append((key, value, currency, accountName))
        

    def accountDownloadEnd(self, accountName):
        """
        portfolio_finished can look at portfolio_structure and account_value
        """

        self.handle_ibtrader.request_finished=True
        self.handle_ibtrader.accountName = accountName
        if self.handle_ibtrader.debug:
           print "accountDownloadEnd accountName = %s" , self.handle_ibtrader.accountName

    def updateAccountTime(self, timeStamp):
        pass 


    def openOrderEnd(self):
        
        if self.handle_ibtrader.debug:
            print "openOrderEnd is_request_open_order = %d" % self.handle_ibtrader.is_request_open_order
        if self.handle_ibtrader.is_request_open_order:
            self.handle_ibtrader.request_finished=True
            self.handle_ibtrader.is_request_open_order=False
        if self.handle_ibtrader.debug:
           print "openOrderEnd"

    def execDetails(self, orderid, contract, execution):

        if self.handle_ibtrader.getting_today_executions == 0 and self.handle_ibtrader.order is None:
           #print "execdetails Open is None"
           return

        self.handle_ibtrader.num_executions += 1


        execid=execution.execId
        exectime=execution.time
        thisorderid=execution.orderId
        account_number=execution.acctNumber
        exchange=execution.exchange
        permid=execution.permId
        avgprice=execution.price
        cumQty=execution.cumQty
        clientid=execution.clientId
        symbol=contract.symbol
        expiry=contract.expiry
        side=execution.side
        localsymbol=contract.localSymbol.replace(' ', '')

        #execdetails = dict(side=str(side), exectime=str(exectime), orderid=str(thisorderid), execshares=int(execution.shares), qty=int(cumQty), avgprice=float(execution.avgPrice), execprice=float(execution.price), symbol=str(symbol), expiry=str(expiry), clientid=str(clientid), execid=str(execid), account=str(account_number), exchange=str(exchange), permid=int(permid), commission=0)
        execdetails = dict(side=str(side), exectime=str(exectime), orderid=int(thisorderid), execshares=int(execution.shares), qty=int(cumQty), avgprice=float(execution.avgPrice), execprice=float(execution.price), symbol=str(symbol), expiry=str(expiry), clientid=int(clientid), execid=str(execid), accountName=str(account_number), exchange=str(exchange), permid=int(permid), commission=str(0), localsymbol=localsymbol, secType=contract.secType, primaryExchange=contract.primaryExchange)

        if self.handle_ibtrader.debug:
#           print "execDetails id = %s contract = %s execution = %s" % (id, str(contract), str(execution))
           print "Execution number = %d "% self.handle_ibtrader.num_executions
           print "execDetails orderId = %d " % execution.orderId
           print "execDetails execId = %s " % execution.execId
           print "execDetails clientId = %d " % execution.clientId
           print "execDetails time = %s " % str(execution.time)
           print "execDetails acctNumber = %s " % str(execution.acctNumber)
           print "execDetails executionExchange = %s " % str(execution.exchange)
           print "execDetails side = %s " % str(execution.side)
           print "execDetails shares = %d " % execution.shares
           print "execDetails price = %s " % str(execution.price)
           print "execDetails permId = %d " % execution.permId
           print "execDetails liquidation = %d " % execution.liquidation
           print "execDetails cumQty = %d " % execution.cumQty
           #print "order.totalQuantity = %d " % order.totalQuantity
           print "execDetails avgPrice = %s " % str(execution.avgPrice)
           print "execDetails orderRef = %s " % (execution.orderRef)
           print "execDetails evRule = %s " % (execution.evRule)

        if self.handle_ibtrader.getting_today_executions == 1:
           if self.handle_ibtrader.debug:
              print "getting_today_executions = 1"
           self.handle_ibtrader.execlist.append(execdetails)
        else:
           self.handle_ibtrader.avg_price_per_share =  execution.avgPrice
           self.handle_ibtrader.total_shares_filled =  execution.cumQty
           self.handle_ibtrader.partial_avg_price_per_share = execution.avgPrice
           self.handle_ibtrader.partial_shares_filled = execution.cumQty
           self.handle_ibtrader.myexecdetails[execution.execId] = execution
           if self.handle_ibtrader.order.totalQuantity == execution.cumQty:
              self.handle_ibtrader.all_trades_filled = 1
           if self.handle_ibtrader.all_comm_filled and ((self.handle_ibtrader.order.totalQuantity == execution.cumQty) or self.handle_ibtrader.request_finished):
              if self.handle_ibtrader.debug:
                 print "request_finished is %s " % self.handle_ibtrader.request_finished
              self.handle_ibtrader.partial_avg_price_per_share = 0
              self.handle_ibtrader.partial_shares_filled = 0
              self.handle_ibtrader.all_trades_filled = 1
              self.handle_ibtrader.avg_price_per_share = execution.avgPrice
              self.handle_ibtrader.total_shares_filled = execution.cumQty
              total_commission_paid = 0
              for key in self.handle_ibtrader.myexecdetails.items():
                  if key in self.handle_ibtrader.mycommdetails:
                      total_commission_paid += self.handle_ibtrader.mycommdetails[key]
                  else:
                      print key
              if self.handle_ibtrader.debug:
                 print "AvgPrice = %.4f TotalFilled = %d TotalComm = %.2f" % (execution.avgPrice, execution.cumQty, total_commission_paid)
              if self.handle_ibtrader.all_comm_filled == 1:
                 self.order_filled.set()


    def execDetailsEnd(self, reqId):
        """
        No more orders to look at if execution details requested
        """
        self.handle_ibtrader.request_finished=True
        if self.handle_ibtrader.debug:
           print "execDetailsEnd for reqId = %d" % reqId

    def managedAccounts(self, openOrderEnd):
        '''Not relevant for our example'''
        pass

    ###############

    def nextValidId(self, validOrderId):
        '''Capture the next order id'''
        self.order_ids.put(validOrderId)
        self.handle_ibtrader.next_valid_orderid = validOrderId

    def orderStatus(self, orderid, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFilledPrice, clientId, whyHeld):

        if self.handle_ibtrader.is_request_open_order:
            return

        if self.handle_ibtrader.debug:
           print(("Order #%s - %s (filled %d, remaining %d, avgFillPrice %f,"
               "last fill price %f)") %
              (orderid, status, filled, remaining, avgFillPrice, lastFilledPrice))
#        if remaining <= 0:
#           self.order_filled.set()


    def openOrder(self, orderID, contract, order, orderState):
        """
        Tells us about any orders we are working now
        
        Note these objects are not persistent or interesting so we have to extract what we want
        
        
        """
        

        ## Get a selection of interesting things about the order
        if self.handle_ibtrader.debug:
           print 'openOrder Order opened for %s orderID %s ' % (contract.symbol, orderID)
        if contract.exchange == 'IDEALPRO' or contract.exchange == 'IDEAL':
           localSymbol = contract.symbol + "." + contract.currency
        else:
           localSymbol = contract.localSymbol
           

        orderdict = dict(accountName=order.account,symbol=contract.symbol , localSymbol = localSymbol, orderState_status = orderState.status, expiry=contract.expiry, 
                       qty=int(order.totalQuantity) ,  limitPrice = order.lmtPrice ,
                       side=order.action , orderid=orderID, clientid=order.clientId , secType=contract.secType, currency=contract.currency,
                       exchange=contract.exchange, primaryExchange=contract.primaryExchange, quantity=order.totalQuantity, orderType=order.orderType, action=order.action) 
        
        self.handle_ibtrader.order_structure.append(orderdict)



    def commissionReport(self, commissionReport):

        self.handle_ibtrader.num_commReport += 1
        self.handle_ibtrader.total_comm += commissionReport.commission
        self.handle_ibtrader.mycommdetails[commissionReport.execId] = commissionReport.commission
        if self.handle_ibtrader.debug:
           print "all_trades_filled = %d num_commReport = %d num_executions %d" % (self.handle_ibtrader.all_trades_filled, self.handle_ibtrader.num_commReport, self.handle_ibtrader.num_executions)
        if (self.handle_ibtrader.all_trades_filled == 1 and self.handle_ibtrader.num_commReport == self.handle_ibtrader.num_executions) or self.handle_ibtrader.request_finished:
           if self.handle_ibtrader.debug:
              print "Alldone in commissionReport"
           self.handle_ibtrader.all_comm_filled = 1
           self.order_filled.set()


        if self.handle_ibtrader.debug:
            print 'Commission ID %s %s %s Total %.2f P&L: %s' % (commissionReport.execId, commissionReport.currency,
                                            commissionReport.commission,
                                            self.handle_ibtrader.total_comm,
                                            commissionReport.realizedPNL)


    def realtimeBar(self, reqId, bartime, baropen, barhigh, barlow, barclose, barvolume, wap, count):

        """
        Note we don't use all the information here

        Just append close prices.
        """

        self.handle_ibtrader.pricevalue.append(barclose)

    def tickString(self, TickerId, field, value):

        ## update string ticks

        tickType=int(field)
        TickerId = int(TickerId)
        self.handle_ibtrader.marketdata[TickerId][tickType] = value
        if self.handle_ibtrader.debug:
            print "tickString TickerId ", TickerId , " " , self.handle_ibtrader.marketdata[TickerId][IB_Tick_Type.SYMBOL],  " tickType ", IB_Tick_Type.desc[tickType], " value ", value
        return
        


    def tickGeneric(self, TickerId, tickType, value):

        ## update generic ticks

        tickType = int(tickType)
        TickerId = int(TickerId)
        self.handle_ibtrader.marketdata[TickerId][tickType] = value
        if self.handle_ibtrader.debug:
            print "tickGeneric TickerId ", TickerId  , " " , self.handle_ibtrader.marketdata[TickerId][IB_Tick_Type.SYMBOL], " tickType ", IB_Tick_Type.desc[tickType], " value ", value
        return
        
          
    def tickSize(self, TickerId, tickType, size):
        
        ## update ticks of the form new size
        

        tickType = int(tickType)
        TickerId = int(TickerId)
        self.handle_ibtrader.marketdata[TickerId][tickType] = size
        if self.handle_ibtrader.debug:
            print "tickSize TickerId ", TickerId , " " , self.handle_ibtrader.marketdata[TickerId][IB_Tick_Type.SYMBOL] ,  " tickType ", IB_Tick_Type.desc[tickType], " size ", size
        return

   
    def tickSnapshotEnd(self, tickerId):
        self.handle_ibtrader.finished=True

    def tickPrice(self, TickerId, tickType, price, canAutoExecute):
        ## update ticks of the form new price
        
        tickType = int(tickType)
        TickerId = int(TickerId)
        self.handle_ibtrader.marketdata[TickerId][tickType] = price
        if self.handle_ibtrader.debug:
            print "tickPrice TickerId ", TickerId , " " , self.handle_ibtrader.marketdata[TickerId][IB_Tick_Type.SYMBOL] ,  " tickType ", IB_Tick_Type.desc[tickType], " price ", price, " canAutoExecute ", canAutoExecute
        return
        
class IBTrader():


    args = None
    debug = False
    use_ib_orderid_call = False
    next_valid_orderid = 0
    accountName = "NO_ACCOUNT_NUM"
    print_normal_order_placed = False
    tws = None
    callback = None
    tcp_port = 4001
    tws_host = ""
    tws_clientid = 8899
    WAIT_TIME = 300
    MAX_WAIT_SECONDS = 30
    DEFAULT_MARKET_DATA_TIME = 20
    parser = None
    marketdata = [[] for i in range(1000)]
#https://www.interactivebrokers.com/en/software/api/apiguide/tables/api_message_codes.htm
    FOREX_SYMS=['EUR', 'JPY', 'GBP', 'AUD', 'USD', 'EUR.USD', 'JPY.USD', 'GBP.USD', 'AUD.USD', 'USD.JPY']
    ERRORS_TO_TRIGGER=[103, 162, 200, 201, 202, 203,  326,399, 406, 412, 420, 434, 478, 502, 504, 505, 511, 512, 515, 516, 517,  1100, 2105 ]
    ERRORS_TO_TRIGGER_ORDRPLACED=[103, 200, 201, 202, 203, 326, 399, 406, 412, 434, 502, 504, 505, 512, 515, 516, 517,  1100 ]

    def init_vars_before_each_call(self):

        self.pricevalue = None
        self.global_errorString = None
        self.global_errorCode = 0
        self.iserror = False
        self.request_finished=False
        self.execlist = []
        self.getting_today_executions = False
        self.partial_avg_price_per_share = 0
        self.partial_shares_filled = 0
        self.avg_price_per_share = 0
        self.total_shares_filled = 0
        self.is_request_open_order = False
        self.overridePercentageConstraints = True
        self.global_errorCode = 0
        self.mycommdetails = {}
        self.myexecdetails = {}
        self.num_executions = 0
        self.num_commReport = 0
        self.all_trades_filled = 0
        self.all_comm_filled = 0
        self.total_comm = 0
        self.order_structure = []
        self.ID_FOR_EXECUTIONS=randint(1000,2000)
        self.ID_FOR_QUOTE=randint(1,999)
        self.is_placing_order = False
        self.errormsg = ""
        self.account_number=""
        self.base_currency_cash=0
        self.order = None

    def __init__(self, account_number, tws_clientid, tws_host, tcp_port, debug, use_ib_orderid_call, wait_time):
       self.debug = debug
       if self.debug:
          print "IBWrapper(account_number = %s, tws_clientid = %d, tws_host = %s, tcp_port = %d, debug = %d, use_ib_orderid_call = %d, wait_time = %s)" % (account_number, int(tws_clientid), tws_host, int(tcp_port), debug, use_ib_orderid_call, wait_time)
       self.account_number = account_number
       if tws_clientid != 'not_a_tws_clientid':
           self.tws_clientid = int(tws_clientid)
       self.tws_host = tws_host
       self.tcp_port = tcp_port
       if wait_time != 'not_a_wait_time':
          self.WAIT_TIME = int(wait_time)
       self.use_ib_orderid_call = use_ib_orderid_call
       self.parser = self.add_all_arguments()
       self.init_vars_before_each_call()
       self.connect_to_tws()
       self.get_CurrentTime()


    def get_base_currency_cash(self):
        return self.base_currency_cash

    def cancel_order(self, orderid_to_cancel):
        self.tws.cancelOrder(orderid_to_cancel)

    def connect_to_tws(self):

        # Instantiate a socket object, allowing us to call TWS directly. Pass our
        # callback object so TWS can respond.
        self.callback = IBWrapper(self)
        self.tws = EPosixClientSocket(self.callback, reconnect_auto=True)


        # Connect to tws running on localhost
        if not self.tws.eConnect(self.tws_host, self.tcp_port, self.tws_clientid):
                raise RuntimeError('Failed to connect to TWS')
        
    def disconnect_from_tws(self):
        self.tws.poll_auto = False
        self.tws.eDisconnect()

    def print_json_start(self, mapkeyword):
        mystr = "{ \"" + mapkeyword + "\" : ["   + "\n"
        return mystr

    def print_json_dictword(self, mystr, dictline):
        mystr +=  str(json.dumps(dictline)) + "," + "\n"
        return mystr

    def print_json_end(self, mystr):
        mystr += "{\"dummy\" : 0} ]"
        if self.global_errorCode != 0 and self.iserror == True:
           mystr += "\n" +  " , " + "\n"
           mystr +=  "\"ErrorMessage\" : [" 
           mystr += "{\"error_code\" : " + str(self.global_errorCode) + "," 
           mystr += "\"error_message\" : \"" +  str(self.global_errorString) + "\""
           mystr += "}]"
           
        mystr += "}"
        return mystr

    def print_dictonary_json(self, mapkeyword, dictword):
        mystr = ""
        
        mystr = self.print_json_start(mapkeyword)
        for key in dictword:
            mystr = self.print_json_dictword(mystr, key)
        mystr = self.print_json_end(mystr)
        print mystr

    def get_order_exchange(self, symbol, secType, currency):
        
        if symbol in self.FOREX_SYMS and secType == "CASH":
            return "IDEALPRO"
        return "SMART"

    def get_CurrentTime(self):
        self.tws.reqCurrentTime()

    def get_open_orders(self):
        """
        Returns a list of any open orders
        """
        
        
        self.init_vars_before_each_call()
        self.iserror=False
        self.request_finished=False
        self.is_request_open_order=True
        self.order_structure=[]
        
        start_time=time.time()
        self.tws.reqAllOpenOrders()
        
        while not self.request_finished:
            if (time.time() - start_time) > self.MAX_WAIT_SECONDS:
                ## You should have thought that IB would told you we had finished
                self.request_finished=True
                self.is_request_open_order=False
            pass
        
        if self.iserror:
            pass
            #raise Exception("Problem getting open orders")

        return self.order_structure    


    def any_open_orders(self):
        """
        Simple wrapper to tell us if we have any open orders
        """

        return len(self.get_open_orders())>0

    def get_IB_positions(self):

        """
        Returns positions held - a particular kind of accounting information
        """

        self.init_vars_before_each_call()
        self.request_finished=False
        self.iserror=False
        self.portfolio_structure=[]
        self.portfolio_holdings = []
        self.account_value=[]
        

        ## Ask to get accounting info, both positions and account details
        if self.debug:
            print "reqAccountUpdates(True, self.account_number)"
        self.tws.reqAccountUpdates(True, self.account_number)
        start_time=time.time()
        while not self.request_finished:
            if (time.time() - start_time) > self.MAX_WAIT_SECONDS:
                self.request_finished=True
                self.iserror=True
            pass
        if self.debug:
            print "reqAccountUpdates(False, self.account_number) iserror = ", self.iserror
        self.tws.reqAccountUpdates(False, self.account_number)

        self.exchange_rates={}
        self.total_cash_balance={}

        ## Create a dictionary of exchange rates
        for x in self.account_value:
            if x[0]=="ExchangeRate":
                self.exchange_rates[x[2]]=float(x[1])
            if x[0]=="TotalCashBalance":
                if self.debug:
                   print "x[0] = ", x[0], 
                   print "x[1] = ", x[1], 
                   print "x[2] = ", x[2] 
                if x[2] == "BASE":
                    self.base_currency_cash = int(x[1])
                self.total_cash_balance[x[2]]=int(x[1])
                if x[2] in self.portfolio_holdings:
                   self.portfolio_holdings[x[2]]["quantity"] = int(x[1])

        #self.tws.reqPositions()
        return (self.portfolio_structure, self.exchange_rates, self.portfolio_holdings, self.total_cash_balance)

           
    def get_contract(self,symbol, secType, exchange, primaryExchange, currency):

        if self.debug:
           print "get_contract(symbol = %s, secType = %s, exchange = %s, primaryExchange = %s, currency = %s)" % (symbol, secType, exchange, primaryExchange, currency)
        contract = Contract()
        contract.symbol = str(symbol)
        contract.secType = secType
        contract.exchange = exchange
        contract.primaryExchange = primaryExchange
        contract.currency = currency
        return contract

    def get_next_valid_orderid(self):
        if self.use_ib_orderid_call:
           order_id = self.callback.order_ids.get(timeout=self.WAIT_TIME)
        else:
           while self.next_valid_orderid == 0:
               time.sleep(1)

           order_id = self.next_valid_orderid
           self.next_valid_orderid += 1

        return order_id
        #endif

    def place_order(self, symbol, secType, exchange, primaryExchange, currency, action, lmtPrice, orderType, totalQuantity, user_account, no_wait_for_complete = True):
        self.init_vars_before_each_call()

        self.is_placing_order = True
        if primaryExchange == '':
           primaryExchange = exchange
        if self.debug:
           print "place_order : Contract.symbol = %s secType = %s exchange = %s primaryExchange = %s currency = %s" % (symbol, secType, exchange, primaryExchange, currency)
        contract = self.get_contract(symbol, secType, exchange, primaryExchange, currency)

        if self.debug:
           print('Waiting for valid order id')
        order_id = self.get_next_valid_orderid()

        if not order_id:
            self.is_placing_order = False
            return None
            #raise RuntimeError('Failed to receive order id after %ds' % WAIT_TIME)


        order = Order()
        order.action = action
        order.lmtPrice = lmtPrice
        order.orderType = orderType
    #    order.overridePercentageConstraints = overridePercentageConstraints
        #order.orderRef = tws_clientid
        order.totalQuantity = totalQuantity


        if self.debug:
           print("Placing order for %d %s's @%s(%s) (id: %d) Action %s Type %s LimitPrice %s" % (order.totalQuantity,
                                                  contract.symbol, contract.exchange, contract.primaryExchange, order_id,  order.action, order.orderType, order.lmtPrice))

    # Place the order
        try:
            self.tws.placeOrder(
                order_id,                                   # orderId,
                contract,                                   # contract,
                order                                       # order
            )
        except:
            return None

        orderdict = dict(localSymbol=contract.localSymbol,symbol=contract.symbol, expiry=contract.expiry, order_id=order_id, action = action, 
                       order_type = orderType, exchange = exchange, primaryExchange = primaryExchange, currency = currency, sectype = secType, accountName = user_account, quantity =  order.totalQuantity)
        if no_wait_for_complete:
            time.sleep(2)
            if self.iserror:
               orderdict.update({'error_code' : self.global_errorCode, 'error_message' : self.global_errorString})
               self.is_placing_order = False
               if self.print_normal_order_placed == True:
                   print "Error placing order %d Message = %s Symbol %s Qty %d Limit %d Action %s Type %s  Account %s SecType %s Exchange %s PrimaryExchange %s Currency %s" % (order_id, self.global_errorString, symbol, order.totalQuantity,  lmtPrice, action, orderType, user_account, secType, exchange, primaryExchange, currency)
            else:
               orderdict.update({'NotWait' : True})
               if self.print_normal_order_placed == True:
                  print "PlacedOrder %d Symbol %s Qty %d Limit %d Action %s Type %s  Account %s SecType %s Exchange %s PrimaryExchange %s Currency %s" % (order_id, symbol, order.totalQuantity,  lmtPrice, action, orderType, user_account, secType, exchange, primaryExchange, currency)

            if self.debug:
                print "Not waiting for order to be completed"
            mstr = None
            if self.print_normal_order_placed == False:
                mstr = self.print_json_start("OrderPlaced")
                mstr = self.print_json_dictword(mstr, orderdict)
                mstr = self.print_json_end(mstr)
                if self.debug:
                    print "DEBUG ", mstr
            return mstr

        if self.debug:
           print("\n====================================================================")
           print(" Order placed, waiting %ds for TWS responses" % self.WAIT_TIME)
           print("====================================================================\n")
           print("Waiting for order to be filled..")



        try:
            self.callback.order_filled.wait(self.WAIT_TIME)
        except KeyboardInterrupt:
            pass
        finally:
            if not self.callback.order_filled.is_set():
                if self.debug:
                    print('Failed to fill order')
        if self.debug:
           print("\nDisconnecting...")

        self.is_placing_order = False
        if self.print_normal_order_placed:
            print "%s " % contract.symbol,
            print "%d " % order.totalQuantity,
            print "%s " % order.action,
            print "%s " % order.orderType,
            print "%d " % order_id,
            print "%.4f " % self.avg_price_per_share,
            print "%d " % self.total_shares_filled,
            print "%.2f " % self.total_comm,
            print "%s " % self.account_number
        else:
            mstr = self.print_json_start("OrderPlaced")
            orderdict.update({'avg_price' : self.avg_price_per_share, 'total_shares_filled' : self.total_shares_filled, 'total_commission' : self.total_comm})
            mstr = self.print_json_dictword(mstr, orderdict)
            mstr = self.print_json_end(mstr)
            if self.debug:
               print "DEBUG2 ", mstr
            return mstr




    def start_market_data(self, ibcontract, reqid):
        ## initialise the tuple
        if self.debug:
            print "init marketdata"
        if reqid == 0:
           reqid = self.ID_FOR_QUOTE
            
        # Request a market data stream 
        if self.debug:
            print "call tws.reqMktData with ID_FOR_QUOTE " , reqid
        self.marketdata[reqid]=[[] for i in range(1000)]
        self.marketdata[reqid][IB_Tick_Type.SYMBOL] = ibcontract.symbol
        self.tws.reqMktData(
                reqid,
                ibcontract,
                "",
                False, None)       
        return reqid 

    def stop_market_data(self, ibcontract, reqid):
        if self.debug:
            print "calling self.tws.cancelMktData"
        self.tws.cancelMktData(reqid)

    def get_IB_market_data(self, ibcontract, reqid=0):
        """
        Returns more granular market data
        
        Returns a tuple (bid price, bid size, ask price, ask size)
        
        """
        self.init_vars_before_each_call()
        self.finished=False
        self.iserror=False
        
        reqid = self.start_market_data(ibcontract, reqid)

        start_time=time.time()
        if self.debug:
            print "calling time.time() for ", str(start_time)
            print "Calling sleep(%d)" % self.DEFAULT_MARKET_DATA_TIME
        time.sleep(self.DEFAULT_MARKET_DATA_TIME)
        if self.debug:
            print "Done  sleep(%d)" % self.DEFAULT_MARKET_DATA_TIME
    #        while not finished:
    #            if (time.time() - start_time) > seconds:
    #                finished=True
    #            pass
        
        ## marketdata should now contain some interesting information
        ## Note in this implementation we overwrite the contents with each tick; we could keep them
        self.stop_market_data(ibcontract, reqid)
        
        if self.iserror:
            pass
            #raise Exception("Problem getting market data")
        
        if self.debug:
            print "returning marketdata"
        quotedict = self.convert_marketdata_to_dictonary(ibcontract, reqid)
        return quotedict

    def convert_marketdata_to_dictonary(self, ibcontract,reqid):
        lasttimeupdate = self.marketdata[reqid][IB_Tick_Type.LAST_TIMESTAMP]
        if lasttimeupdate:
            str_lasttimeupdate = str(datetime.datetime.fromtimestamp(int(lasttimeupdate)))
        else:
            lasttimeupdate = 0
            str_lasttimeupdate = ""
        quotedict = dict(symbol=ibcontract.symbol, localsymbol=ibcontract.localSymbol, lasttimeupdate = str_lasttimeupdate, int_lasttimeupdate = lasttimeupdate)
        for x in range(IB_Tick_Type.MAX_TICK_TYPE):
            val = self.marketdata[reqid][x]
            if val:
                dstr = IB_Tick_Type.desc[x]
                quotedict[dstr] = val
                if self.debug:
                    print "self.marketdata[%d][%s] = %s" % ( reqid, dstr, val)
        return quotedict

    def get_quote_list(self, ibcontract, reqid):
       obj = self.marketdata[reqid]
       return obj

    def get_quote_dictionary(self, ibcontract, reqid):
       obj = self.convert_marketdata_to_dictonary(ibcontract, reqid)
       return obj

    def get_last_bid_price(self,  reqid):
        val = float(self.marketdata[reqid][IB_Tick_Type.BID_PRICE])
        if val == 0:
           val = float(self.marketdata[reqid][IB_Tick_Type.CLOSE_PRICE])
        return val

    def get_last_ask_price(self,  reqid):
        val = float(self.marketdata[reqid][IB_Tick_Type.ASK_PRICE])
        if val == 0:
           val = float(self.marketdata[reqid][IB_Tick_Type.CLOSE_PRICE])
        return val

    def get_last_trade_price(self,  reqid):
        val = float(self.marketdata[reqid][IB_Tick_Type.LAST_PRICE])
        if val == 0:
           val = float(self.marketdata[reqid][IB_Tick_Type.CLOSE_PRICE])
        return val

    def get_last_trade_time(self,  reqid):
        val = int(self.marketdata[reqid][IB_Tick_Type.LAST_TIMESTAMP])
        return val

    def get_executions(self):

        """
        Returns a list of all executions done today
        """



        self.init_vars_before_each_call()
        self.iserror=False
        self.request_finished=False
        self.execlist=[]

        ## Tells the wrapper we are getting executions, not expecting fills
        ## Note that if you try and get executions when fills should be coming will be confusing!
        ## BE very careful with fills code

        self.getting_today_executions=True

        start_time=time.time()

        ## We can change ExecutionFilter to subset different orders

        self.tws.reqExecutions(self.ID_FOR_EXECUTIONS, ExecutionFilter())

        while not self.request_finished:
                if (time.time() - start_time) > self.MAX_WAIT_SECONDS:
                        self.request_finished=True
                        self.iserror=True
                pass

        ## Change this flag back so that the process gets fills properly
        self.getting_today_executions=False

        if self.iserror:
                pass
                #raise Exception("Problem getting executions")

        for key in self.execlist:
            execid = key["execid"]
            if execid in self.mycommdetails:
                key["commission"] = self.mycommdetails[execid]
            else:
                if self.debug:
                   print "No commission YET for execid", execid

        return self.execlist

    def set_args(self, args):
        self.args = args

    def get_args(self):
        return self.args

    @staticmethod
    def add_all_arguments():

        parser = argparse.ArgumentParser()
        parser.add_argument('-iboid', '--use_ib_orderid_call', action='store_true', help="Use IB Orderid mechanism")
        parser.add_argument('-qt', '--quote', action='store_true', help="Get quote for the symbol")
        parser.add_argument('-wt', '--wait_time', default='not_a_wait_time', help="Wait time in seconds for completion")
        parser.add_argument('-gw', '--gateway', action='store_true', help="Use gateway tcp port 4001 by default")
        parser.add_argument('-tws', '--tws', action='store_true', help="Use TWS tcp port 7496 by default")
        parser.add_argument('-new', '--new_order', action='store_true', help="Place a new order")
        parser.add_argument('-ts', '--trade_stock', action='store_true', help="Place a stock order [STK,SMART,USD]")
        parser.add_argument('-tf', '--trade_forex', action='store_true', help="Place a forex order [CASH,IDEALPRO,USD]")
        parser.add_argument('-to', '--trade_options', action='store_true', help="Place an options order [OPT,SMART,USD]")
        parser.add_argument('-ll', '--long_lmt', action='store_true', help="Place a Long Limit order")
        parser.add_argument('-lm', '--long_mkt', action='store_true', help="Place a Long Market order")
        parser.add_argument('-sl', '--short_lmt', action='store_true', help="Place a Short Limit order")
        parser.add_argument('-sm', '--short_mkt', action='store_true', help="Place a Short Market order")
        parser.add_argument('-sym', '--symbol', default='not_a_symbol', help="Symbol")
        parser.add_argument('-ot', '--order_secType', default='not_a_secType', help="Security Type [CASH|STK|FUT|OPT|etc]")
        parser.add_argument('-oe', '--order_exchange', default='not_a_exchange', help="Exchange [IDEALPRO|SMART]")
        parser.add_argument('-ope', '--order_primaryexchange', default='not_a_primaryexchange', help="Primary Exchange [IDEALPRO|SMART]")
        parser.add_argument('-oc', '--order_currency', default='not_a_currency', help="Currency USD")
        parser.add_argument('-oa', '--order_action', default='not_a_action', help="Order action BUY|SELL")
        parser.add_argument('-ol', '--order_limit_price', default='not_a_limit_price', help="Limit Price for the order, ignored in case of market order")
        parser.add_argument('-oo', '--order_type', default='not_a_type', help="Order Type LMT|MKT -- can be more")
        parser.add_argument('-oid', '--order_id', default='not_a_order_id', help="Order ID - used to search execution")
        parser.add_argument('-oq', '--order_quantity', default='not_a_quantity', help="Order Quantity")
        parser.add_argument('-pf', '--print_portfolio', action='store_true', help="Print Portfolio")
        parser.add_argument('-pc', '--print_cash', action='store_true', help="Print Cash in Portfolio")
        parser.add_argument('-pp', '--print_positions', action='store_true', help="Print ALL Positions")
        parser.add_argument('-ps', '--print_sym_position', action='store_true', help="Print Position for Symbol")
        parser.add_argument('-pe', '--print_executions', action='store_true', help="Print Executions")
        parser.add_argument('-pse', '--print_sym_executions', action='store_true', help="Print Executions for Symbol")
        parser.add_argument('-pid', '--print_order_id', action='store_true', help="Print Executions By Order ID")
        parser.add_argument('-po', '--print_open_orders', action='store_true', help="Print Open Orders")
        parser.add_argument('-pso', '--print_open_sym_orders', action='store_true', help="Print Open Orders for Symbol")
        parser.add_argument('-d', '--debug', action='store_true', help="Debug enable")
        parser.add_argument('-nod', '--no-debug', action='store_false', help="Debug disable")
        parser.add_argument('-tcp', '--tcp_port', default='not_a_tcp_port', help="Tcp port to use, default is 4001")
        parser.add_argument('-clid', '--tws_clientid', default='not_a_tws_clientid', help="TWS Client ID, default is 8899")
        parser.add_argument('-host', '--tws_host', default='not_a_tws_host', help="host name/address to use, default is localhost")
        parser.add_argument('-cal', '--cancel_all_orders', action='store_true', help="Cancel ALL open orders")
        parser.add_argument('-cso', '--cancel_sym_order', action='store_true', help="Cancel open orders for Symbol")
        parser.add_argument('-cid', '--cancel_orderid', default='not_a_cancel_orderid', help="Cancel IB order id")
        parser.add_argument('-clo', '--close_all_positions', action='store_true', help="Close ALL positions")
        parser.add_argument('-cls', '--close_sym_position', action='store_true', help="Close positions for Symbol")
        parser.add_argument('-nw', '--no_wait_for_complete', action='store_true', help="Dont wait for completion, just exit after placing order")
        parser.add_argument('-acnum', '--account_number', default='not_a_account_number', help="Account Number")

        return parser

    @staticmethod
    def parse_arguments(parser, args_to_parse):

        args = parser.parse_args(args_to_parse)
        if args.debug:
            print "gateway ", args.gateway
            print "tws ", args.tws
            print "new_order ", args.new_order
            print "wait_time ", args.wait_time
            print "tcp_port ", args.tcp_port
            print "tws_host ", args.tws_host
            print "tws_clientid ", args.tws_clientid
            print "symbol ", args.symbol
            print "trade_stock ", args.trade_stock
            print "trade_forex ", args.trade_forex
            print "trade_options ", args.trade_options
            print "order_secType ", args.order_secType
            print "order_exchange ", args.order_exchange
            print "order_primaryexchange ", args.order_primaryexchange
            print "order_currency ", args.order_currency
            print "order_action ", args.order_action
            print "order_limit_price ", args.order_limit_price
            print "order_type ", args.order_type
            print "order_quantity ", args.order_quantity
            print "print_portfolio ", args.print_portfolio
            print "print_cash ", args.print_cash
            print "print_positions ", args.print_positions
            print "print_sym_position ", args.print_sym_position
            print "print_executions ", args.print_executions
            print "order_id ", args.order_id
            print "print_order_id ", args.print_order_id
            print "print_sym_executions ", args.print_sym_executions
            print "print_open_orders ", args.print_open_orders
            print "print_open_sym_orders ", args.print_open_sym_orders
            print "close_all_positions ", args.close_all_positions
            print "close_sym_position ", args.close_sym_position
            print "cancel_sym_order ", args.cancel_sym_order
            print "cancel_all_orders ", args.cancel_all_orders
            print "cancel_orderid ", args.cancel_orderid
            print "no_wait_for_complete ", args.no_wait_for_complete
            print "long_lmt ", args.long_lmt
            print "long_mkt ", args.long_mkt
            print "short_lmt ", args.short_lmt
            print "short_mkt ", args.short_mkt
            print "account_number ", args.account_number
            print "quote ", args.quote
            print "debug ", args.debug

        return args


    def process_ib_commands(self, args_to_parse):

        args = self.parse_arguments(self.parser, args_to_parse)
        debug = args.debug
        mystr = None
        if args.cancel_sym_order and args.symbol == 'not_a_symbol':
                print "No symbol provided to cancel an order"
                return

        if args.close_sym_position and args.symbol == 'not_a_symbol':
                print "No symbol provided to close a position"
                return

        if args.print_sym_position and args.symbol == 'not_a_symbol':
                print "No symbol provided to print a position"
                return



        if args.trade_stock:
                args.order_secType = "STK"
                if args.order_exchange == 'not_a_exchange':
                        args.order_exchange = "SMART"
                args.order_currency = "USD"

        if args.trade_forex:
                args.order_secType = "CASH"
                if args.order_exchange == 'not_a_exchange':
                        args.order_exchange = "IDEALPRO"
                if args.order_currency == 'not_a_currency':
                        args.order_currency = "USD"

        if args.trade_options:
                args.order_secType = "OPT"
                if args.order_exchange == 'not_a_exchange':
                        args.order_exchange = "SMART"
                args.order_currency = "USD"

        if args.quote:
           if args.symbol == 'not_a_symbol':
                  print "No symbol passed for quote"
                  return
           ibcontract = self.get_contract(args.symbol, args.order_secType, args.order_exchange, args.order_exchange, args.order_currency)
           if args.order_exchange == 'IDEALPRO' or args.order_exchange == 'IDEAL':
              ibcontract.localSymbol = args.symbol + "." + args.order_currency
           else:
              ibcontract.localSymbol = args.symbol
           #ibcontract = Contract()
           #ibcontract.secType = "CASH"
           #ibcontract.symbol="EUR"
           #ibcontract.exchange="IDEALPRO"
           #ibcontract.currency = "USD"
           ans = self.get_IB_market_data(ibcontract)
           mystr = self.print_json_start("Quotes")
           mystr = self.print_json_dictword(mystr, ans)
           mystr = self.print_json_end(mystr)

           return mystr
           

        if args.cancel_orderid != 'not_a_cancel_orderid':
           orderid = int(args.cancel_orderid)
           if orderid != 0 and orderid is not None:
              self.cancel_order(orderid)
              time.sleep(1)

        if args.new_order or args.trade_stock or args.trade_forex or args.trade_options:

                if args.symbol == 'not_a_symbol':
                        print "No symbol passed in order"
                        return

                if args.long_lmt:
                        args.order_action = "BUY"
                        args.order_type = "LMT"

                if args.long_mkt:
                        args.order_action = "BUY"
                        args.order_type = "MKT"

                if args.order_quantity == 'not_a_quantity':
                   print "No quantity specified"
                   return

                if args.short_lmt:
                        args.order_action = "SELL"
                        args.order_type = "LMT"

                if args.short_mkt:
                        args.order_action = "SELL"
                        args.order_type = "MKT"


                order_symbol = args.symbol
                order_secType = args.order_secType
                order_exchange = args.order_exchange
                order_primaryexchange = args.order_primaryexchange
                order_currency = args.order_currency
                order_action = args.order_action
                order_limit_price = args.order_limit_price
                order_type = args.order_type

                order_quantity = int(args.order_quantity)

                if order_secType == 'not_a_secType':
                        print "No secType passed in order"
                        return
                
                if order_exchange == 'not_a_exchange':
                        print "No exchange passed in order"
                        return
                
                if order_currency == 'not_a_currency':
                        order_currency = "USD"
                        if debug:
                           print "No currency passed in order, USD assumed"
                
                if order_action == 'not_a_action':
                        print "No action passed in order"
                        return
                
                if order_type == 'not_a_type':
                        print "No order type passed in order"
                        return

                if order_quantity == 'not_a_quantity':
                        print "No quantity passed in order"
                        return
                
                if order_limit_price == 'not_a_limit_price':
                   if order_type == 'LMT':
                          print "No limit price passed in order"
                          return
                   else:
                          order_limit_price = 0
                else:
                   order_limit_price = float(args.order_limit_price)

                if order_primaryexchange == 'not_a_primaryexchange':
                   order_primaryexchange = order_exchange

                mystr = self.place_order(order_symbol, order_secType, order_exchange, order_primaryexchange, order_currency, order_action, order_limit_price, order_type, order_quantity, args.account_number, args.no_wait_for_complete)
                #print mystr

        if args.print_executions or args.print_sym_executions or args.print_order_id:
           if args.print_order_id and args.order_id == 'not_a_order_id':
                  print 'Order Id not provided'
                  return

           myexecutions = self.get_executions()

           mystr = self.print_json_start("AllTrades")
           for key in myexecutions:
                   sym = key["symbol"]
                   oid = key["orderid"]
                   if args.print_executions or (args.print_sym_executions and sym == args.symbol) or (args.print_order_id and args.order_id == oid):
                           mystr = self.print_json_dictword(mystr, key)
           mystr = self.print_json_end(mystr)
           #print mystr

        if args.print_portfolio or args.print_positions or args.print_sym_position or args.print_cash:
                myport = self.get_IB_positions()
                if args.print_cash:
                        print self.get_base_currency_cash()
                        pass

                #portfolio_structure, exchange_rates, portfolio_holdings, total_cash_balance
                port_struct = myport[0]
                exch_rates = myport[1]
                port_holdings = myport[2]
                total_cb = myport[3]
                #print "AccountName %s" % account_number
                if args.print_portfolio:
                        print "\nPositions"
                        print port_struct
                        print "\nExchange Rates"
                        print exch_rates
                        print "\nTotal Cash Balance"
                        for key, val in  total_cb.items():
                                print key, val

                if debug:
                        print "Portfolio Holdings"
                if args.print_portfolio or args.print_positions or args.print_sym_position:
                        mystr = self.print_json_start("PortfolioHoldings")
                        for key in  port_holdings:
                                if debug:
                                   print "Port_Holdings %s" % (key)
                                qty = key["quantity"]
                                sym = key["localSymbol"]
                                if qty != 0 and (args.print_positions or (args.print_sym_position and sym == args.symbol)):
                                        mystr = self.print_json_dictword(mystr, key)
                        mystr = self.print_json_end(mystr)
                        #print mystr


        if args.close_all_positions or args.close_sym_position:
                myport = self.get_IB_positions()
                all_positions = myport[2]
                args.no_wait_for_complete = 1
                for key in  all_positions:
                        order_localSymbol = key["localSymbol"]
                        order_quantity = key["quantity"]
                        if order_quantity < 0:
                                order_quantity = -order_quantity
                        if order_quantity > 0 and (args.close_all_positions or (args.close_sym_position and args.symbol == order_localSymbol)):
                                if debug:
                                        print "Portfolio %s ", key
                                order_symbol = key["symbol"]
                                order_secType = key["secType"]
                                order_exchange = key["exchange"]
                                order_currency = key["currency"]
                                order_action = key["flip_action"]
                                order_type = "MKT"
                                if debug:
                                   print "Close order_symbol = %s %s %s %d @ %s order_exchange = %s" % (order_symbol, key, order_action, order_quantity, order_type, order_exchange)
                                order_limit_price = 0
                                if order_exchange == '':
                                   order_exchange = self.get_order_exchange(order_symbol, order_secType, order_currency)
                                order_primaryexchange = order_exchange
                                self.place_order(order_symbol, order_secType, order_exchange, order_primaryexchange, order_currency, order_action, order_limit_price, order_type, order_quantity, args.account_number, True)
        #24 {'orderid': 24L, 'exchange': 'IDEALPRO', 'secType': 'CASH', 'orderType': 'LMT', 'primaryExchange': '', 'clientid': 8899L, 'qty': 100000, 'currency': 'USD', 'contract': <swigibpy.Contract; proxy of <Swig Object of type 'Contract *' at 0x7fb0883a2480> >, 'action': 'BUY', 'expiry': '', 'symbol': 'EUR', 'quantity': 100000L, 'side': 'BUY'}
        if args.print_open_orders or args.cancel_all_orders or args.cancel_sym_order or args.print_open_sym_orders:
                openorders = self.get_open_orders()
                mystr = ""
                if debug:
                        print "Active orders: (should just be limit order)"
                if args.print_open_orders or args.print_open_sym_orders:
                   mystr = self.print_json_start("OpenOrders")
                if args.cancel_all_orders or args.cancel_sym_order:
                   mystr = self.print_json_start("CancelOrders")
                for key in openorders:
                        localSymbol = key["localSymbol"]
                        orderid = key["orderid"]
                        #print "args.symbol is ", args.symbol
                        if args.symbol == 'not_a_symbol' or args.symbol == localSymbol:
                                mystr = self.print_json_dictword(mystr, key)
                        #if args.print_open_orders:
        #        print "%d %s %s %s %s %s %s %s %s %s %s " % (key, sym, val["localSymbol"], val["orderState_status"], val["secType"], val["action"], val["orderType"], val["qty"], val["limitPrice"], val["currency"], val["exchange"])
                        
                        if args.cancel_all_orders or (args.cancel_sym_order and args.symbol == localSymbol):
                                if debug:
                                        print "Cancel order id %d symbol = %s" %  (key, sym)
                                self.cancel_order(orderid)

                if args.cancel_all_orders:
                        if debug:
                           print "Waiting for cancellation to finish"
                        while self.any_open_orders():
                          pass
                        if debug:
                           print "All orders canceled"
                mystr = self.print_json_end(mystr)
                #print mystr

        return mystr
def main_function(args_to_parse):


    parser = IBTrader.add_all_arguments()
    args = IBTrader.parse_arguments(parser, args_to_parse)

    if args.wait_time != 'not_a_wait_time':
            args.wait_time = int(args.wait_time)

    if args.gateway:
            args.tcp_port = 4001

    if args.tws:
            args.tcp_port = 7496

    if args.tcp_port != 'not_a_tcp_port':
            args.tcp_port = int(args.tcp_port)

    if args.tws_host != 'not_a_tws_host':
            args.tws_host = args.tws_host

    ibtrader = IBTrader(args.account_number, args.tws_clientid, args.tws_host, int(args.tcp_port), args.debug, args.use_ib_orderid_call, args.wait_time)
    ibtrader.set_args(args)
    return ibtrader

if __name__ == '__main__':
    ibtrader = main_function(sys.argv[1:])
    mystr = ibtrader.process_ib_commands(sys.argv[1:])
    if mystr is not None:
        print mystr
    ibtrader.disconnect_from_tws()
    sys.exit()
