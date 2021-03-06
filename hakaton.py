import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BS(html, 'lxml')
    catalog = soup.find('div', class_='search-results-table')
    cars = catalog.find_all('div', class_='list-item list-label')
    for car in cars:
        try:
            title = car.find('h2', class_='name').text.strip()
        except:
            title = ''
        try:
            price = car.find('p', class_='price').find('strong').text.strip()
        except:
            price = ''
        try:
            img = car.find('div', class_='thumb-item-carousel').find('img').get('data-src')
        except:
            img = ''
        try:
            dscrb1 = car.find('p', class_='year-miles').text.strip()
            dscrb2 = car.find('p', class_='body-type').text.strip()
            dscrb3 = car.find('p', class_='volume').text.strip()
        except:
            dscrb1 = ''
            dscrb2 = ''
            dscrb3 = ''

        data = {
            'title': title,
            'price': price,
            'img': img,
            'dscrb1': dscrb1,
            'dscrb2': dscrb2,
            'dscrb3': dscrb3
        }

        write_csv(data)

def write_csv(data):
    with open('cars.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='\n')
        writer.writerow((data['title'],data['img'], data['price'], data['dscrb1'], data['dscrb2'], data['dscrb3']+'\n'))

def main():
    for page in range(1, 47):
        url = f'https://www.mashina.kg/commercialsearch/all/?type=2&page={page}'
        html = get_html(url)
        data = get_data(html)
main()
