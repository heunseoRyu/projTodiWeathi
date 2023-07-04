import tkinter
from time import sleep
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import Tk
import json
import datetime
import requests
import random

# json 파일에 사용자 정보 저장
def sendInform(ID, pos, weathi):
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
    data['stickers'] = []
    data['stickers'].append({})
    data['stickers'].append({'cnt': 0})
    data['character'] = []
    data['character'].append(['knife','tears','mist','orange','pear'])
    data['character'].append([])

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)


# json파일에 새로운 목표 저장
def sendPlace(now, target):
    with open('UserInform.json', 'r') as file:
        data = json.load(file)
    if 'targets' not in data:
        data['targets'] = [{}]

    data['targets'][0][now] = target
    with open('userInform.json', 'w') as file:
        json.dump(data, file)


# 아이디가 영문자인지 체크
def checkID(windw, ID):
    for i in ID:
        if 97 > ord(i) or ord(i) > 122:
            show_warning(windw, "이름은 영어소문자로 이루어져야 합니다.")
            return False
    else:
        return True


# 사용자가 입력 잘못했을때 경고창
def show_warning(windw, content):
    warn = Label(windw, text=content)
    warn.place(x=300, y=300)
    windw.after(3000, lambda: warn.destroy())


# 목표 받는 인터페이스
def gtTarget(now):
    targt = Tk()
    targt.title("TodiWeathi")  # 창 이름
    targt.geometry('614x355')
    targt.resizable(False, False)

    label = Label(targt, text="오늘의 목표지는?")
    limit = Label(targt, text="(영소문자 10이내의 간단한 목표지를 입력하세요.)")
    entry = Entry(targt, width=40, border=1, relief='solid')

    def clickEvent():
        target1 = entry.get()
        if target1 == '':
            show_warning(targt, "목표를 입력해주세요.")
        elif len(target1) > 10:
            show_warning(targt, "목표는 10글자 이내입니다.")
            return
        elif not checkID(targt, target1):
            return
        else:
            sendPlace(now, target1)
            global target
            target = target1
            targt.destroy()

    submit = Button(targt, text="제출", command=clickEvent)

    label.place(x=272, y=80)
    limit.place(x=180, y=100)
    entry.place(x=130, y=120)
    submit.place(x=280, y=160)

    targt.mainloop()


# 사용자 정보 받기
def gtUserInform():
    # 창 조절
    root = Tk()  # tkinter 모듈의 Tk()클래스 호출 -> 화면에 창 띄워줌.
    root.title("TodiWeathi")  # 창 이름
    root.geometry('614x355')  # 창 크기 지정
    root.resizable(width=False, height=False)  # 창 크기 고정

    # 사용자 이름 입력
    Name = Label(root, text='이름을 입력하시오: ')  # 넣을 텍스트 정보 저장
    Nlimit = Label(root, text='(영어소문자)(10글자 이내)')
    getNm = Entry(root, width=30, border=1, relief='solid')

    # 사용자 거주지 입력
    Ci = Label(root, text='거주지를 선택하시오: ')
    getCi = Combobox(root)
    getCi['values'] = ("수도권/광역시", "Seoul", "Busan", "Ulsan", "Incheon", "Gwangju", "Daejeon", "Daegu", "Gyeonggi-do")
    getCi.current(0)

    # 싫어하는 날씨 입력
    wstW = Label(root, text='싫어하는 날씨를 선택하시오: ')
    AtmosDsc = Label(root, text="*Atmosphere? Mist,smoke,haze,sand/dust,fog etc")
    getWW = Combobox(root)
    getWW['values'] = ("날씨", "Thunderstorm", "Drizzle", "Rain", "Snow", "Clear", "Clouds", "Atmosphere")
    getWW.current(0)

    # 제출 버튼 눌렀을때
    def clickEvent():
        flag = 0  # 입력 완료 여부
        ID = getNm.get()
        pos = getCi.get()
        weathi = getWW.get()
        weathers = ["Thunderstorm", "Drizzle", "Rain", "Snow", "Clear", "Clouds", "Atmosphere"]
        poses = ["Seoul", "Busan", "Ulsan", "Incheon", "Gwangju", "Daejeon", "Daegu", "Gyeonggi-do"]
        '''
        1. 이름이 10글자보다 긴 경우 
        2. 영문자가 아닌 문자가 들어있는 경우
        3. 지역을 선택하지 않은 경우
        4. 날씨를 선택하지 않은 경우
        '''
        if ID == '':
            show_warning(root, "이름을 입력하시오.")
        elif len(ID) > 10:
            show_warning(root, "이름은 10자 이내입니다.")
            return
        elif not checkID(root, ID):
            return
        elif pos not in poses:
            show_warning(root, "거주하는 도시를 선택해주세요.")
            return
        elif weathi not in weathers:
            show_warning(root, "싫어하는 날씨를 선택해주세요.")
            return
        # 값 보내고 창 닫기
        else:
            sendInform(ID, pos, weathi)
            root.destroy()

    # 버튼
    submit = Button(root, text="제출", command=clickEvent)

    # 위치 정하기
    Name.place(x=120, y=80)
    getNm.place(x=225, y=80)
    Nlimit.place(x=120, y=100)

    Ci.place(x=120, y=130)
    getCi.place(x=230, y=130)

    wstW.place(x=120, y=160)
    AtmosDsc.place(x=120, y=180)
    getWW.place(x=230, y=160)

    submit.place(x=270, y=220)
    root.mainloop()


