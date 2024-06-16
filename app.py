from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase 초기화
cred = credentials.Certificate('firebase-key/toy-project-283dc-firebase-adminsdk-3y0s8-751770dc39.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# 번역기 초기화
translator = GoogleTranslator(source='ja', target='ko')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    # 웹사이트에서 데이터 크롤링
    data = request.json
    print(request.json)
    url = data.url
    want_tag = data.tag
    want_type = data.type
    want_how = data.how
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    game_data = soup.body.find_all(class_=want_tag)
    data_list = []
    def translate_text(text):
        return translator.translate(text)
    if want_how == 'excel':
        for detail in game_data:
            title = detail.text
            # content = article.find('p').get_text()

            # 텍스트 번역
            translated_title = translate_text(title)
            # translated_content = translator.translate(content, src='en', dest='ko').text

            data_list.append({
                'title': title,
                'translated_title': translated_title,
                # 'content': content,
                # 'translated_content': translated_content
            })

        df = pd.DataFrame(data_list)
        df.to_excel('crawled_data.xlsx', index=False)

    else:
        for detail in game_data:
            title = detail.text

            # 텍스트 번역
            translated_title = translator.translate(title, src='ja', dest='ko').text

            data_list.append({
                'title': title,
                'translated_title': translated_title,
            })

            # Firestore에 데이터 저장
            doc_ref = db.collection('DATA_CRAWL').document(translated_title)
            doc_ref.set({
                'title': translated_title,
            })

    return "크롤링, 번역 및 Firestore 저장 완료!"

if __name__ == '__main__':
    app.run(debug=True)