from xeggex import XeggeXClient
import argparse
from decimal import Decimal
import asyncio, signal
import time

path = ''

async def place_order(path, market, typ, q, price):
    x = XeggeXClient(path) 
    async with x.websocket_context() as ws:
        await x.ws_login(ws)
        order = await x.ws_create_order(ws, market, typ, str(q), str(price))
        print(order)
    await x.close()
    return order
    
    
async def cancel_order(path, ID):
    x = XeggeXClient(path) 
    async with x.websocket_context() as ws:
        await x.ws_login(ws)
        ord_cancelled = await x.ws_cancel_order(ws, ID) 
    await x.close()
    
async def balance(path, name):
    x = XeggeXClient(path) #if not args.config else XeggeXClient(args.config)
    async with x.websocket_context() as ws:
        await x.ws_login(ws)
        bal = await x.get_balances()
        #print(bal)
        for i in bal:
            if i['asset'] == name:
                print(i)
                break
    await x.close()

async def price(path, symbol):
    x = XeggeXClient(path) #if not args.config else XeggeXClient(args.config)
    async with x.websocket_context() as ws:
        await x.ws_login(ws)
        bal = await x.ws_get_market(ws, symbol)
    await x.close()

async def get_active_orders(path, symbol):
    x = XeggeXClient(path)
    async with x.websocket_context() as ws:
        await x.ws_login(ws)
        time.sleep(2)
        orders = await x.ws_get_active_orders(ws, symbol)
    await x.close()
    return orders 

#asyncio.run(place_order(path, 'BTC/USDT', 'sell', 0.0002, 50000))
