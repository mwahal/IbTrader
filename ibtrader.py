#!/usr/bin/python
'''IBTrader is based on SWIG generated TWS wrapper to communicate with Interactive Brokers.
https://pypi.python.org/pypi/swigibpy/0.4.1

'''

import sys
import argparse
import time
import json
from pprint import pprint
from threading import Event

from swigibpy import (EWrapper, EPosixClientSocket, Contract, Order, TagValue,
                      TagValueList, ExecutionFilter)




try:
    # Python 2 compatibility
    input = raw_input
    from Queue import Queue
except:
    from queue import Queue

###
    

def print_json_start(mapkeyword):
    print "{ \"%s\" : ["  % (mapkeyword)

def print_json_dictword(dictline):
    print "%s, " % json.dumps(dictline)

def print_json_end():
    print "{\"dummy\" : 0} ] }"

def print_dictonary_json(mapkeyword, dictword):
    
    print_json_start(mapkeyword)
    for key in mapkeyword:
        print_json_dictword(key)
    print_json_end()

def get_order_exchange(symbol, secType, currency):
    
    FOREX_SYMS=['EUR', 'JPY', 'GBP', 'AUD', 'USD', 'EUR.USD', 'JPY.USD', 'GBP.USD', 'AUD.USD', 'USD.JPY']
    if symbol in FOREX_SYMS and secType == "CASH":
        return "IDEALPRO"
    return "SMART"

def get_open_orders():
    """
    Returns a list of any open orders
    """
    
    
    global request_finished
    global iserror
    global order_structure
    global is_request_open_order
    
    iserror=False
    request_finished=False
    is_request_open_order=True
    order_structure=[]
    
    start_time=time.time()
    tws.reqAllOpenOrders()
    
    while not request_finished:
        if (time.time() - start_time) > MAX_WAIT_SECONDS:
            ## You should have thought that IB would told you we had finished
            request_finished=True
            is_request_open_order=False
        pass
    
    if iserror:
        raise Exception("Problem getting open orders")

    return order_structure    


def any_open_orders():
    """
    Simple wrapper to tell us if we have any open orders
    """

    return len(get_open_orders())>0

def get_IB_positions():

    """
    Returns positions held - a particular kind of accounting information
    """


    global request_finished
    global iserror
    global portfolio_structure
    global portfolio_holdings
    global account_value
    global base_currency_cash
    global debug

    request_finished=False
    iserror=False
    portfolio_structure=[]
    portfolio_holdings = []
    account_value=[]
    accountid = "DU999999"

    ## Ask to get accounting info, both positions and account details
    if debug:
        print "reqAccountUpdates(True, self.accountid)"
    tws.reqAccountUpdates(True, accountid)
    start_time=time.time()
    while not request_finished:
        if (time.time() - start_time) > MAX_WAIT_SECONDS:
            request_finished=True
            iserror=True
        pass
    if debug:
        print "reqAccountUpdates(False, self.accountid) iserror = ", iserror
    tws.reqAccountUpdates(False, accountid)

    exchange_rates={}
    total_cash_balance={}

    ## Create a dictionary of exchange rates
    for x in account_value:
        if x[0]=="ExchangeRate":
            exchange_rates[x[2]]=float(x[1])
        if x[0]=="TotalCashBalance":
            if debug:
               print "x[0] = ", x[0], 
               print "x[1] = ", x[1], 
               print "x[2] = ", x[2] 
            if x[2] == "BASE":
                base_currency_cash = int(x[1])
            total_cash_balance[x[2]]=int(x[1])
            if x[2] in portfolio_holdings:
               portfolio_holdings[x[2]]["quantity"] = int(x[1])

    #self.tws.reqPositions()
    return (portfolio_structure, exchange_rates, portfolio_holdings, total_cash_balance)

       

