import requests
import json

city = "Seoul" # 도시
apiKey = "hidden" # API 키
lang = "kr" # 언어
units = "metric" # 섭씨 온도로 변경

# API 요청을 보낼 URL 생성
api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}&units={units}"
print(api)
# API 호출
response = requests.post(api)

# 응답 결과 확인
if response.status_code == 200:
    result = json.loads(response.text)
    print(result)
else:
    print("API 요청에 실패했습니다. 상태 코드:", response.status_code)
