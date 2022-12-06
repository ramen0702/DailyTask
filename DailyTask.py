import customtkinter
import tkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウの設定-----------------------------------------------------------------------------
        self.title("Daily Task")
        self.geometry(f"{1100}x{580}")
        self.minsize(300, 580)

        # レイアウトの設定(4×4)------------------------------------------------------------------------------------------
        self.grid_rowconfigure((0,1,2,3), weight=0)
        self.grid_columnconfigure((0,2), weight=1)

        # 上部のバーの表示------------------------------------------------------------------------------------------
        self.topbar_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.topbar_frame.grid(row=0,column=0,columnspan=3,padx=50,pady=50,sticky="nsew")
        self.topbar_frame.grid_columnconfigure(1, weight=1)
        self.topbar_frame.grid_columnconfigure((0,2), weight=0)
        # 本日の日付を表示
        self.today_label = customtkinter.CTkLabel(self.topbar_frame, text="2022/12/06", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.today_label.grid(row=0, column=1, padx=0, pady=10,sticky="nsew")
        # 進む、戻るボタンの表示
        self.prev_button = customtkinter.CTkButton(self.topbar_frame, text="◀", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.prev_button.grid(row=0, column=0, padx=50, pady=10,)
        self.next_button = customtkinter.CTkButton(self.topbar_frame, text="▶", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.next_button.grid(row=0, column=2, padx=50, pady=10,)

        # タスクの表示------------------------------------------------------------------------------------------
        self.main_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.main_frame.grid(row=1,column=0,columnspan=2,padx=50,pady=0,sticky="nsew")
        # 今は仮の辞書型を参照
        di = {"課題":True,"例題":False,"ジム":True,}
        for i in range(len(di)):
            # self.main_frame.grid_rowconfigure(i, weight=1)
            self.main_frame.grid_columnconfigure(i, weight=1)
        # 項目名の表示
        item_name = ["達成","タスク名"]
        self.item_label = [customtkinter.CTkLabel(
            self.main_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=25, weight="bold"))
            for name in item_name]
        for i in range(len(item_name)):
            self.item_label[i].grid(row=0, column=i, padx=0, pady=5)

        # チェックボックスの表示
        self.task_checkbox = []
        for _ in range(len(di)):
            self.task_checkbox.append(customtkinter.CTkCheckBox(master=self.main_frame,text="",))
        for i,key in enumerate(di):
            self.task_checkbox[i].grid(row=i+1, column=0, padx=0, pady=5,)
            if di[key]:
                self.task_checkbox[i].select()
        # タスク名の表示
        self.task_label = [customtkinter.CTkLabel(
            self.main_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=30, weight="bold"))
            for name in di]
        for i in range(len(di)):
            self.task_label[i].grid(row=i+1, column=1, padx=0, pady=5)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()