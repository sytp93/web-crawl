import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import pandas as pd


# 번역기 초기화
translator = GoogleTranslator(source='ja', target='ko')

# 웹사이트에서 데이터 크롤링
url = 'https://xn--bck3aza1a2if6kra4ee0hf.gamewith.jp/article/show/20722'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# 예시로, 기사 제목과 내용을 크롤링한다고 가정
game_data = soup.body.find_all(class_='_n')
data_list = []

def translate_text(text):
    return translator.translate(text)

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

print("완료!!!!!!!!")