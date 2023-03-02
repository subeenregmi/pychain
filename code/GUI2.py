import socket
import threading
import customtkinter
import json
import random
import address
import hashlib
import requests
from PIL import Image
import shutil
from node import Peer
from datetime import datetime
import os
import subprocess, sys
import spubKeycreator
import scriptSigCreator
import rawtxcreator
from transaction import Transaction
import rawtxdecoder

# This sets the general color theme to be dark
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Here are some variables that we want to use throughout our program
        self.balance = 0
        self.count = None
        self.account = None
        self.account_pubkey = None
        self.peer = None
        self.listOfPeers = []

        # We call a method as users may want to go back
        self.start()

    def start(self):

        # This destroys all previous widgets if switching to the start menu.
        for widget in self.winfo_children():
            widget.destroy()
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)

        # Settings for the window
        self.title("Pychain")
        self.geometry("225x350")
        self.resizable(False, False)

        # Settings for a 4x1 grid
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure((1, 2), weight=2)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Settings to create a frame in the first cell
        Title = customtkinter.CTkFrame(master=self, fg_color="transparent", border_color="grey")
        Title.grid(row=0)

        # Settings for the labels inside the frame
        Label = customtkinter.CTkLabel(master=Title, bg_color="transparent", text="Pychain",
                                       font=customtkinter.CTkFont(size=40, weight="bold"), width=130, height=40)

        Label.grid(row=0, column=0, padx=10)
        SubTitle = customtkinter.CTkLabel(master=Title, text="A blockchain sandbox")
        SubTitle.grid(row=1, padx=10, pady=(10, 0), sticky="s")

        # Settings for the login button
        self.LoginButton = customtkinter.CTkButton(master=self, width=180, height=50, text="Login",
                                                   font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="#533FD3",
                                                   hover_color="#2c1346", command=self.Login)

        self.LoginButton.grid(row=1, column=0, padx=0, pady=0, sticky="s")

        # Settings for the create account button
        CreateButton = customtkinter.CTkButton(master=self, width=180, height=50, text="Create New Account",
                                               font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="#533FD3",
                                               hover_color="#2c1346", anchor="center", command=self.CreateNewAccount)
        CreateButton.grid(row=2, column=0, padx=0, pady=0)

        # Settings for the bottom tile
        bottomTitle = customtkinter.CTkLabel(master=self, height=14, anchor="s", corner_radius=0,
                                             text="By Subeen Regmi", text_color="grey")
        bottomTitle.grid(row=3)

    def Login(self):

        # This is trying to open a 'keys.json' file
        try:
            with open('json/keys.json') as file:
                data = json.load(file)
                loaded = True

        except FileNotFoundError:
            # Settings for window that pops up when the user does not have any keys stored in 'keys.json'
            self.generateErrorLabel("Pychain Login", "Keys.json cannot be found in 'json/keys.json'.")

            # Greying out the login button after login fails
            self.LoginButton.configure(state="disabled", fg_color="grey")
            loaded = False

        if loaded:

            # First we need to destroy all the previous widgets to clear the screen
            for widget in self.winfo_children():
                widget.destroy()
            self.grid_rowconfigure((0, 1, 2, 3), weight=0)
            self.grid_columnconfigure((0, 1, 2, 3), weight=0)

            # Geometry for the new window.
            self.title("Pycharm Login")
            self.geometry("1200x700")
            self.resizable(False, False)

            # We need to create a login page that contains a button that displays the image and the pychain address
            # and the image from the path, and then an entry for the password. If the password matches the hash then
            # we can go to the next page, we will also need a slider for multiple accounts, and an enter button.

            # Grid configuration for the actual window. We are doing a 2x3
            self.grid_rowconfigure((0, 1), weight=1)
            self.grid_columnconfigure((0, 1, 2), weight=1)

            # We are getting the data of the first account in 'keys.json'. This data is the pychain address and the
            # icon file path.
            account = data[0]
            account_img_path = account["iconPath"]
            icon_img = Image.open(account_img_path)
            Icon = customtkinter.CTkImage(dark_image=icon_img, size=(250, 250))
            private_key = int(account["privateKey"])
            pychain_address = address.createAddress(address.ECmultiplication(private_key, address.Gx, address.Gy))

            # We need to create an index, so we can loop through all the accounts.
            self.account_index = 0

            # We also need a 2x1 frame to hold the image and the pychain address.
            frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
            frame.grid(row=0, column=1)
            frame.grid_rowconfigure(0, weight=4)
            frame.grid_rowconfigure(1, weight=1)

            # The button has the image of the icon, and once clicked cycles through all the accounts.
            self.icon_button = customtkinter.CTkButton(master=frame, image=Icon, fg_color="transparent", text="",
                                                       hover_color="grey", command=self.switchAccounts)
            self.icon_button.grid(row=0, padx=10, pady=10)

            # This is the text box that holds the pychain address.
            self.pychain_address_label = customtkinter.CTkLabel(master=frame, text=pychain_address,
                                                                font=customtkinter.CTkFont(weight="bold", size=18))
            self.pychain_address_label.grid(row=1, column=0)

            # If there is a name stored we can show it.
            if account['name'] != "":
                self.pychain_address_label.configure(text=f"{pychain_address}\n{account['name']}")

            # This is the entry that holds the password, this will be hashed and checked in order for a successful login
            self.password_entry = customtkinter.CTkEntry(master=self, placeholder_text="Password",
                                                         font=customtkinter.CTkFont(size=30))
            self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

            login_image = Image.open('images/icons/loginIcon.png')
            Login_icon = customtkinter.CTkImage(dark_image=login_image, size=(35, 35))

            # This is the button to log in to the account.
            login_button = customtkinter.CTkButton(master=self, text="", image=Login_icon, width=35, fg_color="#533FD3",
                                                   hover_color="#2c1346", command=self.loginToAccount)
            login_button.grid(row=1, column=2, sticky="w")

    def switchAccounts(self):
        # This function handles the account cycling mechanism in the login screen.

        # We load 'keys.json' into a format we can handle.
        with open('json/keys.json') as file:
            data = json.load(file)

        # We increment the account index by one and mod it with the amount of the keys, thus will get us the index of
        # the specific keys in the list
        self.account_index = (self.account_index + 1) % len(data)
        next_account = data[self.account_index]
        icon_img = Image.open(next_account["iconPath"])
        Icon = customtkinter.CTkImage(dark_image=icon_img, size=(250, 250))
        private_key = next_account["privateKey"]
        pychain_address = address.createAddress(address.ECmultiplication(private_key, address.Gx, address.Gy))

        # We now configure the buttons with the next account.
        self.icon_button.configure(image=Icon)
        self.pychain_address_label.configure(text=pychain_address)

        if next_account['name'] != "":
            self.pychain_address_label.configure(text=f"{pychain_address}\n{next_account['name']}")

    def loginToAccount(self):
        # This function is used in the login screen, to hash the password entered and if the password hash correlates
        # to the one saved then we go onto the actual GUI.

        # We are loading the keys into a python dictionary.
        with open('json/keys.json') as keys:
            data = json.load(keys)

        # If the password's hash matches with the stored hash then we can move onto the gui.
        account = data[self.account_index]
        password = self.password_entry.get()
        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if account['passwordHash'] == hash_password:
            self.account = account
            self.account_pubkey = address.ECmultiplication(self.account['privateKey'], address.Gx, address.Gy)
            with open("json/currentAccount.json") as file:
                data = json.load(file)
                data["privateKey"] = account['privateKey']

            with open('json/currentAccount.json', 'w') as file:
                json.dump(data, file, indent=2)

            self.gui()
            self.balance = 0
        else:
            self.generateErrorLabel("Pychain Login", "Wrong Password.")

    def CreateNewAccount(self):

        # Destroys all previous widgets to clear the screen
        for widget in self.winfo_children():
            widget.destroy()
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)

        # Create new window
        self.title("Pychain")
        self.geometry("1200x700")
        self.resizable(False, False)

        # Creating a 3 row gui, one for the title, one for the addressing, and the last one for passwords and saving
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
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
        Label = customtkinter.CTkLabel(master=frameTitle, anchor="center", text="Pychain Wallet Creator",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        Label.grid(row=0, column=0, padx=10, pady=10)
        Label2 = customtkinter.CTkLabel(master=frameTitle, text="How To Use: Click the button to generate a "
                                                                "pseudorandom address.\nStore the account by "
                                                                "giving it a password and clicking the Save Button!")
        Label2.grid(row=0, column=1, padx=10, pady=10)

        Button = customtkinter.CTkButton(master=frameTitle, text="Generate Address", font=customtkinter.CTkFont(size=30),
                                         text_color="white", fg_color="#533FD3", hover_color="#2c1346",
                                         command=self.addressCreator)
        Button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Frame for the next section requires, the private address view, the public address view, the pychain address
        # view and the randomly generated image, these need to be in a 3x2, with more weight on the left column and the
        # right column to be spanned down to one row.

        frameAddress = customtkinter.CTkFrame(master=self, fg_color="transparent")
        frameAddress.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Grid configuration stated previously
        frameAddress.grid_rowconfigure((0, 1, 2), weight=1)
        frameAddress.grid_columnconfigure(0, weight=4)
        frameAddress.grid_columnconfigure(1, weight=2)

        # Some text to describe the icon
        text = customtkinter.CTkLabel(master=frameAddress, text="This is an image generated based on your private key!",
                                      wraplength=125)
        text.grid(row=0, column=1)

        # Label for the preview icon to go into
        self.previewIcon = customtkinter.CTkLabel(master=frameAddress, text="")
        self.previewIcon.grid(row=1, column=1, sticky="nsew")

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

        # This is the frame for the Pychain Address
        frame3 = customtkinter.CTkFrame(master=frameAddress, border_color="#533FD3", border_width=3)
        frame3.grid(row=2, column=0, sticky="nsew", pady=5)
        frame3.grid_rowconfigure(0, weight=1)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_columnconfigure(1, weight=3)

        # This is the text for the Private Key
        text1 = customtkinter.CTkLabel(master=frame1, text="Private Key :",
                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        text1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.text1k = customtkinter.CTkLabel(master=frame1, text="", anchor="center", wraplength=400)
        self.text1k.grid(row=0, column=1, padx=5, pady=5)

        # This is the text for the Public Key
        text2 = customtkinter.CTkLabel(master=frame2, text="Public Key :",
                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        text2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.text2k = customtkinter.CTkLabel(master=frame2, text="", wraplength=610, anchor="center")
        self.text2k.grid(row=0, column=1, padx=5, pady=5)

        # This is the text for the Pychain Address
        text3 = customtkinter.CTkLabel(master=frame3, text="Pychain Address :",
                                       font=customtkinter.CTkFont(size=15, weight="bold"))
        text3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.text3k = customtkinter.CTkLabel(master=frame3, text="")
        self.text3k.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Frame that stores entry for password and the save to json button
        frame4 = customtkinter.CTkFrame(master=self, border_color="grey")
        frame4.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Frame Configuration
        frame4.grid_rowconfigure(0, weight=1)
        frame4.grid_rowconfigure(1, weight=1)
        frame4.grid_columnconfigure(0, weight=1)
        frame4.grid_columnconfigure(1, weight=4)

        # Label for password
        Label3 = customtkinter.CTkLabel(master=frame4, bg_color="#533FD3", text="Password :",
                                        font=customtkinter.CTkFont(size=20))
        Label3.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Entry for password
        self.passwordEntry = customtkinter.CTkEntry(master=frame4, font=customtkinter.CTkFont(size=20))
        self.passwordEntry.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        # Button to save the current key stored.
        passwordButton = customtkinter.CTkButton(master=frame4, anchor="center", text="Save and Quit",
                                                 fg_color="#533FD3", hover_color="#2c1346", command=self.saveAddress)
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

        r = requests.get(f"https://api.dicebear.com/5.x/identicon/png?seed={randomInteger}")
        with open('images/icons/test.png', 'rb+') as file:
            file.write(r.content)
            image = Image.open(file)
            previewIcon = customtkinter.CTkImage(light_image=image, dark_image=image, size=(125, 125))
            self.previewIcon.configure(image=previewIcon)

    def saveAddress(self):
        # This function will get the private key, and the hash of the password. Then will store it into as a json file,
        # named 'keys.json'.

        # We are getting the data from the labels and the entry
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
                label = customtkinter.CTkLabel(master=window, text="Password has not been entered.", anchor="center",
                                               wraplength=150)
                label.pack(padx=20, pady=20)

            if password != '' and private_key == '':
                label = customtkinter.CTkLabel(master=window, text="Private Key has not been generated.",
                                               anchor="center", wraplength=150)
                label.pack(padx=20, pady=20)

            if password == '' and private_key == '':
                label = customtkinter.CTkLabel(master=window, text="Password and Private Key fields both are empty.",
                                               anchor="center", wraplength=150)
                label.pack(padx=20, pady=20)

        else:
            # Here we store the key, the password hash and the icon created.
            # We open the keys file, load it into an object, store the data, and then append that into the object and
            # then dump it into a json object.

            with open('json/keys.json') as keys:
                data = json.load(keys)

            count = len(data)
            keyInfo = {
                "privateKey": private_key,
                "passwordHash": password_hash,
                "iconPath": f"images/usericons/account_icon{count}.png",
                "name": ""
            }

            data.append(keyInfo)

            with open('json/keys.json', 'w') as keys:
                json.dump(data, keys, indent=2)

            # Here we copy the icon into another file, to be used later.
            shutil.copyfile('images/icons/test.png', f'images/usericons/account_icon{count}.png' )

            # Then we return back into our login page.
            self.start()

    def gui(self):

        # This is the GUI for pychain.
        for widget in self.winfo_children():
            widget.destroy()
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)

        # Title, geometry, and resize config
        self.title("Pychain")
        self.geometry("1200x700")
        self.resizable(False, False)

        # Grid configuration: 1x2 with a weighted first column
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=19)
        self.columnconfigure(1, weight=1)

        # Two frames, one for the tabview and one for the sidebar menu.
        tabview_frame = customtkinter.CTkFrame(master=self)
        tabview_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        tabview_frame.grid_rowconfigure(0, weight=1)
        tabview_frame.grid_rowconfigure(1, weight=0)
        tabview_frame.grid_columnconfigure(0, weight=1)
        tabview_frame.grid_columnconfigure(1, weight=0)

        sidebar_frame = customtkinter.CTkFrame(master=self, width=40)
        sidebar_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        sidebar_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        sidebar_frame.grid_rowconfigure(4, weight=0)
        sidebar_frame.grid_columnconfigure(0, weight=1)
        sidebar_frame.grid_columnconfigure(1, weight=0)

        # The tabview, containing the tabs: Home, Send, Transactions, Blocks, Connect, Mine.
        pychainTabview = customtkinter.CTkTabview(master=tabview_frame, segmented_button_selected_color="#533FD3",
                                                  segmented_button_selected_hover_color="#2c1346")
        pychainTabview.grid(sticky="nsew", padx=20, pady=(0, 20))

        home = pychainTabview.add("Home")
        send = pychainTabview.add("Send")
        transactions = pychainTabview.add("Transactions")
        blocks = pychainTabview.add("Blocks")
        connect = pychainTabview.add("Connect")
        mine = pychainTabview.add("Mine")

        # All things to be displayed in the home section in the tabview:
        # We need to get a balance of pychain coins, the latest transactions, the latest blocks mined.

        # home.configure(fg_color="white", border_color="grey")
        home.grid_rowconfigure(0, weight=1)
        home.grid_rowconfigure(1, weight=1)
        home.grid_rowconfigure(2, weight=5)
        home.grid_rowconfigure(3, weight=1)
        home.grid_rowconfigure(4, weight=5)
        home.grid_rowconfigure(5, weight=0)
        home.grid_columnconfigure(0, weight=19)
        home.grid_columnconfigure(1, weight=1)
        home.grid_columnconfigure(2, weight=0)

        # We have a frame that holds both the welcome label and the balance. We can also update the balance at anytime
        # as we have defined it with self.
        welcomeFrame = customtkinter.CTkFrame(master=home, fg_color="transparent")
        welcomeFrame.grid(row=0, column=0, sticky="nsew")
        welcomeFrame.grid_rowconfigure((0, 1), weight=1)
        welcomeFrame.grid_rowconfigure(2, weight=0)
        welcomeFrame.grid_columnconfigure(1, weight=0)

        welcome_label = customtkinter.CTkLabel(master=welcomeFrame, text="Welcome To Pychain!",
                                               font=customtkinter.CTkFont(size=40, family="Montserrat", weight="bold"))
        welcome_label.grid(row=0, column=0, sticky="nw", padx=5, pady=(5, 0))

        if self.account['name'] != "":
            print(self.account['name'])
            welcome_label.configure(text=f"Welcome to Pychain, {self.account['name']}!")

        self.balance_label = customtkinter.CTkLabel(master=welcomeFrame, text=f"Balance: {self.balance}",
                                                    font=customtkinter.CTkFont(size=20, family="Montserrat"))
        self.balance_label.grid(row=1, column=0, sticky="nw", padx=10)

        # The account image will be displayed next to the welcome, this will be a button to allow you to change
        # accounts.
        path_to_image = self.account["iconPath"]
        Icon_img = Image.open(path_to_image)
        Icon = customtkinter.CTkImage(dark_image=Icon_img, size=(125, 125))

        Icon_button = customtkinter.CTkButton(master=home, image=Icon, fg_color="transparent", text="", width=75,
                                              height=75, hover_color="grey", command=self.Login)
        Icon_button.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        # The option menu that allows you to select a blockchain, and to connect on that, there will also be a button
        # under this menu, to connect and then disable the option menu
        # Getting all the file names in the /blockchains directory
        blockchains = os.listdir("blockchains/")

        self.blockchain_selector = customtkinter.CTkOptionMenu(master=home, values=blockchains, fg_color="#533FD3",
                                                               button_color="#2c1346", button_hover_color="#2c1346",
                                                               font=customtkinter.CTkFont(size=14, family="Montserrat"))
        self.blockchain_selector.grid(row=1, column=1, sticky="se", padx=10, pady=(5, 0))

        self.select_blockchain_button = customtkinter.CTkButton(master=home, text="Connect", fg_color="#533fd3",
                                                                hover_color="#2c1346",
                                                                font=customtkinter.CTkFont(size=14, family="Montserrat"),
                                                                command=self.createNode)
        self.select_blockchain_button.grid(row=2, column=1, sticky="ne", pady=5, padx=10)

        # A transactions button will also be on the home menu, below the button will be the three latest transactions,
        # but you can also click the button to go to the transaction tab
        latest_transaction_label = customtkinter.CTkLabel(master=home, text="Latest Transactions:", fg_color="transparent",
                                                          font=customtkinter.CTkFont(size=20, family="Montserrat"))
        latest_transaction_label.grid(row=1, column=0, sticky="nw", padx=5)

        # There will also be a frame for the three latest transactions, just below the transaction button
        latest_transactions_frame = customtkinter.CTkFrame(master=home, fg_color="transparent")
        latest_transactions_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        latest_transactions_frame.grid_rowconfigure((0, 1, 2), weight=1)
        latest_transactions_frame.grid_rowconfigure(3, weight=0)
        latest_transactions_frame.grid_columnconfigure(0, weight=1)
        latest_transactions_frame.grid_columnconfigure(1, weight=0)

        # There will be three frames inside the frame indicate the transactions. inside those frames we will have a
        # button and the label for the transaction details, we could also have an image to the left of the frame
        # indicating if the transaction was incoming or outgoing.

        self.latest_transaction_one = customtkinter.CTkFrame(master=latest_transactions_frame, height=40)
        self.latest_transaction_one.grid(row=0, sticky="nsew", pady=(0, 5))

        self.latest_transaction_two = customtkinter.CTkFrame(master=latest_transactions_frame, height=40)
        self.latest_transaction_two.grid(row=1, sticky="nsew", pady=(0, 5))

        self.latest_transaction_three = customtkinter.CTkFrame(master=latest_transactions_frame, height=40)
        self.latest_transaction_three.grid(row=2, sticky="nsew")

        # A 'Latest Blocks' button, once clicked will go to the blocks tab.
        latest_blocks_label = customtkinter.CTkLabel(master=home, text="Latest Blocks:", fg_color="transparent",
                                                     font=customtkinter.CTkFont(size=20, family="Montserrat"))
        latest_blocks_label.grid(row=3, column=0, sticky="nw", padx=5, pady=(5, 0))

        # There will be a frame holding tha last three blocks. In each frame we will have the last three blocks. That
        # have been mined.
        latest_blocks_frame = customtkinter.CTkFrame(master=home, fg_color="transparent")
        latest_blocks_frame.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        latest_blocks_frame.grid_rowconfigure((0, 1, 2), weight=1)
        latest_blocks_frame.grid_rowconfigure(3, weight=0)
        latest_blocks_frame.grid_columnconfigure(0, weight=1)
        latest_blocks_frame.grid_columnconfigure(1, weight=0)

        self.latest_block_one = customtkinter.CTkFrame(master=latest_blocks_frame, height=40)
        self.latest_block_one.grid(row=0, sticky="nsew", pady=(0, 5))
        self.latest_block_one.grid_rowconfigure(0, weight=1)
        self.latest_block_one.grid_rowconfigure(1, weight=0)
        self.latest_block_one.grid_columnconfigure(0, weight=1)
        self.latest_block_one.grid_columnconfigure(1, weight=0)

        self.latest_block_two = customtkinter.CTkFrame(master=latest_blocks_frame, height=40)
        self.latest_block_two.grid(row=1, sticky="nsew", pady=(0, 5))
        self.latest_block_two.grid_rowconfigure(0, weight=1)
        self.latest_block_two.grid_rowconfigure(1, weight=0)
        self.latest_block_two.grid_columnconfigure(0, weight=1)
        self.latest_block_two.grid_columnconfigure(1, weight=0)

        self.latest_block_three = customtkinter.CTkFrame(master=latest_blocks_frame, height=40)
        self.latest_block_three.grid(row=2, sticky="nsew", pady=(0, 5))
        self.latest_block_three.grid_rowconfigure(0, weight=1)
        self.latest_block_three.grid_rowconfigure(1, weight=0)
        self.latest_block_three.grid_columnconfigure(0, weight=1)
        self.latest_block_three.grid_columnconfigure(1, weight=0)

        if self.peer:
            self.blockchain_selector.configure(state="disabled")
            self.select_blockchain_button.configure(state="disabled")

            try:
                block = self.peer.blockchain.blocks[-1]
                date = int(block.blocktime)
                date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
                block_one_label = customtkinter.CTkLabel(master=self.latest_block_one, text=f"Block ID = {block.blockid}\n"
                                                                                            f"Block Height = {block.height}\n"
                                                                                            f"{date}",
                                                         font=customtkinter.CTkFont(size=12, family="Montserrat"))
                block_one_label.grid(row=0, sticky="nsew", pady=(5,0))

                block = self.peer.blockchain.blocks[-2]
                date = int(block.blocktime)
                date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
                block_two_label = customtkinter.CTkLabel(master=self.latest_block_two, text=f"Block ID = {block.blockid}\n"
                                                                                            f"Block Height = {block.height}\n"
                                                                                            f"{date}",
                                                         font=customtkinter.CTkFont(size=12, family="Montserrat"))
                block_two_label.grid(row=0, sticky="nsew", pady=(5, 0))

                block = self.peer.blockchain.blocks[-3]
                date = int(block.blocktime)
                date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
                block_three_label = customtkinter.CTkLabel(master=self.latest_block_three, text=f"Block ID = {block.blockid}\n"
                                                                                                f"Block Height = {block.height}\n"
                                                                                                f"{date}",
                                                           font=customtkinter.CTkFont(size=12, family="Montserrat"))
                block_three_label.grid(row=0, sticky="nsew", pady=(5, 0))
            except:
                pass

        # The following code will be about the send tab, this is where you can send a transaction to another user.
        send.grid_rowconfigure((0, 1, 2, 3), weight=1)
        send.grid_columnconfigure((0, 1), weight=1)
        send.grid_rowconfigure(4, weight=0)
        send.grid_columnconfigure(2, weight=0)

        send_label = customtkinter.CTkLabel(master=send, text="Here you can send pyCoins to another address, just type in"
                                                              " an address and select an amount within your balance and click"
                                                              " send!",
                                            font=customtkinter.CTkFont(size=20, family="Montserrat"), wraplength=800)
        send_label.grid(row=0, columnspan=3, pady=5, padx=5)

        if self.peer and self.balance != 0:
            # This only shows when a balance other than 0 exists
            self.send_to_entry = customtkinter.CTkEntry(master=send, placeholder_text="To Address",
                                                   font=customtkinter.CTkFont(size=18, family="Montserrat"),
                                                   height=72)
            self.send_to_entry.grid(row=1, column=0, sticky="ew", padx=20, columnspan=2)

            add_address_image = Image.open("images/icons/addressbookIcon.png")
            add_address_image = customtkinter.CTkImage(dark_image=add_address_image, size=(50, 50))
            save_address_button = customtkinter.CTkButton(master=send, text="", fg_color="#533fd3", hover_color="#2c1346",
                                                          height=72, width=72, image=add_address_image,
                                                          command=self.saveSendAddress)

            save_address_button.grid(row=1, column=2, sticky="w")

            self.amount_slider = customtkinter.CTkSlider(master=send, from_=0, to=self.balance, button_color="#533fd3",
                                                         button_hover_color="#2c1346", command=self.getAmount, width=800)
            self.amount_slider.grid(row=2, column=0, sticky="n", columnspan=2, padx=20)

            self.amount_label = customtkinter.CTkLabel(master=send, text="",
                                                       font=customtkinter.CTkFont(size=20, family="Montserrat"))
            self.amount_label.grid(row=2, column=2, padx=5, pady=(0, 20), sticky="nw")

            send_button = customtkinter.CTkButton(master=send, text="Send",
                                                  font=customtkinter.CTkFont(size=20, family="Montserrat", weight="bold"),
                                                  fg_color="#533fd3", hover_color="#2c1346", height=75, width=150,
                                                  command=self.createTransaction)
            send_button.grid(row=3, column=1, padx=5, pady=5, sticky="nw")

        # The following code will be about the transaction tab, this is where you can see all the transactions
        # that you have sent or given.

        # Grid configurations for transactions tab.
        transactions.grid_rowconfigure((0, 2), weight=1)
        transactions.grid_rowconfigure(1, weight=5)
        transactions.grid_rowconfigure(3, weight=0)
        transactions.grid_columnconfigure((0, 1), weight=1)
        transactions.grid_columnconfigure(2, weight=0)

        # Label describing the transactions tab
        transactions_label = customtkinter.CTkLabel(master=transactions, text="This is the transactions tab, this is"
                                                                              " where you can find all your "
                                                                              "transactions.",
                                                    font=customtkinter.CTkFont(size=20, family="Montserrat"))
        transactions_label.grid(row=0, column=0, sticky="n", pady=(5, 0), columnspan=2)

        # Frame that holds all the transactions
        transactions_frame = customtkinter.CTkScrollableFrame(master=transactions)
        transactions_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Frames Grid Configuration
        transactions_frame.grid_columnconfigure(0, weight=1)
        transactions_frame.grid_columnconfigure(1, weight=0)

        # Balance Label to display the amount of pyCoins the user has.
        balance_label = customtkinter.CTkLabel(master=transactions, text="Balance: ",
                                               font=customtkinter.CTkFont(size=20, family="Montserrat"))
        balance_label.grid(row=3, sticky="sw", padx=5, pady=5)

        # We start getting transactions if a node is created
        if self.peer:

            # We setup three variables, the pyaddress of the current user. The total currency in and out.
            pyaddress = address.createAddress(self.account_pubkey)
            total_in = 0
            total_out = 0

            # All transactions relating to the user
            txs = self.peer.blockchain.findALLTxidsRelatingToKey(self.account_pubkey)
            count = len(txs)

            # We are going to loop through all these transactions and identify if they are either coinbase transactions
            # normal transactions or return transactions.
            for tx in txs:
                print(tx.raw)

                # Here we create another frame to display a transaction
                transaction_frame = customtkinter.CTkFrame(master=transactions_frame, fg_color="black")
                transaction_frame.grid_rowconfigure((0, 1, 2), weight=1)
                transaction_frame.grid_rowconfigure(3, weight=0)
                transaction_frame.grid_columnconfigure(0, weight=19)
                transaction_frame.grid_columnconfigure(1, weight=1)
                transaction_frame.grid_columnconfigure(2, weight=0)
                transaction_frame.grid(row=count, sticky="nsew", padx=5, pady=5)
                count -= 1

                # Label for the transactions txid
                transaction_txid_label = customtkinter.CTkLabel(master=transaction_frame, text=f"TXID: {tx.txid}",
                                                                font=customtkinter.CTkFont(size=16, family="Montserrat",
                                                                                           weight="bold"))
                transaction_txid_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

                # Here we get the block time for that transaction
                trx, block_got = self.peer.blockchain.findBlockIdwithTxid(tx.txid)
                transaction_time = block_got.blocktime
                transaction_time = int(transaction_time)
                transaction_time = datetime.utcfromtimestamp(transaction_time).strftime('%Y-%m-%d %H:%M:%S')

                # Label we are going to put the time information of the transaction
                transaction_time_label = customtkinter.CTkLabel(master=transaction_frame, text=transaction_time,
                                                                font=customtkinter.CTkFont(size=14, family="Montserrat",
                                                                                           weight="bold"),
                                                                wraplength=80)
                transaction_time_label.grid(row=0, column=0, sticky="ne", padx=5, pady=5)

                # Here we find who sent the transaction
                addressWho = self.peer.blockchain.findWhoSentTransaction(tx)

                # If the transaction is a coinbase, the total in increments by 100
                if addressWho == "Coinbase Transaction":
                    # Label for the value of the transaction
                    transaction_value = customtkinter.CTkLabel(master=transaction_frame, text="Value: 100 pyCoins",
                                                               font=customtkinter.CTkFont(size=14, family="Montserrat"))
                    transaction_value.grid(row=1, column=0, sticky="w", padx=5, pady=5)
                    total_in += 100

                    # The label for who sent the transactions, this instance it would be 'Coinbase Transaction'
                    transaction_from = customtkinter.CTkLabel(master=transaction_frame, text=f"Sent From: {addressWho}",
                                                              font=customtkinter.CTkFont(size=14, family="Montserrat"))
                    transaction_from.grid(row=2, column=0, sticky="w", padx=5, pady=5)

                    # This indicates whether we are sending money or receiving, green if receiving and red if sending
                    transaction_colour_frame = customtkinter.CTkFrame(master=transaction_frame, fg_color="#6bde57")
                    transaction_colour_frame.grid_rowconfigure(0, weight=1)
                    transaction_colour_frame.grid_rowconfigure(1, weight=0)
                    transaction_colour_frame.grid_columnconfigure(0, weight=1)
                    transaction_colour_frame.grid_columnconfigure(1, weight=0)
                    transaction_colour_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")

                    # An image to clearly show if sending or receiving
                    image = Image.open('images/icons/plusIcon.png')
                    new_image = customtkinter.CTkImage(dark_image=image, size=(50, 50))
                    image_button = customtkinter.CTkButton(master=transaction_colour_frame, text="", hover=False,
                                                           fg_color="transparent", image=new_image)
                    image_button.grid(row=0, column=0)

                # If the address of who sent the transaction is not our own address, that means we are receiving
                elif addressWho != pyaddress:

                    # We find the total value sent that does not include any outputs to that person.
                    tx_value = tx.findTotalValueSent(addressWho)
                    transaction_value = customtkinter.CTkLabel(master=transaction_frame, text=f"Value: {tx_value}",
                                                               font=customtkinter.CTkFont(size=14, family="Montserrat"))
                    total_in += tx_value
                    transaction_value.grid(row=1, column=0, sticky="w", padx=5, pady=5)

                    # This will display who sent us this transaction
                    transaction_from = customtkinter.CTkLabel(master=transaction_frame, text=f"Sent From: {addressWho}",
                                                              font=customtkinter.CTkFont(size=14, family="Montserrat"))
                    transaction_from.grid(row=2, column=0, sticky="w", padx=5, pady=5)

                    transaction_colour_frame = customtkinter.CTkFrame(master=transaction_frame, fg_color="#6bde57")
                    transaction_colour_frame.grid_rowconfigure(0, weight=1)
                    transaction_colour_frame.grid_rowconfigure(1, weight=0)
                    transaction_colour_frame.grid_columnconfigure(0, weight=1)
                    transaction_colour_frame.grid_columnconfigure(1, weight=0)
                    transaction_colour_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")

                    image = Image.open('images/icons/plusIcon.png')
                    new_image = customtkinter.CTkImage(dark_image=image, size=(50, 50))
                    image_button = customtkinter.CTkButton(master=transaction_colour_frame, text="", hover=False,
                                                           fg_color="transparent", image=new_image)
                    image_button.grid(row=0, column=0)

                # If the user sent the transaction, we are sending currency to another person
                elif addressWho == pyaddress:

                    # We find who we are sending the transaction to.
                    for addr in tx.outputAddress():
                        if addr == pyaddress:
                            pass
                        else:
                            toaddr = addr
                            break

                    # Finding the value disregarding any outputs directed to us
                    tx_value = tx.findTotalValueSent(pyaddress)
                    transaction_value = customtkinter.CTkLabel(master=transaction_frame, text=f"Value: {tx_value}",
                                                               font=customtkinter.CTkFont(size=14, family="Montserrat"))
                    # Incrementing the total out by the value
                    total_out += tx_value
                    transaction_value.grid(row=1, column=0, sticky="w", padx=5, pady=5)
                    transaction_from = customtkinter.CTkLabel(master=transaction_frame, text=f"Sent To: {toaddr}",
                                                              font=customtkinter.CTkFont(size=14, family="Montserrat"))
                    transaction_from.grid(row=2, column=0, sticky="w", padx=5, pady=5)

                    # The colour is now red as we are sending.
                    transaction_colour_frame = customtkinter.CTkFrame(master=transaction_frame, fg_color="#eb4034")
                    transaction_colour_frame.grid_rowconfigure(0, weight=1)
                    transaction_colour_frame.grid_rowconfigure(1, weight=0)
                    transaction_colour_frame.grid_columnconfigure(0, weight=1)
                    transaction_colour_frame.grid_columnconfigure(1, weight=0)
                    transaction_colour_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")

                    # We also have another image clearly showing that we are sending
                    image = Image.open('images/icons/sendingIcon.png')
                    new_image = customtkinter.CTkImage(dark_image=image, size=(50, 50))
                    image_button = customtkinter.CTkButton(master=transaction_colour_frame, text="", hover=False,
                                                           fg_color="transparent", image=new_image)
                    image_button.grid(row=0, column=0)

                # We also update the balance and corresonding labels
                self.balance = total_in - total_out
                balance_label.configure(text=f"Balance: {self.balance} pyCoins")
                self.balance_label.configure(text=f"Balance: {self.balance} pyCoins")

                # Grid configurations for the latest transactions
                self.latest_transaction_one.grid_rowconfigure(0, weight=1)
                self.latest_transaction_one.grid_rowconfigure(1, weight=0)
                self.latest_transaction_one.grid_columnconfigure(0, weight=1)
                self.latest_transaction_one.grid_columnconfigure(1, weight=0)

                self.latest_transaction_two.grid_rowconfigure(0, weight=1)
                self.latest_transaction_two.grid_rowconfigure(1, weight=0)
                self.latest_transaction_two.grid_columnconfigure(0, weight=1)
                self.latest_transaction_two.grid_columnconfigure(1, weight=0)

                self.latest_transaction_three.grid_rowconfigure(0, weight=1)
                self.latest_transaction_three.grid_rowconfigure(1, weight=0)
                self.latest_transaction_three.grid_columnconfigure(0, weight=1)
                self.latest_transaction_three.grid_columnconfigure(1, weight=0)

                # We update the labels in a try as in our blockchain we may have less than three transactions
                # (unlikely but still needs to be looked at)
                try:
                    # Label for the latest transaction
                    label_tx_one = customtkinter.CTkLabel(master=self.latest_transaction_one, text=f"TXID: {txs[-1].txid}",
                                                          font=customtkinter.CTkFont(size=14, family="Montserrat",
                                                                                     weight="bold"))
                    label_tx_one.grid(row=0, column=0, sticky="w", padx=5)

                    # Label for the second latest transaction
                    label_tx_two = customtkinter.CTkLabel(master=self.latest_transaction_two, text=f"TXID: {txs[-2].txid}",
                                                          font=customtkinter.CTkFont(size=14, family="Montserrat",
                                                                                     weight="bold"))
                    label_tx_two.grid(row=0, column=0, sticky="w", padx=5)

                    # Label for the third latest transacition
                    label_tx_three = customtkinter.CTkLabel(master=self.latest_transaction_three, text=f"TXID: {txs[-3].txid}",
                                                            font=customtkinter.CTkFont(size=14, family="Montserrat",
                                                                                       weight="bold"))
                    label_tx_three.grid( row=0, column=0, sticky="w", padx=5)

                except:
                    pass

        # The following code will be about the connect tab this is where you enter an IP address and then trying to
        # connect to an IP, once the ip connection has been made, we can add the peer ip to a json file.

        # The connect tab grid configuration
        connect.grid_rowconfigure((0, 1, 2, 3), weight=19)
        connect.grid_rowconfigure(1, weight=1)
        connect.grid_rowconfigure(4, weight=0)
        connect.grid_columnconfigure((0, 1), weight=1)
        connect.grid_columnconfigure(2, weight=0)

        # Some labels to describe the process of connecting.
        connect_label = customtkinter.CTkLabel(master=connect, text="Type in a IP address, and click connect a pop up"
                                                                    " should appear after a successful connection.",
                                               font=customtkinter.CTkFont(size=18, family="Montserrat"))
        connect_label.grid(row=0, column=0, columnspan=2)

        connect_label_details = customtkinter.CTkLabel(master=connect, text="After clicking the button to connect, "
                                                                            "the app may be unresponsive for around one"
                                                                            " minute, please give it time to connect to"
                                                                            " a peer, if the connection is unsuccessful"
                                                                            " a pop should appear.",
                                                       font=customtkinter.CTkFont(size=14, family="Montserrat"),
                                                       wraplength=400, justify="left")
        connect_label_details.grid(row=1, column=0, sticky="s")

        # The connect entry where you type an ip address.
        self.connect_entry = customtkinter.CTkEntry(master=connect, placeholder_text="IP Address",
                                                    font=customtkinter.CTkFont(size=20, family="Montserrat"),
                                                    height=40, width=170)
        self.connect_entry.grid(row=2, column=0, padx=20, sticky="s", pady=50)

        # The connect button which connects to the ip typed in the entry
        connect_button = customtkinter.CTkButton(master=connect, text="Connect", fg_color="#533fd3",
                                                 hover_color="#2c1346",
                                                 font=customtkinter.CTkFont(size=20, family="Montserrat"),
                                                 command=self.connectToPeer)
        connect_button.grid(row=3, column=0, sticky="n", padx=30)

        # Label for active connections
        connections_label = customtkinter.CTkLabel(master=connect, text="Active Connections:",
                                                   font=customtkinter.CTkFont(size=20, family="Montserrat"))
        connections_label.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Scrollable frame for all active connections
        self.connections_frame = customtkinter.CTkScrollableFrame(master=connect)
        self.connections_frame.grid(row=2, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.connections_frame.grid_columnconfigure(0, weight=1)
        self.connections_frame.grid_columnconfigure(1, weight=0)

        # Here we check if all the connections have been displayed we do this by, after we connect to a user we add the
        # frame and state they have been connected, but we don't check if anyone else has connected to us.
        # To update the frame we have another list, and when we connect with anyone, we add them to our list. But then
        # to check if anyone has joined us, we check for peers that are in self.peer.peers but not in list of peers.

        if self.peer:
            # We need to iterate through each peer in self.peer.peers, and check if any of those peers are not in
            # self.listOfPeers thus we need to add another frame for the new peer that connected to us.
            for peer in self.peer.peers:
                if peer.getpeername() not in self.listOfPeers:

                    # If there is a peer that is not in listOfPeers we add it to the list
                    self.listOfPeers.append(peer)

                    # We can also create another top level showing a peer has connected.
                    connection_top_level = customtkinter.CTkToplevel(self)
                    connection_top_level.geometry("200x50")
                    connection_top_level.title("Pychain Connect")
                    connection_top_level.resizable(False, False)

                    # Label saying peer has connected
                    peer_connection_label = customtkinter.CTkLabel(master=connection_top_level,
                                                                   text=f"{peer.getpeername()} has connected!",
                                                                   font=customtkinter.CTkFont(size=14,
                                                                                              family="Montserrat"))
                    peer_connection_label.pack(anchor="center")

                    # This is the connection frame we create and put into our connections frame
                    connection_frame = customtkinter.CTkFrame(master=self.connections_frame, fg_color="black")

                    # Grid configuration
                    connection_frame.grid_rowconfigure(0, weight=1)
                    connection_frame.grid_rowconfigure(1, weight=0)
                    connection_frame.grid_columnconfigure(0, weight=1)
                    connection_frame.grid_columnconfigure(1, weight=9)
                    connection_frame.grid_columnconfigure(2, weight=0)

                    # We put the connection into the row index of the list of peers-1
                    connection_frame.grid(row=len(self.peer.peers) - 1, sticky="nsew")

                    # We also want to put an image of a green dot, signifying a connection
                    connection_image = Image.open("images/icons/greenicon.png")
                    connection_img = customtkinter.CTkImage(dark_image=connection_image, size=(20, 20))
                    connection_Image_Button = customtkinter.CTkButton(master=connection_frame, image=connection_img,
                                                                      text="", fg_color="transparent", hover=False)
                    connection_Image_Button.grid(row=0, column=0, sticky="w", padx=(5, 0))

                    # This is the label stating that an ip is connected.
                    connection_label = customtkinter.CTkLabel(master=connection_frame,
                                                              text=f"{peer.getpeername()[0]} is connected!",
                                                              font=customtkinter.CTkFont(size=14,
                                                                                         family="Montserrat"))
                    connection_label.grid(row=0, column=1, sticky="w")

                    # Here we append the peers list
                    with open("json/currentAccount.json") as data:
                        data = json.load(data)

                    data['peers'].append(peer.getpeername()[0])

                    with open("json/currentAccount.json", "w") as f:
                        json.dump(data, f)

            # If the lists are not equal meaning that someone left us, we will basically rebuild the whole frame based
            # on the peers in self.peer.peers
            if self.listOfPeers != self.peer.peers:
                self.listOfPeers = []

                # We also need to clear the current connected peers in 'currentAccount.json'
                with open("json/currentAccount.json") as file:
                    data = json.load(file)

                data["peers"] = []

                with open("json/currentAccount.json", "w") as file:
                    json.dump(data, file, indent=2)

                # Here we remove the whole frame that contains all the connections
                for widgets in self.connections_frame.winfo_children():
                    widgets.destroy()

                # We now iterate through the peers in self.peer.peers
                for peer in self.peer.peers:

                    # We also need to append the peer into listOfPeers basically copying self.peer.peers into
                    # self.listOfPeers
                    self.listOfPeers.append(peer)

                    # This is the connection frame we create and put into our connections frame
                    connection_frame = customtkinter.CTkFrame(master=self.connections_frame, fg_color="black")

                    # Grid configuration
                    connection_frame.grid_rowconfigure(0, weight=1)
                    connection_frame.grid_rowconfigure(1, weight=0)
                    connection_frame.grid_columnconfigure(0, weight=1)
                    connection_frame.grid_columnconfigure(1, weight=9)
                    connection_frame.grid_columnconfigure(2, weight=0)

                    # We put the connection into the row index of the list of peers-1
                    connection_frame.grid(row=len(self.peer.peers) - 1, sticky="nsew")

                    # We also want to put an image of a green dot, signifying a connection
                    connection_image = Image.open("images/icons/greenicon.png")
                    connection_img = customtkinter.CTkImage(dark_image=connection_image, size=(20, 20))
                    connection_Image_Button = customtkinter.CTkButton(master=connection_frame, image=connection_img,
                                                                      text="", fg_color="transparent", hover=False)
                    connection_Image_Button.grid(row=0, column=0, sticky="w", padx=(5, 0))

                    # This is the label stating that an ip is connected.
                    connection_label = customtkinter.CTkLabel(master=connection_frame,
                                                              text=f"{peer.getpeername()[0]} is connected!",
                                                              font=customtkinter.CTkFont(size=14,
                                                                                         family="Montserrat"))
                    connection_label.grid(row=0, column=1, sticky="w")

                    # Here we append the peers list
                    with open("json/currentAccount.json") as data:
                        data = json.load(data)

                    data['peers'].append(peer.getpeername()[0])

                    with open("json/currentAccount.json", "w") as f:
                        json.dump(data, f, indent=2)

        # The following code will be about the blocks tabs, this will instantiate the blockchain and will display all
        # the current blocks, we can do this by making it into scrollable frame, and inside we will have frames, that
        # contain the block details, we will order the blocks by the latest at the top of the tab. The individual block
        # frames will contain a button that once clicked opens a new top-level containing all the details of the block.

        # Blocks Tab grid configuration
        blocks.grid_rowconfigure(0, weight=1)
        blocks.grid_rowconfigure(1, weight=19)
        blocks.grid_rowconfigure(2, weight=0)
        blocks.grid_columnconfigure(0, weight=1)
        blocks.grid_columnconfigure(1, weight=0)

        # Label to describe what is going on.
        blocks_label = customtkinter.CTkLabel(master=blocks, text="These are the current blocks, that are loaded in. "
                                                                  "The latest blocks are at the top.",
                                              font=customtkinter.CTkFont(size=20, family="Montserrat"))
        blocks_label.grid(row=0, column=0, sticky="nsew")

        # Frame to hold all other blocks.
        blocks_frame = customtkinter.CTkScrollableFrame(master=blocks)
        blocks_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        blocks_frame.grid_rowconfigure(0, weight=1)
        blocks_frame.grid_columnconfigure(0, weight=1)
        blocks_frame.grid_columnconfigure(1, weight=0)

        # Here we are going through our list of blocks and then adding them to the respective row, this way we can put
        # the blocks in order.

        if self.peer:
            count = len(self.peer.blockchain.blocks)

            for block in self.peer.blockchain.blocks:
                # We create a frame for each of these blocks, inside each frame we will put a button, and the miner who
                # mined it

                # The frame grid configuration
                block_frame = customtkinter.CTkFrame(master=blocks_frame, fg_color="black")
                block_frame.grid(row=count, padx=5, pady=5, sticky="nsew")
                block_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
                block_frame.grid_rowconfigure(6, weight=0)
                block_frame.grid_columnconfigure(0, weight=1)
                block_frame.grid_columnconfigure(1, weight=0)

                # We decrement count at every block to go from the end of the list to the start of the list
                count -= 1

                # We have a label that says the block height for each block
                block_height_label = customtkinter.CTkLabel(master=block_frame, text=f"Block Height: {block.height}",
                                                            fg_color="transparent",
                                                            font=customtkinter.CTkFont(size=20, family="Montserrat",
                                                                                       weight="bold"))
                block_height_label.grid(row=0, column=0, sticky="nw", padx=10, pady=5)

                # We have a label that says 'Block Details' this is for clarity.
                block_details_label = customtkinter.CTkLabel(master=block_frame, text="Block Details",
                                                             fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=15, family="Montserrat",
                                                                                        weight="bold"))
                block_details_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

                # Here we turn the blocks block-time into a date format, turn the nonce into a readable format by giving
                # it commas, and we are also formatting the transactions into a readable format
                date = int(block.blocktime)
                date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
                blockNonce = int(block.nonce)
                blockNonce = "{:,}".format(blockNonce)
                transactions_text = ""
                for transaction in block.transactions:
                    transactions_text += json.dumps(transaction.tx, indent=2)

                # This is a label containing many of the descriptors of the block.
                block_label = customtkinter.CTkLabel(master=block_frame, text=f"Block ID:                        {block.blockid}\n"
                                                                              f"Previous Block ID:      {block.previousblockhash}\n"
                                                                              f"Merkle Hash:                {block.merkle}\n"
                                                                              f"Block Miner:                 {block.miner}\n"
                                                                              f"Block Nonce:                {blockNonce}\n",
                                                     font=customtkinter.CTkFont(size=12, family="Montserrat"),
                                                     justify="left")
                block_label.grid(row=2, column=0, sticky="nsew")

                # This is the label to indicate the next texts are transactions, this is used for clarity
                transaction_details_label = customtkinter.CTkLabel(master=block_frame, text="Transactions",
                                                                   font=customtkinter.CTkFont(size=15,
                                                                                              family="Montserrat",
                                                                                              weight="bold"))
                transaction_details_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

                # This is the label that states all the transactions in their dictionary format.
                transactions_label = customtkinter.CTkLabel(master=block_frame, text=transactions_text,
                                                            font=customtkinter.CTkFont(size=12, family="Montserrat"),
                                                            anchor="center", justify="left")
                transactions_label.grid(row=4, column=0, sticky="nsew")

                # This is the final label which indicates the time the block was mined.
                block_time_label = customtkinter.CTkLabel(master=block_frame, text=date,
                                                          font=customtkinter.CTkFont(size=14, family="Montserrat",
                                                                                     weight="bold"))
                block_time_label.grid(row=5, sticky="nsew")

        # The following code is the mine tab, this shows the recent blocks that the user has mined, this also shows
        # a description on how to mine some pycoins.

        # The mine tabs grid configuration
        mine.grid_rowconfigure((0, 1), weight=1)
        mine.grid_rowconfigure(2, weight=3)
        mine.grid_rowconfigure(3, weight=0)
        mine.grid_columnconfigure((0, 1, 2), weight=1)
        mine.grid_columnconfigure(3, weight=0)

        # The title of the tab.
        mine_label = customtkinter.CTkLabel(master=mine, text="Mine Pycoins by running the mine.py script, this will "
                                                              "try to find new blocks! \nMining rewards are 100 "
                                                              "Pycoins. Below will show blocks you have mined.\n\n"
                                                              "Note: You cannot use this GUI and the mining script"
                                                              " at the same time, peers that you have connected here "
                                                              "will transfer to the mining script.",
                                            font=customtkinter.CTkFont(size=20, family="Montserrat"), wraplength=1000)

        mine_label.grid(row=0, column=0, sticky="nsew", columnspan=3)

        # Button to mine pycoins.
        mine_button = customtkinter.CTkButton(master=mine, text="Refresh",
                                              font=customtkinter.CTkFont(size=18, family="Montserrat"),
                                              fg_color="#533fd3", hover_color="#2c1346", width=125, height=75,
                                              command=self.blocksListen)

        mine_button.grid(row=1, column=1, sticky="n")

        # Stackable frame for blocks that have been mined by user.
        self.blocks_mined = customtkinter.CTkScrollableFrame(master=mine)
        self.blocks_mined.grid(row=2, column=0, sticky="nsew", columnspan=3, padx=20, pady=(0, 20))
        self.blocks_mined.grid_columnconfigure(0, weight=1)
        self.blocks_mined.grid_columnconfigure(1, weight=0)

        # The sidebar has 5 user buttons: Home, Settings, CLI, Create Address, Logout

        # Home button.
        home_button_image = Image.open("images/icons/homeIcon.png")
        home_button_img = customtkinter.CTkImage(dark_image=home_button_image, size=(40, 40))
        home_button = customtkinter.CTkButton(master=sidebar_frame, image=home_button_img, width=40, height=40, text="",
                                              fg_color="transparent", hover_color="grey", command=self.gui)
        home_button.grid(row=0, sticky="nsew")

        # Settings Button
        settings_button_image = Image.open("images/icons/settingsIcon.png")
        settings_button_img = customtkinter.CTkImage(dark_image=settings_button_image, size=(40, 40))
        settings_button = customtkinter.CTkButton(master=sidebar_frame, image=settings_button_img, width=40, height=40,
                                                  text="", fg_color="transparent", hover_color="grey", command=self.settings)
        settings_button.grid(row=1, sticky="nsew")

        # Create account button
        CreateAccount_button_image = Image.open("images/icons/createUserIcon.png")
        CreateAccount_button_img = customtkinter.CTkImage(dark_image=CreateAccount_button_image, size=(40, 40))
        CreateAccount_button = customtkinter.CTkButton(master=sidebar_frame, image=CreateAccount_button_img, width=40,
                                                       height=40, text="", fg_color="transparent", hover_color="grey",
                                                       command=self.CreateNewAccount)
        CreateAccount_button.grid(row=2, sticky="nsew")

        # Exit button
        Exit_button_image = Image.open("images/icons/logoutIcon.png")
        Exit_button_img = customtkinter.CTkImage(dark_image=Exit_button_image, size=(40, 40))
        Exit_button = customtkinter.CTkButton(master=sidebar_frame, image=Exit_button_img, width=40, height=40, text="",
                                              fg_color="transparent", hover_color="grey", command=self.start)
        Exit_button.grid(row=3, sticky="nsew")

    def createNode(self):
        # This grabs the blockchain that is selected.
        blockchainfile = self.blockchain_selector.get()

        # This gets the local ip address, by connecting to google's public domain and seeing what the IP is.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]

        # This creates a peer using the blockchain that got selected.
        self.peer = Peer(f"blockchains/{blockchainfile}", ip, 50000, 50500, 10, self.account['privateKey'])
        listenUDPThread = threading.Thread(target=self.peer.listenOnUDP)
        listenUDPThread.start()
        self.select_blockchain_button.configure(state="disabled")
        self.blockchain_selector.configure(values=[blockchainfile])
        self.blockchain_selector.configure(state="disabled")

        # As a node is created we want to update our currentAccount.json as this is what will be used in the
        # mining script.

        data = {
            "blockchainfile": f"blockchains/{blockchainfile}",
            "host": ip,
            "portMin": 50000,
            "portMax": 50500,
            "maxPeers": 10,
            "privateKey": self.account['privateKey'],
            "peers": [],
            "mempool": []
        }

        with open('json/currentAccount.json', 'w') as current:
            json.dump(data, current, indent=2)

        self.gui()

    def connectToPeer(self):

        # This function will get what is stored in the entry and then try to connect to that peer.
        ip = self.connect_entry.get()

        # We first check if there is a peer object, this is created when the blockchain is selected.
        if self.peer:

            # We then check if the IP is not already a peer
            if self.peer.checkIPisPeer(ip) is False:

                # We try to connect to the peer and then clear the entry.
                connection_success = self.peer.connectToPeer(ip)
                self.connect_entry.delete(0, 16)

                # If the connection is successful we can add it to our current connections frame and
                # then add it to our current peers in currentAccount.json
                if connection_success:

                    # Successful connection top-level
                    success_top_level = customtkinter.CTkToplevel(self)
                    success_top_level.geometry("200x50")
                    success_top_level.title("Pychain Connect")
                    success_top_level.resizable(False, False)

                    # Label saying peer has connected
                    success_label = customtkinter.CTkLabel(master=success_top_level, text="Peer Connected!",
                                                           font=customtkinter.CTkFont(size=14, family="Montserrat"))
                    success_label.pack(anchor="center")

                    # This is the connection frame we create and put into our connections frame
                    connection_frame = customtkinter.CTkFrame(master=self.connections_frame, fg_color="black")

                    # Grid configuration
                    connection_frame.grid_rowconfigure(0, weight=1)
                    connection_frame.grid_rowconfigure(1, weight=0)
                    connection_frame.grid_columnconfigure(0, weight=1)
                    connection_frame.grid_columnconfigure(1, weight=9)
                    connection_frame.grid_columnconfigure(2, weight=0)

                    # We put the connection into the row index of the list of peers-1
                    connection_frame.grid(row=len(self.peer.peers)-1, sticky="nsew")

                    # We also want to put an image of a green dot, signifying a connection
                    connection_image = Image.open("images/icons/greenicon.png")
                    connection_img = customtkinter.CTkImage(dark_image=connection_image, size=(20, 20))
                    connection_Image_Button = customtkinter.CTkButton(master=connection_frame, image=connection_img,
                                                                      text="", fg_color="transparent", hover=False)
                    connection_Image_Button.grid(row=0, column=0, sticky="w", padx=(5, 0))

                    # This is the label stating the ip has connected.
                    connection_label = customtkinter.CTkLabel(master=connection_frame, text=f"{ip} is connected!",
                                                              font=customtkinter.CTkFont(size=14, family="Montserrat",))
                    connection_label.grid(row=0, column=1, sticky="w")

                    # Here we append the peers list
                    with open("json/currentAccount.json") as file:
                        data = json.load(file)

                    data['peers'].append(ip)

                    with open("json/currentAccount.json", "w") as file:
                        json.dump(data, file, indent=2)

                    self.listOfPeers.append(ip)

                    self.peer.RequestBlockCount()

                else:
                    # This is incase the connection is unsuccessful, we display another toplevel.
                    self.generateErrorLabel("Pychain Connect", "Connection was unsuccessful.")
            else:
                # THis is incase the ip we are trying to connect to is already a peer.
                self.generateErrorLabel("Pychain Connect", "Ip is already a peer.")
        else:
            # This is incase the peer object hasn't been created, thus a blockchain has not been selected.
            self.generateErrorLabel("Pychain Connect", "Node has not connected to a blockchain.")

    def blocksListen(self):
        # This function is used for listening for blocks that are mined by the user and then will append that
        # block into the frame in the mine tab
        if self.peer:
            # We need calculate the users pychain address
            miner_address = address.createAddress(self.account_pubkey)
            self.usermined_blocks = []

            # We iterate through each block in our blockchain
            for block in self.peer.blockchain.blocks:

                # And we check if the blocks miner is the user
                if block.miner == miner_address:

                    # We calculate the index of where to place the frame
                    index = len(self.usermined_blocks)

                    # We create a frame for the user-mined-block
                    block_mined_frame = customtkinter.CTkFrame(master=self.blocks_mined, fg_color="black")
                    block_mined_frame.grid(row=index, padx=10, pady=10, sticky="nsew")
                    block_mined_frame.grid_rowconfigure((0, 1), weight=1)
                    block_mined_frame.grid_rowconfigure(2, weight=0)
                    block_mined_frame.grid_columnconfigure(0, weight=1)
                    block_mined_frame.grid_columnconfigure(1, weight=0)

                    self.usermined_blocks.append(block)

                    # This is the label inside the frame,
                    label = customtkinter.CTkLabel(master=block_mined_frame, text=f"Block Id = {block.blockid}",
                                                   font=customtkinter.CTkFont(size=18, family="Montserrat",
                                                                              weight="bold"))
                    label.grid(row=0, column=0, sticky="nsew", padx=6)

                    # This is the label for the reward of the block
                    reward_label = customtkinter.CTkLabel(master=block_mined_frame, text="Reward = 100 pyCoins",
                                                          font=customtkinter.CTkFont(size=13, family="Montserrat"))
                    reward_label.grid(row=1, column=0, sticky="nsew", pady=(0, 5))
        else:
            # If no blockchain is selected.
            self.generateErrorLabel("Pychain Mine", "Blockchain not selected.")

    def getAmount(self, value):
        self.value = round(value)
        self.amount_label.configure(text=f"{self.value} pyCoins")

    def createTransaction(self):
        # This function creates a transaction, by automatically using the UTXO's and creating script signatures and
        # the script pub keys.

        # Here we calculate the users pycharm address, this will be useful when creating return transactions.
        account_address = address.createAddress(self.account_pubkey)

        # We need to check if there is a value, this only occurs when the slider has been interacted with
        if self.value:

            # This checks that value we are trying to send does not exceed the balance
            if self.value <= self.balance:

                # Here we get the address that has been entered by the user.
                sendaddress = self.send_to_entry.get()

                if sendaddress[:2] != "69":
                    # We try to find an address saved as whats in the entry if its not in the correct format
                    with open('json/addressbook.json') as file:
                        data = json.load(file)

                    try:
                        index = 0
                        for value in data.values():
                            if sendaddress == value:
                                break
                            else:
                                index += 1

                        sendaddress = (list(data.keys())[index])

                    except:
                        self.generateErrorLabel("Pychain Send", "Address in incorrect format, or not in address book.")
                        return

                # Here we check that an address has been inputted.
                if sendaddress != '':
                    print("Sending to : " + sendaddress)
                    # We now check for the inputs and output transactions for the specific user key
                    inputs, outputs = self.peer.blockchain.findTxidsRelatingToKey(self.account_pubkey)

                    # We create two variables, inputTotal and remainder these will track total value we are
                    # trying to send and the difference if we are using transactions that have more value then what
                    # we are trying to send out.
                    inputTotal = 0
                    remainder = 0

                    inputTransactionsToUse = []

                    # We look at all the input transactions and until we have reached the value we are trying to send
                    # we keep on using more.
                    for transaction in inputs:
                        inputTransactionsToUse.append(transaction)
                        inputTotal += transaction.findTotalValueSent()
                        if inputTotal >= self.value:
                            remainder = inputTotal - self.value
                            break

                    # Here we create the script public keys, one for the actual transaction and one for the
                    # return transaction back to the user.
                    scriptPubkeys = []
                    p2pkh = spubKeycreator.createPayToPubKeyHashwithHash(sendaddress)
                    scriptPubkeys.append((p2pkh, self.value))
                    if remainder != 0:
                        p2pkh = spubKeycreator.createPayToPubKeyHash(self.account_pubkey)
                        scriptPubkeys.append((p2pkh, remainder))

                    print(p2pkh)

                    # The following code creates a transaction based on the script pub keys, and the input txids.
                    inputcounter = str(len(inputTransactionsToUse)).zfill(2)
                    txDict = {
                        "Version": "01",
                        "InputCount": inputcounter,
                    }

                    # This adds the input txids, and also gets the vout for the input transaction
                    for i in range(len(inputTransactionsToUse)):
                        vout = inputTransactionsToUse[i].outputAddress().index(account_address)
                        vout = (hex(vout)[2:]).zfill(4)
                        txDict[f"txid{i}"] = inputTransactionsToUse[i].txid
                        txDict[f"vout{i}"] = vout
                        txDict[f"sizeSig{i}"] = "0"
                        txDict[f"scriptSig{i}"] = "0"

                    # This adds the script pub keys and their value
                    outputcounter = str(len(scriptPubkeys)).zfill(2)
                    txDict["OutputCount"] = outputcounter
                    for i in range(len(scriptPubkeys)):
                        value = scriptPubkeys[i][1]
                        value = str(hex(int(value))[2:]).zfill(16)
                        scriptpubkey = scriptPubkeys[i][0]
                        print(len(scriptpubkey))
                        size = (hex(len(scriptpubkey))[2:]).zfill(4)
                        txDict[f"value{i}"] = value
                        txDict[f"sizePk{i}"] = size
                        txDict[f"scriptPubKey{i}"] = scriptpubkey

                    # We create the signature and then validate the transaction
                    rand = random.randint(0, address.n)
                    txDict["locktime"] = "00000000"
                    txDict, rawtx2 = scriptSigCreator.createDictWithSig(txDict, self.account['privateKey'], rand)
                    txraw = rawtxcreator.createTxFromDict(txDict)
                    tx = Transaction(txraw)
                    self.peer.validateTransaction(tx, self.account_pubkey)
                    self.peer.sendTransaction(tx.raw, self.account_pubkey)
                    with open('json/currentAccount.json') as file:
                        data = json.load(file)

                    data['mempool'].append(tx.raw)

                    with open('json/currentAccount.json', 'w') as file:
                        json.dump(data, file, indent=2)

                else:
                    self.generateErrorLabel("Pychain Send", "Account has not been entered.")
            else:
                self.generateErrorLabel("Pychain Send", "Value selected is more than balance.")
        else:
            self.generateErrorLabel("Pychain Send", "Value has not been selected.")

    def generateErrorLabel(self, title, message):
        # This generates a simple customizable error message, using this saves lots of copy and pasting.

        error_top_level = customtkinter.CTkToplevel(self)
        error_top_level.geometry("200x50")
        error_top_level.title(title)
        error_top_level.resizable(False, False)

        error_label = customtkinter.CTkLabel(master=error_top_level, text=message,
                                             font=customtkinter.CTkFont(size=14, family="Montserrat"), wraplength=190)

        error_label.pack(anchor="center")

    def settings(self):
        # This opens a new settings tab, which shows some settings such as
        #   - Account naming
        #   - Deleting Accounts with password

        # Settings for the tab
        settings_tab = customtkinter.CTkToplevel(self)
        settings_tab.geometry("800x600")
        settings_tab.title("Pychain Settings")
        settings_tab.resizable(False, False)

        # Grid config
        settings_tab.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        settings_tab.grid_columnconfigure((0, 1), weight=1)
        settings_tab.grid_columnconfigure(2, weight=0)

        # Settings label
        settings_label = customtkinter.CTkLabel(master=settings_tab, text="Settings Tab",
                                                font=customtkinter.CTkFont(size=20, family="Montserrat",
                                                                           weight="bold"))
        settings_label.grid(row=0, sticky="n", pady=(10, 0), columnspan=2)

        # Label for changing names for accounts
        name_change_label = customtkinter.CTkLabel(master=settings_tab,
                                                   text="Here you can add or change names for saved accounts.",
                                                   font=customtkinter.CTkFont(size=14, family="Montserrat"))
        name_change_label.grid(row=0, sticky="w", padx=20)

        # Frame for all the accounts
        with open('json/keys.json') as file:
            data = json.load(file)

        # We add the all pychain addresses into a list
        addresses = []
        for account in data:
            pubkey = address.ECmultiplication(account['privateKey'], address.Gx, address.Gy)
            miner = address.createAddress(pubkey)
            addresses.append(miner)

        # We remove the users address from the list and added
        user_address = address.createAddress(self.account_pubkey)
        addresses.remove(user_address)
        addresses.insert(0, user_address)

        # This is the address box used to select which address to modify.
        self.address_option_box = customtkinter.CTkOptionMenu(master=settings_tab, values=addresses,
                                                              command=self.changeImage, fg_color="#533fd3",
                                                              dropdown_hover_color="#533fd3", button_color="#2c1346")
        self.address_option_box.grid(row=0, column=0, sticky="sw", padx=20)

        # We should put an image so it's much easier to see what account to modify
        image = Image.open(self.account['iconPath'])
        new_image = customtkinter.CTkImage(dark_image=image, light_image=image, size=(100, 100))
        self.address_image_button = customtkinter.CTkButton(master=settings_tab, text="", fg_color="transparent",
                                                            image=new_image, anchor="center", hover=False)
        self.address_image_button.grid(row=0, column=1, sticky="e", padx=10)

        # A frame to hold an entry and a button for changing a name and saving it to the json files.
        address_config_frame = customtkinter.CTkFrame(master=settings_tab, height=125)
        address_config_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10, columnspan=2)

        address_config_frame.grid_rowconfigure(0, weight=1)
        address_config_frame.grid_rowconfigure((0, 1, 2, 3), weight=0)
        address_config_frame.grid_columnconfigure(0, weight=1)
        address_config_frame.grid_columnconfigure(1, weight=0)

        # This will be the button to change the name
        change_name_button = customtkinter.CTkButton(master=address_config_frame, text="Change name", fg_color="#533fd3"
                                                     , hover_color="#2c1346",
                                                     font=customtkinter.CTkFont(size=20, family="Montserrat"),
                                                     command=self.changeName)
        change_name_button.grid(row=0, sticky="w", padx=200, pady=(50, 0))

        # This is the button to delete the account.
        delete_account_button = customtkinter.CTkButton(master=address_config_frame, text="Delete Account",
                                                        fg_color="#ff4747", hover_color="#5e0000",
                                                        font=customtkinter.CTkFont(size=20, family="Montserrat"),
                                                        command=self.deleteAccount)
        delete_account_button.grid(row=0, sticky="e", padx=200, pady=(50, 0))

    def changeImage(self, text):
        # This function changes the account image, based on what you select on the option box.

        # We first need to open the file
        with open('json/keys.json') as file:
            data = json.load(file)

        # We look at each key in the json file
        for key in data:

            # and find the pychain address.
            public_key = address.ECmultiplication(key['privateKey'], address.Gx, address.Gy)
            py_address = address.createAddress(public_key)

            # once the account the user has selected in the entry box is found, we can update the image
            if py_address == text:

                filepath = key['iconPath']
                image = Image.open(filepath)
                newimage = customtkinter.CTkImage(dark_image=image, light_image=image, size=(100, 100))
                self.address_image_button.configure(image=newimage)

    def changeName(self):
        # This function serves to change the name for the account selected by the user.
        name = customtkinter.CTkInputDialog(text="Enter Name", title="Pychain Name Change", button_fg_color="#533fd3",
                                            button_hover_color="#2c1346")
        user_entered = name.get_input()
        if user_entered == "":
            return

        with open('json/keys.json') as file:
            data = json.load(file)

        text = self.address_option_box.get()

        # We again find the specific key in our 'json/keys.json' file, and then update the name
        for key in data:

            public_key = address.ECmultiplication(key['privateKey'], address.Gx, address.Gy)
            py_address = address.createAddress(public_key)

            if py_address == text:
                key['name'] = user_entered

                # We write it into our file and into our account object
                with open('json/keys.json', 'w') as file:
                    json.dump(data, file, indent=2)

                self.account['name'] = user_entered
                break

    def deleteAccount(self):
        # This function will prompt the user with a password entry and then if the password matches the hash then, we
        # can delete the account, and then return them to the login page.

        # The input for the password.
        password_input = customtkinter.CTkInputDialog(text="Enter that accounts password\nNote after deletion the "
                                                           "account is not restorable.", title="Pychain Delete Change",
                                                      button_fg_color="#533fd3", button_hover_color="#2c1346")

        # The following gets the password and hashes it, and also gets the pychain address of the account that is going
        # to be deleted
        password = password_input.get_input()
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        text = self.address_option_box.get()

        with open('json/keys.json') as file:
            data = json.load(file)

        # We again find the specific key in our 'json/keys.json' file, and then update the name
        for key in data:

            public_key = address.ECmultiplication(key['privateKey'], address.Gx, address.Gy)
            py_address = address.createAddress(public_key)

            # Once, we have found the address, we can check if the hashes match
            if py_address == text:
                if hash == key['passwordHash']:
                    # We remove it from the json file and we remove the icon.
                    data.remove(key)

                    filepath = key['iconPath']
                    os.remove(filepath)

                    with open('json/keys.json', 'w') as file:
                        json.dump(data, file, indent=2)

                    # The user will also return to the login page.
                    self.Login()
                    break
                else:
                    self.generateErrorLabel("Pychain Delete Account", "Password does not correlate with hash.")

    def saveSendAddress(self):
        # This function saves an address with a name, so that they can refer to a name instead of the address for future
        # transactions.

        # This gets the address in the entry
        addressEntry = self.send_to_entry.get()

        if addressEntry[:2] == "69":
            name_input = customtkinter.CTkInputDialog(text=f"Give a name for {addressEntry}",title="Pychain Address Book",
                                                      button_fg_color="#533fd3", button_hover_color="#2c1346")
            # Gets the input from the input dialog
            name = name_input.get_input()

            if name != "":

                # We store in 'addressbook.json'
                with open('json/addressbook.json') as file:
                    data = json.load(file)

                    data[addressEntry] = name

                with open('json/addressbook.json', "w") as file:
                    json.dump(data, file, indent=2)

                self.generateErrorLabel("Pychain Address Book", "Address added successfully")
            else:
                self.generateErrorLabel("Pychain Address Book", "Name is empty.")
        elif addressEntry == "":
            # If the user has not input any address we can show them a top level that shows the address book.
            address_book_top_level = customtkinter.CTkToplevel(self)
            address_book_top_level.geometry("600x800")
            address_book_top_level.title("Pychain Address Book")
            address_book_top_level.resizable(False, False)

            label = customtkinter.CTkLabel(master=address_book_top_level, text="Addresses Saved: ")
            label.pack()

            # This allows all of the saved address to be displayed in a nicer format.
            with open('json/addressbook.json') as file:
                data = json.load(file)

            label = customtkinter.CTkLabel(master=address_book_top_level, text=json.dumps(data, indent=2),
                                           font=customtkinter.CTkFont(size=14, family="Montserrat", weight="bold"),
                                           wraplength=575, anchor="w", justify="left")
            label.pack()

        else:
            self.generateErrorLabel("Pychain Address Book", "Invalid name format.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
