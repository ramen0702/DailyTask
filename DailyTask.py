import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("Daily Task")
        self.geometry(f"{1100}x{580}")
        self.minsize(300, 580)

        # レイアウトの設定(3×3)
        self.grid_rowconfigure((0,1,2), weight=0)
        self.grid_columnconfigure((0,2), weight=1)

        # 上部のバーの描画
        self.topbar_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.topbar_frame.grid(row=0,column=0,columnspan=3,padx=50,pady=50,sticky="nsew")
        self.topbar_frame.grid_columnconfigure(1, weight=1)
        self.topbar_frame.grid_columnconfigure((0,2), weight=0)
        self.today_label = customtkinter.CTkLabel(self.topbar_frame, text="2022/12/06", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.today_label.grid(row=0, column=1, padx=0, pady=10,sticky="nsew")
        self.prev_button = customtkinter.CTkButton(self.topbar_frame, text="◀", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.prev_button.grid(row=0, column=0, padx=50, pady=10,)
        self.next_button = customtkinter.CTkButton(self.topbar_frame, text="▶", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.next_button.grid(row=0, column=2, padx=50, pady=10,)

        # タスクの描画
        # これからやる

if __name__ == "__main__":
    app = App()
    app.mainloop()