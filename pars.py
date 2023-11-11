import json

import requests

from bs4 import BeautifulSoup



url = 'https://megogo.net/ua/search-extended?category_id=16&main_tab=filters&sort=popular&vod_free=true'


res = requests.get(url)


# with open('megogo.html', 'w', encoding='utf-8') as file:
#     file.write(res.html.html)

# Використання BeautifulSoup для аналізу HTML
soup = BeautifulSoup(res.text, 'html.parser')

# Знаходження всіх елементів div з класом "card videoItem"
video_cards = soup.find_all('div', class_='videoItem')
print(f"Cards count: {len(video_cards)}")


films = []
# Перегляд кожної карти і витягнення необхідних даних
for card in video_cards:
    title = card.find('h3', class_='video-title').text.strip()
    year = card.find('span', class_='video-year').text.strip()
    country = card.find('span', class_='video-country').text.strip()
    free_label = card.find('div', class_='free-label').text.strip()
    image_url = card.find('img')['data-original']
    video_url = card.find('a', class_='overlay')['href']

    res= requests.get(video_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    discription = soup.find('div', class_='video-description').text.strip()
    
    
    
    # Виведення отриманих даних
    films.append({
        'title': title,
        'year': year,
        'country': country,
        'discription': discription,
        'image_url': image_url,
        'video_url': video_url,
    })
        
    print(f"Title: {title}")
    
with open('films.json', 'w', encoding='utf-8') as file:
    json.dump(films, file, indent=4, ensure_ascii=False)
