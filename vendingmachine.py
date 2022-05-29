import tkinter as tk, threading
from tkinter import messagebox
from PIL import Image, ImageTk
import imageio, time, random, qrcode, requests, os

root = None

# Stok
emptyStock = False
stocks = [random.randint(2, 9) for i in range(6)]

# Item
names = ["Aqua Mineral (600 mL)", "Ion Water (600 mL)", "Hydro Coco (250 mL)", "Pocari Sweat (330 mL)", "Oronamin C (120 mL)", "Ion Water (300 mL)"]
prices = [10000, 10000, 10000, 7000, 7000, 7000]

# Cash
money = 0

# QR
QR_URL = "https://f6660e92472ee61c9470746a70d15708.m.pipedream.net/"
API_URL = "https://api.pipedream.com/v1/sources/dc_bPuP0p8/event_summaries?expand=event"
HEADER = {'Authorization': 'Bearer 6965cf707033b622b4aac2840fe1baef'}
accounts = ["16521122", "16521432", "16521462", "16521472"]
account = accounts[0]
balances = [0, 0, 0, 0]
balance = balances[0]
qr_bool = False

# Emoney
emoney = 0

# Admin Mode
moneySpent = 0

# Mulai
def downloadGDrive(id, path):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None
    def save_response_content(response, path):
        CHUNK_SIZE = 32768
        with open(path, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = {"id": id}, stream = True)
    token = get_confirm_token(response)
    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, path)    

def download():
    if os.path.exists("welcome.mp4") == False:
        downloadGDrive("1P4hO5suzw4C3f15_ToeiTYytPs0KVXcL", "welcome.mp4")
    if os.path.exists("aboutus.png") == False:
        downloadGDrive("1ghH9wlk2pUw39iMHxcH3aQxRS6WhKs7M", "aboutus.png")
    if os.path.exists("adminmode.png") == False:
        downloadGDrive("1xEGQoqCOzthpy-WyvTN1SysLc_r19Kkv", "adminmode.png")
    if os.path.exists("emoneydone.png") == False:
        downloadGDrive("1SNfB3UOEAUawk4BtqRGh9wEpF11Q7GpQ", "emoneydone.png")
    if os.path.exists("emoneyshow.png") == False:
        downloadGDrive("1FwZ0TY-I7L7c4GwWeBkcXi1zeivE4GMc", "emoneyshow.png")
    if os.path.exists("menucash.png") == False:
        downloadGDrive("1ORaFnSxOjXZrE8wImdB_5Rh4wvRwdUe8", "menucash.png")
    if os.path.exists("menuemoney.png") == False:
        downloadGDrive("1TrojiziQUDm8vHoWnE1NldfAWbRkO7ER", "menuemoney.png")
    if os.path.exists("menuqr.png") == False:
        downloadGDrive("1dv0lHigW7jLJfLhtuDMy_LYedvexgz48", "menuqr.png")
    if os.path.exists("opsipembayaran-off.png") == False:
        downloadGDrive("1fNness_IZpSxTmrDkIZgd_0GwFQBvEJP", "opsipembayaran-off.png")
    if os.path.exists("opsipembayaran-on.png") == False:
        downloadGDrive("1ztOTo-po85ItbljyJ-eZunTZ5P1u3ZlV", "opsipembayaran-on.png")
    if os.path.exists("qrshow.png") == False:
        downloadGDrive("1kjXoWZg8SAcdj4lRpSyUk_88YyjGk_LR", "qrshow.png")

def stream(label):
    x = 0
    video_name = "welcome.mp4"
    video = imageio.get_reader(video_name)
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        label.config(image=frame_image)
        label.image = frame_image
        if x == 0:
            adjustWindow(frame_image.width(), frame_image.height(), center=True)
            x += 1
    label.destroy()
    opsiPembayaran()