def place_order(symbol, secType, exchange, primaryExchange, currency, action, lmtPrice, orderType, totalQuantity, user_account):

    global debug
    global order
    global account_number
    global args
    global is_placing_order
    global global_errorString

    is_placing_order = True
    if primaryExchange == '':
       primaryExchange = exchange
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.primaryExchange = primaryExchange
    contract.currency = currency
    if debug:
       print("place_order : Contract.symbol = %s secType = %s exchange = %s primaryExchange = %s currency = %s" % (symbol, secType, exchange, primaryExchange, currency))

    if debug:
       print('Waiting for valid order id')
    order_id = callback.order_ids.get(timeout=WAIT_TIME)
    if not order_id:
        is_placing_order = False
        raise RuntimeError('Failed to receive order id after %ds' % WAIT_TIME)


    order = Order()
    order.action = action
    order.lmtPrice = lmtPrice
    order.orderType = orderType
#    order.overridePercentageConstraints = overridePercentageConstraints
    #order.orderRef = tws_clientid
    order.totalQuantity = totalQuantity


    if debug:
       print("Placing order for %d %s's @%s(%s) (id: %d) Action %s Type %s LimitPrice %s" % (order.totalQuantity,
                                              contract.symbol, contract.exchange, contract.primaryExchange, order_id,  order.action, order.orderType, order.lmtPrice))

# Place the order
    tws.placeOrder(
        order_id,                                   # orderId,
        contract,                                   # contract,
        order                                       # order
    )

    if args.no_wait_for_complete:
        time.sleep(2)
        if iserror:
           is_placing_order = False
           print "Error placing order %d Message = %s Symbol %s Qty %d Limit %d Action %s Type %s  Account %s SecType %s Exchange %s PrimaryExchange %s Currency %s" % (order_id, global_errorString, symbol, order.totalQuantity,  lmtPrice, action, orderType, user_account, secType, exchange, primaryExchange, currency)
        else:
           print "PlacedOrder %d Symbol %s Qty %d Limit %d Action %s Type %s  Account %s SecType %s Exchange %s PrimaryExchange %s Currency %s" % (order_id, symbol, order.totalQuantity,  lmtPrice, action, orderType, user_account, secType, exchange, primaryExchange, currency)

        if debug:
            print "Not waiting for order to be completed"
        return

    if debug:
       print("\n====================================================================")
       print(" Order placed, waiting %ds for TWS responses" % WAIT_TIME)
       print("====================================================================\n")
       print("Waiting for order to be filled..")



    try:
        callback.order_filled.wait(WAIT_TIME)
    except KeyboardInterrupt:
        pass
    finally:
        if not callback.order_filled.is_set():
            if debug:
                print('Failed to fill order')
    if debug:
       print("\nDisconnecting...")

    is_placing_order = False
    print "%s " % contract.symbol,
    print "%d " % order.totalQuantity,
    print "%s " % order.action,
    print "%s " % order.orderType,
    print "%d " % order_id,
    print "%.4f " % avg_price_per_share,
    print "%d " % total_shares_filled,
    print "%.2f " % total_comm,
    print "%s " % account_number


def get_executions():
	"""
	Returns a list of all executions done today
	"""


	global request_finished
	global iserror
	global execlist
	global getting_today_executions

	iserror=False
	request_finished=False
	execlist=[]

	## Tells the wrapper we are getting executions, not expecting fills
	## Note that if you try and get executions when fills should be coming will be confusing!
	## BE very careful with fills code

	getting_today_executions=True

	start_time=time.time()

	## We can change ExecutionFilter to subset different orders

	tws.reqExecutions(MEANINGLESS_NUMBER, ExecutionFilter())

	while not request_finished:
		if (time.time() - start_time) > MAX_WAIT_SECONDS:
			request_finished=True
			iserror=True
		pass

	## Change this flag back so that the process gets fills properly
	getting_today_executions=False

	if iserror:
		raise Exception("Problem getting executions")

        for key in execlist:
            execid = key["execid"]
            key["commission"] = mycommdetails[execid]

	return execlist

