p = 23
p_order = []

while p >= 1:

    if p % 2 == 0:

        p //= 2
        p_order.insert(0, "double")

    if p % 2 != 0:
        
        p -= 1 
        p_order.insert(0, "add")


est_p = 0

for item in p_order:
    if item == "double":
        est_p *= 2 
    if item == "add":
        est_p += 1

print(est_p)
print(p)

if est_p == p:
    print("correct")
