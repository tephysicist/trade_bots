from pybit.unified_trading import HTTP
import os

API_KEY = ''
API_SECRET = ''

client = HTTP(api_key=API_KEY, api_secret=API_SECRET)

def place_spot_order(symbol: str,
                     side: str,
                     order_type: str,
                     qty: str = None,
                     quote_qty: str = None,
                     price: str = None,
                     time_in_force: str = "GTC"):
    """
    Универсальная функция для создания Spot-ордера.
    
    - Market:
        qty      -> указываем количество в базовой валюте (например, 0.01 BTC)
        quote_qty -> указываем сумму в котируемой валюте (например, 100 USDT)
    - Limit:
        qty + price обязательны
    """

    params = {
        "category": "spot",
        "symbol": symbol,
        "side": side,
        "orderType": order_type,
        "timeInForce": time_in_force
    }

    if order_type == "Market":
        if quote_qty:
            params["orderQty"] = quote_qty
            params["marketUnit"] = "quote"
        elif qty:
            params["qty"] = qty
        else:
            raise ValueError("Для Market ордера укажите qty или quote_qty")
    elif order_type == "Limit":
        if not qty or not price:
            raise ValueError("Для Limit ордера нужны qty и price")
        params["qty"] = qty
        params["price"] = price
    else:
        raise ValueError("order_type должен быть 'Market' или 'Limit'")

    return client.place_order(**params)

print(client.get_open_orders(
    category="spot",
    symbol="USDCUSDT",
    openOnly=0,
    limit=10,
))

print()
print(client.get_wallet_balance(
    accountType="UNIFIED",
    coin="USDT",
))

print()
print(client.get_fee_rates(
    symbol="USDCUSDT",
))

if __name__ == "__main__":
    # Пример: Limit ордер — купить
    #res1 = place_spot_order(symbol="USDCUSDT", side="Buy", order_type="Limit", qty="100", price="0.1")
    #print("Limit order:", res1)
    pass
'''
    # Пример: Market ордер — купить BTC на 100 USDT
    res2 = place_spot_order(symbol="BTCUSDT", side="Buy", order_type="Market", quote_qty="100")
    print("Market order (quote):", res2)

    # Пример: Market ордер — купить 0.01 BTC
    res3 = place_spot_order(symbol="BTCUSDT", side="Buy", order_type="Market", qty="0.01")
    print("Market order (qty):", res3)
'''

'''
Result after order creation:
Limit order: {'retCode': 0, 'retMsg': 'OK', 'result': {'orderId': '2049814637196872193', 'orderLinkId': '2049814637196872194'}, 'retExtInfo': {}, 'time': 1759092946611}

Result after getting open orders:
{'retCode': 0, 'retMsg': 'OK', 'result': {'nextPageCursor': '2049814637196872193%3A1759092946611%2C2049814637196872193%3A1759092946611', 'category': 'spot', 'list': [{'symbol': 'USDCUSDT', 'orderType': 'Limit', 'orderLinkId': '2049814637196872194', 'slLimitPrice': '0', 'orderId': '2049814637196872193', 'cancelType': 'UNKNOWN', 'avgPrice': '0.0000', 'stopOrderType': '', 'lastPriceOnCreated': '', 'orderStatus': 'New', 'takeProfit': '0', 'cumExecValue': '0.000000', 'smpType': 'None', 'triggerDirection': 0, 'blockTradeId': '', 'cumFeeDetail': {}, 'isLeverage': '0', 'rejectReason': 'EC_NoError', 'price': '0.1000', 'orderIv': '', 'createdTime': '1759092946611', 'tpTriggerBy': '', 'positionIdx': 0, 'trailingPercentage': '0', 'timeInForce': 'GTC', 'leavesValue': '10.000000', 'basePrice': '0.9995', 'updatedTime': '1759092946613', 'side': 'Buy', 'smpGroup': 0, 'triggerPrice': '0.0000', 'tpLimitPrice': '0', 'trailingValue': '0', 'cumExecFee': '0', 'leavesQty': '100', 'slTriggerBy': '', 'closeOnTrigger': False, 'placeType': '', 'cumExecQty': '0', 'reduceOnly': False, 'activationPrice': '0', 'qty': '100.00', 'stopLoss': '0', 'marketUnit': '', 'smpOrderId': '', 'triggerBy': ''}]}, 'retExtInfo': {}, 'time': 1759092954833}

{'retCode': 0, 'retMsg': 'OK', 'result': {'list': [{'accountIMRate': '', 'totalMaintenanceMarginByMp': '', 'totalInitialMargin': '', 'accountType': 'UNIFIED', 'accountMMRate': '', 'accountMMRateByMp': '', 'accountIMRateByMp': '', 'totalInitialMarginByMp': '', 'totalMaintenanceMargin': '', 'totalEquity': '1726.0737782', 'totalMarginBalance': '', 'totalAvailableBalance': '', 'totalPerpUPL': '0', 'totalWalletBalance': '1726.0737782', 'accountLTV': '', 'coin': [{'spotBorrow': '0', 'availableToBorrow': '', 'bonus': '0', 'accruedInterest': '0', 'availableToWithdraw': '', 'totalOrderIM': '0', 'equity': '1187.28197477', 'totalPositionMM': '0', 'usdValue': '1187.79131874', 'unrealisedPnl': '0', 'collateralSwitch': True, 'spotHedgingQty': '0', 'borrowAmount': '0', 'totalPositionIM': '0', 'walletBalance': '1187.28197477', 'cumRealisedPnl': '-1925.81719762', 'locked': '814.28431', 'marginCollateral': True, 'coin': 'USDT'}]}]}, 'retExtInfo': {}, 'time': 1759119164092}

{'retCode': 0, 'retMsg': 'OK', 'result': {'list': [{'symbol': 'USDCUSDT', 'takerFeeRate': '0.00055', 'makerFeeRate': '0.0002'}]}, 'retExtInfo': {}, 'time': 1759119165053}
'''
