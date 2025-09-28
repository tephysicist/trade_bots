#import psycopg2
from datetime import datetime
import time
from mexc_sdk import Spot
from sender import send_msg
#from postgresql import get_postgresql_connect
import functions as f
import asyncio
import urllib


insert_sql = '''insert into orders VALUES ('{order_id}', 1, '{market}', '{price}', to_date('{create_at}','YYYY-MM-DD HH24:MI:SS'), '{type}', '{quantity}',null, null, '{burse}')'''
close_orders = '''update orders set close_at = to_date('{cancel_at}','YYYY-MM-DD HH24:MI:SS'), active = 0
where active = 1 and order_id = '{orders}'
'''


def sell_buy(burse, Type, cursor, created_ord, market, quantity, price):
    path = ''
    api_key = ''
    api_secret = ''
    if burse =='xeggex':
        order = asyncio.run(f.place_order(path, market, Type, quantity, price))
        order_id = order['result']['id']
    elif burse =='mexc':
        client = Spot(api_key=api_key, api_secret=api_secret)
        order = client.new_order(symbol=market, side=Type, order_type="LIMIT",
                                  options={"quantity": quantity, "price": price})
        order_id = order['orderId']
    created_ord.append(order_id)
    '''sell_sql = insert_sql.format(order_id=order_id, market=market, burse=burse, price=price,
                                 create_at=datetime.today().strftime('%Y-%m-%d %H:%M:%S'), type=Type,
                                 quantity=quantity)
    cursor.execute(sell_sql)'''
def check_internet_connection():
    try:
        urllib.request.urlopen('http://www.google.com', timeout=1)
        return True
    except urllib.request.URLError:
        return False
def check_orders(burse, market):
    path = '/home/viki/trade_robot_xeggex/xeggggs_settings.json'
    api_key = ''
    api_secret = ''
    if burse =='xeggex':
        active_orders_cycle = asyncio.run(f.get_active_orders(path, market))
        c_active_orders_cycle = []
        for i in range(len(active_orders_cycle['result'])):
            c = active_orders_cycle['result'][i]
            c_active_orders_cycle.append(c['id'])
    elif burse =='mexc':
        client = Spot(api_key=api_key, api_secret=api_secret)
        active_orders_cycle = client.open_orders(symbol=market)
        c_active_orders_cycle = []
        for i in range(len(active_orders_cycle)):
            c = active_orders_cycle[i]
            c_active_orders_cycle.append(c['orderId'])
    return c_active_orders_cycle


def mexc_bot(burse, market, type_deal, quantity, sell_price, buy_price):
    #pg_connection = get_postgresql_connect()
    #cursor = pg_connection.cursor()
    created_ord = []
# (burse, Type, cursor, created_ord, market, quantity, price)
    if type_deal == 'SELL_BUY':
        sell_buy(burse, 'SELL', cursor, created_ord, market, quantity, sell_price) # создаем новые заказы на покупку
        pg_connection.commit()
        # на продажу
        sell_buy(burse,'BUY', cursor, created_ord, market, quantity, buy_price)
        pg_connection.commit()
    elif type_deal == 'SELL':
        sell_buy(burse,'SELL', cursor, created_ord, market, quantity, sell_price)
        pg_connection.commit()
    elif type_deal == 'BUY':
        sell_buy(burse,'BUY', cursor, created_ord, market, quantity, buy_price)
        pg_connection.commit()
    order_list = []
    previous_time = datetime.today().strftime('%H')
    #cycle check_orders
    while 1:
        if f.check_internet_connection():
            pass
        else:
            continue
        time.sleep(60)
        print_time = datetime.today().strftime('%H')
        if previous_time != print_time:
            print(datetime.today().strftime('%Y-%m-%d %H'))
            previous_time = print_time
        try:
            c_active_orders_cycle = check_orders(burse, market)
            #если созданные заказы не равно активные
            if set(created_ord)-set(c_active_orders_cycle) != set():
                # проверяем какого заказа нет и с каким статусом
                ords_id = set(created_ord)-set(c_active_orders_cycle)
                print('Заказ закрылся ', ords_id)
                # поиск типа заказа который закрылся
                cursor.execute(''' select type from orders where order_id = {orders}
                        '''.format(orders=str(ords_id).replace('}','').replace('{','')))
                type_ord = cursor.fetchall()[0][0]
                #закрытие заказа
                cursor.execute(close_orders.format(orders = str(ords_id).replace('}','').replace('{','').replace("'",''), cancel_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
                ords = list(ords_id)[0]
                created_ord.remove(ords)
                msg = burse + ' ' + market + ' ' + type_ord + ' закрылся'
                send_msg(msg)
                if type_ord == 'SELL':
                    sell_buy(burse, 'BUY', cursor, created_ord, market, quantity, buy_price)
                    pg_connection.commit()
                elif type_ord == 'BUY':
                    sell_buy(burse, 'SELL', cursor, created_ord, market, quantity, sell_price)
                    pg_connection.commit()

        except Exception:
            print('Проблемы')
            time.sleep(600)
    print('VSE')
    cursor.close()