def opsiPembayaran():
    global image_name
    root.title("Vending Machine Minuman")
    def handleClick(button_place, button_no=0):
        label.destroy()
        if button_place == "top":
            adminMode()
        elif button_place == "mid":
            if button_no == 1:
                mainMenu(payment="cash")
            elif button_no == 2:
                mainMenu(payment="qr")
            elif button_no == 3:
                mainMenu(payment="emoney")
        elif button_place == "bot":
            aboutUs()
    label = tk.Label(root)
    label.pack()
    if emptyStock == True:
        image_name = "opsipembayaran-off.png"
    else:
        image_name = "opsipembayaran-on.png"
    image = ImageTk.PhotoImage(file=image_name)
    label.config(image=image)
    label.image = image
    button_top = tk.Button(root, text="Admin Mode", height=3, width=15, font=(None, 12), command=lambda: handleClick("top"))
    button_top.place(x=628, y=72, anchor=tk.CENTER)
    button_mid_1 = tk.Button(root, text="Cash", height=2, width=19, font=(None, 12), command=lambda: handleClick("mid", 1))
    button_mid_1.place(x=360, y=307, anchor=tk.CENTER)
    button_mid_2 = tk.Button(root, text="QR", height=2, width=19, font=(None, 12), command=lambda: handleClick("mid", 2))
    button_mid_2.place(x=360, y=400, anchor=tk.CENTER)
    button_mid_3 = tk.Button(root, text="E-Money", height=2, width=19, font=(None, 12), command=lambda: handleClick("mid", 3))
    button_mid_3.place(x=360, y=492, anchor=tk.CENTER)
    button_bot = tk.Button(root, text="About Us", height=4, width=18, font=(None, 12), command=lambda: handleClick("bot"))
    button_bot.place(x=126, y=623, anchor=tk.CENTER)
    adjustWindow(image.width(), image.height())