class IBClient(EWrapper):
    '''Callback object passed to TWS, these functions will be called directly
    by TWS.

    '''

    def __init__(self):
        super(IBClient, self).__init__()
        self.order_filled = Event()
        self.order_ids = Queue()


    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        """
        Add a row to the portfolio structure
        """
        global portfolio_holdings
        global request_finished
        global debug

        if request_finished == True:
           return

                
        if debug:
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
        portdict=dict(localSymbol=contract.localSymbol,symbol=contract.symbol, expiry=contract.expiry, 
                       secType=contract.secType, currency=contract.currency,
                       exchange=contract.exchange,quantity=position,
                       primaryExchange = contract.primaryExchange,
                       marketPrice=marketPrice, marketValue= marketValue, averageCost=averageCost,
                       curr_action=curr_action, flip_action=flip_action,hold_type=hold_type,
                       unrealizedPNL=unrealizedPNL, realizedPNL=realizedPNL, accountName=accountName, costPrice=costPrice, gainloss=gnloss) 

        #portfolio_holdings[sym] = portdict
        portfolio_holdings.append(portdict)
        #portfolio_holdings[sym] = (contract.symbol, contract.expiry, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName, contract.currency)
        portfolio_structure.append((sym, contract.expiry, position, marketPrice, marketValue, averageCost, 
                                    unrealizedPNL, realizedPNL, accountName, contract.currency, contract.exchange, contract.primaryExchange))

    def error(self, id, errorCode, errorString):
        """
        error handling, simple for now
       
        Here are some typical IB errors
        INFO: 2107, 2106
        WARNING 326 - can't connect as already connected
        CRITICAL: 502, 504 can't connect to TWS.
            200 no security definition found
            162 no trades

        """
        global iserror
        global errormsg
        global finished
        global request_finished
        global is_placing_order
        global global_errorString

        ## Any errors not on this list we just treat as information
        ERRORS_TO_TRIGGER=[201, 103, 502, 504, 509, 200, 162, 420, 2105, 1100, 478, 201, 399]
        global_errorString = errorString
       
        #print "ERROR errorCode = %d errorString = %s" % (errorCode, errorString)
        if errorCode in ERRORS_TO_TRIGGER:
            iserror=True
            errormsg="Code=%d IB error id %d errorcode %d string %s" %(errorCode, id, errorCode, errorString)
            if is_placing_order == False:
                print errormsg
            finished=True  
            request_finished=True  
           
        ## Wrapper functions don't have to return anything this is to tidy
        return 0
      
    def updateAccountValue(self, key, value, currency, accountName):
        """
        Populates account value dictionary
        """
        global request_finished
        global debug
        global account_number
        if request_finished == True:
           return
        if debug:
           print "updateAccountValue portfolio_finished = %d key = %s value = %s currency = %s accountName = %s" % (request_finished, key, value, currency, accountName)
        if key == "AccountCode":
            accountName = value
        account_value.append((key, value, currency, accountName))
        

    def accountDownloadEnd(self, accountName):
        global request_finished
        global debug
        """
        portfolio_finished can look at portfolio_structure and account_value
        """

        request_finished=True
        if debug:
           print "accountDownloadEnd accountName = %s" % accountName

    def updateAccountTime(self, timeStamp):
        pass 


    def openOrderEnd(self):
        global debug
        global request_finished
        global is_request_open_order
        
        if debug:
            print "openOrderEnd is_request_open_order = %d" % is_request_open_order
        if is_request_open_order:
            request_finished=True
            is_request_open_order=False
        if debug:
           print "openOrderEnd"
        pass

    def execDetails(self, id, contract, execution):
        global num_executions
        global myexecdetails
        global all_trades_filled
        global avg_price_per_share
        global total_shares_filled
        global partial_avg_price_per_share
        global partial_shares_filled
        global getting_today_executions
        global execlist
        global order
        global account_number
        global request_finished
        num_executions += 1



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

        #execdetails=dict(side=str(side), exectime=str(exectime), orderid=str(thisorderid), execshares=int(execution.shares), qty=int(cumQty), avgprice=float(execution.avgPrice), execprice=float(execution.price), symbol=str(symbol), expiry=str(expiry), clientid=str(clientid), execid=str(execid), account=str(account_number), exchange=str(exchange), permid=int(permid), commission=0)
        execdetails=dict(side=str(side), exectime=str(exectime), orderid=int(thisorderid), execshares=int(execution.shares), qty=int(cumQty), avgprice=float(execution.avgPrice), execprice=float(execution.price), symbol=str(symbol), expiry=str(expiry), clientid=int(clientid), execid=str(execid), accountName=str(account_number), exchange=str(exchange), permid=int(permid), commission=str(0), localsymbol=localsymbol, secType=contract.secType, primaryExchange=contract.primaryExchange)

        if debug:
