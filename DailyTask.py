import customtkinter
import tkinter
import datetime
import os
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        # 画面状態を記憶する変数
        # 1:メイン,2:追加,3:削除,4:グラフ
        self.screen_id = 1

        # メニューバー(左)の表示------------------------------------------------------------------------------------------
        # レイアウトの設定
        self.menu_names = ["追加","削除","グラフ"]
        self.menubar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.menubar_frame.grid(row=0,column=0,rowspan=2,sticky="nsew")
        for i in range(len(self.menu_names)+5):
            self.menubar_frame.grid_rowconfigure(i, weight=1)
        # ロゴの表示(ロゴを押すとメイン画面へ遷移)
        self.logo_label = customtkinter.CTkLabel(self.menubar_frame, text="DailyTask", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_label.bind("<1>",self.display_main)
        # メニューボタンの表示
        self.menu_button = [customtkinter.CTkButton(master=self.menubar_frame,text=self.menu_names[i],font=customtkinter.CTkFont(family="メイリオ")) for i in range(len(self.menu_names))]
        # 追加ボタン
        self.menu_button[0].configure(command=self.add_task_button)
        # 削除ボタン
        self.menu_button[1].configure(command=self.remove_task_button)
        # グラフボタン
        self.menu_button[2].configure(command=self.graph_button)
        for i in range(len(self.menu_names)):
            self.menu_button[i].grid(row=i+1, column=0, padx=50, pady=0,)

        # ダークモードとライトモードの選択メニュー
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.menubar_frame, values=["System" ,"Light", "Dark"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))

        self.week = ["(月)","(火)","(水)","(木)","(金)","(土)","(日)"]

        # daily.jsonを読む
        self.read_daily()

        # 開始日をdaily.jsonから読み、それ以前の日にちには遷移させない
        self.check_first_date()

        # 開始日から今日までの日付をall_dateに格納
        self.get_all_date()

        # 日付フレーム(右上)の表示
        self.display_topbar()

        # タスクフレーム(右,右下)の表示
        self.display_taskbar()

        # 現在日から最後に起動した翌日までさかのぼって、daily.jsonにtask名とFalseを付ける
        self.set_false_date()
        
    # ダークモードとライトモードを切り替える関数------------------------------------------------------------------------------------------
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if self.screen_id == 4:
            self.remove_gird()
            self.display_graph()
        elif self.screen_id == 1:
            self.remove_gird()
            self.display_topbar()
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
    
    # 開始日をdaily.jsonから読む関数------------------------------------------------------------------------------------------
    def check_first_date(self):
        date = []
        for key in self.daily_di:
            date.append(key)
        if len(date) >= 1:
            self.min_date = min(date)
        else:
            self.min_date = datetime.datetime.now().strftime('%Y/%m/%d')
    
        
    # 開始日から今日までの日付をall_dateに格納する関数------------------------------------------------------------------------------------------
    def get_all_date(self):
        y,m,d = map(int,self.min_date.split("/"))
        self.all_date = []
        index_date = datetime.date(y, m, d)
        now = datetime.datetime.now()
        while index_date.strftime('%Y/%m/%d/') != now.strftime('%Y/%m/%d/'):
            self.all_date.append(index_date.strftime('%Y/%m/%d')+self.week[index_date.weekday()])
            index_date += datetime.timedelta(days=1)
        self.all_date.append(index_date.strftime('%Y/%m/%d')+self.week[index_date.weekday()])
        self.all_date = list(reversed(self.all_date))

    # 日付フレーム(右上)を表示する関数------------------------------------------------------------------------------------------
    def display_topbar(self):
        # レイアウトの設定
        self.topbar_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.topbar_frame.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
        self.topbar_frame.grid_columnconfigure(1, weight=1)
        self.topbar_frame.grid_columnconfigure((0,2), weight=0)
        # 本日の日付を表示
        # 表示する日付(可変)はself.dt_nowに格納される(datetime型)
        self.dt_now = datetime.datetime.now()
        initial_date = customtkinter.StringVar(value=self.dt_now.strftime('%Y/%m/%d')+self.week[self.dt_now.weekday()])
        self.date_combobox = customtkinter.CTkOptionMenu(self.topbar_frame,values=self.all_date, variable=initial_date
        ,command=self.change_date_event,font=customtkinter.CTkFont(size=30, weight="bold") ,anchor = "center")
        self.date_combobox.grid(row=0, column=1, padx=0, pady=10,sticky="nsew")
        # 進む、戻るボタンの表示
        self.prev_button = customtkinter.CTkButton(self.topbar_frame, text="◀"
        , font=customtkinter.CTkFont(size=15, weight="bold"),command=self.prev_button_event)
        self.prev_button.grid(row=0, column=0, padx=50, pady=10,)
        self.next_button = customtkinter.CTkButton(self.topbar_frame, text="▶"
        , font=customtkinter.CTkFont(size=15, weight="bold"),command=self.next_button_event,state="disabled")
        self.next_button.grid(row=0, column=2, padx=50, pady=10,)
        # もし表示日数が開始日なら、それ以前に戻らせないよう、戻るボタンを無効化
        if self.dt_now.strftime('%Y/%m/%d') == self.min_date:
            self.prev_button.configure(state="disabled")        

    # タスクフレーム(右,右下)を表示する関数------------------------------------------------------------------------------------------
    def display_taskbar(self):
        # レイアウトの設定
        # tmp_frameにcanvasとscrollbarが配置され、canvasにmain_frameの内容を表示する
        # scrollbarはcanvasを動かし、同時にmain_frameもスライドする
        self.tmp_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.tmp_frame.grid(row=1,column=1,padx=20,pady=20,sticky="nsew")
        self.tmp_frame.grid_columnconfigure(0,weight=1)
        self.tmp_frame.grid_rowconfigure(0,weight=1)
        if self._get_appearance_mode() == "dark":
            self.main_canvas = tkinter.Canvas(self.tmp_frame, background = "gray17", highlightthickness=0)
        else:
            self.main_canvas = tkinter.Canvas(self.tmp_frame, background = "gray87", highlightthickness=0)
        self.main_canvas.grid(row=0,column=0,sticky="nsew")
        self.main_canvas.grid_columnconfigure(0,weight=1)
        self.main_canvas.grid_rowconfigure(0,weight=1)
        self.main_frame = customtkinter.CTkFrame(self.main_canvas,corner_radius=0)
        # 現在開いている日付の、タスク名と真偽値をtask.jsonから参照し、
        # now_date_task_diに辞書型として記録
        self.read_task()
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
            self.task_label[i].grid(row=i+1, column=1, padx=0, pady=10)
        # scrollbarを作成・配置し、canvasと紐づける
        self.main_frame.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1)
        self.scrollbar = tkinter.Scrollbar(self.tmp_frame, orient=tkinter.VERTICAL, command=self.main_canvas.yview)
        self.main_canvas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=(tkinter.N, tkinter.S))
        # canvasの横幅を取得し、横幅に合わせてframeを描画
        self.update()
        canvas_width = self.main_canvas.winfo_width()
        self.main_canvas.create_window((0,0), window=self.main_frame, anchor="nw",width=canvas_width)
        # Frameの大きさを確定してCanvasにスクロール範囲を設定
        self.main_frame.update_idletasks()
        self.main_canvas.config(scrollregion=self.main_canvas.bbox("all"))

    # task.jsonを読み込み、表示中の日付のtask名と真偽値をself.now_date_task_diに格納する関数------------------------------------------------------------------------------------------
    def read_task(self):
        # task.jsonを読み込み、task_diという辞書に記録する
        path = "task.json"
        # 作業ディレクトリをこのファイル直下に設定
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.task_di = {}
        try:
            with open(path) as f:
                self.task_di = json.load(f)
        except:
            print("エラー")
        self.now_date_task_di = {}
        # 表示中の日にちがdaily_di(daily.json)に格納されていれば参照
        if self.dt_now.strftime('%Y/%m/%d') in self.daily_di:
            self.now_date_task_di = self.daily_di[self.dt_now.strftime('%Y/%m/%d')]
        # 格納されて無ければ、Falseで初期化
        # daily_diにも追加し、daily.jsonに書き込む
        else:
            self.daily_di[self.dt_now.strftime('%Y/%m/%d')] = {}
            for key in self.task_di:
                self.now_date_task_di[key] = False
                self.daily_di[self.dt_now.strftime('%Y/%m/%d')][key] = False
            self.write_daily()
    
    # 現在日から最後に起動した翌日までさかのぼって、daily.jsonにtask名とFalseを付ける関数------------------------------------------------------------------------------------------
    def set_false_date(self):
        if self.dt_now.strftime('%Y/%m/%d') == self.min_date:
            return
        date = self.dt_now - datetime.timedelta(days=1)
        while date.strftime('%Y/%m/%d') != self.min_date:
            if date.strftime('%Y/%m/%d') not in self.daily_di:
                self.daily_di[date.strftime('%Y/%m/%d')] = {}
                for key in self.task_di:
                    self.daily_di[date.strftime('%Y/%m/%d')][key] = False
            else:
                break
            date -= datetime.timedelta(days=1)
        self.write_daily()


    # メイン画面へ遷移する関数--------------------------------------------------------------------------------
    def display_main(event,self):
        # 不必要なフレームを削除
        event.remove_gird()
        # 日付フレーム(右上)の表示
        event.display_topbar()
        # タスク欄の表示
        event.display_taskbar()
        # 画面状態を更新
        event.screen_id = 1
    
    # 不必要なフレームを削除する関数--------------------------------------------------------------------------------
    def remove_gird(self):
        if self.screen_id == 1:
            self.topbar_frame.grid_forget()
            self.date_combobox.grid_forget()
            self.prev_button.grid_forget()
            self.next_button.grid_forget()
            self.main_frame.grid_forget()
            for i in range(2):
                self.item_label[i].grid_forget()
            for i in range(len(self.now_date_task_di)):
                self.task_checkbox[i].grid_forget()
                self.task_label[i].grid_forget()
        elif self.screen_id == 2:
            self.add_frame.grid_forget()
            self.add_name_frame.grid_forget()
            self.add_name_label.grid_forget()
            self.add_name_entry.grid_forget()
            self.add_ok_button.grid_forget()
        elif self.screen_id == 3:
            self.remove_frame.grid_forget()
            for i in range(2):
                self.remove_item_label[i].grid_forget()
            for i in range(len(self.today_date_task)):
                self.remove_task_checkbox[i].grid_forget()
                self.remove_task_label[i].grid_forget()
            self.remove_ok_button.grid_forget()
        elif self.screen_id == 4:
            self.graph_frame.grid_forget()
            self.graph_date_frame.grid_forget()
            self.date_label.grid_forget()
            self.graph_prev_button.grid_forget()
            self.graph_next_button.grid_forget()

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
    
    # task.jsonへ書き込む用の関数--------------------------------------------------------------------------------------------------------
    def write_task(self):
        path = "task.json"
        # 残ったtask_diをすべてtask.jsonへ書き込み
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open(path, 'w') as f:
            json.dump(self.task_di, f, indent=4, ensure_ascii=False)
    
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
        new_date = customtkinter.StringVar(value=self.dt_now.strftime('%Y/%m/%d') +self.week[self.dt_now.weekday()])
        self.date_combobox.configure(variable=new_date)
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
        # もし更新後の表示日数が開始日なら、それ以前に戻らせないよう、戻るボタンを無効化
        if self.dt_now.strftime('%Y/%m/%d') == self.min_date:
            self.prev_button.configure(state="disabled")
        else:
            self.prev_button.configure(state="normal")
    
    # コンボボックスから日付を変更した時用の関数
    def change_date_event(self,choice):
        y,m,d = choice.split("/")
        d = d[:2]
        y,m,d = map(int,(y,m,d))
        self.dt_now = datetime.date(y,m,d)
        self.daily_func()

    # タスク追加ボタン用の関数-----------------------------------------------------------------------------------------------------------------------------------
    def add_task_button(self):
        # 不要なフレームを削除
        self.remove_gird()
        # 画面状態を更新
        self.screen_id = 2
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
        # task名が半角16文字以下ならtask_diに、新しく追加するtask名と現在時刻を追加して格納
        task_name = self.add_name_entry.get()
        if len(task_name.encode('shift_jis')) > 16:
            window = customtkinter.CTkToplevel(self)
            window.geometry("400x200")
            label = customtkinter.CTkLabel(window, text="16バイト以下のタスク名を設定してください",font=customtkinter.CTkFont(family="メイリオ"))
            label.pack(padx=40, pady=25)
            def button_event():
                window.destroy()
            button = customtkinter.CTkButton(window, text="OK",font=customtkinter.CTkFont(family="メイリオ"),command=button_event)
            button.pack(padx=40, pady=25)
            return
        self.task_di[task_name] = self.dt_now.strftime('%Y/%m/%d')
        # 格納したデータをtask.jsonにファイル書き込み
        self.write_task()
        # daily_diにもtask名とfalseを格納
        if datetime.datetime.now().strftime('%Y/%m/%d') not in self.daily_di:
            self.daily_di[datetime.datetime.now().strftime('%Y/%m/%d')] = {}
        self.daily_di[datetime.datetime.now().strftime('%Y/%m/%d')][task_name] = False
        # 新しいdaily_diをdaily.jsonに更新
        self.write_daily()
        # 画面遷移
        # タスク追加画面をフレームをすべて削除
        self.remove_gird()
        # 日付フレーム(右上)とタスクフレーム(右,右下)の表示
        self.screen_id = 1
        self.display_topbar()
        self.display_taskbar()
    
    # タスク削除ボタン用の関数-----------------------------------------------------------------------------------------------------------------------------------
    def remove_task_button(self):
        # 不要なフレームを削除
        self.remove_gird()
        # 画面状態を更新
        self.screen_id = 3
        # レイアウトの設定
        self.remove_frame = customtkinter.CTkFrame(self, height=140, corner_radius=0)
        self.remove_frame.grid(row=0,column=1,rowspan = 2,padx=20,pady=20,sticky="nsew")
        # self.task_diからタスク名を参照し、today_date_taskにリストとして記録
        self.today_date_task = []
        for name in self.task_di:
            self.today_date_task.append(name)
        for i in range(len(self.today_date_task)+2):
            self.remove_frame.grid_rowconfigure(i, weight=1)
        # 項目名の表示
        item_names = ["削除項目　　　","タスク名"]
        self.remove_item_label = [customtkinter.CTkLabel(
            self.remove_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=25, weight="bold"))
            for name in item_names]
        for i in range(len(item_names)):
            self.remove_frame.grid_columnconfigure(i, weight=1)
            self.remove_item_label[i].grid(row=0, column=i, padx=0, pady=5)
        # チェックボックスの表示
        self.remove_task_checkbox = [customtkinter.CTkCheckBox(master=self.remove_frame,text="",command=self.task_checkbox_event) for _ in range(len(self.today_date_task))]
        for i in range(len(self.today_date_task)):
            self.remove_task_checkbox[i].grid(row=i+1, column=0, padx=0, pady=5,)
        # タスク名の表示
        self.remove_task_label = [customtkinter.CTkLabel(
            self.remove_frame
            , text=name
            , font=customtkinter.CTkFont(family="メイリオ",size=30, weight="bold"))
            for name in self.today_date_task]
        for i in range(len(self.today_date_task)):
            self.remove_task_label[i].grid(row=i+1, column=1, padx=0, pady=5)
        self.remove_ok_button = customtkinter.CTkButton(self.remove_frame,text="削除", font=customtkinter.CTkFont(family="メイリオ",size=25, weight="bold"),command=self.remove_ok_event)
        self.remove_ok_button.grid(row = len(self.today_date_task)+1,column=1)
    
    # 削除確定ボタンを押したとき用の関数--------------------------------------------------------------------------------------------------------
    def remove_ok_event(self):
        # チェックが入れられたタスク名はremove_listというリストに格納される
        remove_list = []
        for i in range(len(self.remove_task_checkbox)):
            if self.remove_task_checkbox[i].get() == 1:
                remove_list.append(self.remove_task_label[i].cget("text"))
        # remove_listに入っているタスクをtask_diから削除
        for s in remove_list:
            self.task_di.pop(s)
        # 残ったtask_diをすべてtask.jsonへ書き込み
        self.write_task()
        # daily_diにも更新を行う
        for s in remove_list:
            self.daily_di[datetime.datetime.now().strftime('%Y/%m/%d')].pop(s)
        # 新しいdaily_diをdaily.jsonに更新
        self.write_daily()
        # 画面遷移
        # タスク追加画面をフレームをすべて削除
        self.remove_gird()
        # 日付フレーム(右上)とタスクフレーム(右,右下)の表示
        self.screen_id = 1
        self.display_topbar()
        self.display_taskbar()

    # グラフボタンが押されたとき用の関数--------------------------------------------------------------------------------------------------------
    def graph_button(self):
        self.dt_now = datetime.datetime.now()
        self.display_graph()

    def display_graph(self):
        # 不要なフレームを削除
        self.remove_gird()
        # 画面状態を更新
        self.screen_id = 4
        self.display_graph_date()
        # matplotlib配置用フレーム
        self.graph_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.graph_frame.grid(row=1,column=1,padx=20,pady=20,sticky="nsew")
        # matplotlibの描画領域の作成
        if self._get_appearance_mode() == "dark":
            fig = Figure(facecolor="0.2", edgecolor="white")
        else:
            fig = Figure()
        # 座標軸の作成
        self.ax = fig.add_subplot(111)
        if self._get_appearance_mode() == "dark":
            self.ax.set_facecolor("0.2")
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.spines['right'].set_color('white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.tick_params(axis='x', colors='white')
            self.ax.tick_params(axis='y', colors='white')
        else:
            self.ax.tick_params(axis='x')
            self.ax.tick_params(axis='y')
        self.ax.set_xlabel("日付", fontname="MS Gothic")
        self.ax.set_ylabel("達成率(%)", fontname="MS Gothic")
        self.ax.set_ylim(0, 100)
        # matplotlibの描画領域とウィジェット(Frame)の関連付け
        self.fig_canvas = FigureCanvasTkAgg(fig, self.graph_frame)
        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=customtkinter.BOTH, expand=True)
        # daily.jsonを読み込んdaily_diへ
        self.sort_date = sorted(self.daily_di,reverse=True)
        # sort_dateがdt_nowと一致するインデックスを探索
        dt_index = self.sort_date.index(self.dt_now.strftime('%Y/%m/%d'))
        y = []
        x = []
        i = dt_index
        while i < dt_index+7:
            if i >= len(self.sort_date):
                break
            date = self.sort_date[i]
            today = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:]))
            x.append(date[-5:]+self.week[today.weekday()])
            date_count = len(self.daily_di[date])
            ok_count = 0
            for name in self.daily_di[date]:
                if self.daily_di[date][name]:
                    ok_count += 1
            percent = ok_count / date_count * 100
            y.append(percent)
            i+=1
        x = x[::-1]
        y = y[::-1]
        self.ax.set_xticks(list(range(len(x))))
        self.ax.set_xticklabels(x,fontfamily="MS Gothic")
        # グラフの描画
        self.ax.plot(x, y, marker='o')
        for i, value in enumerate(y):
            if self._get_appearance_mode() == "dark":
                self.ax.text(x[i], y[i]+3, round(value),color='white')
            else:
                self.ax.text(x[i], y[i]+3, round(value))
    
    # グラフの日付フレーム(右上)を表示する関数------------------------------------------------------------------------------------------
    def display_graph_date(self):
        # レイアウトの設定
        self.graph_date_frame = customtkinter.CTkFrame(self, height=30, corner_radius=0)
        self.graph_date_frame.grid(row=0,column=1,padx=20,pady=20,sticky="nsew")
        self.graph_date_frame.grid_columnconfigure(1, weight=1)
        self.graph_date_frame.grid_columnconfigure((0,2), weight=0)
        # 本日の日付を表示
        # 表示する日付(可変)はself.dt_nowに格納される(datetime型)
        self.date_label = customtkinter.CTkLabel(self.graph_date_frame, text="～"+self.dt_now.strftime('%Y/%m/%d')+self.week[self.dt_now.weekday()]
        , font=customtkinter.CTkFont(size=30, weight="bold"))
        self.date_label.grid(row=0, column=1, padx=0, pady=10,sticky="nsew")
        # 進む、戻るボタンの表示
        self.graph_prev_button = customtkinter.CTkButton(self.graph_date_frame, text="◀"
        , font=customtkinter.CTkFont(size=15, weight="bold"),command=self.graph_prev_button_event)
        self.graph_prev_button.grid(row=0, column=0, padx=50, pady=10,)
        self.graph_next_button = customtkinter.CTkButton(self.graph_date_frame, text="▶"
        , font=customtkinter.CTkFont(size=15, weight="bold"),command=self.graph_next_button_event,state="disabled")
        self.graph_next_button.grid(row=0, column=2, padx=50, pady=10,)
        # もし表示日数が開始日なら、それ以前に戻らせないよう、戻るボタンを無効化
        if (self.dt_now - datetime.timedelta(days=7)).strftime('%Y/%m/%d') not in self.daily_di:
            self.graph_prev_button.configure(state="disabled")      
    
    # グラフの進む、戻るボタン関連の関数-----------------------------------------------------------------------------------------------
    # 翌週に進むボタン
    def graph_next_button_event(self):
        # 日付を加算
        self.dt_now += datetime.timedelta(days=7)
        self.weekly_func()

    # 前週に戻るボタン
    def graph_prev_button_event(self):
        # 日付を減算
        self.dt_now -= datetime.timedelta(days=7)
        self.weekly_func()
    
    # 日付変更時の表示更新
    def weekly_func(self):
        # タスクバーの更新表示
        self.display_graph()
        # 更新後の表示日数と、現実の日数が同じならば、未来へいけないように進むボタンを無向化
        # 更新後の表示日数と、現実の日数が同じゃなければ、タスクのチェックボタンを無向化
        if self.dt_now.strftime('%Y/%m/%d') == datetime.datetime.now().strftime('%Y/%m/%d'):
            self.graph_next_button.configure(state="disabled")
        else:
            self.graph_next_button.configure(state="normal")
        # もし更新後の表示日数が開始日なら、それ以前に戻らせないよう、戻るボタンを無効化
        if (self.dt_now - datetime.timedelta(days=7)).strftime('%Y/%m/%d') not in self.daily_di:
            self.graph_prev_button.configure(state="disabled")
        else:
            self.graph_prev_button.configure(state="normal")
    
    # ウィンドウリサイズが起きた時にUIを更新する関数---------------------------------------------------------------------------------------------------------------------
    def callback(event,self):
        global width, height
        # ウィンドウリサイズ以外のイベントは無視
        if (event.winfo_width() == width) and (event.winfo_height() == height):
            return
        width = event.winfo_width()
        height = event.winfo_height()
        if event.screen_id == 1:
            event.display_taskbar()


if __name__ == "__main__":
    app = App()
    width = 1100
    height = 580
    # もしウィンドウリサイズが起きたらUIも更新
    app.bind("<Configure>", app.callback)
    app.mainloop()