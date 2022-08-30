import random

p = 4000000000000000000000000000000

p_solved = False
p_counter = 0

p_order = []

while p_solved != True:

    if p % 2 == 0:
        p = p/2
        p_counter += 2
        p_order.append("d")
    else: 
        p -= 1
        p_counter += 1
        p_order.append("a")
    
    if p == 1:
        p_solved = True


print(f"P_COUNT:{p_counter}\nORDER: {p_order}")

last_item = len(p_order) 
est_p = 1 

for x in range(-(last_item), 0):

    if p_order[x] == "d":
        est_p = est_p * 2
        
    elif p_order[x] == "a":
        est_p = est_p + 1 

print(est_p)