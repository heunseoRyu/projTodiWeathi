import tkinter
from tkinter import *
from tkinter.ttk import Combobox
import json
import datetime


#json 파일에 사용자 정보 저장
def sendInform(ID,pos,weathi):
    file_path = './UserInform.json'
    data = {}
    data['posts'] = []
    data['posts'].append({
        'name': ID,
        'city': pos,
        'weathi': weathi
    })
    data['targets'] = []
    data['targets'].append({})

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)

#json파일에 새로운 목표 저장
def sendPlace(now,target):
    with open('UserInform.json','r') as file:
        data = json.load(file)
    if 'targets' not in data:
        data['targets'] = [{}]

    data['targets'][0][now] = target
    with open('userInform.json','w') as file:
        json.dump(data,file)

#아이디가 영문자인지 체크
def checkID(windw,ID):
    for i in ID:
        if 97 > ord(i) or ord(i) > 122:
            show_warning(windw,"이름은 영어소문자로 이루어져야 합니다.")
            return False
    else:
        return True

# 사용자가 입력 잘못했을때 경고창
def show_warning(windw,content):
    warn = Label(windw, text=content)
    warn.place(x=300, y=300)
    windw.after(3000, lambda: warn.destroy())

# 목표 받는 인터페이스
def gtTarget(now):
    targt = Tk()
    targt.title("TodiWeathi")  # 창 이름
    targt.geometry('614x355')
    flag = 0
    label = Label(targt,text="오늘의 목표지는?")
    limit = Label(targt,text="(영소문자 10이내의 간단한 목표지를 입력하세요.)")
    entry = Entry(targt,width=40,border=1,relief='solid')

    def clickEvent():
        target1 = entry.get()
        if len(target1) > 10:
            show_warning(targt,"목표는 10글자 이내입니다.")
            return
        elif not checkID(targt,target1):
            return
        else:
            sendPlace(now,target1)
            targt.destroy()
            target = target1
    submit = Button(targt, text="제출", command=clickEvent)

    label.place(x=272,y=80)
    limit.place(x=180,y=100)
    entry.place(x=130,y=120)
    submit.place(x=280,y=160)

    targt.mainloop()


# 사용자 정보 받기
def gtUserInform():
    # 창 조절
    root = Tk()  # tkinter 모듈의 Tk()클래스 호출 -> 화면에 창 띄워줌.
    root.title("TodiWeathi")  # 창 이름
    root.geometry('614x355')  # 창 크기 지정
    root.resizable(width=False, height=False)  # 창 크기 고정

    # 사용자 이름 입력
    Name = Label(root,text='이름을 입력하시오: ') #넣을 텍스트 정보 저장
    Nlimit = Label(root,text='(영어소문자)(10글자 이내)')
    getNm = Entry(root,width=30,border=1,relief='solid')
    flag = 0
    # 사용자 거주지 입력
    Ci = Label(root, text='거주지를 선택하시오: ')
    getCi = Combobox(root)
    getCi['values'] =("수도권/광역시","Seoul","Busan","Ulsan","Incheon","Gwangju","Daejeon","Daegu","Gyeonggi-do")
    getCi.current(0)

    # 싫어하는 날씨 입력
    wstW = Label(root,text='싫어하는 날씨를 선택하시오: ')
    AtmosDsc = Label(root,text="*Atmosphere? Mist,smoke,haze,sand/dust,fog etc")
    getWW = Combobox(root)
    getWW['values'] =("날씨","Thunderstorm","Drizzle","Rain","Snow","Clear","Clouds","Atmosphere")
    getWW.current(0)




    # 제출 버튼 눌렀을때
    def clickEvent():
        flag = 0 # 입력 완료 여부
        ID = getNm.get()
        pos = getCi.get()
        weathi = getWW.get()
        weathers = ["Thunderstorm","Drizzle","Rain","Snow","Clear","Clouds","Atmosphere"]
        poses = ["Seoul","Busan","Ulsan","Incheon","Gwangju","Daejeon","Daegu","Gyeonggi-do"]
        '''
        1. 이름이 10글자보다 긴 경우 
        2. 영문자가 아닌 문자가 들어있는 경우
        3. 지역을 선택하지 않은 경우
        4. 날씨를 선택하지 않은 경우
        '''
        if len(ID) > 10:
            show_warning(root,"이름은 10자 이내입니다.")
            return
        elif not checkID(root,ID):
            return
        elif pos not in poses:
            show_warning(root,"거주하는 도시를 선택해주세요.")
            return
        elif weathi not in weathers:
            show_warning(root,"싫어하는 날씨를 선택해주세요.")
            return
        # 값 보내고 창 닫기
        else:
            sendInform(ID,pos,weathi)
            root.destroy()
            return



    # 버튼
    submit = Button(root,text="제출",command=clickEvent)

    # 위치 정하기
    Name.place(x=120,y=80)
    getNm.place(x=225,y=80)
    Nlimit.place(x=120,y=100)

    Ci.place(x=120,y=130)
    getCi.place(x=230,y=130)

    wstW.place(x=120,y=160)
    AtmosDsc.place(x=120,y=180)
    getWW.place(x=230,y=160)

    submit.place(x=270,y=220)
    root.mainloop()

def showInterface():
    interface = Tk()
    interface.title("todiWeathi")
    interface.geometry("614x355")


    interface.mainloop()







file_path = './UserInform.json'

#사용자 정보 불러오기
while True:
    try:
        with open(file_path, "r") as json_file:
            user_data = json.load(json_file)
            userID = user_data['posts'][0]['name']
            city = user_data['posts'][0]['city']
            wrstW = user_data['posts'][0]['weathi']
        break
# 정보가 없으면 새로 입력받기
    except:
        gtUserInform()

now = datetime.datetime.now()
now_str = f"{now.year}.{now.month}.{now.day}"

# 목표 불러오기
with open(file_path, "r") as json_file:
    user_data = json.load(json_file)


try:
    target = user_data["targets"][0][now_str]
except KeyError:
    target = gtTarget(now_str)


print(target)
showInterface()