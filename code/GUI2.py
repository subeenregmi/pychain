import customtkinter
import tkinter
import json
import random
import address
import hashlib
import requests
from PIL import Image
import shutil
from node import Peer
from datetime import datetime

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # We call a method as users may want to go back
        self.account=None
        self.peer = None
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
        self.grid_rowconfigure((0), weight=2)
        self.grid_rowconfigure((1,2), weight=2)
        self.grid_rowconfigure((3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Settings to create a frame in the first cell
        Title = customtkinter.CTkFrame(master=self, fg_color="transparent", border_color="grey")
        Title.grid(row=0)

        # Settings for the labels inside the frame
        Label = customtkinter.CTkLabel(master=Title, bg_color="transparent", text="Pychain",
                                       font=customtkinter.CTkFont(size=40, weight="bold"), width=130, height=40)

        Label.grid(row = 0, column = 0, padx=10)
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
        bottomTitle = customtkinter.CTkLabel(master=self, height=14, anchor="s", corner_radius=0, text="By Subeen Regmi", text_color="grey")
        bottomTitle.grid(row=3)

    def Login(self):
        # This is going to bring up the login page if the keys have been loaded in successfully.
        try:
            f = open("keys.json")
            data = json.load(f)
            print("LOADED")
            loaded = True
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
            loaded = False

        if loaded:
            # First we need to destroy all the previous widgets to clear the screen
            for widget in self.winfo_children():
                widget.destroy()
            self.grid_rowconfigure( (0, 1, 2, 3), weight=0 )
            self.grid_columnconfigure( (0, 1, 2, 3), weight=0 )
            # Geometry for the new window.
            self.title("Pycharm Login")
            self.geometry("1200x700")
            self.resizable(False, False)

            # We need to create a login page that contains a slider that displays the image and the pychain address
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

            # The button has the image of the icon, and once clicked cycles through the accounts.
            self.icon_button = customtkinter.CTkButton(master=frame, image=Icon, fg_color="transparent", text="",
                                                       hover_color="grey", command=self.switchAccounts)
            self.icon_button.grid(row=0, padx=10, pady=10)

            # This is the text box that holds the pychain address.
            self.pychain_address_label = customtkinter.CTkLabel(master=frame, text=pychain_address,
                                                                font=customtkinter.CTkFont(weight="bold", size=18))
            self.pychain_address_label.grid(row=1, column=0)

            # This is the entry that holds the password, this will be hashed and checked in order for a successful login
            self.password_entry = customtkinter.CTkEntry(master=self, placeholder_text="Password",
                                                    font=customtkinter.CTkFont(size=30))
            self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

            login_image = Image.open('icons/loginIcon.png')
            Login_icon = customtkinter.CTkImage(dark_image=login_image, size=(35, 35))

            # This is the button to log in to the account.
            login_button = customtkinter.CTkButton(master=self, text="", image=Login_icon, width=35, fg_color="#533FD3",
                                                   hover_color="#2c1346", command=self.loginToAccount)
            login_button.grid(row=1, column=2, sticky="w")

    def switchAccounts(self):
        # This function handles the account cycling mechanism in the login screen.

        # We load 'keys.json' into a format we can handle.
        with open('keys.json') as file:
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

    def loginToAccount(self):
        # This function is used in the login screen, to hash the password entered and if the password hash correlates
        # to the one saved then we go onto the actual GUI.

        # We are loading the keys into a python object.
        with open('keys.json') as keys:
            data = json.load(keys)

        # If the password's hash matches with the stored hash then we can move onto the gui
        account = data[self.account_index]
        password = self.password_entry.get()
        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        if account['passwordHash'] == hash_password:
            self.account = account
            self.peer = Peer("blockchain.txt", "192.168.0.111", 50000, 50500, 10, self.account['privateKey'])
            self.gui()

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
        # right column to be spanned to one column

        frameAddress = customtkinter.CTkFrame(master=self, fg_color="transparent")
        frameAddress.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Grid configuration stated previously
        frameAddress.grid_rowconfigure((0, 1, 2), weight=1)
        frameAddress.grid_columnconfigure(0, weight=4)
        frameAddress.grid_columnconfigure(1, weight=2)

        # Some text to describe the icon
        text = customtkinter.CTkLabel(master=frameAddress, text="This is an image generated based on your private key!", wraplength=125)
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
        self.text2k = customtkinter.CTkLabel(master=frame2, text="", wraplength=610, anchor="center")
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
        with open('icons/test.png', 'rb+') as file:
            file.write(r.content)
            image = Image.open(file)
            previewIcon = customtkinter.CTkImage(light_image=image, dark_image=image, size=(125, 125))
            self.previewIcon.configure(image=previewIcon,)

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
            # Here we store data about or keys, the password hash and the icon created.
            # We open the keys file, load it into an object, store the data, and then append that into the object and
            # then dump it into a json object.

            with open('keys.json') as keys:
                data = json.load(keys)

            count = len(data)
            keyInfo = {
                "privateKey": private_key,
                "passwordHash": password_hash,
                "iconPath": f"icons/account_icon{count}.png"
            }

            data.append(keyInfo)

            with open('keys.json', 'w') as keys:
                json.dump(data, keys, indent=2)

            # Here we copy the icon into another file, to be used later.
            shutil.copyfile('icons/test.png', f'icons/account_icon{count}.png')

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
        sidebar_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        sidebar_frame.grid_rowconfigure(5, weight=0)
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
        self.balance_label = customtkinter.CTkLabel(master=welcomeFrame, text="Balance: ",
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

        # A transactions button will also be on the home menu, below the button will be the three latest transactions,
        # but you can also click the button to go to the transaction tab
        transaction_label = customtkinter.CTkButton(master=home, text="Latest Transactions:", fg_color="transparent",
                                                    font=customtkinter.CTkFont(size=20, family="Montserrat"),
                                                    hover_color="grey")
        transaction_label.grid(row=1, column=0, sticky="nw", padx=5)

        # There will also be a frame for the three latest transactions, just below the transaction button
        transactions_frame = customtkinter.CTkFrame(master=home, fg_color="transparent")
        transactions_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        transactions_frame.grid_rowconfigure((0, 1, 2), weight=1)
        transactions_frame.grid_rowconfigure(3, weight=0)
        transactions_frame.grid_columnconfigure(0, weight=1)
        transactions_frame.grid_columnconfigure(1, weight=0)

        # There will be three frames inside the frame indicate the transactions. inside those frames we will have a
        # button and the label for the transaction details, we could also have an image to the left of the frame
        # indicating if the transaction was incoming or outgoing.

        self.latest_transaction_one = customtkinter.CTkFrame(master=transactions_frame, height=40)
        self.latest_transaction_one.grid(row=0, sticky="nsew", pady=(0, 5))

        self.latest_transaction_two = customtkinter.CTkFrame(master=transactions_frame, height=40)
        self.latest_transaction_two.grid(row=1, sticky="nsew", pady=(0, 5))

        self.latest_transaction_three = customtkinter.CTkFrame(master=transactions_frame, height=40)
        self.latest_transaction_three.grid(row=2, sticky="nsew")

        # A 'Latest Blocks' button, once clicked will go to the blocks tab.
        latest_blocks_label = customtkinter.CTkButton(master=home, text="Latest Blocks:", fg_color="transparent",
                                                      font=customtkinter.CTkFont(size=20, family="Montserrat"),
                                                      hover_color="grey")
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

        self.latest_block_two = customtkinter.CTkFrame(master=latest_blocks_frame, height=40)
        self.latest_block_two.grid(row=1, sticky="nsew", pady=(0, 5))

        self.latest_block_three = customtkinter.CTkFrame(master=latest_blocks_frame, height=40)
        self.latest_block_three.grid(row=2, sticky="nsew", pady=(0, 5))

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
                                                        font=customtkinter.CTkFont(size=20, family="Montserrat", weight="bold"))
            block_height_label.grid(row=0, column=0, sticky="nw", padx=10, pady=5)

            # We have a label that says 'Block Details' this is for clarity.
            block_details_label = customtkinter.CTkLabel(master=block_frame, text="Block Details",
                                                         fg_color="transparent",
                                                         font=customtkinter.CTkFont(size=15, family="Montserrat",
                                                                                    weight="bold"))
            block_details_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

            # Here we turn the blocks block-time into a date format, turn the nonce into a readable format by giving it
            # commas, and we are also formatting the transactions into a readable format
            date = int(block.blocktime)
            date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
            blockNonce = int(block.nonce)
            blockNonce = "{:,}".format(blockNonce)
            transactions_text = ""
            for transaction in block.transactions:
                print(json.dumps(transaction.tx, indent=3))
                transactions_text += json.dumps(transaction.tx, indent=2)

            # This is a label containing many of the descriptors of the block.
            block_label = customtkinter.CTkLabel(master=block_frame, text=f"Block ID: {block.blockid}\n"
                                                                          f"Previous Block ID: {block.previousblockhash}\n"
                                                                          f"Merkle Hash: {block.merkle}\n"
                                                                          f"Block Miner: {block.miner}\n"
                                                                          f"Block Nonce: {blockNonce}\n",
                                                 font=customtkinter.CTkFont(size=12, family="Montserrat"), justify="left")
            block_label.grid(row=2, column=0, sticky="nsew")

            # This is the label to indicate the next texts are transactions, this is used for clarity
            transaction_details_label = customtkinter.CTkLabel(master=block_frame, text="Transactions",
                                                               font=customtkinter.CTkFont(size=15, family="Montserrat",
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

        # The sidebar has 5 user buttons: Home, Settings, CLI, Create Address, Logout

        # Home button.
        home_button_image = Image.open("icons/homeIcon.png")
        home_button_img = customtkinter.CTkImage(dark_image=home_button_image, size=(40, 40))
        home_button = customtkinter.CTkButton(master=sidebar_frame, image=home_button_img, width=40, height=40, text="",
                                              fg_color="transparent", hover_color="grey")
        home_button.grid(row=0, sticky="nsew")

        # Settings Button
        settings_button_image = Image.open("icons/settingsIcon.png")
        settings_button_img = customtkinter.CTkImage(dark_image=settings_button_image, size=(40, 40))
        settings_button = customtkinter.CTkButton(master=sidebar_frame, image=settings_button_img, width=40, height=40,
                                                  text="", fg_color="transparent", hover_color="grey")
        settings_button.grid(row=1, sticky="nsew")

        # CLI button
        CLI_button_image = Image.open("icons/cliIcon.png")
        CLI_button_img = customtkinter.CTkImage(dark_image=CLI_button_image, size=(40, 40))
        CLI_button = customtkinter.CTkButton(master=sidebar_frame, image=CLI_button_img, width=40, height=40, text="",
                                             fg_color="transparent", hover_color="grey")
        CLI_button.grid(row=2, sticky="nsew")

        # Create account button
        CreateAccount_button_image = Image.open("icons/createUserIcon.png")
        CreateAccount_button_img = customtkinter.CTkImage(dark_image=CreateAccount_button_image, size=(40, 40))
        CreateAccount_button = customtkinter.CTkButton(master=sidebar_frame, image=CreateAccount_button_img, width=40,
                                                       height=40, text="", fg_color="transparent", hover_color="grey",
                                                       command=self.CreateNewAccount)
        CreateAccount_button.grid(row=3, sticky="nsew")

        # Exit button
        Exit_button_image = Image.open("icons/logoutIcon.png")
        Exit_button_img = customtkinter.CTkImage(dark_image=Exit_button_image, size=(40, 40))
        Exit_button = customtkinter.CTkButton(master=sidebar_frame, image=Exit_button_img, width=40, height=40, text="",
                                              fg_color="transparent", hover_color="grey", command=self.start)
        Exit_button.grid(row=4, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()