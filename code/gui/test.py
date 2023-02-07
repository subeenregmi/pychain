import time
import threading

def counter():
    count = 0
    count1 = 0
    while True:
       print(f"count = {count}")
       count += 1
       time.sleep(1)
       while True:
           print(f"count1: {count1}")
           count1 += 1
           time.sleep(1)
           if count1 == 3:
               break

counter()