def decoder(scriptsig):
    size = int(scriptsig[0:2], 16)
    scriptsig_x = scriptsig[2:2+size]
    size2 = int(scriptsig[2+size:4+size], 16)
    scriptsig_y = scriptsig[4+size:4+size+size2]

    scriptsig_x = int(scriptsig_x, 16)
    scriptsig_y = int(scriptsig_y, 16)    
    return (scriptsig_x, scriptsig_y)

def main():
    print(decoder("408b22520c20af4de60e54aa2af78486e661efbffc38286253a54bcf24ab2b79934020d79daebf01adb60a15f87eec4c2f41bf5804eab89a8aa995b6224f15f5782c"))
if __name__ == "__main__":
    main()