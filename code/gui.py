import tkinter as tk
from address import *
import random
import hashlib

#window config
window = tk.Tk()
window.geometry("1500x750+0+0")
window.configure(background="#E7E7E7")
window.configure()

#variables
private_key_store = tk.IntVar()
public_key_store_x = tk.IntVar()
public_key_store_y = tk.IntVar()
py_address = tk.StringVar()
digital_signature_x = tk.IntVar()
digital_signature_y = tk.IntVar()

#title of page
window_title = tk.Label(text="pyChain", foreground="Black", background="#E7E7E7", font=("", 24))
window_title.pack()    

def createall():
    
    generate_private_key()
    create_public_key()
    generate_pychain_address()


#function to generate key
def generate_private_key():
    private_key = random.randint(1, n)
    private_key_store.set(private_key)
    print(private_key_store.get)
    privatekey_label.config(text = str(private_key))

def create_public_key():
    p = private_key_store.get()
    #print(p)
    public_key = ECmultiplication(p, Gx, Gy)
    print(public_key)
    public_key_store_x.set(public_key[0])
    public_key_store_y.set(public_key[1])
    publickey_label.config(text=(public_key_store_x.get(), public_key_store_y.get()))
    publickey_hash_label.config(text = (hex(public_key_store_x.get())[2:], hex(public_key_store_y.get())[2:]))


def generate_pychain_address():
    public_key = (public_key_store_x.get(), public_key_store_y.get())
    paddy = createAddress(public_key)
    py_address.set(paddy)
    print(py_address.get())
    py_chain_address_label.configure(text = py_address.get())
    
def create_digital_signature():
    data2hash = hash_input.get()
    hashed_data = hashlib.sha256(data2hash.encode('utf-8')).hexdigest()
    hashed_data = int(hashed_data, 16)
    r, s = signatureGeneration(private_key_store.get(), random.randint(1, n), hashed_data)  
    digital_signature_x.set(r)
    digital_signature_y.set(s)
    digital_signature_label.config(text=(digital_signature_x.get(), digital_signature_y.get()))



#button to create private key 
generate_key_button = tk.Button(text="Generate Key", command=generate_private_key)
generate_key_button.place(x=0, y=100)

#button to create address
create_address_button = tk.Button(text="Create Address", command=create_public_key)
create_address_button.place(x=0, y=150)

#button to create py address 
create_pychain_address_button = tk.Button(text="Create PyAddress", command=generate_pychain_address)
create_pychain_address_button.place(x=0, y=200)

#button to do all things 
create_all_button = tk.Button(text="Create a new address", command=createall)
create_all_button.place(x=50, y=20)

#button to hash
create_digital_signature_button = tk.Button(text="Create digital signature", command=create_digital_signature)
create_digital_signature_button.place(x=0, y=250)

#label for private key 
privatekey_label = tk.Label(text="", state="active")
privatekey_label.place(x = 200, y = 100)

#label for public key 
publickey_label = tk.Label(text="")
publickey_label.place(x=200, y=150)

#label for hashed public key 
publickey_hash_label = tk.Label(text="")
publickey_hash_label.place(x=200, y=175)

#label to display the py address
py_chain_address_label = tk.Label(text="")
py_chain_address_label.place(x=200, y=200)

#digital signature out
digital_signature_label = tk.Label(text="")
digital_signature_label.place(x=200, y=275)

#enter data for digital signature
hash_input = tk.Entry(window, width=100)
hash_input.place(x=200, y=250)



window.mainloop()