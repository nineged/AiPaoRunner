'''
    Author:PWND0U
    Ver:1.0
'''
from tkinter import *
import tkinter.filedialog
import json
from random import randint, uniform
from tkinter import ttk
import requests


def encrypt(number):
    key = "xfvdmyirsg"
    numbers = list(map(int, list(str(number))))
    return_key = "".join([key[i] for i in numbers])
    return return_key


def pretty_print(jsonStr):
    print(json.dumps(json.loads(jsonStr), indent=4, ensure_ascii=False))


class Aipaoer(object):
    def __init__(self, IMEICode):
        self.IMEICode = IMEICode
        self.userName = ""
        self.userId = ""
        self.schoolName = ""
        self.token = ""
        self.runId = ""
        self.distance = 2400
        self.minSpeed = 2.0
        self.maxSpeed = 3.0
        self.shixiao = False

    def __str__(self):
        return str(self.__dict__).replace("\'", "\"")

    def check_imeicode(self):
        IMEICode = self.IMEICode
        url = "http://client3.aipao.me/api/%7Btoken%7D/QM_Users/Login_AndroidSchool?IMEICode={IMEICode}".format(
            IMEICode=IMEICode)
        rsp = requests.get(url)
        try:
            if rsp.json()["Success"]:
                okJson = rsp.json()
                self.token = okJson["Data"]["Token"]
                self.userId = okJson["Data"]["UserId"]
        except KeyError:
            print("IMEICode 失效")

    def get_info(self):
        token = self.token
        url = "http://client3.aipao.me/api/{token}/QM_Users/GS".format(token=token)
        rsp = requests.get(url)
        try:
            if rsp.json()["Success"]:
                okJson = rsp.json()
                self.userName = okJson["Data"]["User"]["NickName"]
                self.schoolName = okJson["Data"]["SchoolRun"]["SchoolName"]
                self.minSpeed = okJson["Data"]["SchoolRun"]["MinSpeed"]
                self.maxSpeed = okJson["Data"]["SchoolRun"]["MaxSpeed"]
                self.distance = okJson["Data"]["SchoolRun"]["Lengths"]
        except KeyError:
            print("Unknown error in get_info")

    def get_runId(self):
        token = self.token
        distance = self.distance
        url = "http://client3.aipao.me/api/{token}/QM_Runs/SRS?S1=40.62828&S2=120.79108&S3={distance}" \
            .format(token=token, distance=distance)
        rsp = requests.get(url)
        try:
            if rsp.json()["Success"]:
                self.runId = rsp.json()["Data"]["RunId"]
        except KeyError:
            print("Unknown error in get_runId")

    def upload_record(self):
        my_speed = round(uniform(self.minSpeed + 0.3, self.maxSpeed - 0.5), 2)
        my_distance = self.distance + randint(1, 5)
        my_costTime = int(my_distance // my_speed)
        my_step = randint(1555, 2222)
        print(my_speed, my_distance, my_costTime, my_step)
        myParams = {
            "token": self.token,
            "runId": self.runId,
            "costTime": encrypt(my_costTime),
            "distance": encrypt(my_distance),
            "step": encrypt(my_step)}
        url = "http://client3.aipao.me/api/{token}/QM_Runs/ES?" \
              "S1={runId}&S4={costTime}&S5={distance}&S6=A0A2A1A3A0&S7=1&S8=xfvdmyirsg&S9={step}".format(**myParams)
        rsp = requests.get(url)
        try:
            if rsp.json()["Success"]:
                #Label(main_box, text=str(self.IMEICode+"：" + self.userName+"：" + "成功!")).grid(row=rowIndex, column=0, columnspan=3)
                value = ["成功!",self.userName]
                tree.insert("", "end", text=self.IMEICode, values=value)
                print(self.userName + ": 成功!")
        except KeyError:
            #Label(main_box, text=str(self.IMEICode + "：失败")).grid(row=rowIndex, column=0, columnspan=3)
            value = ["失败!", self.userName]
            tree.insert("", "end", text=self.IMEICode, values=value)
            with open("失败.txt", "a+") as f:
                f.write(self.IMEICode + "\n")
            print("失败")


def selectPath():
    # 选择文件path_接收文件地址
    path_ = tkinter.filedialog.askopenfilename()

    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    # path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    global path_all
    path_all = ""
    path_all = path_
    path.set(path_)


def printPath():
    x = tree.get_children()
    for item in x:
        tree.delete(item)
    imeicodes = [IMCode.get()]
    IMEICodes = []
    if imeicodes[0] == '':
        imeicodes.pop()
        if path_all != "":
            with open(path_all, "rb") as fp:
                IMEICodes = fp.readlines()
                for IMEICode in IMEICodes:
                    IMEICode = IMEICode.decode("utf8")
                    imeicodes.append(IMEICode[:32])
            fp.close()
        else:
            print("请选择任意一种方式运行程序")
        print("读入 IMEICode完成，共 {}".format(len(IMEICodes)))
        print(imeicodes)
    if not imeicodes:
        return
    for IMEICode in imeicodes:
        if IMEICode[0] == "#":
            print("跳过：" + IMEICode)
            continue
        aipaoer = Aipaoer(IMEICode)
        aipaoer.check_imeicode()
        aipaoer.get_info()
        aipaoer.get_runId()
        aipaoer.upload_record()
        # pretty_print(str(aipaoer))
    # print(path_all)


def main():
    global main_box
    main_box = Tk()
    global win_table
    win_table = Tk()
    # 设置标题
    main_box.title('阳光长跑程序')
    # 设置窗口大小
    main_box.geometry('380x110')
    # 设置窗口是否可变长、宽，True：可变，False：不可变
    main_box.resizable(width=False, height=True)
    # 变量path
    global path
    path = StringVar()
    # IMCode
    global IMCode
    IMCode = StringVar()
    TextName = StringVar()
    # 输入框，标记，按键
    Label(main_box, text="目标路径: ").grid(row=0, column=0)
    # 输入框绑定变量path
    Entry(main_box, textvariable=path).grid(row=0, column = 1)
    Button(main_box, text="路径选择", command=selectPath).grid(row=0, column=2)
    Label(main_box, text="IMEICode: ").grid(row=1, column=0)
    # IMcode框
    Entry(main_box, textvariable=IMCode).grid(row=1, column=1)
    Label(main_box, text="单独给自己跑请填入\n批量选择txt文件 ").grid(row=1, column=2)
    # 把这里的command函数改成你自己的
    Button(main_box, text="开始跑步", command=printPath).grid(row=2, column = 1)
    win_table.title("结果：失败请查看当前目录底下(失败.txt)")  # #窗口标题
    win_table.geometry("400x300")  # #窗口位置500后面是字母x
    '''
    表格
    '''
    global tree
    tree = ttk.Treeview(win_table)  # #创建表格对象
    tree["columns"] = ("Status", "备注")  # #定义列
    tree.column("Status", width=75)
    tree.column("备注", width=75)
    tree.heading("Status", text="Status")
    tree.heading("备注", text="备注")
    tree.pack()
    main_box.mainloop()


if __name__ == "__main__":
    main()
