import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import Tk
import json
import datetime
import requests


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
        if len(target1) > 10:
            show_warning(targt, "목표는 10글자 이내입니다.")
            return
        elif not checkID(targt, target1):
            return
        else:
            sendPlace(now, target1)
            targt.destroy()
            target = target1

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
        if len(ID) > 10:
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
            return

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


def showInterface(tmi, city,target):
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
    ching = Label(interface, text=f'칭찬스티커:개', font=("Helvetica", 15), fg="white", bg="#57adff")
    ching.place(x=760, y=48)
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

    # 날씨 알려주기
    w = Label(interface, text=tmi['weather'], font=("Helvetica", 40), fg="white", bg="#57adff")
    w.place(x=722, y=180)

    # 목적지 gui
    Round_box2 = PhotoImage(file="image/검은사각형 복사본.png")
    Label(interface, image=Round_box2, bg="#57adff").place(x=30, y=250)
    loc2 = Label(interface, text=f'오늘의 목적지:{target}', font=("Helvetica", 15), fg="white", bg="#203243")
    loc2.place(x=100, y=300)
    done = Button(interface, text="도착!",command=clickEvent)
    done.place(x=140,y=330)
    # 칭찬스티커 개수 올리는 함수 구현
    
    def clickEvent():
    interface.mainloop()


def getWeather(city):
    city1 = city  # 도시
    apiKey = "24aa027670b6c7e617372b3c649ae18b"  # API 키
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
    except:
        gtUserInform()

# 하루 가져오기
now = datetime.datetime.now()
now_str = f"{now.year}.{now.month}.{now.day}"

# 목표 불러오기
with open(file_path, "r") as json_file:
    user_data = json.load(json_file)
try:
    target = user_data["targets"][0][now_str]
except KeyError:
    target = gtTarget(now_str)

tmi = getWeather(city)

# print(target)
showInterface(tmi, city,target)
