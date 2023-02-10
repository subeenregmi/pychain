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
    if result == True:
        stack.append(1)
    else:
        stack.append(0)

    print(stack)

def runScript(stack, script, tx):

    for opcode in script:
        print(stack)
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
    sigDec = scriptsigdecoder.decoder("408b22520c20af4de60e54aa2af78486e661efbffc38286253a54bcf24ab2b79934020d79daebf01adb60a15f87eec4c2f41bf5804eab89a8aa995b6224f15f5782c")
    stack = [sigDec, (92641855401206585750031304985966472123204240504167073082041014802408154789641, 5320727137213493453320294950656953718594582159943012446202168292331376026727)]
    script = ['OP_DUP', 'OP_HASH', '6918d03beae3e40678ce42cebbafbd713d19a7de97af5c20fe720761a030bccdf7', 'OP_EQUALVERIFY', 'OP_CHECKSIG']
    rawtx = 10037537529027807805101128294953053531362950071905592013635380982446285951243
    t = runScript(stack, script, rawtx)
    print(t)
if __name__ == "__main__":
    main()