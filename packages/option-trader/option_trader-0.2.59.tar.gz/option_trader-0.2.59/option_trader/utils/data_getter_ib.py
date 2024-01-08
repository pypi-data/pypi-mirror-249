import pandas as pd
import numpy  as np
import math

from  option_trader.settings import ib_settings
from  option_trader.settings import app_settings   
from  option_trader.admin import quote
from  option_trader.consts import asset as at
from  option_trader.admin.position_summary import position_summary_col_name as pscl
from  option_trader.admin.position import position_col_name as pcl

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.ticktype import TickTypeEnum
from ibapi.utils import *
from ibapi.account_summary_tags import AccountSummaryTags
from ibapi.contract import Contract, ComboLeg, ContractDetails
from ibapi.order import *
from ibapi.order_state import OrderState
from ibapi.execution import Execution

from threading import Timer

#from ib_insync import *

import logging

#import option_trader.admin.position_summary as ps
#from option_trader.admin.position import position       

from datetime import time, date, datetime, timedelta
from pytz import timezone
from option_trader.consts import strategy as st
import json


def place_ib_order(ps_row, TWS=False, live=False, simple_order=False):
    with IBClient(TWS=TWS, Live=live) as ibClient:
        x = ibClient.place_ib_order(ps_row, bracket=False)    
    return x

