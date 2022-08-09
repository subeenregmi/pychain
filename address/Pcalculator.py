p = 100
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

    print(f"\nValue of current p = {p}\nP counter : {p_counter}\nP solved : {p_solved}\nORDER: {p_order}")


