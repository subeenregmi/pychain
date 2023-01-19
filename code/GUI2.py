import customtkinter
import tkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pychain")
        self.geometry("260x450")
        
        self.grid_rowconfigure((0), weight=1)    
        self.grid_rowconfigure((1,2), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.Title = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self.Title.grid(row=0, padx=10, pady=10)
        self.Label = customtkinter.CTkLabel(master=self.Title, bg_color="transparent", text="Pychain", font=customtkinter.CTkFont(size=40, weight="bold"), width=130, height=40)
        self.Label.grid(row = 0, column = 0, padx=10, pady=10)
        self.SubTitle = customtkinter.CTkTextbox(master=self.Title, width=146,height=20)
        self.SubTitle.insert(index="0.0", text="A blockchain sandbox")
        self.SubTitle.grid(row=1, padx=0, pady=0)
        
        self.LoginButton = customtkinter.CTkButton(master=self, width=180, height=50, text="Login", font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="#533FD3", hover_color="#2c1346")
        self.LoginButton.grid(row=1, column=0, padx=20, pady=0)
       
        self.CreateButton = customtkinter.CTkButton(master=self, width=180, height=50, text="Create New Account", font=customtkinter.CTkFont(size=15, weight="bold"), fg_color="#533FD3", hover_color="#2c1346")
        self.CreateButton.grid(row=2, column=0, padx=20, pady=(0), sticky="n")

if __name__ == "__main__":
    app = App()
    app.mainloop()