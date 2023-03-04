import queue

from address import *
import scriptsigdecoder

def DUPLICATE(stack):
    stack.append(stack[-1])
    return stack

def HASH(stack):
    element = stack.pop()
    address = createAddress(element)
    stack.append(address)
    return stack

def EQUALVERIFY(stack):
    element1 = stack.pop()
    element2 = stack.pop()
    if element1 == element2:
        return stack
    else:
        stack.append("OP_FALSE")
        return stack

def OPCHECKSIG(stack, tx):

    public_address = stack.pop()
    signature = stack.pop()
    result = verifySig(signature[0], signature[1], tx, public_address)
    if result:
        stack.append(1)
    else:
        stack.append(0)

    print(stack)

def runScript(stack, script, tx):
    while not script.empty():
        print(stack)
        opcode = script.get()

        if opcode == "OP_DUP":
            DUPLICATE(stack)

        elif opcode == "OP_HASH":
            HASH(stack)

        elif opcode == "OP_EQUALVERIFY":
            EQUALVERIFY(stack)

        elif opcode == "OP_CHECKSIG":
            OPCHECKSIG(stack, tx)

        else:
            stack.append(opcode)

    return stack

def main():

    stack = [1, 2]
    stack = DUPLICATE(stack)
    print(stack)

    stack = EQUALVERIFY(stack)
    print(stack)

    stack = [(55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)]
    stack = HASH(stack)
    print(stack)

    sigDec = scriptsigdecoder.decoder("408b22520c20af4de60e54aa2af78486e661efbffc38286253a54bcf24ab2b79934020d79daebf01adb60a15f87eec4c2f41bf5804eab89a8aa995b6224f15f5782c")
    stack = [sigDec, (92641855401206585750031304985966472123204240504167073082041014802408154789641, 5320727137213493453320294950656953718594582159943012446202168292331376026727)]
    script1 = ['OP_DUP', 'OP_HASH', '6918d03beae3e40678ce42cebbafbd713d19a7de97af5c20fe720761a030bccdf7', 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    script = queue.Queue()
    for item in script1:
        script.put(item)

    rawtx = 10037537529027807805101128294953053531362950071905592013635380982446275951243
    t = runScript(stack, script, rawtx)

if __name__ == "__main__":
    main()