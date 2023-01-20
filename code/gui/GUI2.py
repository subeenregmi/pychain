import customtkinter
import tkinter
import json
import time

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Settings for the window
        self.title("Pychain")
        self.geometry("225x350")
        self.resizable(False, False)

        #Settinngs for a 4x1 grid        
        self.grid_rowconfigure((0), weight=2)    
        self.grid_rowconfigure((1,2), weight=2)
        self.grid_rowconfigure((3), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #Settings to create a frame in the first cell
        self.Title = customtkinter.CTkFrame(master=self, fg_color="transparent", border_color="grey")
        self.Title.grid(row=0)

        #Settings for the labels inside the frame
        self.Label = customtkinter.CTkLabel(master=self.Title, bg_color="transparent", text="Pychain", font=customtkinter.CTkFont(size=40, weight="bold"), width=130, height=40)
        self.Label.grid(row = 0, column = 0, padx=10)
        self.SubTitle = customtkinter.CTkLabel(master=self.Title, text="A blockchain sandbox")
        self.SubTitle.grid(row=1, padx=10, pady=(10, 0), sticky="s")
        
        #Settings for the login button
        self.LoginButton = customtkinter.CTkButton(master=self, width=180, height=50, text="Login", font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="#533FD3", hover_color="#2c1346", command=self.Login)
        self.LoginButton.grid(row=1, column=0, padx=0, pady=0, sticky="s")
       
        #Settings for the create account button
        self.CreateButton = customtkinter.CTkButton(master=self, width=180, height=50, text="Create New Account", font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="#533FD3", hover_color="#2c1346", anchor="center", command=self.CreateNewAccount)
        self.CreateButton.grid(row=2, column=0, padx=0, pady=(0))

        #Settings for the bottom tile
        self.bottomTitle = customtkinter.CTkLabel(master=self, height=14, anchor="s", corner_radius=0, text="By Subeen Regmi", text_color="grey")
        self.bottomTitle.grid(row=3)
        

    def Login(self):
        try:
            f = open("keys.json")
            data = json.load(f)
            #Do something here, e.g: send to next menu.
            print("LOADED")
            f.close()
        except:
            #settings for window that pops up when the user does not have any keys stored in 'keys.json'
            window = customtkinter.CTkToplevel(self)
            window.geometry("200x100")
            window.resizable(False, False)

            #label inside the window
            label = customtkinter.CTkLabel(master=window, text="No account found!\n\nCreate a new account", anchor="center")
            label.pack(padx=20, pady=20)

            #greying out the login button after login fails
            self.LoginButton.configure(state="disabled", fg_color="grey")

    def CreateNewAccount(self):

        #hide the previous window // seems to only work on OSX well
        self.iconify()

        #create new window
        window = customtkinter.CTkToplevel(self)
        window.title("Pycharm")
        window.geometry("1200x700")
        window.resizable(False, False)

        #creating a 3 row gui, one for the title, one for the addressing, and the last one for passwords and saving
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=3)
        window.grid_rowconfigure(2, weight=1)
        window.grid_columnconfigure(0, weight=1)

        #frame for the top row to seperate the title on the left to the description on the right
        frameTitle = customtkinter.CTkFrame(master=window, border_width=3, border_color="#533FD3")
        frameTitle.grid(row=0, padx=10, pady=10, sticky="nsew")
        
        #setting up the 2 columns required for the title frame
        frameTitle.grid_columnconfigure(0, weight=1)
        frameTitle.grid_columnconfigure(1, weight=1)
        frameTitle.grid_rowconfigure(0, weight=1)

        #title at the top of the window, and the description on the right
        Label = customtkinter.CTkLabel(master=frameTitle, anchor="center", text="Pycharm")
        Label.grid(row=0, column=0, padx=10, pady=10)
        Label2 = customtkinter.CTkLabel(master=frameTitle, text="How to use:")
        Label2.grid(row=0, column=1, padx=10, pady=10)

        #frame for the next section requires, the private address view, the public address view, the pychain address view
        #and the randomly generated image, these need to be in a 3x2, with more weight on the left column and the right column to
        #be spanned to one column

        frameAddress = customtkinter.CTkFrame(master=window, fg_color="transparent")
        frameAddress.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # grid configurement stated previously
        frameAddress.grid_rowconfigure((0, 1, 2), weight=1)
        frameAddress.grid_columnconfigure(0, weight=4)
        frameAddress.grid_columnconfigure(1, weight=1)

        # Adding three frames, one for each row on the first column
        frame1 = customtkinter.CTkFrame(master=frameAddress, border_color="#533FD3", border_width=3)
        frame1.grid(row=0, column=0, sticky="nsew", pady=5)
        frame1.grid_rowconfigure(0, weight=1)
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_columnconfigure(1, weight=3)
                
        frame2 = customtkinter.CTkFrame(master=frameAddress, border_color="#533FD3", border_width=3)
        frame2.grid(row=1, column=0, sticky="nsew", pady=5)
        frame2.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_columnconfigure(1, weight=3)

        frame3 = customtkinter.CTkFrame(master=frameAddress, border_color="#533FD3", border_width=3)
        frame3.grid(row=2, column=0, sticky="nsew", pady=5)
        frame3.grid_rowconfigure(0, weight=1)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_columnconfigure(1, weight=3)

        # texts to go in each frame
        text1 = customtkinter.CTkLabel(master=frame1, text="Private Key :")
        text1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        text1 = customtkinter.CTkLabel(master=frame1, text="Key")
        text1.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        text2 = customtkinter.CTkLabel(master=frame2, text="Public Key :")
        text2.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        text2 = customtkinter.CTkLabel(master=frame2, text="Key")
        text2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
                
        text3 = customtkinter.CTkLabel(master=frame3, text="Pychain Address :")
        text3.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        text3 = customtkinter.CTkLabel(master=frame3, text="Key")
        text3.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        #Frame that stores entry for password and the save to json button
        frame4 = customtkinter.CTkFrame(master=window, border_color="grey")
        frame4.grid(row=2, column=0, sticky="nesw", padx=10, pady=(0,10))

        # Frame Configuration
        frame4.grid_rowconfigure(0, weight=1)
        frame4.grid_rowconfigure(1, weight=1)
        frame4.grid_columnconfigure(0, weight=1)
        frame4.grid_columnconfigure(1, weight=4)

        # Label for password 
        Label3 = customtkinter.CTkLabel(master=frame4, bg_color="#533FD3", text="Password :")
        Label3.grid(row=0, column=0, sticky="nesw", padx=10, pady=10)

        # Entry for password 
        passwordEntry = customtkinter.CTkEntry(master=frame4, font=customtkinter.CTkFont(size=20))
        passwordEntry.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

        # Butto
        passwordButton = customtkinter.CTkButton(master=frame4, anchor="center", text="Save and Quit", fg_color="#533FD3", hover_color="#2c1346")
        passwordButton.grid(row=1, column=0, columnspan=2, ipadx=10, ipady=10)

        #protocol if window is closed
        window.protocol("WM_DELETE_WINDOW", self.deiconify())



if __name__ == "__main__":
    app = App()
    app.mainloop()