def adminMode():
    def handleClick(button_place, button_no=0):
        global moneySpent
        def addStock(item_no):
            stocks[item_no-1] += 1
            updateStock()
            messagebox.showinfo("Succeed", f'Berhasil menambahkan stok untuk item {names[item_no-1]}')
        def lessStock(item_no):
            if stocks[item_no-1] > 0:
                stocks[item_no-1] -= 1
                updateStock()
                messagebox.showinfo("Succeed", f'Berhasil mengurangi stok untuk item {names[item_no-1]}')
            else:
                messagebox.showinfo("Failed", f'Gagal mengurangi stok untuk item {names[item_no-1]}, stok sudah habis')
        if button_place == "top":
            label.destroy()
            opsiPembayaran()
        elif button_place == "mid":
            if button_no % 2 == 0:
                addStock(button_no // 2)
            else:
                lessStock((button_no // 2) + 1)
        elif button_place == "bot":
            if moneySpent > 0:
                messagebox.showinfo("Succeed", f'Berhasil mengambil uang sebanyak {str(moneySpent)}')
                moneySpent = 0
                label_top.config(text=str(moneySpent))
            else:
                messagebox.showinfo("Failed", "Gagal mengambil uang, belum ada uang yang terkumpul")
    def updateStock():
        global emptyStock
        try:
            stocks.index(0)
            emptyStock = True
        except:
            emptyStock = False
        if stocks[0] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[0]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=197, y=352, anchor=tk.CENTER)
        if stocks[1] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[1]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=437, y=350, anchor=tk.CENTER)
        if stocks[2] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[2]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=677, y=352, anchor=tk.CENTER)
        if stocks[3] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[3]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=197, y=634, anchor=tk.CENTER)
        if stocks[4] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[4]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=437, y=632, anchor=tk.CENTER)
        if stocks[5] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[5]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=677, y=634, anchor=tk.CENTER)
    label = tk.Label(root)
    label.pack()
    image_name = "adminmode.png"
    image = ImageTk.PhotoImage(file=image_name)
    label.config(image=image)
    label.image = image
    adjustWindow(image.width(), image.height())
    updateStock()

    label_top = tk.Label(root, text=str(moneySpent), width=10, font=(None, 22), bg="#ffdcc4", anchor=tk.W)
    label_top.place(x=860, y=230)

    button_top = tk.Button(root, text="Kembali", height=2, width=19, font=(None, 12), command=lambda: handleClick("top"))
    button_top.place(x=951, y=95, anchor=tk.CENTER)
    button_mid_1_left = tk.Button(root, text="-", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 1))
    button_mid_1_left.place(x=137, y=386, anchor=tk.CENTER)
    button_mid_1_right = tk.Button(root, text="+", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 2))
    button_mid_1_right.place(x=237, y=386, anchor=tk.CENTER)
    button_mid_2_left = tk.Button(root, text="-", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 3))
    button_mid_2_left.place(x=377, y=386, anchor=tk.CENTER)
    button_mid_2_right = tk.Button(root, text="+", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 4))
    button_mid_2_right.place(x=477, y=386, anchor=tk.CENTER)
    button_mid_3_left = tk.Button(root, text="-", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 5))
    button_mid_3_left.place(x=617, y=386, anchor=tk.CENTER)
    button_mid_3_right = tk.Button(root, text="+", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 6))
    button_mid_3_right.place(x=717, y=386, anchor=tk.CENTER)
    button_mid_4_left = tk.Button(root, text="-", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 7))
    button_mid_4_left.place(x=137, y=668, anchor=tk.CENTER)
    button_mid_4_right = tk.Button(root, text="+", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 8))
    button_mid_4_right.place(x=237, y=668, anchor=tk.CENTER)
    button_mid_5_left = tk.Button(root, text="-", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 9))
    button_mid_5_left.place(x=377, y=668, anchor=tk.CENTER)
    button_mid_5_right = tk.Button(root, text="+", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 10))
    button_mid_5_right.place(x=477, y=668, anchor=tk.CENTER)
    button_mid_6_left = tk.Button(root, text="-", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 11))
    button_mid_6_left.place(x=617, y=668, anchor=tk.CENTER)
    button_mid_6_right = tk.Button(root, text="+", height=1, width=3, font=(None, 16), command=lambda: handleClick("mid", 12))
    button_mid_6_right.place(x=717, y=668, anchor=tk.CENTER)
    button_bot = tk.Button(root, text="Ambil", height=1, width=9, font=(None, 16), command=lambda: handleClick("bot"))
    button_bot.place(x=923, y=297, anchor=tk.CENTER)

