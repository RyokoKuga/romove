from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import stat
import shutil
import configparser
import filecmp

# 設定ファイルの読込み
config = configparser.ConfigParser()
config.read("config.ini")
read_base = config["Paths"]

##### 関数 #####
# エントリーBOXの初期値
def read_entry():
    try:
        entry0.insert("end", read_base.get("src"))
    except:
        pass
    try:
        entry1.insert("end", read_base.get("dst"))
    except:
        pass

# Sorecr(Browseボタン)
def save_src():
    # 開くテキストファイルのパス
    typ = [("Excel Book", "*.xlsx"), ("Excel Book", "*.xls"), ("All Files", "*.*")]
    save_path = filedialog.askopenfilename(filetypes = typ)
    
    # ファイルが選択された場合データを書込み
    if len(save_path) != 0:
        # エントリーBOXのデータ消去
        entry0.delete("0","end")
        # エントリーBOXへパス反映
        entry0.insert("end", save_path)

# Destination(Browseボタン)
def save_dst():
    # 開くテキストファイルのパス
    typ = [("Excel Book", "*.xlsx"), ("Excel Book", "*.xls"), ("All Files", "*.*")]
    save_path = filedialog.askopenfilename(filetypes = typ)
    
    # ファイルが選択された場合データを書込み
    if len(save_path) != 0:
        # エントリーBOXのデータ消去
        entry1.delete("0","end")
        # エントリーBOXへパス反映
        entry1.insert("end", save_path)

# Stratボタン(ファイルコピー)
# ファイル比較
def comp_func():
    global src, dst
    
    # エントリーBOXからパス取得
    src = entry0.get()
    dst = entry1.get()
    
    try:
        # バックアップ先のファイルパス
        bu_file = os.path.join("TempFolder", os.path.basename(dst))
        
        # ファイルが更新されている場合
        if not filecmp.cmp(bu_file, dst):
            # 続行するかYes/No
            if messagebox.askyesno("Continue?", "May have been updated."):
                # ファイルコピー
                copy_func()
            
            # 更新ファイルを保存するかYes/No
            elif messagebox.askyesno("Save?", "Save the updated file?"):
                
                # 保存ダイアログの表示
                typ = [("Excel Book", "*.xlsx"), ("Excel Book", "*.xls"), ("All Files", "*.*")]
                save_path = filedialog.asksaveasfilename(filetypes = typ, defaultextension = "xlsx")
                # ァイルが選択された場合保存
                if len(save_path) != 0:
                    shutil.copy(dst, save_path)
 
        else:
            # ファイルコピー
            copy_func()
    except:
        # ファイルコピー
        copy_func()

# ファイルコピー
def copy_func():
    try:
        # 読取り専用に変更(src)
        os.chmod(path = src, mode=stat.S_IREAD)

        # 読取り専用を外す(dst)
        os.chmod(path = dst, mode=stat.S_IWRITE)

        # ファイルのコピー
        shutil.copy(src, dst)

        # 読取り専用を外す(src)
        os.chmod(path = src, mode=stat.S_IWRITE)

        # 設定ファイルへ保存
        config["Paths"] = {"src": src, "dst": dst}
        with open("config.ini", "w+") as file:
            config.write(file)

        # バックアップ
        shutil.copy(dst, "TempFolder")
        # 読取り専用に変更
        os.chmod(path = os.path.join("TempFolder", os.path.basename(dst)), mode=stat.S_IWRITE)
        
        # 終了通知
        messagebox.showinfo("Done!!", "Completed !!")
        
    except:
        # エラーメッセージ
        messagebox.showerror("Error", "Invalid file path !!")
    
        try:
            # srcが読取り専用なら
            if not os.access(src, os.W_OK):
                # 読取り専用を外す(src)
                os.chmod(path = src, mode=stat.S_IWRITE)
        except:
            pass
        
        try:
            # dstが読取り専用でなければ
            if os.access(dst, os.W_OK):
                # 読取り専用に変更(dst)
                os.chmod(path = dst, mode=stat.S_IREAD)
        except:
            pass
                
##### GUI #####
window = Tk()
window.title("romove ver.2.0.0")
window.resizable(False, False)
window.iconphoto(True, PhotoImage(file = "tb_icon.png"))

window.geometry("757x300")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 300,
    width = 757,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    378.5, 150.0,
    image=background_img)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    299.5, 117.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry0.place(
    x = 46, y = 102,
    width = 507,
    height = 28)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    299.5, 185.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 46, y = 170,
    width = 507,
    height = 28)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = comp_func,
    relief = "flat")

b0.place(
    x = 46, y = 235,
    width = 665,
    height = 40)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = save_dst,
    relief = "flat")

b1.place(
    x = 581, y = 165,
    width = 130,
    height = 40)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = save_src,
    relief = "flat")

b2.place(
    x = 581, y = 97,
    width = 130,
    height = 40)

# エントリーBOXの初期値反映
read_entry()

window.mainloop()