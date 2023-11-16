import customtkinter as ctk
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure themes
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # configure window
        self.title("Result display")
        # self.iconbitmap('icon.ico')
        self.geometry(f"{980}x{450}")
        self.resizable(False, False)

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.widgets()
        
    
    def widgets(self):
        # style variables
        self.options = {"padx": (10, 10), "pady": (10, 10), "sticky": "nsew"}

        # output image frame
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=0, column=0, columnspan=3, **self.options)
        
        
    def addImages(self, img_path_1, img_path_2, img_path_3):
        img_size = (300, 300)
        self.outputFrame1 = ctk.CTkFrame(self.output_frame)
        self.outputFrame1.grid(row=0, column=0, **self.options)
        self.outputImage1 = ctk.CTkLabel(self.outputFrame1, image=ctk.CTkImage(Image.open(img_path_1), size=img_size), text="")
        self.outputImage1.pack(side="top", fill="both", expand=True)
        self.outputText1 = ctk.CTkLabel(self.outputFrame1, text="BFS")
        self.outputText1.pack(side="bottom", fill="both", expand=True)


        self.outputFrame2 = ctk.CTkFrame(self.output_frame)
        self.outputFrame2.grid(row=0, column=1, **self.options)
        self.outputImage2 = ctk.CTkLabel(self.outputFrame2, image=ctk.CTkImage(Image.open(img_path_2), size=img_size), text="")
        self.outputImage2.pack(side="top", fill="both", expand=True)
        self.outputText2 = ctk.CTkLabel(self.outputFrame2, text="Dijkstra")
        self.outputText2.pack(side="bottom", fill="both", expand=True)
        

        self.outputFrame3 = ctk.CTkFrame(self.output_frame)
        self.outputFrame3.grid(row=0, column=2, **self.options)
        self.outputImage3 = ctk.CTkLabel(self.outputFrame3, image=ctk.CTkImage(Image.open(img_path_3), size=img_size), text="")
        self.outputImage3.pack(side="top", fill="both", expand=True)
        self.outputText3 = ctk.CTkLabel(self.outputFrame3, text="A*")
        self.outputText3.pack(side="bottom", fill="both", expand=True)