import customtkinter
import tkinter
import datetime
import csv
import os
import subprocess

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウの設定-----------------------------------------------------------------------------
        self.title("Daily Task")
        self.geometry(f"{1100}x{580}+{100}+{100}")
        self.minsize(300, 580)

        # レイアウトの設定(2×2)------------------------------------------------------------------------------------------
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

         # メニューバー(左)の表示------------------------------------------------------------------------------------------
        self.menu_names = ["追加","絞り込み","一覧","修正","管理",]
        self.menubar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.menubar_frame.grid(row=0,column=0,rowspan=2,sticky="nsew")
        for i in range(len(self.menu_names)+1):
            self.menubar_frame.grid_rowconfigure(i, weight=1)
        # ロゴの表示
        self.logo_label = customtkinter.CTkLabel(self.menubar_frame, text="DailyTask", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # メニューボタンの表示
        self.menu_button = [customtkinter.CTkButton(master=self.menubar_frame,text=self.menu_names[i],font=customtkinter.CTkFont(family="メイリオ")) for i in range(len(self.menu_names))]
        self.menu_button[0].configure(command=self.add_task_button)
        for i in range(len(self.menu_names)):
            self.menu_button[i].grid(row=i+1, column=0, padx=50, pady=0,)

        # 日付フレーム(右上)の表示------------------------------------------------------------------------------------------
        self.topbar_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.topbar_frame.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
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

        # タスク欄の表示
        self.task_display()
    
    # タスク欄を表示するときの処理------------------------------------------------------------------------------------------
    def task_display(self):
        self.main_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.main_frame.grid(row=1,column=1,padx=20,pady=20,sticky="nsew")
        # タスク名をtask.csvから参照(型は辞書型でValueはすべてFalse)
        self.di = self.read_task()
        for i in range(len(self.di)+1):
            self.main_frame.grid_rowconfigure(i, weight=1)
        # 項目名の表示
        item_names = ["達成　　　","タスク名"]
        self.item_label = [customtkinter.CTkLabel(
            self.main_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=25, weight="bold"))
            for name in item_names]
        for i in range(len(item_names)):
            self.main_frame.grid_columnconfigure(i, weight=1)
            self.item_label[i].grid(row=0, column=i, padx=0, pady=5)

        # チェックボックスの表示
        self.task_checkbox = [customtkinter.CTkCheckBox(master=self.main_frame,text="",) for _ in range(len(self.di))]
        for i,key in enumerate(self.di):
            self.task_checkbox[i].grid(row=i+1, column=0, padx=0, pady=5,)
            if self.di[key]:
                self.task_checkbox[i].select()
        # タスク名の表示
        self.task_label = [customtkinter.CTkLabel(
            self.main_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=30, weight="bold"))
            for name in self.di]
        for i in range(len(self.di)):
            self.task_label[i].grid(row=i+1, column=1, padx=0, pady=5)
    
    # イベトン用関数-----------------------------------------------------------------------------------------------
    # 翌日に進むボタン
    def next_button_event(self):
        self.dt_now += datetime.timedelta(days=1)
        self.daily_func()

    # 前日に戻るボタン
    def prev_button_event(self):
        self.dt_now -= datetime.timedelta(days=1)
        self.daily_func()
    
    # 日数変更時の表示更新
    def daily_func(self):
        self.today_label.configure(text=self.dt_now.strftime('%Y/%m/%d'))
        if self.dt_now.strftime('%Y/%m/%d') == datetime.datetime.now().strftime('%Y/%m/%d'):
            self.next_button.configure(state="disabled")
            for i in range(len(self.task_checkbox)):
                self.task_checkbox[i].configure(state="normal")
        else:
            self.next_button.configure(state="normal")
            for i in range(len(self.task_checkbox)):
                self.task_checkbox[i].configure(state="disabled")
    
    # タスク追加ボタン
    def add_task_button(self):
        # 追加ウィンドの設定---------------------------------------------------------------------
        self.add_window = customtkinter.CTkToplevel(self)
        self.add_window.title("add task")
        self.add_window.geometry(f"{1100}x{580}")
        self.add_window.minsize(300, 580)

        # グリッドの設定(2×2)
        self.add_window.grid_rowconfigure((0,1), weight=1)
        self.add_window.grid_columnconfigure((0,1), weight=1)
        # タスク名入力を促すフレーム
        self.add_name_frame = customtkinter.CTkFrame(self.add_window, height=140, corner_radius=0)
        self.add_name_frame.grid(row=0,column=0,columnspan=2,padx=50,pady=50,sticky="nsew")
        self.add_name_frame.grid_rowconfigure((0,1), weight=1)
        self.add_name_frame.grid_columnconfigure((0,1), weight=1)
        self.add_name_label = customtkinter.CTkLabel(self.add_name_frame, text="タスク名",font=customtkinter.CTkFont(family="メイリオ",size=25))
        self.add_name_label.grid(row=0, column=0,rowspan=2)
        self.add_name_entry = customtkinter.CTkEntry(self.add_name_frame,font=customtkinter.CTkFont(family="メイリオ",size=25),width=300)
        self.add_name_entry.grid(row=0, column=1,rowspan=2)
        # 追加確定ボタン
        self.add_ok_button = customtkinter.CTkButton(self.add_window,text="追加", font=customtkinter.CTkFont(family="メイリオ",size=25, weight="bold"),command=self.add_ok_event)
        self.add_ok_button.grid(row=1, column=1,)
        self.iconify()

    # 追加確定ボタンを押したときの処理(ファイル書き込み)
    def add_ok_event(self):
        path = "task.csv"
        task_name = self.add_name_entry.get()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        try:
            with open(path, mode='x',newline='') as f:
                writer = csv.writer(f)
                writer.writerow([task_name])
        except FileExistsError:
            with open(path, mode='a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow([task_name])
        subprocess.check_call(["attrib", "+H", path])
        self.add_window.withdraw()
        # タスク欄の更新
        self.task_display()
        self.deiconify()
    
    # task.csvを読み込む処理
    def read_task(self):
        path = "task.csv"
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        di = {}
        try:
            with open(path) as f:
                reader = csv.reader(f)
                for row in reader:
                    di[row[0]] = False
        except:
            print("エラー")
        return di


if __name__ == "__main__":
    app = App()
    app.mainloop()