# 스티커 받은 기록 보는 곳
def chkStRecord(now):
    file_path = './UserInform.json'
    with open(file_path, "r") as json_file:
        user_data = json.load(json_file)
    stRecord = user_data['stickers'][0]
    if now in stRecord.keys():
        return True
    else:
        return False


def chgeSt(n,op):
    with open('UserInform.json', 'r') as file:
        data = json.load(file)
    cnt = data['stickers'][1]['cnt']
    if op==1:
        data['stickers'][1]['cnt'] -= n
    else:
        data['stickers'][1]['cnt'] += n

    with open('userInform.json', 'w') as file:
        json.dump(data, file)


def recordgetSt(now):
    with open('UserInform.json', 'r') as file:
        data = json.load(file)
    data['stickers'][0][now] = 'gg'
    with open('userInform.json', 'w') as file:
        json.dump(data, file)

def chkStCnt():
    with open('UserInform.json', 'r') as file:
        data = json.load(file)
    a = data['stickers'][1]['cnt']
    if a>=100:
        return True
    else:
        return False

def getCnt():
    with open('UserInform.json', 'r') as file:
        data = json.load(file)
    return data['stickers'][1]['cnt']

def GetCha():
    with open('UserInform.json', 'r') as file:
        data = json.load(file)
    index = random.randrange(len(data['character'][0]))
    data['character'][1].append(data['character'][0][index])
    del data['character'][0][index]

    with open('userInform.json', 'w') as file:
        json.dump(data, file)

def chaCnt():
    with open('UserInform.json', 'r') as file:
        data = json.load(file)
    return data['character'][1]

def clear():
    data = {}
    with open('userInform.json', 'w') as file:
        json.dump(data, file)

