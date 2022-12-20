from address import *

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
    pass

if __name__ == "__main__":
    main()