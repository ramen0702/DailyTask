import customtkinter
import tkinter
import datetime
import os
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

        # ウィンドウレイアウトの設定(2×2)------------------------------------------------------------------------------------------
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # メニューバー(左)の表示------------------------------------------------------------------------------------------
        # レイアウトの設定
        self.menu_names = ["追加","絞り込み","一覧","読み込み","書き込み",]
        self.menubar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.menubar_frame.grid(row=0,column=0,rowspan=2,sticky="nsew")
        for i in range(len(self.menu_names)+1):
            self.menubar_frame.grid_rowconfigure(i, weight=1)
        # ロゴの表示(ロゴを押すとメイン画面へ遷移)
        self.logo_label = customtkinter.CTkLabel(self.menubar_frame, text="DailyTask", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_label.bind("<1>",self.display_main)
        # メニューボタンの表示
        self.menu_button = [customtkinter.CTkButton(master=self.menubar_frame,text=self.menu_names[i],font=customtkinter.CTkFont(family="メイリオ")) for i in range(len(self.menu_names))]
        # 追加ボタン
        self.menu_button[0].configure(command=self.add_task_button)
        # 読み込みボタン(デバッグ用)
        self.menu_button[3].configure(command=self.read_daily)
        # 書き込みボタン(デバッグ用)
        self.menu_button[4].configure(command=self.write_daily)
        for i in range(len(self.menu_names)):
            self.menu_button[i].grid(row=i+1, column=0, padx=50, pady=0,)

        # daily.jsonを読む
        self.read_daily()

        # 日付フレーム(右上)の表示
        self.display_topbar()
        # タスクフレーム(右,右下)の表示
        self.display_taskbar()
    
    # daily.jsonを読み込む関数------------------------------------------------------------------------------------------
    def read_daily(self):
        path = "daily.json"
        # 作業ディレクトリをこのファイル直下に設定
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # daily.jsonの内容はself.daily_diに格納される
        self.daily_di = {}
        try:
            with open(path) as f:
                self.daily_di = json.load(f)
        except:
            print("エラー")
    
    # 日付フレーム(右上)を表示する関数------------------------------------------------------------------------------------------
    def display_topbar(self):
        # レイアウトの設定
        self.topbar_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.topbar_frame.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
        self.topbar_frame.grid_columnconfigure(1, weight=1)
        self.topbar_frame.grid_columnconfigure((0,2), weight=0)
        # 本日の日付を表示
        # 本日の日付はself.dt_nowに格納される(datetime型)
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


    # タスクフレーム(右,右下)を表示する関数------------------------------------------------------------------------------------------
    def display_taskbar(self):
        # レイアウトの設定
        self.main_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.main_frame.grid(row=1,column=1,padx=20,pady=20,sticky="nsew")
        # 現在開いている日付の、タスク名と真偽値をtask.jsonから参照し、
        # now_date_task_diに辞書型として記録
        self.now_date_task_di = self.read_task()
        for i in range(len(self.now_date_task_di)+1):
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
        self.task_checkbox = [customtkinter.CTkCheckBox(master=self.main_frame,text="",command=self.task_checkbox_event) for _ in range(len(self.now_date_task_di))]
        for i,key in enumerate(self.now_date_task_di):
            self.task_checkbox[i].grid(row=i+1, column=0, padx=0, pady=5,)
            # もし真偽値が真ならチェックを入れる
            if self.now_date_task_di[key]:
                self.task_checkbox[i].select()
        # タスク名の表示
        self.task_label = [customtkinter.CTkLabel(
            self.main_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=30, weight="bold"))
            for name in self.now_date_task_di]
        for i in range(len(self.now_date_task_di)):
            self.task_label[i].grid(row=i+1, column=1, padx=0, pady=5)
    
    # task.jsonを読み込み、表示中の日付のtask名と真偽値を返す関数------------------------------------------------------------------------------------------
    def read_task(self):
        path = "task.json"
        # 作業ディレクトリをこのファイル直下に設定
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        di = {}
        try:
            with open(path) as f:
                di = json.load(f)
        except:
            print("エラー")
        today_di = {}
        for key in di:
            # もしすでに、現在表示中の日付の真偽値がdaily_diに記録されていたらそのまま格納
            try:
                today_di[key] = self.daily_di[self.dt_now.strftime('%Y/%m/%d')][key]
            # 記録されてなかったら、taskの記録日と現在表示中の日付を比べ、格納すべきか判断
            # すべきならFalseで初期化
            except:
                read_date = list(map(int,di[key].split("/")))
                read_date = datetime.date(read_date[0],read_date[1],read_date[2])
                if read_date <= self.dt_now.date():
                    today_di[key] = False
        return today_di

    # メイン画面へ遷移する関数--------------------------------------------------------------------------------
    def display_main(event,self):
        # 不必要なフレームの削除
        event.add_frame.grid_forget()
        event.add_name_frame.grid_forget()
        event.add_name_label.grid_forget()
        event.add_name_entry.grid_forget()
        event.add_ok_button.grid_forget()
        # 日付フレーム(右上)の表示
        event.display_topbar()
        # タスク欄の表示
        event.display_taskbar()

    # チェックボックスを押したとき用の関数--------------------------------------------------------------------------------------------------------
    def task_checkbox_event(self):
        # 現在表示している日付のタスクを管理するnow_date_task_diと
        # daily.jsonの内容を格納するdaily_diに更新を行う
        for i,state in enumerate(self.task_checkbox):
            if state.get() == 1:
                self.now_date_task_di[self.task_label[i].cget("text")] = True
                # もしすでにdaily_diに現在の日にち(dt_now)で真偽値が格納されていたら、現在の状態の真偽値に更新を
                try:
                    self.daily_di[self.dt_now.strftime('%Y/%m/%d')][self.task_label[i].cget("text")] = True
                # 格納されていなかったら、新たに本日の日付を用意する辞書型を宣言し、現在の状態で初期化する
                except:
                    self.daily_di[self.dt_now.strftime('%Y/%m/%d')] = {}
                    self.daily_di[self.dt_now.strftime('%Y/%m/%d')][self.task_label[i].cget("text")] = True
            else:
                self.now_date_task_di[self.task_label[i].cget("text")] = False
                try:
                    self.daily_di[self.dt_now.strftime('%Y/%m/%d')][self.task_label[i].cget("text")] = False
                except:
                    self.daily_di[self.dt_now.strftime('%Y/%m/%d')] = {}
                    self.daily_di[self.dt_now.strftime('%Y/%m/%d')][self.task_label[i].cget("text")] = True
        # dayly.jsonへファイル書き込みを行い、更新する
        self.write_daily()

    # daily.jsonにファイル書き込みを行う関数--------------------------------------------------------------------------------------------------------
    def write_daily(self):
        # daily.jsonにdaily_diの内容をファイル書き込み
        path = "daily.json"
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open(path, 'w') as f:
            json.dump(self.daily_di, f, indent=4, ensure_ascii=False)
    
    # 進む、戻るボタン関連の関数-----------------------------------------------------------------------------------------------
    # 翌日に進むボタン
    def next_button_event(self):
        # 日付を加算
        self.dt_now += datetime.timedelta(days=1)
        self.daily_func()

    # 前日に戻るボタン
    def prev_button_event(self):
        # 日付を減算
        self.dt_now -= datetime.timedelta(days=1)
        self.daily_func()
    
    # 日付変更時の表示更新
    def daily_func(self):
        # ラベルのテキスト変更
        self.today_label.configure(text=self.dt_now.strftime('%Y/%m/%d'))
        # タスクバーの更新表示
        self.display_taskbar()
        # 更新後の表示日数と、現実の日数が同じならば、未来へいけないように進むボタンを無向化
        # 更新後の表示日数と、現実の日数が同じゃなければ、タスクのチェックボタンを無向化
        if self.dt_now.strftime('%Y/%m/%d') == datetime.datetime.now().strftime('%Y/%m/%d'):
            self.next_button.configure(state="disabled")
            for i in range(len(self.task_checkbox)):
                self.task_checkbox[i].configure(state="normal")
        else:
            self.next_button.configure(state="normal")
            for i in range(len(self.task_checkbox)):
                self.task_checkbox[i].configure(state="disabled")
    
    # タスク追加ボタン用の関数-----------------------------------------------------------------------------------------------------------------------------------
    def add_task_button(self):
        # 不必要なフレームを削除
        self.topbar_frame.grid_forget()
        self.main_frame.grid_forget()
        # レイアウトの設定
        self.add_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.add_frame.grid(row=0,column=1,rowspan=2,padx=20,pady=20,sticky="nsew")
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

    # 追加確定ボタンを押したとき用の関数--------------------------------------------------------------------------------------------------------
    def add_ok_event(self):
        # task.jsonの内容をすべて読み込む
        path = "task.json"
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        new_di = {}
        try:
            with open(path) as f:
                new_di = json.load(f)
        except:
            print("エラー")
        # 読み込んだ内容に、新しく追加するtask名と現在時刻を追加して格納
        task_name = self.add_name_entry.get()
        new_di[task_name] = self.dt_now.strftime('%Y/%m/%d')
        # 格納したデータをtask.jsonにファイル書き込み
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open(path, 'w') as f:
            json.dump(new_di, f, indent=4, ensure_ascii=False)
        # 画面遷移
        # タスク追加画面をフレームをすべて削除
        self.add_frame.grid_forget()
        self.add_name_frame.grid_forget()
        self.add_name_label.grid_forget()
        self.add_name_entry.grid_forget()
        self.add_ok_button.grid_forget()
        # 日付フレーム(右上)とタスクフレーム(右,右下)の表示
        self.display_topbar()
        self.display_taskbar()

if __name__ == "__main__":
    app = App()
    app.mainloop()