# 인터페이스 띄우는 함수
def showInterface(tmi, city, wrstW, target, now,ID):
    # 인터페이스 설정
    interface = Tk()
    interface.title("todiWeathi")
    interface.geometry("890x470+300+200")
    interface.resizable(False, False)
    interface.configure(bg="#57adff")
    Round_box = PhotoImage(file="image/검은사각형.png")
    Label(interface, image=Round_box, bg="#57adff").place(x=30, y=30)

    # 오른쪽 디자인
    tite = Label(interface, text="Weather", font=("Helvetica", 20), fg="white", bg="#203243")
    tite.place(x=50, y=16)

    label1 = Label(interface, text="Temperature", font=('Helvetica', 11), fg="white", bg="#203243")
    label1.place(x=50, y=80)

    label2 = Label(interface, text="Humidity", font=('Helvetica', 11), fg="white", bg="#203243")
    label2.place(x=50, y=100)

    label3 = Label(interface, text="Pressure", font=('Helvetica', 11), fg="white", bg="#203243")
    label3.place(x=50, y=120)

    label4 = Label(interface, text="Wind Speed", font=('Helvetica', 11), fg="white", bg="#203243")
    label4.place(x=50, y=140)

    label5 = Label(interface, text="Description", font=('Helvetica', 11), fg="white", bg="#203243")
    label5.place(x=50, y=160)

    t1 = Label(interface, text=tmi['temp'], font=("Helvetica", 11), fg="white", bg="#203243")
    t1.place(x=140, y=80)

    t2 = Label(interface, text=tmi['humid'], font=("Helvetica", 11), fg="white", bg="#203243")
    t2.place(x=140, y=100)

    t3 = Label(interface, text=tmi['pressure'], font=("Helvetica", 11), fg="white", bg="#203243")
    t3.place(x=140, y=120)

    t4 = Label(interface, text=tmi['windspeed'], font=("Helvetica", 11), fg="white", bg="#203243")
    t4.place(x=140, y=140)

    t5 = Label(interface, text=tmi['description'], font=("Helvetica", 11), fg="white", bg="#203243")
    t5.place(x=140, y=160)

    # 왼쪽 인터페이스 디자인
    loc = Label(interface, text=f'Location:{city}', font=("Helvetica", 30), fg="white", bg="#57adff")
    loc.place(x=650, y=10)

    temp = tmi['weather']

    # 날씨에 따라 아이콘 보이기
    if temp == 'Thunderstorm':
        icon = PhotoImage(file="image/thunderstorm.png")
        Label(interface, image=icon, bg="#57adff").place(x=700, y=40)
    elif temp == 'Drizzle':
        icon = PhotoImage(file="image/showerRain.png")
        Label(interface, image=icon, bg="#57adff").place(x=700, y=40)
    elif temp == 'Rain':
        a = tmi['description']
        if a == 'light rain' or a == 'moderate rain' or a == 'heavy intensity rain' or a == 'very heavy rain' or a == 'extreme rain':
            icon = PhotoImage(file="image/rain.png")
            Label(interface, image=icon, bg="#57adff").place(x=700, y=70)
        elif a == 'freezing rain':
            icon = PhotoImage(file="image/snow.png")
            Label(interface, image=icon, bg="#57adff").place(x=700, y=70)
        else:
            icon = PhotoImage(file="image/showerRain.png")
            Label(interface, image=icon, bg="#57adff").place(x=700, y=70)
    elif temp == 'Snow':
        icon = PhotoImage(file="image/snow.png")
        Label(interface, image=icon, bg="#57adff").place(x=700, y=70)
    elif temp == 'Atmosphere':
        icon = PhotoImage(file="image/scattered clouds.png")
        Label(interface, image=icon, bg="#57adff").place(x=700, y=70)
    elif temp == 'Clear':
        icon = PhotoImage(file="image/해.png")
        Label(interface, image=icon, bg="#57adff").place(x=700, y=70)
    else:
        a = tmi['description']
        if 'few clouds:' in a:
            icon = PhotoImage(file="image/few clouds.png")
            Label(interface, image=icon, bg="#57adff").place(x=700, y=70)
        elif 'scattered clouds' in a:
            icon = PhotoImage(file="image/scattered clouds.png")
            Label(interface, image=icon, bg="#57adff").place(x=700, y=70)
        else:
            icon = PhotoImage(file="image/brokenclouds.png")
            Label(interface, image=icon, bg="#57adff").place(x=700, y=70)


    hello = Label(interface, text=f"{ID}님! 오늘도 즐거운 하루되세요!", font=("Helvetica", 15), fg="white", bg="#57adff")
    hello.place(x=630, y=48)

    # 날씨 알려주기
    w = Label(interface, text=tmi['weather'], font=("Helvetica", 40), fg="white", bg="#203243")
    w.place(x=722, y=180)

    # 목적지 gui
    Round_box2 = PhotoImage(file="image/검은사각형 복사본.png")
    Label(interface, image=Round_box2, bg="#57adff").place(x=30, y=250)
    loc2 = Label(interface, text=f'오늘의 목적지:{target}', font=("Helvetica", 15), fg="white", bg="#203243")
    loc2.place(x=100, y=300)

    # 랜덤박스 gui
    Round_box3 = PhotoImage(file="image/검은사각형 복사본.png")
    Label(interface, image=Round_box3, bg="#57adff").place(x=322, y=250)
    giftI = PhotoImage(file="image/gift.png")
    Label(interface, image=giftI).place(x=340, y=270)
    ran = Label(interface, text='랜덤박스를 열고 캐릭터를 모으세요!', font=("Helvetica", 15), fg="white", bg="orange")
    ran.place(x=400, y=250)
    ran2 = Label(interface, text='칭찬스티커 100개 소요', font=("Helvetica", 15), fg="white", bg="#203243")
    ran2.place(x=450, y=290)

    #캐릭터들 gui
    characters = chaCnt()
    if 'knife' in characters:
        char1 = PhotoImage(file="image/캐릭터/신민호의칼날.png")
        Label(interface, image=char1,bg="#57adff").place(x=450, y=70)
    if 'tears' in characters:
        char2 = PhotoImage(file="image/캐릭터/창대쌤의눈물.png")
        Label(interface, image=char2,bg="#57adff").place(x=255, y=50)
    if 'mist' in characters:
        char3 = PhotoImage(file="image/캐릭터/먼지.png")
        Label(interface, image=char3,bg="#57adff").place(x=350, y=30)
    if 'orange' in characters:
        char4 = PhotoImage(file="image/캐릭터/오렌지.png")
        Label(interface, image=char4,bg="#57adff").place(x=525, y=70)
    if 'pear' in characters:
        char5 = PhotoImage(file="image/캐릭터/배.png")
        Label(interface, image=char5,bg="#57adff").place(x=550, y=160)
    if len(characters) ==0:
        cheer = Label(interface, text='목적지에 도착하고 칭찬스티커를 모아서 인터페이스를 채우세요!', font=("Helvetica", 15), fg="white", bg="#57adff")
        cheer.place(x=255, y=125)

    Round_box4 = PhotoImage(file="image/검은사각형 복사본 2.png")
    Label(interface, image=Round_box4, bg="#57adff").place(x=615, y=250)
    c = Label(interface, text='내 칭찬스티커 개수는?', font=("Helvetica", 15), fg="white", bg="#203243")
    c.place(x=675, y=290)



    # 알려줌
    def tellAbtStk(sent):
        warn = Label(interface, text=sent)
        warn.place(x=140, y=350)
        interface.after(3000, lambda: warn.destroy())

    def clickEvent(now, tmi, wrstW):
        # now = datetime.datetime.now()
        # now_str = f"{now.year}.{now.month}.{now.day}"
        if chkStRecord(now):
            tellAbtStk("오늘은 이미 받았습니다.")
            return
        else:
            recordgetSt(now)
            tellAbtStk("성공!!")

            if tmi['weather'] == wrstW:
                chgeSt(6,0)
                return
            else:
                chgeSt(3,0)
                return

    done = Button(interface, text="도착!", command=lambda: clickEvent(now, tmi, wrstW))  # 왜 람다를 썼냐 -> chatgpt
    done.place(x=140, y=330)

    def tellAbtStk2(sent):
        warn = Label(interface, text=sent)
        warn.place(x=400, y=400)
        interface.after(3000, lambda: warn.destroy())

    def clickEvent2():
        chas = chaCnt()
        if len(chas) >= 5:
            tellAbtStk2("캐릭터를 모두 수집했어요!")
            return
        if chkStCnt():
            chgeSt(100,1)
            GetCha()
            tellAbtStk2("구매완료!!과연 어떤 캐릭터가 찾아올까요?다음 방문때 확인하세요!")
        else:
            tellAbtStk2("돈없는데 누르면,스티커를 입에,넣어버리겠습니다.")
            return
    def clickEvent3():
        warn = Label(interface, text=f"{getCnt()}개 모았어요!")
        warn.place(x=800, y=400)
        interface.after(3000, lambda: warn.destroy())
    def clickEvent4():
        global clrBtCnt
        def clickEvent5():
            global clrBtCnt
            clrBtCnt = 0
            clr2.destroy()
            warn1 = Label(interface, text="취소되었습니다.", font="Helvetica 30")
            warn1.place(x=300, y=425)
            interface.after(3000, lambda: warn1.destroy())
        if not clrBtCnt:
            clr2 = Button(interface, text="초기화취소", command=clickEvent5)
            clr2.place(x=650, y=425)
            warn = Label(interface, text="정말 초기화하시겠습니까?버튼을 한번더 누르세요",font="Helvetica 30")
            warn.place(x=300, y=425)
            interface.after(3000, lambda: warn.destroy())
            clrBtCnt = 1
        else:
            # 초기화
            clear()
            print("5초뒤에 화면이 꺼집니다.")
            sleep(5)
            interface.destroy()
            return



    open = Button(interface, text="열기", command=clickEvent2)  # 왜 람다를 썼냐 -> chatgpt
    open.place(x=490, y=325)
    stkCnt = Button(interface,text="확인하기",command=clickEvent3)
    stkCnt.place(x=703,y=320)

    clr = Button(interface, text="내 정보 초기화", command=clickEvent4)
    clr.place(x=750, y=425)

    interface.mainloop()