def mainMenu(payment="cash"):
    global emoney
    root.title("Vending Machine Minuman")
    def handleClick(button_place, button_no=0):
        global emoney
        if button_place == "top":
            label.destroy()
            emoney = 0
            opsiPembayaran()
        elif button_place == "mid":
            buyDrink(button_no)
        elif button_place == "bot":
            if payment == "cash":
                if button_no == 1:
                    topUp(5000)
                elif button_no == 2:
                    topUp(10000)
                elif button_no == 3:
                    topUp(20000)
                elif button_no == 4:
                    topUp(50000)
                elif button_no == 5:
                    topUp(100000)
            elif payment == "emoney":
                updateMoney()
    def topUp(amount, acc=None):
        global money, balance, emoney
        return_text = f'Berhasil memasukkan uang sebanyak {str(amount)}'
        if payment == "cash":
            if (money + amount) < 500000:
                money += amount
                updateMoney()
            else:
                messagebox.showinfo("Failed", "Gagal memasukkan uang, uang tidak boleh melebihi batas (500000)")
        elif payment == "qr":
            i = accounts.index(acc)
            balance = balances[i]
            balance += amount
            updateMoney()
            balances[i] = balance
            return_text += f' ke rekening {acc}'
        elif payment == "emoney":
            emoney += amount
            updateMoney()
        messagebox.showinfo("Succeed", return_text)
    def buyDrink(item_no):
        global money, emoney, moneySpent
        if stocks[item_no-1] > 0:
            if payment == "cash":
                if money >= prices[item_no-1]:
                    money -= prices[item_no-1]
                    moneySpent += prices[item_no-1]
                    updateMoney()
                    stocks[item_no-1] -= 1
                    updateStock()
                    messagebox.showinfo("Succeed", f'Berhasil membeli {names[item_no-1]}')
                else:
                    messagebox.showinfo("Failed", f'Gagal membeli {names[item_no-1]} karena uang tidak mencukupi')
            elif payment == "qr":
                if balance > prices[item_no-1]:
                    label.destroy()
                    showQr(item_no)
                else:
                    messagebox.showinfo("Failed", f'Gagal membeli {names[item_no-1]} karena saldo tidak mencukupi')
            elif payment == "emoney":
                if emoney >= prices[item_no-1]:
                    label.destroy()
                    showCard(item_no)
                else:
                    messagebox.showinfo("Failed", f'Gagal membeli {names[item_no-1]} karena e-money tidak mencukupi')
        else:
            messagebox.showinfo("Failed", f'Gagal membeli {names[item_no-1]} karena stok habis.')
    def updateMoney():
        if payment == "cash":
            label_top = tk.Label(root, text=str(money), width=16, font=(None, 22), bg="#ffdcc4", anchor=tk.W)
            label_top.place(x=530, y=75)
        elif payment == "qr":
            label_top = tk.Label(root, text=str(balance), width=16, font=(None, 22), bg="#ffdcc4", anchor=tk.W)
            label_top.place(x=530, y=75)
        elif payment == "emoney":
            label_top = tk.Label(root, text=str(emoney), width=16, font=(None, 22), bg="#ffdcc4", anchor=tk.W)
            label_top.place(x=530, y=75)
    def updateStock():
        global emptyStock
        try:
            stocks.index(0)
            emptyStock = True
        except:
            emptyStock = False
        if stocks[0] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[0]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=197, y=352, anchor=tk.CENTER)
        if stocks[1] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[1]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=437, y=350, anchor=tk.CENTER)
        if stocks[2] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[2]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=677, y=352, anchor=tk.CENTER)
        if stocks[3] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[3]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=197, y=634, anchor=tk.CENTER)
        if stocks[4] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[4]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=437, y=632, anchor=tk.CENTER)
        if stocks[5] >= 0:
            label_stock_1 = tk.Label(root, text=str(stocks[5]), font=(None, 12), bg="#ffdcc4")
            label_stock_1.place(x=677, y=634, anchor=tk.CENTER)
    label = tk.Label(root)
    label.pack()
    if payment == "cash":
        image_name = "menucash.png"
    elif payment == "qr":
        image_name = "menuqr.png"
    elif payment == "emoney":
        image_name = "menuemoney.png"
    image = ImageTk.PhotoImage(file=image_name)
    label.config(image=image)
    label.image = image
    adjustWindow(image.width(), image.height())
    updateMoney()
    updateStock()

    button_top = tk.Button(root, text="Kembali", height=2, width=19, font=(None, 12), command=lambda: handleClick("top"))
    button_top.place(x=951, y=95, anchor=tk.CENTER)
    button_mid_1 = tk.Button(root, text="10.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("mid", 1))
    button_mid_1.place(x=186, y=390, anchor=tk.CENTER)
    button_mid_2 = tk.Button(root, text="10.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("mid", 2))
    button_mid_2.place(x=426, y=388, anchor=tk.CENTER)
    button_mid_3 = tk.Button(root, text="10.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("mid", 3))
    button_mid_3.place(x=666, y=390, anchor=tk.CENTER)
    button_mid_4 = tk.Button(root, text="7.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("mid", 4))
    button_mid_4.place(x=186, y=672, anchor=tk.CENTER)
    button_mid_5 = tk.Button(root, text="7.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("mid", 5))
    button_mid_5.place(x=426, y=670, anchor=tk.CENTER)
    button_mid_6 = tk.Button(root, text="7.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("mid", 6))
    button_mid_6.place(x=666, y=672, anchor=tk.CENTER)
    if payment == "cash":
        root.title("Vending Machine Minuman - Metode Pembayaran Cash")
        button_bot_1 = tk.Button(root, text="+5.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("bot", 1))
        button_bot_1.place(x=898, y=228, anchor=tk.CENTER)
        button_bot_2 = tk.Button(root, text="+10.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("bot", 2))
        button_bot_2.place(x=1003, y=228, anchor=tk.CENTER)
        button_bot_3 = tk.Button(root, text="+20.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("bot", 3))
        button_bot_3.place(x=898, y=295, anchor=tk.CENTER)
        button_bot_4 = tk.Button(root, text="+50.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("bot", 4))
        button_bot_4.place(x=1003, y=295, anchor=tk.CENTER)
        button_bot_5 = tk.Button(root, text="+100.000", height=2, width=9, font=(None, 12), command=lambda: handleClick("bot", 5))
        button_bot_5.place(x=951, y=365, anchor=tk.CENTER)
    elif payment == "qr":
        root.title("Vending Machine Minuman - Metode Pembayaran QR")
        def getValue(*args):
            global balance, account
            acc = var.get()
            i = accounts.index(acc)
            balance = balances[i]
            account = acc
            updateMoney()
        def addBalance():
            amount = int(entry.get())
            acc = var.get()
            topUp(amount, acc)
        var = tk.StringVar()
        var.set(account)
        var.trace("w", getValue)
        option_account = tk.OptionMenu(root, var, *accounts)
        option_account.config(font=(None, 12), highlightthickness=0)
        option_account.place(x=940, y=225, width=160, height=50, anchor=tk.CENTER)
        optionmenu = root.nametowidget(option_account.menuname)
        optionmenu.config(font=(None, 12))
        entry = tk.Entry(width=10, highlightthickness=0, font=(None, 15))
        entry.place(x=920, y=353, width=120, height=40, anchor=tk.CENTER)

        button_bot = tk.Button(root, text="Enter", height=2, width=6, command=addBalance)
        button_bot.place(x=1014, y=352, anchor=tk.CENTER)
    elif payment == "emoney":
        root.title("Vending Machine Minuman - Metode Pembayaran E-Money")
        def addEmoney():
            amount = int(entry.get())
            topUp(amount)
        entry = tk.Entry(width=10, highlightthickness=0, font=(None, 15))
        entry.place(x=920, y=223, width=120, height=40, anchor=tk.CENTER)
        button_bot = tk.Button(root, text="Enter", height=2, width=6, command=addEmoney)
        button_bot.place(x=1014, y=223, anchor=tk.CENTER)

def showQr(item_no):
    global balance, balances, qr_bool, moneySpent
    root.title("Metode Pembayaran QR - Scan QR")
    qr_bool = False
    def handleClick(button_place):
        if button_place == "top":
            global qr_bool
            clearWidgets()
            qr_bool = True
            mainMenu(payment="qr")
    def handleDone():
        clearWidgets()
        mainMenu(payment="qr")
        messagebox.showinfo("Succeed", f'Berhasil membeli {names[item_no-1]}')
    def clearWidgets():
        widgets = root.pack_slaves()
        for widget in widgets:
            widget.destroy()
    label = tk.Label(root)
    label.pack()
    image_name = "qrshow.png"
    image = ImageTk.PhotoImage(file=image_name)
    label.config(image=image)
    label.image = image
    label_top = tk.Label(text="180", font=(None, 30), bg="#fec89a")
    label_top.place(x=540, y=45, anchor=tk.CENTER)
    label_bot = tk.Label(text=names[item_no-1], font=(None, 15), bg="white")
    label_bot.place(x=540, y=630, anchor=tk.CENTER)
    button_top = tk.Button(text="Kembali", height=2, width=24, command=lambda: handleClick("top"))
    button_top.place(x=953, y=97, anchor=tk.CENTER)

    # Buat QR
    qr = qrcode.QRCode(version=1, box_size=12, border=5)
    qr.add_data(QR_URL + str(item_no))
    qr.make(fit=True)
    qr = qr.make_image(fill="black", back_color="white")
    qr.save("qr.png")
    qr_image = ImageTk.PhotoImage(file="qr.png")
    label_mid = tk.Label(image=qr_image, bd=0)
    label_mid.image = qr_image
    label_mid.place(x=540, y=360, anchor=tk.CENTER)

    # Request pertama
    request_1 = requests.get(API_URL, headers=HEADER).json()

    rundown_time = 0
    time_1 = time.time()
    time_2 = time.time()
    while rundown_time < 180:
        time_3 = time.time()
        if int(time_3 - time_2) == 1:
            rundown_time += 1
            time_2 = time_3
            label_top.config(text=180-rundown_time)
            root.update()
            if rundown_time % 10 == 0:
                request_2 = requests.get(API_URL, headers=HEADER).json()
                if len(request_2["data"]) > len(request_1["data"]):
                    for i in range(len(request_2["data"])):
                        if request_2["data"][i]["event"]["path"] == '/' + str(item_no):
                            if request_2["data"][i]["id"][:10] > str(int(time_1)):
                                rundown_time = 181
                                stocks[item_no-1] -= 1
                                i = accounts.index(account)
                                balance -= prices[item_no-1]
                                moneySpent += prices[item_no-1]
                                balances[i] = balance
                                mainMenu("qr")
                                root.after(0, handleDone)
        if qr_bool == True:
            qr_bool = False
            break
    root.after(0, lambda: handleClick("top"))

def showCard(item_no):
    root.title("Metode Pembayaran E-Money - Scan Card")
    def handleClick(button_place):
        if button_place == "top":
            label.destroy()
            mainMenu("emoney")
        elif button_place == "bot":
            label.destroy()
            showCardDone(item_no)
    label = tk.Label(root)
    label.pack()
    image_name = "emoneyshow.png"
    image = ImageTk.PhotoImage(file=image_name)
    label.config(image=image)
    label.image = image

    button_top = tk.Button(root, text="Kembali", height=2, width=19, font=(None, 12), command=lambda: handleClick("top"))
    button_top.place(x=951, y=97, anchor=tk.CENTER)
    button_bot = tk.Button(root, text="Scan", height=2, width=19, font=(None, 22), command=lambda: handleClick("bot"))
    button_bot.place(x=542, y=650, anchor=tk.CENTER)

def showCardDone(item_no):
    global emoney, moneySpent
    root.title("Metode Pembayaran E-Money - Scan Card Done")
    def handleBack():
        messagebox.showinfo("Succeed", f'Anda berhasil membeli {names[item_no-1]}')
        label.destroy()
        mainMenu("emoney")
    label = tk.Label(root)
    label.pack()
    image_name = "emoneydone.png"
    image = ImageTk.PhotoImage(file=image_name)
    label.config(image=image)
    label.image = image
    stocks[item_no-1] -= 1
    emoney -= prices[item_no-1]
    moneySpent += prices[item_no-1]
    root.after(2000, handleBack)

def aboutUs():
    root.title("Vending Machine Minuman - About Us")
    def handleClick(button_place):
        if button_place == "bot":
            label.destroy()
            opsiPembayaran()
    label = tk.Label(root)
    label.pack()
    image_name = "aboutus.png"
    image = ImageTk.PhotoImage(file=image_name)
    label.config(image=image)
    label.image = image
    adjustWindow(image.width(), image.height())
    button_bot = tk.Button(root, text="Kembali", height=4, width=22, command=lambda: handleClick("bot"))
    button_bot.place(x=360, y=639, anchor=tk.CENTER)

def adjustWindow(app_width, app_height, center=False):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width - app_width)/2)
    y = int((screen_height - app_height)/2) - 40
    if center:
        root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    else:
        root.geometry(f'{app_width}x{app_height}')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Vending Machine Minuman - Welcome")
    download()
    label = tk.Label(root)
    label.pack()
    thread = threading.Thread(target=stream, args=(label,))
    thread.daemon = 1
    thread.start()
    root.mainloop()