class IBClient:    

    def __init__(self, 
                 host=ib_settings.HostIP, 
                 TWS=ib_settings.TWS, 
                 Live=ib_settings.LIVE, 
                 marketDataType=ib_settings.IBConfig.marketDataType):
        
        self.TWS = TWS
        self.Live = Live
        self.host = host

        self.marketDataType = marketDataType

        self.logger = logging.getLogger(__name__)

        if TWS:
            self.port = ib_settings.IBConfig.TWS_live.port if Live else ib_settings.IBConfig.TWS_papaer.port
            self.clientID = ib_settings.IBConfig.TWS_live.clientId if Live else ib_settings.IBConfig.TWS_papaer.clientId
        else:
            self.port = ib_settings.IBConfig.Gateway_live.port if Live else ib_settings.IBConfig.Gateway_papaer.port
            self.clientID = ib_settings.IBConfig.Gateway_live.clientId if Live else ib_settings.IBConfig.Gateway_papaer.clientId
      
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        return

    def get_option_contId(self, symbol, exp_date, strike, otype):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'OPT'
        contract.exchange = 'SMART'
        contract.lastTradeDateOrContractMonth = exp_date
        contract.strike = strike
        contract.right = otype
            #put_contract.multiplier = '100' 
        with contract_details(contract) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()  
            return app.conId
        
    def get_option_snapshot_guote(self, symbol, exp_date, strike, otype):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'OPT'
        contract.exchange = 'SMART'
        contract.lastTradeDateOrContractMonth = exp_date
        contract.strike = strike
        contract.right = otype

            #put_contract.multiplier = '100' 
        with snapshot_guote(contract) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.quotes, contract
        
    def get_stock_snapshot_guote(self, symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = 'STK'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
            #put_contract.multiplier = '100' 
        with snapshot_guote(contract) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()  
            return app.quotes, contract

    def get_spread_option_guote(self, symbol, optionLegs):
        spread_contract = Contract()
        spread_contract.symbol = symbol
        spread_contract.secType = "BAG"
        spread_contract.currency = "USD"
        spread_contract.exchange = "SMART"
        spread_contract.comboLegs = optionLegs          
            #put_contract.multiplier = '100' 
        with snapshot_guote(spread_contract) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.quotes, spread_contract

    def get_accounts_summary(self):
        with accounts_summary() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.accountSummary_df
        
    def get_accounts_values_profolio(self):
        account_list = self.get_account_list()
        with accounts_values_profolio(account_list) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.accountValue_dict, app.accountPortfolio_df        

    def get_option_geeks(self, ml):
        with option_geeks(ml) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.mlist      
        
    def get_accounts_positions(self):
        with accounts_positions() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.pos  
        
    def get_accounts_openOrders(self):
        with accounts_openOrders() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(ib_settings.SLEEP_TIME, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.open_orders  
                
    def get_account_list(self):
        with ib_app_base() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(1, app.stop)
            t. start()            
            app.run()
            t.cancel()            
            return app.accountList

    def get_next_orderId(self, count=1):
        with next_orderId() as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            t = Timer(20, app.stop)       
            t. start()            
            app.run()
            t.cancel()            
            return app.nextOrderId
        
    def place_simple_order(self, contract, order):
        with simple_order(contract, order) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                
            #t = Timer(ib_settings.SLEEP_TIME, app.stop)
            #t. start()            
            app.run()
            #t.cancel()            
            return app.status
        
    def place_bracket_order(self, contract, primary_order, take_profit_order, stop_loss_order):
        with bracket_order(contract, primary_order, take_profit_order, stop_loss_order) as app:
            app.connect(ib_settings.HostIP, self.port, self.clientID)                         
            app.run()      
            #output = {'primary_status'       : app.primary_status,
            #         'primary_orderId'      : app.primary_orderId,
            #          'take_profit_status'   : app.take_profit_status,
            #          'take_profit_orderId'  : app.take_profit_oderId,                      
            #          'app.stop_loss_status' : app.stop_loss_status,
            #          'app.stop_loss_orderId' : app.stop_loss_orderId}
            return app.primary_status, app.take_profit_status, app.stop_loss_status

    def place_ib_order(self, srow, bracket=True):
        symbol   =   srow[pscl.SYMBOL]       
        quantity =   srow[pscl.QUANTITY]
        strategy =   srow[pscl.STRATEGY]
        open_price = srow[pscl.OPEN_PRICE]
        credit =     srow[pscl.CREDIT]=='True'

        self.logger.debug("%s %s quantity %.2f price %.2f credit %s" % (symbol, strategy, quantity, open_price, str(credit)))

        srow[pscl.IB_P_ORDER_ID] = np.nan
        srow[pscl.IB_T_ORDER_ID] = np.nan
        srow[pscl.IB_S_ORDER_ID] = np.nan                
        srow[pscl.IB_CLIENT_ID]  = np.nan        
        srow[pscl.IB_P_STATUS]   = ""            
        srow[pscl.IB_T_STATUS]   = ""   
        srow[pscl.IB_S_STATUS]   = ""
        srow['ErrorCode']       = ""

        contract = Contract()
        order = Order()     
        contract.symbol = symbol
        contract.exchange = 'SMART'
        contract.currency = 'USD'  
        order.orderType = 'LMT'
        order.lmtPrice =  -1 * open_price if credit else open_price
        order.action = 'SELL' if credit else 'BUY'
        order.totalQuantity = quantity
                                    
        if strategy == st.UNPAIRED:
            contract.secType = 'STK'
            if bracket:
                if credit:
                    stopLossPrice = -1 * open_price * (1+(app_settings.RISK_MGR.stop_gain_percent / 100)) 
                    takeProfitLimitPrice = -1 * open_price  * (1-(app_settings.RISK_MGR.stop_loss_percent/100))
                else:
                    takeProfitLimitPrice = open_price * (1+(app_settings.RISK_MGR.stop_gain_percent / 100)) 
                    stopLossPrice = open_price  * (1-(app_settings.RISK_MGR.stop_loss_percent/100))
        else:
            exp_date   = srow[pscl.EXP_DATE].replace("-","")    
            legs       = srow[pscl.LEGS]       
            
            if len(legs) == 1:                
                contract.secType = 'OPT'
                contract.lastTradeDateOrContractMonth = exp_date
                contract.strike = legs[0].strike
                contract.right = 'P' if leg.otype==at.PUT else 'C'                       

                if bracket:
                    if credit:
                        stopLossPrice = -1 * open_price * (1+(app_settings.RISK_MGR.stop_gain_percent / 100))
                        takeProfitLimitPrice = -1 * open_price  * (1-(app_settings.RISK_MGR.stop_loss_percent/100))
                    else:
                        takeProfitLimitPrice = open_price * (1+(app_settings.RISK_MGR.stop_gain_percent / 100))
                        stopLossPrice = open_price  * (1-(app_settings.RISK_MGR.stop_loss_percent/100))

                    takeProfitLimitPrice = open_price * (1+(app_settings.RISK_MGR.stop_gain_percent / 100)) 
                    stopLossPrice = open_price  * (1-(app_settings.RISK_MGR.stop_loss_percent/100))
            else:
                spread = srow[pscl.SPREAD]                    
                contract.secType = "BAG"
                contract.currency = "USD"
                contract.comboLegs = []
        
                for leg in legs:
                    ratio =  leg[pcl.SCALE]
                    action = 'BUY' if 'buy' in leg[pcl.OPEN_ACTION] else 'SELL'
                    strike = leg[pcl.STRIKE]
                    otype = 'P' if leg[pcl.OTYPE]==at.PUT else 'C' 
                    leg = ComboOptionLeg(symbol, exp_date, strike, otype, ratio, action, ibClient=self)
                    if math.isnan(leg.conId):                        
                        srow['ErrorCode'] = "Get conID Failed"
                        return srow
                    
                    contract.comboLegs.append(leg)

                order.action = 'BUY'
                order.totalQuantity = quantity
                order.lmtPrice =  -1 * open_price if credit else open_price  

                if bracket:
                    if credit:
                        stopLossPrice = -1 * min(spread - 0.10, open_price * (1+(app_settings.RISK_MGR.stop_gain_percent / 100)))
                        takeProfitLimitPrice = -1 * max(0.10, open_price  * (1-(app_settings.RISK_MGR.stop_loss_percent/100)))
                    else:
                        takeProfitLimitPrice = min(spread - 0.10, open_price * (1+(app_settings.RISK_MGR.stop_gain_percent / 100)))
                        stopLossPrice = max(0.10, open_price  * (1-(app_settings.RISK_MGR.stop_loss_percent/100)))
                        
        order.lmtPrice = round(order.lmtPrice, 1)

        order.orderId = self.get_next_orderId()
        if math.isnan(order.orderId):
            self.logger.error('Unable to get next order Id')
            srow['ErrorCode'] = "Get orderID Failed"            
            return srow
                
        if bracket:
            takeProfitLimitPrice= round(takeProfitLimitPrice, 1)
            stopLossPrice = round(stopLossPrice, 1)
                
            porder, torder, sorder = BracketOrder(order.action, 
                                        quantity, 
                                        order.lmtPrice, 
                                        takeProfitLimitPrice, 
                                        stopLossPrice)
            
            #self.place_simple_order(contract, order)
            pstatus, tstatus, sstatus = self.place_bracket_order(contract, porder, torder, sorder)
            srow[pscl.IB_CLIENT_ID] = order.clientId
            srow[pscl.IB_P_ORDER_ID] = porder.orderId
            srow[pscl.IB_T_ORDER_ID] = torder.orderId
            srow[pscl.IB_S_ORDER_ID] = sorder.orderId                
            srow[pscl.IB_P_STATUS] = pstatus            
            srow[pscl.IB_T_STATUS] = tstatus   
            srow[pscl.IB_S_STATUS] = sstatus  
        else:
            status = self.place_simple_order(contract, order)
            srow[pscl.IB_CLIENT_ID] = order.clientId
            srow[pscl.IB_P_ORDER_ID] = order.orderId               
            srow[pscl.IB_P_STATUS] = status            
 
        return srow

class ComboOptionLeg(ComboLeg):
    def __init__(self, symbol, exp_date, strike, otype, ratio, action, conId=None, ibClient=None):
        super().__init__()
        self.symbol = symbol
        self.exp_date = exp_date
        self.strike = strike
        self.otype = otype
        self.ratio = ratio
        self.action = action
        #self.exchange = "SMART"     
        if ibClient != None and conId == None:   
            self.conId = ibClient.get_option_contId(symbol, exp_date, strike, otype)
        self.exchange = "SMART"     

class ib_app_base(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.logger = logging.getLogger(__name__)           

    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if self.isConnected():
            self.stop()

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        super().error(reqId, errorCode, errorString, advancedOrderRejectJson)
        if reqId < 0:
            self.logger.debug("Info: ", reqId, " ", errorCode, " ", errorString, " ", advancedOrderRejectJson )
        else:
            self.logger.error( "Error: %d %d %s %s" % (reqId, errorCode, errorString, str(advancedOrderRejectJson) ) )
        
    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.logger.debug("nextVailid. Id=", orderId)
        self.orderId = orderId
        self.start(orderId)

    def updatePortfolio(self, contract, position, marketPrice, marketValue,averageCost, unrealizedPNL, realizedPNL, accountName):
        super().updatePortfolio(contract, position, marketPrice, marketValue,averageCost, unrealizedPNL, realizedPNL, accountName)
        self.logger.debug("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
              "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:", averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)

    def updateAccountValue(self, key, val, currency, accountName):
        super().updateAccountValue(key, val, currency, accountName)
        self.logger.debug("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)

    def updateAccountTime(self, timeStamp):
        super().updateAccountTime(timeStamp)
        self.logger.debug("UpdateAccountTime. Time:", timeStamp)

    def accountDownloadEnd(self, accountName):
        super().accountDownloadEnd(accountName)
        self.logger.debug("AccountDownloadEnd. Account:", accountName)

    def updatePortfolio(
        self,
        contract: Contract,
        position: float,
        marketPrice: float,
        marketValue: float,
        averageCost: float,
        unrealizedPNL: float,
        realizedPNL: float,
        accountName: str,
    ):  
        super().updatePortfolio(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName)

        self.logger.debug('updatePortfolio position=', position, 
                ' marketPrice=', marketPrice, 
                ' marketValue=', marketValue,
                ' averageCost=', averageCost,
                ' unrealizedPNL=', unrealizedPNL,
                ' realizedPNL=', realizedPNL,
                ' accountName=', accountName)
        
        self.logger.debug("updatePortfolio contract. conId:", contract.conId,
                " symbol=", contract.symbol,
                " secType=", contract.secType,
                " lastTradeDateOrContractMonth=", contract.lastTradeDateOrContractMonth,
                " strike=", contract.strike,
                " right=", contract.right,
                " multiplier=", contract.multiplier,
                " exchange=", contract.exchange,
                " primaryExchange=", contract.primaryExchange,
                " currency=", contract.currency,
                " localSymbol=", contract.localSymbol,
                " tradingClass=", contract.tradingClass,              
                " includeExpired=", contract.includeExpired,   
                " secIdType=", contract.secIdType,   
                " secId=", contract.secId,   
                " description=", contract.description,   
                " issuerId=", contract.issuerId,   
                    # combos              
                " comboLegsDescrip=", contract.comboLegsDescrip,
                " comboLegs=", contract.comboLegs,
                " deltaNeutralContract=", contract.deltaNeutralContract)        

    def tickString(self, reqId, tickType, value):
        super().tickString(reqId, tickType, value)
        self.logger.debug("TickString. TickerId:", reqId, "Type:", TickTypeEnum.toStr(tickType), "Value:", value)

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        self.logger.debug("TickPrice. TickerId:", reqId, "tickType:", TickTypeEnum.toStr(tickType),"Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,"PastLimit:", attrib.pastLimit, end=' ')

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)   
        self.logger.debug("TickSize. TickerId:", reqId, "TickType:", TickTypeEnum.toStr(tickType), "Size: ", decimalMaxString(size))            

    def tickGeneric(self, reqId, tickType, value):
        super().tickGeneric(reqId, tickType, value)
        self.logger.debug("TickGeneric. TickerId:", reqId, "TickType:", TickTypeEnum.toStr(tickType), "Value:", floatMaxString(value))

    def marketDataType(self, reqId, marketDataType):
        super().marketDataType(reqId, marketDataType)
        self.logger.debug("marketDataType. ReqId:", reqId, "Type:", marketDataType)

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.logger.debug(accountsList)  
        self.accountList = accountsList[:-1].split(",")

    def tickSnapshotEnd(self, reqId):
        super().tickSnapshotEnd(reqId)
        self.logger.debug("tickSnapshotEnd. ReqId:", reqId)

    """ market data call back for Exchange for Physical
    tickerId -      The request's identifier.
    tickType -      The type of tick being received.
    basisPoints -   Annualized basis points, which is representative of
        the financing rate that can be directly compared to broker rates.
    formattedBasisPoints -  Annualized basis points as a formatted string
        that depicts them in percentage form.
    impliedFuture - The implied Futures price.
    holdDays -  The number of hold days until the lastTradeDate of the EFP.
    futureLastTradeDate -   The expiration date of the single stock future.
    dividendImpact - The dividend impact upon the annualized basis points
        interest rate.
    dividendsToLastTradeDate - The dividends expected until the expiration
        of the single stock future."""
        
    def tickEFP(self,reqId,tickType,basisPoints,formattedBasisPoints,totalDividends,holdDays,
                futureLastTradeDate,dividendImpact,dividendsToLastTradeDate):
        super().tickEFP(reqId,tickType,basisPoints,formattedBasisPoints,totalDividends,holdDays,
                futureLastTradeDate,dividendImpact,dividendsToLastTradeDate)
        
        self.logger.debug("tickEFP. TickerId:", reqId, 
              "TickType:", TickTypeEnum.toStr(tickType), 
              "basePosints:", floatMaxString(basisPoints),
              "formattedBasisPoints:", formattedBasisPoints,
              "totalDividends:", totalDividends,
              "holdDays:", holdDays,
              "futureLastTradeDate:", futureLastTradeDate,
              "dividendImpact:", dividendImpact,
              "dividendsToLastTradeDate:",dividendsToLastTradeDate)
    
    def tickOptionComputation(self,reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice):
        super().tickOptionComputation(reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice)
        """This function is called when the market in an option or its
        underlier moves. TWS's option model volatilities, prices, and
        deltas, along with the present value of dividends expected on that
        options underlier are received."""

        #print(self.mlist.at[reqId, 'symbol'], TickTypeEnum.toStr(tickType))
        
        self.logger.debug("tickOptionComputation. TickerId:", reqId, 
              "TickType:", TickTypeEnum.toStr(tickType), 
              "tickAttrib:", tickAttrib,
              "impliedVol:", impliedVol,
              "delta:", delta,
              "optPrice:", optPrice,
              "pvDividend:", pvDividend,
              "gamma:", gamma,
              "vega:", vega,
              "theta:",  theta,
              "undPrice:", undPrice)              
            
    def accountSummary(self, reqId, account, tag, value, currency):
        """Returns the data from the TWS Account Window Summary tab in
        response to reqAccountSummary()."""        
        super().accountSummary(reqId, account, tag, value, currency)
        self.logger.debug('accountSummary, reqId=%d account=%s tag=%s value=%s, currency=%s' % (reqId, account, tag, str(value), currency))
    
    def accountSummaryEnd(self, reqId: int):
        """This method is called once all account summary data for a
        given request are received."""
        super().accountSummaryEnd(reqId)
        self.logger.debug('accountSummaryEnd, reqId %d' % reqId)
            
    def position(self, account, contract, position, avgCost):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""
        super().position(account, contract, position, avgCost)        
        self.logger.debug("position. account:", account, " position=", position, "avgCost=", avgCost )
        self.logger.debug("contract. conId:", contract.conId,
              " symbol=", contract.symbol,
              " secType=", contract.secType,
              " lastTradeDateOrContractMonth=", contract.lastTradeDateOrContractMonth,
              " strike=", contract.strike,
              " right=", contract.right,
              " multiplier=", contract.multiplier,
              " exchange=", contract.exchange,
              " primaryExchange=", contract.primaryExchange,
              " currency=", contract.currency,
              " localSymbol=", contract.localSymbol,
              " tradingClass=", contract.tradingClass,              
              " includeExpired=", contract.includeExpired,   
              " secIdType=", contract.secIdType,   
              " secId=", contract.secId,   
              " description=", contract.description,   
              " issuerId=", contract.issuerId,   
                # combos              
              " comboLegsDescrip=", contract.comboLegsDescrip,
              " comboLegs=", contract.comboLegs,
              " deltaNeutralContract=", contract.deltaNeutralContract)

    def positionEnd(self):
        """This is called once all position data for a given request are
        received and functions as an end marker for the position() data."""
        super().positionEnd()
        self.logger.debug('positionEnd')

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""
        super().contractDetails(reqId, contractDetails)
        contract = contractDetails.contract
        self.logger.debug('contractDetails reqId=', reqId, #, ' contractDetails=', vars(contractDetails))
              "contract. conId:", contract.conId,
              " symbol=", contract.symbol,
              " secType=", contract.secType,
              " lastTradeDateOrContractMonth=", contract.lastTradeDateOrContractMonth,
              " strike=", contract.strike,
              " right=", contract.right,
              " multiplier=", contract.multiplier,
              " exchange=", contract.exchange,
              " primaryExchange=", contract.primaryExchange,
              " currency=", contract.currency,
              " localSymbol=", contract.localSymbol,
              " tradingClass=", contract.tradingClass,              
              " includeExpired=", contract.includeExpired,   
              " secIdType=", contract.secIdType,   
              " secId=", contract.secId,   
              " description=", contract.description,   
              " issuerId=", contract.issuerId,   
                # combos              
              " comboLegsDescrip=", contract.comboLegsDescrip,
              " comboLegs=", contract.comboLegs,
              " deltaNeutralContract=", contract.deltaNeutralContract)
             
        self.logger.debug('minTick =', contractDetails.minTick,
              #'validExchanges', contractDetails.validExchanges,
              #'orderTypes', contractDetails.orderTypes,
              'priceMagnifier', contractDetails.priceMagnifier,
              'underConId', contractDetails.underConId,
              'longName =', contractDetails.longName,
              'contractMonth', contractDetails.contractMonth,
              'industry = ', contractDetails.industry,
              'category = ', contractDetails.category,
              'subcategory = ', contractDetails.subcategory,
              'timeZoneId = ', contractDetails.timeZoneId,
              #'tradingHours =', contractDetails.tradingHours,
              #'liquidHours = ', contractDetails.liquidHours,
              'evRule = ', contractDetails.evRule,
              'evMultiplier = ', contractDetails.evMultiplier,
              'aggGroup = ', contractDetails.aggGroup,
              'underSymbol = ', contractDetails.underSymbol,
              'underSecType = ', contractDetails.underSecType,
              #'marketRuleIds = ', contractDetails.marketRuleIds,
              'secIdList = ', contractDetails.secIdList,
              'realExpirationDate = ', contractDetails.realExpirationDate,
              'lastTradeTime = ', contractDetails.lastTradeTime,
              'stockType = ', contractDetails.stockType,
              'minSize = ', contractDetails.minSize,
              'sizeIncrement = ', contractDetails.sizeIncrement,
              'suggestedSizeIncrement = ', contractDetails.suggestedSizeIncrement)       

    def bondContractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().bondContractDetails(reqId, contractDetails)
        """This function is called when reqContractDetails function
        has been called for bonds."""
        self.logger.debug('bondContractDetails reqId=', reqId, ' contractDetails=', contractDetails)

    def contractDetailsEnd(self, reqId: int):
        super().contractDetailsEnd(reqId)
        """This function is called once all contract details for a given
        request are received. This helps to define the end of an option
        chain."""
        self.logger.debug('contractDetailsEnd reqId=', reqId)

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        super().orderStatus(orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        self.logger.debug('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)

    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)
        self.logger.debug('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

        self.logger.debug("Order. PermId:", intMaxString(order.permId), 
              "ClientId:", intMaxString(order.clientId), 
              "OrderId:", intMaxString(orderId), 
              "Account:", order.account,
              "Action:", order.action, 
              "OrderType:", order.orderType)
        
        self.logger.debug("Contract, Symbol:", contract.symbol, 
              "SecType:", contract.secType,
              "Exchange:", contract.exchange, 
              "TotalQty:", decimalMaxString(order.totalQuantity), 
              "CashQty:", floatMaxString(order.cashQty), 
              "LmtPrice:", floatMaxString(order.lmtPrice), 
              "AuxPrice:", floatMaxString(order.auxPrice), 
              "MinTradeQty:", intMaxString(order.minTradeQty), 
              "MinCompeteSize:", intMaxString(order.minCompeteSize),
              "competeAgainstBestOffset:", "UpToMid" if order.competeAgainstBestOffset == COMPETE_AGAINST_BEST_OFFSET_UP_TO_MID else floatMaxString(order.competeAgainstBestOffset),
              "MidOffsetAtWhole:", floatMaxString(order.midOffsetAtWhole),"MidOffsetAtHalf:" ,floatMaxString(order.midOffsetAtHalf),
              "FAGroup:", order.faGroup, 
              "FAMethod:", order.faMethod)
   
        self.logger.debug('orderState.status=', orderState.status,
                'initMarginBefore=', orderState.initMarginBefore,
                'maintMarginBefore=',orderState.maintMarginBefore,
                'equityWithLoanBefore=', orderState.equityWithLoanBefore,
                'initMarginChange=', orderState.initMarginChange,
                'maintMarginChange=', orderState.maintMarginChange, 
                'equityWithLoanChange=',orderState.equityWithLoanChange, 
                'initMarginAfter=',orderState.initMarginAfter,
                'maintMarginAfter=', orderState.maintMarginAfter,
                'equityWithLoanAfter=', orderState.equityWithLoanAfter,
                'commission=', orderState.commission,
                'minCommission=', orderState.minCommission,
                'maxCommission=',orderState.maxCommission, 
                'commissionCurrency=', orderState.commissionCurrency,
                'warningText=', orderState.warningText,
                'completedTime=', orderState.completedTime,
                'completedStatus=', orderState.completedStatus)

    def openOrderEnd(self):
        super().openOrderEnd()        
        """This is called at the end of a given request for open orders."""
        self.logger.debug('openOrderEnd')

    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        super().execDetails(reqId, contract, execution)
        self.logger.debug('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

    def completedOrder(self, contract: Contract, order: Order, orderState: OrderState):
        """This function is called to feed in completed orders.
        contract: Contract - The Contract class attributes describe the contract.
        order: Order - The Order class gives the details of the completed order.
        orderState: OrderState - The orderState class includes completed order status details.
        """        
        super().completedOrder(contract, order, orderState)
        self.logger.debug("Contract, Symbol:", contract.symbol, 
              "SecType:", contract.secType,
              "Exchange:", contract.exchange, 
              "TotalQty:", decimalMaxString(order.totalQuantity), 
              "CashQty:", floatMaxString(order.cashQty), 
              "LmtPrice:", floatMaxString(order.lmtPrice), 
              "AuxPrice:", floatMaxString(order.auxPrice), 
              "MinTradeQty:", intMaxString(order.minTradeQty), 
              "MinCompeteSize:", intMaxString(order.minCompeteSize),
              "competeAgainstBestOffset:", "UpToMid" if order.competeAgainstBestOffset == COMPETE_AGAINST_BEST_OFFSET_UP_TO_MID else floatMaxString(order.competeAgainstBestOffset),
              "MidOffsetAtWhole:", floatMaxString(order.midOffsetAtWhole),"MidOffsetAtHalf:" ,floatMaxString(order.midOffsetAtHalf),
              "FAGroup:", order.faGroup, 
              "FAMethod:", order.faMethod)
   
        self.logger.debug('orderState.status=', orderState.status,
                'initMarginBefore=', orderState.initMarginBefore,
                'maintMarginBefore=',orderState.maintMarginBefore,
                'equityWithLoanBefore=', orderState.equityWithLoanBefore,
                'initMarginChange=', orderState.initMarginChange,
                'maintMarginChange=', orderState.maintMarginChange, 
                'equityWithLoanChange=',orderState.equityWithLoanChange, 
                'initMarginAfter=',orderState.initMarginAfter,
                'maintMarginAfter=', orderState.maintMarginAfter,
                'equityWithLoanAfter=', orderState.equityWithLoanAfter,
                'commission=', orderState.commission,
                'minCommission=', orderState.minCommission,
                'maxCommission=',orderState.maxCommission, 
                'commissionCurrency=', orderState.commissionCurrency,
                'warningText=', orderState.warningText,
                'completedTime=', orderState.completedTime,
                'completedStatus=', orderState.completedStatus)        

    def completedOrdersEnd(self):
        super().completedOrdersEnd()
        self.logger.debug('completeOrderEnd')
        """This is called at the end of a given request for completed orders."""

    def start(self, reqId):
        return

    def stop(self):
        self.disconnect()
class option_geeks(ib_app_base):
    
    def __init__(self, mlist):
        super().__init__()     
        self.mlist = mlist
        self.tickSnapshotEndCount = 0

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        index = reqId - self.reqIdBase
        self.mlist.at[index, TickTypeEnum.toStr(tickType)] = price
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            self.logger.debug("PreOpen:", attrib.preOpen)

    def tickOptionComputation(self,reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice):
        super().tickOptionComputation(reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice)
        """This function is called when the market in an option or its
        underlier moves. TWS's option model volatilities, prices, and
        deltas, along with the present value of dividends expected on that
        options underlier are received."""

        index = reqId - self.reqIdBase

        #print(self.mlist.at[reqId, 'symbol'], TickTypeEnum.toStr(tickType))
        
        if tickType == TickTypeEnum.DELAYED_MODEL_OPTION or tickType == TickTypeEnum.MODEL_OPTION:
            self.mlist.at[index, 'impliedVol'] = impliedVol               
            self.mlist.at[index, 'delta'] = delta
            self.mlist.at[index, 'gamma'] = gamma
            self.mlist.at[index, 'vega'] = vega
            self.mlist.at[index, 'theta'] = theta  
            self.mlist.at[index, "tickAttrib"] = tickAttrib
            self.mlist.at[index, "optPrice"] = optPrice,
            self.mlist.at[index, "pvDividend:"] = pvDividend
            self.mlist.at[index, "undPrice"] = undPrice                 
                
    def tickSnapshotEnd(self, reqId):
        super().tickSnapshotEnd(reqId)
        self.tickSnapshotEndCount += 1
        if self.tickSnapshotEndCount >= self.reqCount:
            self.stop()

    def start(self, reqId):
        # Account number can be omitted when using reqAccountUpdates with single account structure
        #self.reqAccountUpdates(True, "U11921459")
        self.reqIdBase = reqId

        self.reqMarketDataType(3)    
        self.reqCount = 0
        il = list(self.mlist.index)
        for i in il:  
            symbol = self.mlist.at[i, 'symbol']
            exp_date = self.mlist.at[i, 'exp_date']
            strike = self.mlist.at[i, 'strike']
            if isinstance(exp_date, str) == False:
                self.logger.debug('nan expdate')
                continue
            else:
                self.logger.debug(symbol, exp_date, strike)                   
            contract = Contract()
            contract.symbol = symbol
            contract.secType = 'OPT'
            contract.exchange = 'SMART'
            contract.currency = 'USD'
            contract.lastTradeDateOrContractMonth = exp_date
            contract.strike = strike
            contract.right = 'C'
            contract.multiplier = '100'          
            #self.qualifyContracts(contract) 
            self.reqMktData(i+self.reqIdBase, contract, '', True, False, [])
            self.reqCount += 1
            import time
            time.sleep(1)
class accounts_summary(ib_app_base):
    def __init__(self, user=None):
        super().__init__()
        #EClient.__init__(self, self)
        self.user = user

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        self.accountSummary_df = pd.DataFrame({'Account': self.accountList})
        self.accountSummary_df.set_index(['Account'], inplace=True)  
                        
    def accountSummary(self, reqId, account, tag, value, currency):
        """Returns the data from the TWS Account Window Summary tab in
        response to reqAccountSummary()."""        
        super().accountSummary(reqId, account, tag, value, currency)       
        self.accountSummary_df.at[account, tag] = value

    def accountSummaryEnd(self, reqId: int):
        """This method is called once all account summary data for a
        given request are received."""
        super().accountSummaryEnd(reqId)
        self.cancelAccountSummary(reqId)        
        self.stop()

    def start(self, reqId):
        self.reqAccountSummary(reqId, "All", AccountSummaryTags.AllTags)               
class accounts_values_profolio(ib_app_base):
    def __init__(self, account_list, user=None):
        super().__init__()
        #EClient.__init__(self, self)
        self.user = user
        self.accountList = account_list
        self.account_index = 0
                              
    def updateAccountValue(self, key, val, currency, accountName):
        super().updateAccountValue(key, val, currency, accountName)

        if accountName not in self.accountValue_dict.keys():
            self.accountValue_dict[accountName] = {}

        self.accountValue_dict[accountName][key] = val

    def accountDownloadEnd(self, accountName):
        super().accountDownloadEnd(accountName)
         
        if self.account_index+1 >= len(self.accountList):
             self.stop()
        else:    
            self.reqAccountUpdates(False, self.accountList[self.account_index])    
            self.account_index += 1              
            self.accountValue_dict[self.accountList[self.account_index]]={}          
            self.reqAccountUpdates(True, self.accountList[self.account_index])  
        
    def updateAccountTime(self, timeStamp):
        super().updateAccountTime(timeStamp)
        
        for key in self.accountValue_dict:        
            self.accountValue_dict[key]['timeStamp'] = timeStamp     
                
        self.accountPortfolio_df['timeStamp'] = timeStamp          

    def updatePortfolio(self,
            contract: Contract,
            position: float,
            marketPrice: float,
            marketValue: float,
            averageCost: float,
            unrealizedPNL: float,
            realizedPNL: float,
            accountName: str):
        
        index = self.accountPortfolio_df.shape[0]        
        self.accountPortfolio_df.at[index, 'position'] = float(position)       
        self.accountPortfolio_df.at[index, 'marketPrice'] =  marketPrice      
        self.accountPortfolio_df.at[index, 'marketValue'] = marketValue      
        self.accountPortfolio_df.at[index, 'averageCost'] = averageCost      
        self.accountPortfolio_df.at[index, 'unrealizedPNL'] = unrealizedPNL          
        self.accountPortfolio_df.at[index, 'realizedPNL'] = realizedPNL   
        self.accountPortfolio_df.at[index, 'accountName'] = accountName          
        
        self.accountPortfolio_df.at[index, 'symbol'] = contract.symbol 
        self.accountPortfolio_df.at[index, 'secType'] = contract.secType         
        
        if contract.secType == 'OPT':
            self.accountPortfolio_df.at[index, 'exp_date'] = contract.lastTradeDateOrContractMonth
            self.accountPortfolio_df.at[index, 'strike'] = contract.strike
            self.accountPortfolio_df.at[index, 'right'] = contract.right          
            self.accountPortfolio_df.at[index, 'comboLegsDescrip'] = contract.comboLegsDescrip            
            self.accountPortfolio_df.at[index, 'comboLegs'] = str(contract.comboLegs)  

    def start(self, reqId):
        if len(self.accountList) == 0:
            self.logger.error('No account found')
            return
        
        self.accountValue_dict = {}
        self.accountPortfolio_df = pd.DataFrame()       
        self.reqAccountUpdates(True, self.accountList[self.account_index])             
class accounts_positions(ib_app_base):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.pos = pd.DataFrame()        
                        
    def position(self, account, contract, position, avgCost):
        """This event returns real-time positions for all accounts in
        response to the reqPositions() method."""
        super().position(account, contract, position, avgCost)        
        index = self.pos.shape[0]
        self.pos.at[index, 'account'] = account     
        self.pos.at[index, 'symbol'] = contract.symbol 
        self.pos.at[index, 'secType'] = contract.secType         
        self.pos.at[index, 'position'] = float(position)
        self.pos.at[index, 'avgCost'] =  float(avgCost) 
        
        if contract.secType == 'OPT':
            self.pos.at[index, 'exp_date'] = contract.lastTradeDateOrContractMonth
            self.pos.at[index, 'strike'] = contract.strike
            self.pos.at[index, 'right'] = contract.right    
            self.pos.at[index, 'comboLegsDescrip'] = contract.comboLegsDescrip
            self.pos.at[index, 'comboLegs'] = str(contract.comboLegs)           

    def positionEnd(self):
        """This is called once all position data for a given request are
        received and functions as an end marker for the position() data."""
        super().positionEnd()
        self.cancelPositions()        
        self.stop()

    def start(self, reqId):             
        self.reqPositions()
class accounts_openOrders(ib_app_base):

    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.open_orders = pd.DataFrame()        
                        
    def openOrder(self, orderId, contract, order, orderState):
        super().openOrder(orderId, contract, order, orderState)

        index = self.open_orders.shape[0]
        self.open_orders.at[index, 'account']       = order.account    
        self.open_orders.at[index, 'orderId']       = orderId
        self.open_orders.at[index, 'orderType']     = order.orderType       
        self.open_orders.at[index, 'symbol']        = contract.symbol 
        self.open_orders.at[index, 'secType']       = contract.secType         
        self.open_orders.at[index, 'action']        = order.action
        self.open_orders.at[index, 'totalQuantity'] = order.totalQuantity
        self.open_orders.at[index, 'LmtPrice']      = float(order.lmtPrice)
        self.open_orders.at[index, 'status']        = orderState.status

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        super().orderStatus(orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        index = self.open_orders.shape[0]-1
        if orderId != self.open_orders.at[index, 'orderId']:
            self.logger.error('orderId %s != %s' % (orderId, self.open_orders.at[index, 'orderId']))
        else:
            self.open_orders.at[index, 'filled'] = float(filled)
            self.open_orders.at[index, 'remaining'] = float(remaining)
            self.open_orders.at[index, 'parentId'] = parentId
            self.open_orders.at[index, 'lastFillPrice'] = lastFillPrice
            self.open_orders.at[index, 'avgFullPrice'] = avgFullPrice
            self.open_orders.at[index, 'lastFillPrice'] = lastFillPrice
            self.open_orders.at[index, 'clientId'] = clientId
            self.open_orders.at[index, 'whyHeld'] = whyHeld
            self.open_orders.at[index, 'mktCapPrice'] = mktCapPrice

    def openOrderEnd(self):
        super().openOrderEnd()        
        """This is called at the end of a given request for open orders."""
        self.stop()


    def start(self, reqId):             
        self.reqAllOpenOrders()
class contract_details(ib_app_base):
    def __init__(self, contract):
        super().__init__()    
        self.contract = contract
        self.conId = np.nan
        self.errorCode = np.nan

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
        super().error(reqId, errorCode, errorString, advancedOrderRejectJson)
        if reqId > 0:
             self.errorCode = errorCode
             self.stop()

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails )
        """Receives the full contract's definitions. This method will return all
        contracts matching the requested via EEClientSocket::reqContractDetails.
        For example, one can obtain the whole option chain with it."""
        self.contractDetails = contractDetails
        self.conId = contractDetails.contract.conId


    def contractDetailsEnd(self, reqId: int):
        super().contractDetailsEnd(reqId)
        self.stop()
        """This function is called once all contract details for a given
        request are received. This helps to define the end of an option
        chain."""
        
    def start(self, reqId):             
        self.reqContractDetails(reqId, self.contract)
class snapshot_guote(ib_app_base):
    
    def __init__(self, contract):
        super().__init__()     
        self.contract = contract
        self.quotes = {}

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        self.quotes[TickTypeEnum.toStr(tickType)] = price
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            self.quotes["PreOpen"] = attrib.preOpen

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        self.quotes[TickTypeEnum.toStr(tickType)] = size        

    def tickGeneric(self, reqId, tickType, value):
        super().tickGeneric(reqId, tickType, value)
        self.quotes[TickTypeEnum.toStr(tickType)] = value    

    def tickSnapshotEnd(self, reqId):
        super().tickSnapshotEnd(reqId)
        self.stop()

    def tickOptionComputation(self,reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice):
        super().tickOptionComputation(reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice)
        """This function is called when the market in an option or its
        underlier moves. TWS's option model volatilities, prices, and
        deltas, along with the present value of dividends expected on that
        options underlier are received."""   
        tickTypeStr = TickTypeEnum.toStr(tickType)
        self.quotes[tickTypeStr] = {}
        self.quotes[tickTypeStr]['impliedVol'] = impliedVol               
        self.quotes[tickTypeStr]['delta'] = delta
        self.quotes[tickTypeStr]['gamma'] = gamma
        self.quotes[tickTypeStr]['vega'] = vega
        self.quotes[tickTypeStr]['theta'] = theta  
        self.quotes[tickTypeStr]["tickAttrib"] = tickAttrib
        self.quotes[tickTypeStr]["optPrice"] = optPrice,
        self.quotes[tickTypeStr]["pvDividend:"] = pvDividend
        self.quotes[tickTypeStr]["undPrice"] = undPrice                 
        self.quotes[tickTypeStr]["optPrice"] = optPrice            
        self.quotes[tickTypeStr]["pvDividend"] = pvDividend  

    def start(self, reqId):
        self.reqMarketDataType(ib_settings.IBConfig.marketDataType)    
        self.reqMktData(reqId, self.contract, '', True, False, [])
class simple_order(ib_app_base):
    def __init__(self, contract:Contract, order:Order):
        super().__init__()
        self.contract = contract
        self.order = order
        self.status = None

    def nextValidId(self, orderId):
        #super().nextValidId(orderId)
        self.order.orderId = orderId        
        self.placeOrder(orderId, self.contract, self.order) 

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        super().orderStatus(orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        self.logger.debug('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
        if orderId == self.order.orderId:
            self.status = status 
            self.filled = filled
            self.remaining = remaining
            self.avgFullPrice = avgFullPrice
            self.permId = permId
            self.parentId = parentId
            self.lastFillPrice = lastFillPrice
            self.clientId = clientId
            self.whyHeld = whyHeld
            self.mktCapPrice = mktCapPrice
            self.stop()                       

    def execDetails(self, orderId, contract, execution):
        super.execDetails(orderId, contract, execution)
        self.logger.debug('Order Executed: ', orderId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)
        if orderId == self.order.orderId:
            self.stop()                    
class bracket_order(ib_app_base):
    def __init__(self, contract:Contract, primary_order:Order, take_profit_order:Order, stop_loss_order:Order):
        super().__init__()
        self.contract =  contract
        self.primary_order = primary_order
        self.take_profit_order = take_profit_order
        self.stop_loss_order = stop_loss_order
        self.primary_submitted = False
        self.take_profit_submitted = False
        self.stop_loss_submitted = False
        self.primary_orderId = -1
        self.take_profit_orderId = -1
        self.stop_loss_orderId = -1
        self.primary_status = None
        self.take_profit_status = None
        self.stop_loss_status = None        

    def nextValidId(self, orderId):
        if self.primary_submitted == False:
            self.primary_order.orderId = orderId 
            self.take_profit_order.parentId = orderId
            self.stop_loss_order.parentId = orderId       
            self.placeOrder(orderId, self.contract, self.primary_order) 
            self.primary_submitted = True
            self.primary_orderId = orderId
            self.reqIds(1)
        elif self.take_profit_submitted == False:
            self.take_profit_order.orderId = orderId   
            self.placeOrder(orderId, self.contract, self.take_profit_order) 
            self.take_profit_submitted = True
            self.take_profit_orderId = orderId
            self.reqIds(1)            
        elif self.stop_loss_submitted == False:
            self.stop_loss_order.orderId = orderId   
            self.placeOrder(orderId, self.contract, self.stop_loss_order) 
            self.stop_loss_submitted = True
            self.stop_loss_orderId = orderId

    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        super().orderStatus(orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        self.logger.debug('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
        if orderId == self.primary_orderId:
            self.primary_status = status 
            self.primary_filled = filled
            self.primary_remaining = remaining
            self.primary_avgFullPrice = avgFullPrice
            self.primary_permId = permId
            self.primary_parentId = parentId
            self.primary_lastFillPrice = lastFillPrice
            self.primary_clientId = clientId
            self.primary_whyHeld = whyHeld
            self.primary_mktCapPrice = mktCapPrice
        elif orderId == self.take_profit_orderId:
            self.take_profit_status = status 
            self.take_profit_filled = filled
            self.take_profit_remaining = remaining
            self.take_profit_avgFullPrice = avgFullPrice
            self.take_profit_permId = permId
            self.take_profit_parentId = parentId
            self.take_profit_lastFillPrice = lastFillPrice
            self.take_profit_clientId = clientId
            self.take_profit_whyHeld = whyHeld
            self.take_profit_mktCapPrice = mktCapPrice
        elif orderId == self.stop_loss_orderId:
            self.stop_loss_status = status 
            self.stop_loss_filled = filled
            self.stop_loss_remaining = remaining
            self.stop_loss_avgFullPrice = avgFullPrice
            self.stop_loss_permId = permId
            self.stop_loss_parentId = parentId
            self.stop_loss_lastFillPrice = lastFillPrice
            self.stop_loss_clientId = clientId
            self.stop_loss_whyHeld = whyHeld
            self.stop_loss_mktCapPrice = mktCapPrice                    

        if self.primary_status != None and self.take_profit_status != None and self.stop_loss_status != None:
            self.stop()  

    def execDetails(self, orderId, contract, execution):
        super().execDetails(orderId, contract, execution)
        self.logger.debug('Order Executed: ', orderId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)               

class  next_orderId(ib_app_base):
    def __init__(self):
        super().__init__()       

    def nextValidId(self, orderId):
        self.nextOrderId = orderId
        self.stop()

def build_OTM_option_requests(ml, DTE_list, max_strike_ratio=0.50):
    output = pd.DataFrame()    
    il = list(ml.index)
    #print(il)
    for i in il:
        symbol = ml.at[i, 'symbol']    
        for DTE in DTE_list:
            from  option_trader.utils.data_getter import get_option_chain            
            chain = get_option_chain(symbol, at.CALL, max_strike_ratio=max_strike_ratio, min_days_to_expire=DTE-3, max_days_to_expire=DTE+3)    
            if chain.shape[0] == 0:
                continue
            if chain.shape[0] > 1:
                target = chain.shape[0]//2
            else:
                target = 0
            #print(i, symbol, chain.shape[0], target, output.shape[0])
            df = (chain.iloc[target][['stock_price', 'strike', 'exp_date', 'days to expire', 'delta', 'gamma', 'vega', 'theta']])   
            
            ml.at[i, 'stock_price'] = df.stock_price
            ml.at[i, 'strike'] = df.strike
            ml.at[i, 'exp_date'] = df.exp_date.replace('-','')
            ml.at[i, 'days to expire'] = df['days to expire']
            ml.at[i, 'yahoo delta'] = df.delta
            ml.at[i, 'yahoo gamma'] = df.gamma
            ml.at[i, 'yahoo vega'] = df.vega    
            ml.at[i, 'yahoo theta'] = df.theta        
            output = pd.concat([output, ml.loc[i:i:1]])    
    output.reset_index(drop=True, inplace=True)

    return output

def BracketOrder(action:str, 
                 quantity: float, #Decimal, 
                 limitPrice:float, 
                 takeProfitLimitPrice:float, 
                 stopLossPrice:float):

    #This will be our main or "parent" order
    parent = Order()
    parent.action = action
    parent.orderType = "LMT"
    parent.totalQuantity = quantity
    parent.lmtPrice = limitPrice
    #The parent and children orders will need this attribute set to False to prevent accidental executions.
    #The LAST CHILD will have it set to True, 
    parent.transmit = False

    takeProfit = Order()
    takeProfit.action = "SELL" if action == "BUY" else "BUY"
    takeProfit.orderType = "LMT"
    takeProfit.totalQuantity = quantity
    takeProfit.lmtPrice = takeProfitLimitPrice
    takeProfit.transmit = False

    stopLoss = Order()
    stopLoss.action = "SELL" if action == "BUY" else "BUY"
    stopLoss.orderType = "STP"
    #Stop trigger price
    stopLoss.auxPrice = stopLossPrice
    stopLoss.totalQuantity = quantity
    stopLoss.transmit = True

    return parent, takeProfit, stopLoss

if __name__ == '__main__':


    stock_contract = Contract()
    stock_contract.symbol = 'AAPL'
    stock_contract.secType = 'STK'
    stock_contract.exchange = 'SMART'
    stock_contract.currency = 'USD'

    stock_order = Order()
    stock_order.action = 'BUY'
    stock_order.totalQuantity = 100
    stock_order.orderType = 'LMT'
    stock_order.lmtPrice = '190'       

    stock_primary, stock_take_profit, stock_stop_loss = BracketOrder('BUY', 10, 190, 200, 170)

    put_contract = Contract()
    put_contract.symbol = 'NVDA'
    put_contract.secType = 'OPT'
    put_contract.exchange = 'SMART'
    #put_contract.currency = 'USD'
    put_contract.lastTradeDateOrContractMonth = '20231229'
    put_contract.strike = 400
    put_contract.right = 'P'
#put_contract.multiplier = '100'          

    put_order = Order()
    put_order.action = 'BUY'
    put_order.totalQuantity = 100
    put_order.orderType = 'LMT'
    put_order.lmtPrice = '2.0'

#self.placeOrder(reqId, stock_contract, put_order) 

    spread_contract = Contract()
    spread_contract.symbol = "NVDA"
    spread_contract.secType = "BAG"
    spread_contract.currency = "USD"
    spread_contract.exchange = "SMART"

    leg1 = ComboLeg()
    leg1.conId = 664952285 #DBK Jun21'24 2 CALL @EUREX
    leg1.ratio = 1
    leg1.action = "BUY"
    leg1.exchange = "SMART"
         
    leg2 = ComboLeg()
    leg2.conId = 670866725 #DBK Dec15'23 2 CALL @EUREX
    leg2.ratio = 1       
    leg2.action = "SELL"
    leg2.exchange = "SMART"
 
    spread_contract.comboLegs = []
    spread_contract.comboLegs.append(leg1)
    spread_contract.comboLegs.append(leg2)

    spread_order = Order()
    spread_order.action = 'BUY'
    spread_order.totalQuantity = 100
    spread_order.orderType = 'LMT'
    spread_order.lmtPrice = '-2.5'

    from option_trader.admin.site import site
    from datetime import time, date, datetime, timedelta
    from pytz import timezone
    from option_trader.consts import strategy as st
    from option_trader.consts import asset as at
    from option_trader.utils.data_getter_ib import ComboOptionLeg
    import json
    from ibapi.contract import Contract, ComboLeg, ContractDetails
    from ibapi.order import *

    site_name = 'mysite'
    mysite = site(site_name)
    ib_user = mysite.get_user('ib_user')
    DU8147717i_acct = ib_user.get_account('DU8147717')
    ps_df = DU8147717i_acct.get_position_summary()

    with IBClient(TWS=True, Live=False) as ibClient:
        #ibClient.reqGlobalCancel()  
        print(ibClient.get_option_contId('NVDA', '20240105', 495, 'P'))
        #print(ibClient.get_option_snapshot_guote('NVDA', '20231229', 495, 'P'))
        #print(ibClient.get_stock_snapshot_guote('NVDA'))
        #print(ibClient.get_next_orderId())
        #print(ibClient.place_simple_order(stock_contract, stock_order))
        #print(ibClient.place_bracket_order(stock_contract, stock_primary, stock_take_profit, stock_stop_loss))
        # for i, row in ps_df.head(10).iterrows():
        #    x = ibClient.place_one_order(row)
        #    print(x['ib_p_status'], x['ib_t_status'], x['ib_s_status'])
        #print(ibClient.get_accounts_openOrders())
        #legs = []
        #legs.append(ComboOptionLeg('NVDA', '20240105', 495, 'P', 1, 'BUY',  ibClient=ibClient))
        #legs.append(ComboOptionLeg('NVDA', '20240105', 500, 'P', 1, 'SELL', ibClient=ibClient))  
        #legs.append(ComboOptionLeg('NVDA', '20240105', 500, 'C', 1, 'SELL', ibClient=ibClient))
        #legs.append(ComboOptionLeg('NVDA', '20240105', 505, 'C', 1, 'BUY',  ibClient=ibClient))               
        #quote_dict, contract = ibClient.get_spread_option_guote('NVDA', legs)
        #orderId = ibClient.get_next_orderId()        
        #print('orderId=', orderId)
        #lmtPrice = quote_dict['DELAYED_BID']
        #bracketOrder = BracketOrder(orderId, 'BUY', 5, lmtPrice, lmtPrice * -0.05, lmtPrice * -1.5)
        #order = Order()
        #order.action = 'BUY'
        #order.totalQuantity = 10
        #order.orderType = 'LMT'
        #order.lmtPrice = quote_dict['DELAYED_BID']
  
        #print(ibClient.place_simple_order(contract, order))
        #print(ibClient.go_place_order(contract, bracketOrder))
        #print(ibClient.go_place_order(contract, [order]))        
        #print(ibClient.get_accounts_summary())
        #print(ibClient.get_accounts_values_profolio())
        #print(ibClient.get_accounts_positions())
        #print(ibClient.get_account_list())
        '''
        from option_trader.admin.site import site
        mysite = site('mysite')        
        ml = mysite.get_monitor_df()

        total_size = ml.shape[0]
        chunk_size = 5
        chunk_number = total_size // chunk_size
        chunks = np.array_split(ml, chunk_number)

        output = pd.DataFrame()
        for i, chunk in enumerate(chunks):
            print(f"Chunk {i+1}:")
            print(chunk['symbol'].unique())      
            mlist = ibClient.get_option_geeks(build_OTM_option_requests(chunk, [30]))      
            output = pd.concat([output, mlist])
        '''
        