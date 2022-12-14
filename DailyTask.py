import customtkinter
import tkinter
import datetime
import csv
import os
import subprocess
import json

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
        self.menu_names = ["追加","絞り込み","一覧","読み込み","書き込み",]
        self.menubar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.menubar_frame.grid(row=0,column=0,rowspan=2,sticky="nsew")
        for i in range(len(self.menu_names)+1):
            self.menubar_frame.grid_rowconfigure(i, weight=1)
        # ロゴの表示
        self.logo_label = customtkinter.CTkLabel(self.menubar_frame, text="DailyTask", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_label.bind("<1>",self.main_display)
        # メニューボタンの表示
        self.menu_button = [customtkinter.CTkButton(master=self.menubar_frame,text=self.menu_names[i],font=customtkinter.CTkFont(family="メイリオ")) for i in range(len(self.menu_names))]
        self.menu_button[0].configure(command=self.add_task_button)
        self.menu_button[3].configure(command=self.read_daily)
        self.menu_button[4].configure(command=self.write_daily)
        for i in range(len(self.menu_names)):
            self.menu_button[i].grid(row=i+1, column=0, padx=50, pady=0,)

        self.read_daily()

        # 日付フレーム(右上)の表示
        self.topbar_display()
        # タスク欄の表示
        self.task_display()

    # 日付フレーム(右上)を表示するときの処理------------------------------------------------------------------------------------------
    def topbar_display(self):
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


    # タスク欄を表示するときの処理------------------------------------------------------------------------------------------
    def task_display(self):
        self.main_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.main_frame.grid(row=1,column=1,padx=20,pady=20,sticky="nsew")
        # タスク名をtask.csvから参照(型は辞書型でValueはすべてFalse)
        self.task_di = self.read_task()
        for i in range(len(self.task_di)+1):
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
        self.task_checkbox = [customtkinter.CTkCheckBox(master=self.main_frame,text="",command=self.task_checkbox_event) for _ in range(len(self.task_di))]
        for i,key in enumerate(self.task_di):
            self.task_checkbox[i].grid(row=i+1, column=0, padx=0, pady=5,)
            if self.task_di[key]:
                self.task_checkbox[i].select()
        # タスク名の表示
        self.task_label = [customtkinter.CTkLabel(
            self.main_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=30, weight="bold"))
            for name in self.task_di]
        for i in range(len(self.task_di)):
            self.task_label[i].grid(row=i+1, column=1, padx=0, pady=5)
    
    # task.csvを読み込む処理
    def read_task(self):
        path = "task.csv"
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        di = {}
        try:
            with open(path) as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        if self.daily_di[self.dt_now.strftime('%Y/%m/%d')][row[0]]:
                            di[row[0]] = True
                        else:    
                            di[row[0]] = False
                    except:
                        di[row[0]] = False
        except:
            print("エラー")
        return di

    # ロゴを押すと、メイン画面に遷移
    def main_display(event,self):
        event.add_frame.grid_forget()
        event.add_name_frame.grid_forget()
        event.add_name_label.grid_forget()
        event.add_name_entry.grid_forget()
        event.add_ok_button.grid_forget()
        # 日付フレーム(右上)の表示
        event.topbar_display()
        # タスク欄の表示
        event.task_display()

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
        self.task_display()
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
        # 不必要なフレームを削除
        self.topbar_frame.grid_forget()
        self.main_frame.grid_forget()

        # 追加フレームの表示---------------------------------------------------------------------
        self.add_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.add_frame.grid(row=0,column=1,rowspan=2,padx=20,pady=20,sticky="nsew")
        self.add_frame.grid_columnconfigure(1, weight=1)
        self.add_frame.grid_columnconfigure((0,2), weight=0)

        # グリッドの設定(2×2)
        self.add_frame.grid_rowconfigure((0,1), weight=1)
        self.add_frame.grid_columnconfigure((0,1), weight=1)
        # タスク名入力を促すフレーム
        self.add_name_frame = customtkinter.CTkFrame(self.add_frame, height=140, corner_radius=0)
        self.add_name_frame.grid(row=0,column=0,columnspan=2,padx=50,pady=50,sticky="nsew")
        self.add_name_frame.grid_rowconfigure((0,1), weight=1)
        self.add_name_frame.grid_columnconfigure((0,1), weight=1)
        self.add_name_label = customtkinter.CTkLabel(self.add_name_frame, text="タスク名",font=customtkinter.CTkFont(family="メイリオ",size=25))
        self.add_name_label.grid(row=0, column=0,rowspan=2)
        self.add_name_entry = customtkinter.CTkEntry(self.add_name_frame,font=customtkinter.CTkFont(family="メイリオ",size=25),width=300)
        self.add_name_entry.grid(row=0, column=1,rowspan=2)
        # 追加確定ボタン
        self.add_ok_button = customtkinter.CTkButton(self.add_frame,text="追加", font=customtkinter.CTkFont(family="メイリオ",size=25, weight="bold"),command=self.add_ok_event)
        self.add_ok_button.grid(row=1, column=1,)

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
        # 画面遷移
        self.add_frame.grid_forget()
        self.add_name_frame.grid_forget()
        self.add_name_label.grid_forget()
        self.add_name_entry.grid_forget()
        self.add_ok_button.grid_forget()
        self.topbar_display()
        self.task_display()

    def read_daily(self):
        path = "daily.json"
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        try:
            with open(path) as f:
                self.daily_di = json.load(f)
        except:
            self.daily_di = {}
            print("エラー")

    def write_daily(self):
        di = {self.dt_now.strftime('%Y/%m/%d'):self.task_di}
        print(di)
        path = "daily.json"
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open(path, 'w') as f:
            json.dump(di, f, indent=4, ensure_ascii=False)

    def task_checkbox_event(self):
        for i,state in enumerate(self.task_checkbox):
            if state.get() == 1:
                self.task_di[self.task_label[i].cget("text")] = True
                self.daily_di[self.dt_now.strftime('%Y/%m/%d')][self.task_label[i].cget("text")] = True
            else:
                self.task_di[self.task_label[i].cget("text")] = False
                self.daily_di[self.dt_now.strftime('%Y/%m/%d')][self.task_label[i].cget("text")] = False
        self.write_daily()

if __name__ == "__main__":
    app = App()
    app.mainloop()
