from main import redis_db, Order
import time

key = 'refund_order'
group = 'payment_group'

try:
    redis_db.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        results = redis_db.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            print(results)
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)