def decoder(scriptsig):
    size = int(scriptsig[0:2], 16)
    scriptsig_x = scriptsig[2:2+size]
    size2 = int(scriptsig[2+size:4+size], 16)
    scriptsig_y = scriptsig[4+size:4+size+size2]

    scriptsig_x = int(scriptsig_x, 16)
    scriptsig_y = int(scriptsig_y, 16)    
    return (scriptsig_x, scriptsig_y)

def main():
    print(decoder("4027d9a8a59366991c370394c03af99f0a065109c22d826e0889933b1af89931cb40328e8db58d8216ebbc4efe90173c1951506974592c1ece0860a9110281433b5a"))

if __name__ == "__main__":
    main()