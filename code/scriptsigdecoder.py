def decoder(scriptsig):
    size = int(scriptsig[0:2], 16)
    scriptsig_x = scriptsig[2:2+size]
    size2 = int(scriptsig[2+size:4+size], 16)
    scriptsig_y = scriptsig[4+size:4+size+size2]

    scriptsig_x = int(scriptsig_x, 16)
    scriptsig_y = int(scriptsig_y, 16)    
    return (scriptsig_x, scriptsig_y)

def main():
    print(decoder("40c1f396fd90ca13d8d1458b87139c6954c95063f8f14146681a5ae2e496c4bd864052ccbae772e5b72ca807993f25ac96cc0cb6e2ab2a36e53a494ce828bfdfce8a"))


if __name__ == "__main__":
    main()