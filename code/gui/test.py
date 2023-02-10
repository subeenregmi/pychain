import time

pk = (109202608928186078798810435615768733302210942101644208012371426004931197383580, 71410754864688073695457690215266571394339322412556530640671956032708356876659)

rawtx = "01017b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed6000100050000000000010000000000000064002676a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac00000000"
rawtx = "01017b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed6000100050000000000010000000000000064002676a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac00000000"
public_key_x_length = hex(len(str(pk[0])))[2:].zfill(4)
print(public_key_x_length)
public_key_y_length = hex(len(str(pk[1])))[2:].zfill(4)
print(public_key_y_length)
transaction_length = hex(len(rawtx))[2:].zfill(4)
print(transaction_length)
transaction_message = f"TX:{transaction_length}{rawtx}{public_key_x_length}{pk[0]}{public_key_y_length}{pk[1]}"
print(f"<TCP SEND> TRANSACTION TO BE SENT: {transaction_message}")

message = transaction_message
raw_transaction = message[3:]
print(f"message = {raw_transaction}")

transaction_length = raw_transaction[:4]
print(f"tx length = {transaction_length}")
transaction_length = int(transaction_length, 16)
print(transaction_length)

raw_transaction = raw_transaction[4:4+transaction_length]
print(f"tx ={raw_transaction}")
public_key = message[4+transaction_length]
print(public_key)

public_key_x_length = public_key[:4]
print(f"pubLeng = {public_key_x_length}")
public_key_x_length = int(public_key_x_length, 16)
public_key_x = public_key[4:4+public_key_x_length]
public_key_y_length = public_key[4+public_key_x_length:8+public_key_x_length]
public_key_y_length = int(public_key_y_length, 16)
public_key_y = public_key[8+public_key_x_length:public_key_y_length]