from main import redis_db, Product
import time

key = 'order_completed'
group = 'inventory_group'

try:
    redis_db.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        # Comsume events from the Redis Stream with matched key and group.
        # {key: '>'}: read only new messages that arrive after this command is executed.
        # None: a count parameter, specifying the number of entries to return, in this case means no limit.
        results = redis_db.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1] # Only get the product from the result.
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity']) # Adjust product's quantity once the order is completed. 
                    product.save()
                except:
                    # If an error happened, send an event to the payment service to cancel the order.
                    redis_db.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)