#           print "execDetails id = %s contract = %s execution = %s" % (id, str(contract), str(execution))
           print "Execution number = %d "% num_executions
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

        if getting_today_executions == 1:
           if debug:
              print "getting_today_executions = 1"
           execlist.append(execdetails)
        else:
           avg_price_per_share =  execution.avgPrice
           total_shares_filled =  execution.cumQty
           partial_avg_price_per_share = execution.avgPrice
           partial_shares_filled = execution.cumQty
           myexecdetails[execution.execId] = execution
           if (order.totalQuantity == execution.cumQty):
              all_trades_filled = 1
           if all_comm_filled and ((order.totalQuantity == execution.cumQty) or request_finished):
              if debug:
                 print "request_finished is %s " % request_finished
              partial_avg_price_per_share = 0
              partial_shares_filled = 0
              all_trades_filled = 1
              avg_price_per_share = execution.avgPrice
              total_shares_filled = execution.cumQty
              total_commission_paid = 0
              for key in myexecdetails.items():
                  if key in mycommdetails:
                      total_commission_paid += mycommdetails[key]
                  else:
                      print key
              if debug:
                 print "AvgPrice = %.4f TotalFilled = %d TotalComm = %.2f" % (execution.avgPrice, execution.cumQty, total_comm)
              if (all_comm_filled == 1):
                 self.order_filled.set()


    def execDetailsEnd(self, reqId):
        """
        No more orders to look at if execution details requested
        """
        global request_finished
        request_finished=True
        if debug:
           print "execDetailsEnd for reqId = %d" % reqId

    def managedAccounts(self, openOrderEnd):
        '''Not relevant for our example'''
        pass

    ###############

    def nextValidId(self, validOrderId):
        '''Capture the next order id'''
        self.order_ids.put(validOrderId)

    def orderStatus(self, id, status, filled, remaining, avgFillPrice, permId,
                    parentId, lastFilledPrice, clientId, whyHeld):

        global is_request_open_order
        if is_request_open_order:
            return

        if debug:
           print(("Order #%s - %s (filled %d, remaining %d, avgFillPrice %f,"
               "last fill price %f)") %
              (id, status, filled, remaining, avgFillPrice, lastFilledPrice))
#        if remaining <= 0:
#           self.order_filled.set()


    def openOrder(self, orderID, contract, order, orderState):
        """
        Tells us about any orders we are working now
        
        Note these objects are not persistent or interesting so we have to extract what we want
        
        
        """
        
        global order_structure

        ## Get a selection of interesting things about the order
        if debug:
           print 'openOrder Order opened for %s orderID %s ' % (contract.symbol, orderID)
        if contract.exchange == 'IDEALPRO' and contract.exchange == 'IDEAL':
           localSymbol = contract.symbol + "." + contract.currency
        else:
           localSymbol = contract.localSymbol
           

        orderdict=dict(accountName=order.account,symbol=contract.symbol , localSymbol = localSymbol, orderState_status = orderState.status, expiry=contract.expiry, 
                       qty=int(order.totalQuantity) ,  limitPrice = order.lmtPrice ,
                       side=order.action , orderid=orderID, clientid=order.clientId , secType=contract.secType, currency=contract.currency,
                       exchange=contract.exchange, primaryExchange=contract.primaryExchange, quantity=order.totalQuantity, orderType=order.orderType, action=order.action) 
        
        order_structure.append(orderdict)



    def commissionReport(self, commissionReport):
        global total_comm;
        global mycommdetails;
        global num_commReport;
        global all_trades_filled;

        num_commReport += 1
        total_comm += commissionReport.commission
        mycommdetails[commissionReport.execId] = commissionReport.commission
        if debug:
           print "all_trades_filled = %d num_commReport = %d num_executions %d" % (all_trades_filled, num_commReport, num_executions)
        if (all_trades_filled == 1 and num_commReport == num_executions) or request_finished:
           if debug:
              print "Alldone in commissionReport"
           all_comm_filled = 1
           self.order_filled.set()


        if debug:
            print 'Commission ID %s %s %s Total %.2f P&L: %s' % (commissionReport.execId, commissionReport.currency,
                                            commissionReport.commission,
                                            total_comm,
                                            commissionReport.realizedPNL)

