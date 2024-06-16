import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
cred = credentials.Certificate('firebase-key/toy-project-283dc-firebase-adminsdk-3y0s8-751770dc39.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# 번역기 초기화
translator = Translator()

# 웹사이트에서 데이터 크롤링
url = 'https://xn--bck3aza1a2if6kra4ee0hf.gamewith.jp/article/show/20722'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# 예시로, 기사 제목과 내용을 크롤링한다고 가정
game_data = soup.body.find_all(class_='_n')
data_list = []

for detail in game_data:
    title = detail.text
    # content = article.find('p').get_text()
    
    # 텍스트 번역
    translated_title = translator.translate(title, src='ja', dest='ko').text
    # translated_content = translator.translate(content, src='en', dest='ko').text

    data_list.append({
        'title': title,
        'translated_title': translated_title,
        # 'content': content,
        # 'translated_content': translated_content
    })

    # Firestore에 데이터 저장
    doc_ref = db.collection('DATA_CRAWL').document(translated_title)
    doc_ref.set({
        'title': translated_title,
        # 'translated_title': translated_title,
        # 'content': content,
        # 'translated_content': translated_content
    })

print("크롤링, 번역 및 Firestore 저장 완료!")