import requests

from typing import Any
from bs4 import BeautifulSoup
from datetime import datetime

class ChesuNews:
    def __init__(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            tg = BeautifulSoup(requests.get("https://www.chesu.ru").text, 'lxml').find_all('a', {'class':'image'})
            self.new_number = tg[0]['href'].split('=')[1] #Получение номера последней новости
            self.number = int(url.split('=')[1])

            self.tags = [tag.get_text().strip() for tag in soup.findAll('a', {"class": "tag"})]
            self.headline = soup.find('h3', {"class":"ma-title"}).get_text().strip()
            self.date = soup.find('div', {"class":"datetime"}).get_text().split()[0].strip()
            self.time = soup.find('div', {"class":"datetime"}).get_text().split()[2].strip()
            self.text = soup.find('div', {"class":"clearfix"}).get_text().strip()
            self.images = [img['src'] for img in soup.find_all('img')][1:len(soup.find_all('img'))-2]
            self.datetime = datetime.strptime(self.date + " " + self.time, '%d.%m.%Y %H:%M').strftime('%d.%m.%Y %H:%M')

        except:
            print("Ошибка при парсинге")
    
    def items(self):
        return {
            "number":self.number,
            "tags":self.tags,   
            "headline":self.headline, 
            "text":self.text, 
            "datetime":self.datetime, 
            "images":self.images
        }

        
    

def scrap_news(myPyrebase):
    tg = BeautifulSoup(requests.get("https://www.chesu.ru").text, 'lxml').find_all('a', {'class':'image'})
    new_number = int(tg[0]['href'].split('=')[1]) #Получение номера последней новости  
    print(new_number)  
    current_number = 7609
    while current_number != new_number:
        try:
            url = f"https://www.chesu.ru/news-item?p={current_number}"
            data = list(ChesuNews(url).items().values())
            
            print("Добавлена новость:", current_number)
            myPyrebase.set_news(id=data[0], datetime=data[4], headline=data[2], text=data[3], images=data[5], tags=data[1])
        
        except:
            print(f"Новость {current_number} не найдена")
        current_number = current_number + 1