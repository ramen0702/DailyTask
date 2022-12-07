import customtkinter
import tkinter
import datetime

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
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
        self.dt_now = datetime.datetime.now()
        self.today_label = customtkinter.CTkLabel(self.topbar_frame, text=self.dt_now.strftime('%Y/%m/%d')
        , font=customtkinter.CTkFont(size=30, weight="bold"))
        self.today_label.grid(row=0, column=1, padx=0, pady=10,sticky="nsew")
        # 進む、戻るボタンの表示
        self.prev_button = customtkinter.CTkButton(self.topbar_frame, text="◀"
        , font=customtkinter.CTkFont(size=15, weight="bold"),command=self.prev_button_event)
        self.prev_button.grid(row=0, column=0, padx=50, pady=10,)
        self.next_button = customtkinter.CTkButton(self.topbar_frame, text="▶"
        , font=customtkinter.CTkFont(size=15, weight="bold"),command=self.next_button_event,state="disabled")
        self.next_button.grid(row=0, column=2, padx=50, pady=10,)

        # タスクの表示------------------------------------------------------------------------------------------
        self.main_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.main_frame.grid(row=1,column=0,columnspan=2,padx=50,pady=0,sticky="nsew")
        # 今は仮の辞書型を参照
        di = {"課題":True,"例題":False,"ジム":True,"体操":False,"お買い物":True}
        for i in range(len(di)):
            self.main_frame.grid_columnconfigure(i, weight=1)
        # 項目名の表示
        item_names = ["達成","タスク名"]
        self.item_label = [customtkinter.CTkLabel(
            self.main_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=25, weight="bold"))
            for name in item_names]
        for i in range(len(item_names)):
            self.main_frame.grid_rowconfigure(i, weight=1)
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
        

        # トロフィー（？）の表示------------------------------------------------------------------------------------------
        self.trophy_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.trophy_frame.grid(row=1,column=2,columnspan=2,padx=50,pady=0,sticky="nsew")
        # 仮テキストを表示
        self.tmp_label = customtkinter.CTkLabel(self.trophy_frame, text="トロフィー"
        , font=customtkinter.CTkFont(family="メイリオ",size=30, weight="bold"))
        # self.tmp_label.grid(row=0, column=0, padx=0, pady=100,sticky="nsew")
        self.tmp_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # メニューバー(下部)の表示------------------------------------------------------------------------------------------
        menu_names = ["追加","絞り込み","一覧","修正","管理",]
        self.menubar_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.menubar_frame.grid(row=2,column=0,columnspan=3,padx=50,pady=50,sticky="nsew")
        for i in range(len(menu_names)):
            self.menubar_frame.grid_columnconfigure(i, weight=1)
        # メニューボタンの表示
        self.menu_button = []
        for i in range(len(menu_names)):
            self.menu_button.append(customtkinter.CTkButton(master=self.menubar_frame,text=menu_names[i]))
        self.menu_button[0].configure(command=self.add_task_button)
        for i in range(len(menu_names)):
            self.menu_button[i].grid(row=0, column=i, padx=0, pady=5,)
    
    # イベトン用関数-----------------------------------------------------------------------------------------------
    # 翌日に進むボタン
    def next_button_event(self):
        self.dt_now += datetime.timedelta(days=1)
        self.today_label = customtkinter.CTkLabel(self.topbar_frame, text=self.dt_now.strftime('%Y/%m/%d')
        , font=customtkinter.CTkFont(size=30, weight="bold"))
        self.today_label.grid(row=0, column=1, padx=0, pady=10,sticky="nsew")
        if self.dt_now.strftime('%Y/%m/%d') == datetime.datetime.now().strftime('%Y/%m/%d'):
            self.next_button.configure(state="disabled")
        else:
            self.next_button.configure(state="normal")

    # 前日に戻るボタン
    def prev_button_event(self):
        self.next_button
        self.dt_now -= datetime.timedelta(days=1)
        self.today_label = customtkinter.CTkLabel(self.topbar_frame, text=self.dt_now.strftime('%Y/%m/%d')
        , font=customtkinter.CTkFont(size=30, weight="bold"))
        self.today_label.grid(row=0, column=1, padx=0, pady=10,sticky="nsew")
        self.next_button.configure(state="normal")
    
    # タスク追加ボタン
    def add_task_button(self):
        window = customtkinter.CTkToplevel(self)
        window.title("add task")
        window.geometry(f"{1100}x{580}")
        window.minsize(300, 580)

        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text="追加画面へようこそ")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)

        

if __name__ == "__main__":
    app = App()
    app.mainloop()
