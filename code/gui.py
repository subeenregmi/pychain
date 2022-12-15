import tkinter as tk
from address import *
import random

#window config
window = tk.Tk()
window.geometry("1000x750+0+0")
window.configure(background="#000000")
window.configure()

#variables
private_key_store = tk.IntVar()
public_key_store = tk.IntVar()

#title of page
window_title = tk.Label(text="pyChain", foreground="white", background="black", font=("", 24))
window_title.pack()    

#function to generate key
def generate_private_key():
    private_key = random.randint(1, n)
    private_key_store.set(private_key)
    privatekey_label.config(text = str(private_key))

def create_public_key():
    p = private_key_store.get()
    public_key = ECmultiplication(p, Gx, Gy)
    public_key_store.set(p)
    publickey_label.config(text = public_key)
    
#button to create private key 
generate_key_button = tk.Button(text="Generate Key", command=generate_private_key)
generate_key_button.place(x=0, y=100)

#button to create address
create_address_button = tk.Button(text="Create Address", command=create_public_key)
create_address_button.place(x=0, y=150)

#label for private key 
privatekey_label = tk.Label(text=private_key_store)
privatekey_label.place(x = 200, y = 100)

#label for public key 
publickey_label = tk.Label(text=public_key_store)
publickey_label.place(x=200, y=150)






window.mainloop()