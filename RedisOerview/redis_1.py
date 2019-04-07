#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：连海峰
# __time__：2018/11/13 22:04
import json
import random

from redis import StrictRedis
import time

redis = StrictRedis(host="localhost", port=6379, db=0)
redis.set("name", "zhangsan")
time.sleep(2)
print(redis.get("hello"))

def send_sold_email_via_queue(conn, seller, item, price, buyer):
    data = {
        "seller_id": seller,
        "item_id": item,
        "price": price,
        "buyer": buyer,
        "time": time.time()
    }
    conn.rpush("queue.email", json.dumps(data))

personarry = ["德玛", "瑞文", "提莫", "vn", "光辉"]
for i in range(5):
    send_sold_email_via_queue(redis, random.choice(personarry), random.choice([i for i in range(100)]), random.choice([666, 998, 10000, 1314, 10086]),random.choice(personarry) + "66")

QUIT = False
def process_sold_email_queue(conn):
    while not QUIT:
        packed = conn.blpop(["queue.email_2", "queue.email"], 30)
        if not packed:
            continue
        to_send = json.loads(packed[1])
        print(to_send)

process_sold_email_queue(redis)