def getWeather(city):
    city1 = city  # 도시
    apiKey = "hidden"  # API 키
    lang = "eng"  # 언어
    units = "metric"  # 섭씨 온도로 변경

    # API 요청을 보낼 URL 생성
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city1}&appid={apiKey}&lang={lang}&units={units}"

    # API 호출
    response = requests.post(api)  # api를 통해 받아온 데이터를 requests를 통해 응답받음.

    # 응답 결과 확인
    if response.status_code == 200:
        # 응답받은 데이터를 json 형태로 변환하여 저장
        result = json.loads(response.text)  # 이 중에서 원하는 정보만 뽑아오기 위한 쉬운 방법 => json 모듈 사용
        # 필요한 날씨 정보 추출
        tmi = {
            "weather": result["weather"][0]["main"],
            "temp": result["main"]["temp"],
            "humid": result["main"]["humidity"],
            "pressure": result["main"]["pressure"],
            "windspeed": result["wind"]["speed"],
            "description": result["weather"][0]["description"],
        }
        return tmi
    else:
        print("API 요청에 실패했습니다. 상태 코드:", response.status_code)


file_path = './UserInform.json'

# 사용자 정보 불러오기
while True:
    try:
        with open(file_path, "r") as json_file:
            user_data = json.load(json_file)
            userID = user_data['posts'][0]['name']
            city = user_data['posts'][0]['city']
            wrstW = user_data['posts'][0]['weathi']
        break
    # 정보가 없으면 새로 입력받기
    except :
        gtUserInform()

# 하루 가져오기
now = datetime.datetime.now()
now_str = f"{now.year}.{now.month}.{now.day}"


target = ''
# 목표 불러오기
with open(file_path, "r") as json_file:
    user_data = json.load(json_file)
try:
    target = user_data["targets"][0][now_str]
except KeyError:
    gtTarget(now_str)



tmi = getWeather(city)
clrBtCnt = 0

showInterface(tmi, city, wrstW, target, now_str,userID)