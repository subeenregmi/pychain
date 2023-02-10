import time

tx = "TX:013801017b6632fce3914fd9b098a10760a995a41dcb260a9a740b7ed6fd0902e2c47ed6000042408b22520c20af4de60e54aa2af78486e661efbffc38286253a54bcf24ab2b79934020d79daebf01adb60a15f87eec4c2f41bf5804eab89a8aa995b6224f15f5782c010000000000000064002676a92169b75cdd59e53f0ced19cbf30efad3ec5ea3026f805d9e1ed6aea18f5a593e29b788ac00000000004d63954422509139660694275478881573291931659433822585593108077818434106113196321004d26900081337699559997929288916999997486541154242084777368521628620275013037611"

message = tx[3:]
print(message)

txlength = message[:4]
txlength = int(txlength, 16)

print(txlength)

transaction = message[4:4+txlength]
print(transaction)

public_key = message[4+txlength:]
print(public_key)

pubxlenght = public_key[:4]
pubxlenght = int(pubxlenght, 16)
print(pubxlenght)

pubx = public_key[4:4+pubxlenght]
print(pubx)

pubylen = public_key[4+pubxlenght: 8+pubxlenght]
pubylen = int(pubylen, 16)
print(pubylen)

puby = public_key[8+pubxlenght: 8+pubxlenght+pubylen]
print(puby)