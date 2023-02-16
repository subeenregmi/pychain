import customtkinter
import tkinter
import json
import random
import address
import hashlib
import requests


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # we call a method as users may want to go back
        self.start()

    def start(self):

        # This destroys all previous widgets if switching to the start menu.
        for widget in self.winfo_children():
            widget.destroy()

        # Settings for the window
        self.title("Pychain")
        self.geometry("225x350")
        self.resizable(False, False)

        # Settings for a 4x1 grid
        self.grid_rowconfigure((0), weight=2)
        self.grid_rowconfigure((1,2), weight=2)
        self.grid_rowconfigure((3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Settings to create a frame in the first cell
        Title = customtkinter.CTkFrame(master=self, fg_color="transparent", border_color="grey")
        Title.grid(row=0)

        # Settings for the labels inside the frame
        Label = customtkinter.CTkLabel(master=Title, bg_color="transparent", text="Pychain", font=customtkinter.CTkFont(size=40, weight="bold"), width=130, height=40)
        Label.grid(row = 0, column = 0, padx=10)
        SubTitle = customtkinter.CTkLabel(master=Title, text="A blockchain sandbox")
        SubTitle.grid(row=1, padx=10, pady=(10, 0), sticky="s")

        # Settings for the login button
        self.LoginButton = customtkinter.CTkButton(master=self, width=180, height=50, text="Login", font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="#533FD3", hover_color="#2c1346", command=self.Login)
        self.LoginButton.grid(row=1, column=0, padx=0, pady=0, sticky="s")

        # Settings for the create account button
        CreateButton = customtkinter.CTkButton(master=self, width=180, height=50, text="Create New Account", font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="#533FD3", hover_color="#2c1346", anchor="center", command=self.CreateNewAccount)
        CreateButton.grid(row=2, column=0, padx=0, pady=0)

        # Settings for the bottom tile
        bottomTitle = customtkinter.CTkLabel(master=self, height=14, anchor="s", corner_radius=0, text="By Subeen Regmi", text_color="grey")
        bottomTitle.grid(row=3)

    def Login(self):
        try:
            f = open("keys.json")
            data = json.load(f)
            # Do something here, e.g: send to next menu.
            print("LOADED")
            f.close()
        except FileNotFoundError:
            # Settings for window that pops up when the user does not have any keys stored in 'keys.json'
            window = customtkinter.CTkToplevel(self)
            window.geometry("200x100")
            window.resizable(False, False)

            # Label inside the window
            label = customtkinter.CTkLabel(master=window, text="No account found!\n\nCreate a new account", anchor="center")
            label.pack(padx=20, pady=20)

            # Greying out the login button after login fails
            self.LoginButton.configure(state="disabled", fg_color="grey")

    def CreateNewAccount(self):

        # Destroys all previous widgets to clear the screen
        for widget in self.winfo_children():
            widget.destroy()

        # Create new window
        self.title("Pycharm")
        self.geometry("1200x700")
        self.resizable(False, False)

        # Creating a 3 row gui, one for the title, one for the addressing, and the last one for passwords and saving
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame for the top row to separate the title on the left to the description on the right
        frameTitle = customtkinter.CTkFrame(master=self, border_width=3, border_color="#533FD3")
        frameTitle.grid(row=0, padx=10, pady=10, sticky="nsew")

        # Setting up the 3 columns required for the title frame
        frameTitle.grid_columnconfigure(0, weight=1)
        frameTitle.grid_columnconfigure(1, weight=1)
        frameTitle.grid_columnconfigure(2, weight=1)
        frameTitle.grid_rowconfigure(0, weight=1)

        # Title at the top of the window, and the description on the right, and a button to generate an address
        Label = customtkinter.CTkLabel(master=frameTitle, anchor="center", text="Pychain Wallet Creator", font=customtkinter.CTkFont(size=20, weight="bold"))
        Label.grid(row=0, column=0, padx=10, pady=10)
        Label2 = customtkinter.CTkLabel(master=frameTitle, text="How To Use: Click the button to generate a pseudorandom"
                                                                " Address\nStore the account by giving it a password and "
                                                                "click the Save Button!")
        Label2.grid(row=0, column=1, padx=10, pady=10)

        Button = customtkinter.CTkButton(master=frameTitle, text="Generate Address", font=customtkinter.CTkFont(size=30), text_color="white", fg_color="#533FD3", hover_color="#2c1346", command=self.addressCreator)
        Button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Frame for the next section requires, the private address view, the public address view, the pychain address
        # view and the randomly generated image, these need to be in a 3x2, with more weight on the left column and the
        # right column to be spanned to one column

        frameAddress = customtkinter.CTkFrame(master=self, fg_color="transparent")
        frameAddress.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Grid configuration stated previously
        frameAddress.grid_rowconfigure((0, 1, 2), weight=1)
        frameAddress.grid_columnconfigure(0, weight=4)
        frameAddress.grid_columnconfigure(1, weight=2)

        # Adding three frames, one for each row on the first column
        # This is the frame for the private key.
        frame1 = customtkinter.CTkFrame(master=frameAddress, border_color="#533FD3", border_width=3)
        frame1.grid(row=0, column=0, sticky="nsew", pady=5)
        frame1.grid_rowconfigure(0, weight=1)
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_columnconfigure(1, weight=3)

        # This is the frame for the public key.
        frame2 = customtkinter.CTkFrame(master=frameAddress, border_color="#533FD3", border_width=3)
        frame2.grid(row=1, column=0, sticky="nsew", pady=5)
        frame2.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_columnconfigure(1, weight=3)

        # THis is the frame for the Pychain Address
        frame3 = customtkinter.CTkFrame(master=frameAddress, border_color="#533FD3", border_width=3)
        frame3.grid(row=2, column=0, sticky="nsew", pady=5)
        frame3.grid_rowconfigure(0, weight=1)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_columnconfigure(1, weight=3)

        # This is the text for the Private Key
        text1 = customtkinter.CTkLabel(master=frame1, text="Private Key :", font=customtkinter.CTkFont(size=15, weight="bold"))
        text1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.text1k = customtkinter.CTkLabel(master=frame1, text="", anchor="center", wraplength=400)
        self.text1k.grid(row=0, column=1, padx=5, pady=5)

        # This is the text for the Public Key
        text2 = customtkinter.CTkLabel(master=frame2, text="Public Key :", font=customtkinter.CTkFont(size=15, weight="bold"))
        text2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.text2k = customtkinter.CTkLabel(master=frame2, text="", wraplength=600, anchor="center")
        self.text2k.grid(row=0, column=1, padx=5, pady=5)

        # This is the text for the Pychain Address
        text3 = customtkinter.CTkLabel(master=frame3, text="Pychain Address :", font=customtkinter.CTkFont(size=15, weight="bold"))
        text3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.text3k = customtkinter.CTkLabel(master=frame3, text="")
        self.text3k.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Frame that stores entry for password and the save to json button
        frame4 = customtkinter.CTkFrame(master=self, border_color="grey")
        frame4.grid(row=2, column=0, sticky="nesw", padx=10, pady=(0,10))

        # Frame Configuration
        frame4.grid_rowconfigure(0, weight=1)
        frame4.grid_rowconfigure(1, weight=1)
        frame4.grid_columnconfigure(0, weight=1)
        frame4.grid_columnconfigure(1, weight=4)

        # Label for password 
        Label3 = customtkinter.CTkLabel(master=frame4, bg_color="#533FD3", text="Password :", font=customtkinter.CTkFont(size=20))
        Label3.grid(row=0, column=0, sticky="nesw", padx=10, pady=10)

        # Entry for password 
        self.passwordEntry = customtkinter.CTkEntry(master=frame4, font=customtkinter.CTkFont(size=20))
        self.passwordEntry.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        # Button to save the current key stored.
        passwordButton = customtkinter.CTkButton(master=frame4, anchor="center", text="Save and Quit", fg_color="#533FD3", hover_color="#2c1346", command=self.saveAddress)
        passwordButton.grid(row=1, column=0, columnspan=2, ipadx=10, ipady=10)

    def addressCreator(self):
        # This function creates a random private key, public key and pychain address. This is used in the 'Generate
        # Address' Button.

        randomInteger = random.randint(0, address.n)
        public_key = address.ECmultiplication(randomInteger, address.Gx, address.Gy)
        pychainAddress = address.createAddress(public_key)
        self.text1k.configure(text=randomInteger)
        self.text2k.configure(text=public_key)
        self.text3k.configure(text=pychainAddress)

    def saveAddress(self):
        # This function will get the private key, and the hash of the password. Then will store it into as a json file,
        # named 'keys.json'.

        # We are getting the data from the labels (textboxes) and the entry (inputs)
        private_key = self.text1k.cget("text")
        password = self.passwordEntry.get()
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if private_key == '' or password == '':
            # Settings for window that pops up when the user does not have any password or key, and they are trying to
            # save and quit.
            window = customtkinter.CTkToplevel(self)
            window.geometry("200x100")
            window.resizable(False, False)

            # These conditional statements are to check that all appropriate fields have been filled properly. If either
            # one is not filled when trying to save a new window pops up and then indicates the problem.

            if password == '' and private_key != '':
                label = customtkinter.CTkLabel(master=window, text="Password has not been entered.", anchor="center", wraplength=150)
                label.pack(padx=20, pady=20)

            if password != '' and private_key == '':
                label = customtkinter.CTkLabel(master=window, text="Private Key has not been generated.", anchor="center", wraplength=150)
                label.pack(padx=20, pady=20)

            if password == '' and private_key == '':
                label = customtkinter.CTkLabel(master=window, text="Password and Private Key fields both are empty.", anchor="center", wraplength=150)
                label.pack(padx=20, pady=20)

        else:
            # Here we store the hash of the password so, the private keys are secure, we do this by instantiating a json
            # object into a list and then once all the fields are filled we can create another dictionary and append it
            # to the list, and then dump it as a json object.

            with open('keys.json') as keys:
                data = json.load(keys)

            data.append({private_key: password_hash})

            with open('keys.json', 'w') as keys:
                json.dump(data, keys, indent=2)

            self.start()

if __name__ == "__main__":
    app = App()
    app.mainloop()