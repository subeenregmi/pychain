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

        #hide the previous window
        self.iconify()

        #create new window
        window = customtkinter.CTkToplevel(self)
        window.title("Pycharm")
        window.geometry("700x700")
        window.resizable(False, False)

        #protocol if window is closed
        window.protocol("WM_DELETE_WINDOW", self.deiconify())







if __name__ == "__main__":
    app = App()
    app.mainloop()