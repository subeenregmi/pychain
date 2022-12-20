def decoder(scriptsig):
    size = int(scriptsig[0:2], 16)
    scriptsig_x = scriptsig[2:2+size]
    size2 = int(scriptsig[2+size:4+size], 16)
    scriptsig_y = scriptsig[4+size:4+size+size2]

    scriptsig_x = int(scriptsig_x, 16)
    scriptsig_y = int(scriptsig_y, 16)    
    return (scriptsig_x, scriptsig_y)

def main():
    pass

if __name__ == "__main__":
    main()