#prompt = input("WARNING: This example will place an order on your IB "
#               "account, are you sure? (Type yes to continue): ")
#if prompt.lower() != 'yes':
#    sys.exit()
iserror = False
request_finished=False
execlist = []
getting_today_executions = False
accountName = "NO_ACCOUNT_NUM"
partial_avg_price_per_share = 0
partial_shares_filled = 0
avg_price_per_share = 0
total_shares_filled = 0
is_request_open_order = False
overridePercentageConstraints = True

mycommdetails = {}
myexecdetails = {}
num_executions = 0
num_commReport = 0
all_trades_filled = 0
all_comm_filled = 0
total_comm = 0
debug = 0
#tcp_port = 7496
tcp_port = 4001
tws_host = ""
tws_clientid = 8899
WAIT_TIME = 300
MAX_WAIT_SECONDS = 30
order_structure = []
MEANINGLESS_NUMBER=1729
is_placing_order = False
errormsg = ""
account_number=""
base_currency_cash=0

# Instantiate our callback object
callback = IBClient()

parser = argparse.ArgumentParser()
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
parser.add_argument('-clo', '--close_all_positions', action='store_true', help="Close ALL positions")
parser.add_argument('-cls', '--close_sym_position', action='store_true', help="Close positions for Symbol")
parser.add_argument('-nw', '--no_wait_for_complete', action='store_true', help="Dont wait for completion, just exit after placing order")
parser.add_argument('-acnum', '--account_number', default='not_a_account_number', help="Account Number")


args = parser.parse_args()
if args.debug:
    debug = 1
if debug:
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
    print "no_wait_for_complete ", args.no_wait_for_complete
    print "long_lmt ", args.long_lmt
    print "long_mkt ", args.long_mkt
    print "short_lmt ", args.short_lmt
    print "short_mkt ", args.short_mkt
    print "account_number ", args.account_number
    print "debug ", args.debug

if args.gateway:
    args.tcp_port = 4001

if args.tws:
    args.tcp_port = 7496

if args.tcp_port != 'not_a_tcp_port':
    tcp_port = int(args.tcp_port)

if args.tws_host != 'not_a_tws_host':
    tws_host = args.tws_host

if args.cancel_sym_order and args.symbol == 'not_a_symbol':
    print "No symbol provided to cancel an order"
    sys.exit()

if args.close_sym_position and args.symbol == 'not_a_symbol':
    print "No symbol provided to close a position"
    sys.exit()

if args.print_sym_position and args.symbol == 'not_a_symbol':
    print "No symbol provided to print a position"
    sys.exit()

# Instantiate a socket object, allowing us to call TWS directly. Pass our
# callback object so TWS can respond.
tws = EPosixClientSocket(callback)

if args.tws_clientid != 'not_a_tws_clientid':
   tws_clientid = int(args.tws_clientid)

if debug:
   print 'tws_clientid is  ', tws_clientid



# Connect to tws running on localhost
if not tws.eConnect(tws_host, tcp_port, tws_clientid):
    raise RuntimeError('Failed to connect to TWS')

