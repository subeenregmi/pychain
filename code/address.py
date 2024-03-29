import hashlib

Pcurve = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424

def ECadd(x1, x2, y1, y2):

    lam = ((y2 - y1) * pow((x2 - x1), -1, Pcurve)) % Pcurve
    x3 = (lam*lam - x1 - x2) % Pcurve
    y3 = (lam *(x1 - x3) - y1) % Pcurve

    return (x3, y3)

def ECdouble(x1, y1):

    lamD = ((3*(x1*x1)+0) * pow((2*y1), -1, Pcurve)) % Pcurve
    x3 = ((lamD*lamD) - (2*x1)) % Pcurve
    y3 = (lamD * (x1 - x3) - y1) % Pcurve

    return(x3, y3)

def ECmultiplication(Scalar, GenX, GenY):

    if Scalar == 0 or Scalar >= n:
        raise Exception("Invalid")

    scalar_binary = str(bin(Scalar))[2:]
    CurX, CurY = GenX, GenY

    for i in range(1, len(scalar_binary)):
        CurX, CurY = ECdouble(CurX, CurY)
        if scalar_binary[i] == "1":
            CurX, CurY = ECadd(CurX, GenX, CurY, GenY)
        
    return (CurX, CurY)
    
def signatureGeneration(privateKey, randomNumber, hashedMessage):

    x, y = ECmultiplication(randomNumber, Gx, Gy)
    r = x % n
    s = (pow(randomNumber, -1, n) * (hashedMessage + r*privateKey)) % n
    return (r, s)

def verifySig(r1, s1, hashedMessage, publicKey):

    if ((r1 <= 0) or (s1 <= 0) or (r1 >= (n)) or (s1 >= (n))):
        raise Exception("Invalid")

    u1 = hashedMessage * pow(s1, -1, n)
    u2 = r1 * pow(s1, -1, n)

    xu1, yu1 = ECmultiplication(u1%n, Gx, Gy)
    xu2, yu2 = ECmultiplication(u2%n, publicKey[0], publicKey[1])

    x, y = ECadd(xu1, xu2, yu1, yu2)

    if (r1 == x%n):
        return True
    else:
        return False

def createAddress(publickey):

    pubkeyStr = str(publickey[0]) + str(publickey[1])
    hash1 = hashlib.sha256(pubkeyStr.encode('utf-8')).hexdigest()
    hash2 = hashlib.sha256(hash1.encode('utf-8')).hexdigest()
    address = "69" + str(hash2)

    return address


def main():

    # Digital signatures
    randNumber = 1989189239293293
    HashOfMessage = 239823823823283232983982323892893

    # Erroneous Data
    # privKey = n+1
    # privKey = 0

    # Normal Data
    # privKey = 23828932738278372

    # Boundary data
    # privKey = n-1
    privKey =91865318790474171578907765630969544070277788816505973228091873448746859054462

    print("--------------------Private Key--------------------")
    print(privKey)
    print("--------------------Public Key--------------------")
    pubKey = ECmultiplication(privKey, Gx, Gy)
    print(pubKey)
    print("--------------------Uncompressed Public Key--------------------")
    print("04 " + str(hex(pubKey[0])[2:]) + " " + str(hex(pubKey[1]))[2:])
    print("--------------------PyChain Address--------------------")
    pyaddress = createAddress(pubKey)
    print(pyaddress)
    r, s = signatureGeneration(privKey, randNumber, HashOfMessage)
    print("--------------------Signature Generation--------------------")
    print((r, s))
    print("--------------------Signature Verification--------------------")
    result = verifySig(r, s, HashOfMessage, pubKey)
    print(result)
    print("--------------------------------------------------------------")

if __name__ == "__main__":
    main()