if args.new_order or args.trade_stock or args.trade_forex or args.trade_options:

    if args.symbol == 'not_a_symbol':
        print "No symbol passed in order"
        sys.exit()

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
        if order_exchange == 'not_a_exchange':
            args.order_exchange = "SMART"
        args.order_currency = "USD"

    if args.long_lmt:
        args.order_action = "BUY"
        args.order_type = "LMT"

    if args.long_mkt:
        args.order_action = "BUY"
        args.order_type = "MKT"

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
        sys.exit()
    
    if order_exchange == 'not_a_exchange':
        print "No exchange passed in order"
        sys.exit()
    
    if order_currency == 'not_a_currency':
        order_currency = "USD"
        if debug:
           print "No currency passed in order, USD assumed"
    
    if order_action == 'not_a_action':
        print "No action passed in order"
        sys.exit()
    
    if order_type == 'not_a_type':
        print "No order type passed in order"
        sys.exit()

    if order_quantity == 'not_a_quantity':
        print "No quantity passed in order"
        sys.exit()
    
    if order_limit_price == 'not_a_limit_price':
       if order_type == 'LMT':
          print "No limit price passed in order"
          sys.exit()
       else:
          order_limit_price = 0
    else:
       order_limit_price = float(args.order_limit_price)

    if order_primaryexchange == 'not_a_primaryexchange':
       order_primaryexchange = order_exchange

    place_order(order_symbol, order_secType, order_exchange, order_primaryexchange, order_currency, order_action, order_limit_price, order_type, order_quantity, args.account_number)

if args.print_executions or args.print_sym_executions or args.print_order_id:
   if args.print_order_id and args.order_id == 'not_a_order_id':
      print 'Order Id not provided'
      sys.exit()

   myexecutions = get_executions()

   print_json_start("AllTrades")
   for key in myexecutions:
       sym = key["symbol"]
       oid = key["orderid"]
       if args.print_executions or (args.print_sym_executions and sym == args.symbol) or (args.print_order_id and args.order_id == oid):
           print_json_dictword(key)
   print_json_end()

if args.print_portfolio or args.print_positions or args.print_sym_position or args.print_cash:
    myport = get_IB_positions()
    if args.print_cash:
        print base_currency_cash
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
        print_json_start("PortfolioHoldings")
        for key in  port_holdings:
            if debug:
               print "Port_Holdings %s" % (key)
            qty = key["quantity"]
            sym = key["localSymbol"]
            if qty != 0 and (args.print_positions or (args.print_sym_position and sym == args.symbol)):
                print_json_dictword(key)
        print_json_end()


if args.close_all_positions or args.close_sym_position:
    myport = get_IB_positions()
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
               order_exchange = get_order_exchange(order_symbol, order_secType, order_currency)
            order_primaryexchange = order_exchange
            place_order(order_symbol, order_secType, order_exchange, order_primaryexchange, order_currency, order_action, order_limit_price, order_type, order_quantity, accountName)
#24 {'orderid': 24L, 'exchange': 'IDEALPRO', 'secType': 'CASH', 'orderType': 'LMT', 'primaryExchange': '', 'clientid': 8899L, 'qty': 100000, 'currency': 'USD', 'contract': <swigibpy.Contract; proxy of <Swig Object of type 'Contract *' at 0x7fb0883a2480> >, 'action': 'BUY', 'expiry': '', 'symbol': 'EUR', 'quantity': 100000L, 'side': 'BUY'}
if args.print_open_orders or args.cancel_all_orders or args.cancel_sym_order or args.print_open_sym_orders:
    openorders = get_open_orders()
    if debug:
        print "Active orders: (should just be limit order)"
    if args.print_open_orders or args.print_open_sym_orders:
       print_json_start("OpenOrders")
    if args.cancel_all_orders or args.cancel_sym_order:
       print_json_start("CancelOrders")
    for key in openorders:
        localSymbol = key["localSymbol"]
        orderid = key["orderid"]
		if args.symbol == None or args.symbol == localSymbol:
           print_json_dictword(key)
        #if args.print_open_orders:
#        print "%d %s %s %s %s %s %s %s %s %s %s " % (key, sym, val["localSymbol"], val["orderState_status"], val["secType"], val["action"], val["orderType"], val["qty"], val["limitPrice"], val["currency"], val["exchange"])
        
        if args.cancel_all_orders or (args.cancel_sym_order and args.symbol == localSymbol):
            if debug:
                print "Cancel order id %d symbol = %s" %  (key, sym)
            tws.cancelOrder(orderid)

    if args.cancel_all_orders:
        if debug:
           print "Waiting for cancellation to finish"
        while any_open_orders():
          pass
        if debug:
           print "All orders canceled"
    print_json_end()

tws.eDisconnect()
